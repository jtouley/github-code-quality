import os
import json
from dotenv import load_dotenv
from github_client import GitHubClient
from ai_client import AIClient

load_dotenv()  # Loads environment variables from .env if available


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
        # You might want to wrap the code in markdown code block markers.
        prompt_code = f"```\n{code}\n```"
        analysis = ai_client.analyze_code(prompt_code)
        results[path] = analysis

    # Save the analysis output to a file
    with open("analysis_feedback.md", "w") as f:
        for file, feedback in results.items():
            f.write(f"## Analysis for {file}\n")
            f.write(feedback + "\n\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    analyze_repo()
