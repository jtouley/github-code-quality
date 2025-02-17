import pytest
from src.github_client import GitHubClient


def test_github_client_init(monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "dummy_token")
    # Expect an error when trying to access a non-existent repo with a dummy token.
    with pytest.raises(Exception):
        GitHubClient("nonexistent/repo")
