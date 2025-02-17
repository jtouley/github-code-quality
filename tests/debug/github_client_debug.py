from dotenv import load_dotenv
from github_client import GitHubClient
import os

load_dotenv()

repo_name = os.getenv("REPO")
client = GitHubClient(repo_name)
files = client.get_files()

for path, code in files:
    print(f"--- {path} ---")
    print(code)
    print("\n")
