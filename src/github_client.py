import os
import base64
import requests
from dotenv import load_dotenv
from src.utils import log


class EnvironmentManager:
    """Manages environment variables and configuration."""

    @staticmethod
    def load_environment():
        """Loads environment variables from .env file."""
        load_dotenv()

    @staticmethod
    def get_required_env_var(var_name):
        """Gets a required environment variable or raises an error."""
        value = os.getenv(var_name)
        if not value:
            raise ValueError(f"{var_name} is not set in the environment.")
        return value

    @staticmethod
    def get_env_var(var_name, default=None):
        """Gets an environment variable with a fallback default."""
        return os.getenv(var_name, default)


class GitHubAPIClient:
    """Low-level client for GitHub API requests."""

    def __init__(self, token):
        self.token = token

    def get_auth_headers(self):
        """Returns authentication headers for GitHub API requests."""
        return {"Authorization": f"token {self.token}"}

    def make_request(self, url):
        """Makes a GET request to the GitHub API."""
        headers = self.get_auth_headers()
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise ValueError(
                f"GitHub API error: {response.status_code} {response.json()}"
            )

        return response.json()


class GitHubClient:
    """Client for interacting with GitHub repositories."""

    def __init__(self, repo_name):
        # Load environment and configuration
        EnvironmentManager.load_environment()

        # Get required configuration
        self.token = EnvironmentManager.get_required_env_var("GITHUB_TOKEN")
        self.repo_name = repo_name
        self.branch = EnvironmentManager.get_env_var("GITHUB_BRANCH", "main")

        # Initialize API client
        self.api_client = GitHubAPIClient(self.token)

        # Log configuration
        log(f"Initialized GitHub client for repo: {repo_name}, branch: {self.branch}")

    def _get_tree_url(self):
        """Returns the URL for the repository tree API."""
        return f"https://api.github.com/repos/{self.repo_name}/git/trees/{self.branch}?recursive=1"

    def _get_content_url(self, file_path):
        """Returns the URL for a file's content API."""
        return f"https://api.github.com/repos/{self.repo_name}/contents/{file_path}?ref={self.branch}"

    def get_files(self, extension=".py"):
        """Fetch all files with the specified extension recursively from the repo."""
        tree_url = self._get_tree_url()

        try:
            data = self.api_client.make_request(tree_url)
            files = []

            for item in data.get("tree", []):
                if item["type"] == "blob" and item["path"].endswith(extension):
                    content = self.get_file_content(item["path"])
                    if content:  # Only add if content was successfully retrieved
                        files.append((item["path"], content))

            if not files:
                log(f"⚠️ No {extension} files found in the repository.")

            return files

        except Exception as e:
            log(f"Error fetching repository files: {str(e)}")
            return []

    def get_file_content(self, file_path):
        """Fetch and decode the file content."""
        content_url = self._get_content_url(file_path)

        try:
            data = self.api_client.make_request(content_url)
            encoded_content = data.get("content", "")
            return base64.b64decode(encoded_content).decode("utf-8")

        except Exception as e:
            log(f"⚠️ Unable to fetch content for {file_path}: {str(e)}")
            return ""
