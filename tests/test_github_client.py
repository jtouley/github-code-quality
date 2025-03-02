import pytest
from src.github_client import GitHubClient

def test_github_client_init(monkeypatch):
    """Ensure GitHubClient raises an error when accessing a non-existent repo."""
    monkeypatch.setenv("GITHUB_TOKEN", "dummy_token")

    # Initialize GitHubClient with a non-existent repo and verify it raises an error
    with pytest.raises(Exception):
        client = GitHubClient(repo_name="nonexistent/repo")
        client.get_repository()  # Force an API call to trigger the expected error