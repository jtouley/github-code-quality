from dotenv import load_dotenv
load_dotenv()

from github_client import GitHubClient
import os

repo_name = os.getenv("REPO")
client = GitHubClient(repo_name)
files = client.get_files()

for path, code in files:
    print(f"--- {path} ---")
    print(code)
    print("\n")