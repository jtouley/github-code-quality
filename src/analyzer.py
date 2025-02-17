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
        # TODO: Enhance the prompt and error handling as needed
        score = ai_client.analyze_code(code)
        results[path] = score

    # Output results (can be extended to write to file or database)
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    analyze_repo()
