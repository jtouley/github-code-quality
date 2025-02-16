import os
import base64
import requests
from github import Github

class GitHubClient:
    def __init__(self, repo_name):
        from dotenv import load_dotenv
        load_dotenv()  # Ensure env variables are loaded

        token = os.getenv("GITHUB_TOKEN")
        if not token:
            raise ValueError("GITHUB_TOKEN is not set in the environment.")
        self.token = token
        self.repo_name = repo_name
        self.branch = os.getenv("GITHUB_BRANCH", "main")  # Use branch from env, default to main
        print(f"DEBUG: Using branch: {self.branch}")  # Debug print to verify branch
        self.api_url = f"https://api.github.com/repos/{repo_name}/git/trees/{self.branch}?recursive=1"

    def get_files(self):
        """Fetch all Python files recursively from the repo using GitHub API."""
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(self.api_url, headers=headers)

        if response.status_code != 200:
            raise ValueError(f"GitHub API error: {response.status_code} {response.json()}")

        data = response.json()
        files = []

        for item in data.get("tree", []):
            if item["type"] == "blob" and item["path"].endswith(".py"):
                files.append((item["path"], self.get_file_content(item["path"])))

        if not files:
            print("⚠️ No Python files found in the repository.")

        return files

    def get_file_content(self, file_path):
        """Fetch and decode the file content."""
        url = f"https://api.github.com/repos/{self.repo_name}/contents/{file_path}?ref={self.branch}"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            encoded_content = data.get("content", "")
            return base64.b64decode(encoded_content).decode('utf-8')
        else:
            print(f"⚠️ Unable to fetch content for {file_path}: {response.status_code}")
            return ""