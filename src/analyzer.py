import os
import json
import re
from dotenv import load_dotenv
from src.github_client import GitHubClient
from src.ai_client import AIClient
from src.config_loader import load_config

load_dotenv()  # Loads environment variables from .env if available


def extract_scores(response_text):
    """Extracts DRY and SOLID scores (1-10) from OpenAI's response."""
    dry_match = re.search(r"### DRY Analysis\n\*\*Score:\s*(\d+)/10\*\*", response_text)
    solid_match = re.search(
        r"### SOLID Analysis\n\*\*Score:\s*(\d+)/10\*\*", response_text
    )

    dry_score = int(dry_match.group(1)) if dry_match else None
    solid_score = int(solid_match.group(1)) if solid_match else None

    return dry_score, solid_score


def analyze_repo():
    if os.getenv("ENABLE_ANALYSIS", "true").lower() != "true":
        print("Code analysis is disabled. Exiting.")
        return

    repo_name = os.getenv("REPO")
    if not repo_name:
        print("REPO environment variable is not set.")
        return

    # Initialize clients
    github_client = GitHubClient(repo_name)
    ai_client = AIClient()

    files = github_client.get_files()
    results = {}

    for path, code in files:
        # Wrap the code in markdown code block markers
        prompt_code = f"```\n{code}\n```"
        analysis = ai_client.analyze_code(prompt_code)

        # Extract scores from AI analysis
        dry_score, solid_score = extract_scores(analysis)

        results[path] = {
            "dry_score": dry_score if dry_score is not None else "N/A",
            "solid_score": solid_score if solid_score is not None else "N/A",
            "full_analysis": analysis,
        }

    # Save the analysis output to a file
    with open("analysis_feedback.md", "w") as f:
        for file, feedback in results.items():
            f.write(f"## Analysis for {file}\n")
            f.write(json.dumps(feedback, indent=2) + "\n\n")

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    analyze_repo()
