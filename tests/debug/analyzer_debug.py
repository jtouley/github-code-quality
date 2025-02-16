from github_client import GitHubClient
from ai_client import AIClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

def analyze_repo():
    repo_name = os.getenv("REPO")
    if not repo_name:
        print("REPO environment variable is not set.")
        return

    github_client = GitHubClient(repo_name)
    ai_client = AIClient()

    files = github_client.get_files()
    results = {}

    for path, code in files:
        print(f"DEBUG: Analyzing {path} (code length: {len(code)} characters)")
        # Wrap code in triple backticks for clarity
        prompt_code = f"```\n{code}\n```"
        result = ai_client.analyze_code(prompt_code)
        results[path] = result

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    analyze_repo()