import pytest
from unittest.mock import patch
from src.github_client import GitHubClient, GitHubAPIClient, EnvironmentManager


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Setup mock environment variables."""
    monkeypatch.setenv("GITHUB_TOKEN", "dummy_token")
    monkeypatch.setenv("GITHUB_BRANCH", "test-branch")


def test_environment_manager():
    """Test the environment manager functions."""
    # Test with a non-existent variable
    with pytest.raises(ValueError):
        EnvironmentManager.get_required_env_var("NON_EXISTENT_VAR")

    # Test with a default value
    default_value = "default"
    assert (
        EnvironmentManager.get_env_var("NON_EXISTENT_VAR", default_value)
        == default_value
    )


def test_github_api_client():
    """Test the GitHub API client."""
    token = "test_token"
    api_client = GitHubAPIClient(token)

    # Test auth headers
    headers = api_client.get_auth_headers()
    assert headers["Authorization"] == f"token {token}"


@patch("src.github_client.GitHubAPIClient.make_request")
def test_github_client_get_files(mock_make_request, mock_env_vars):
    """Test getting files from GitHub repository."""
    # Mock response from GitHub API
    mock_make_request.return_value = {
        "tree": [
            {"path": "test.py", "type": "blob"},
            {"path": "not_python.txt", "type": "blob"},
            {"path": "folder/nested.py", "type": "blob"},
        ]
    }

    # Mock the client to avoid actual API calls
    with patch(
        "src.github_client.GitHubClient.get_file_content", return_value="# Test content"
    ):
        client = GitHubClient("test/repo")
        files = client.get_files()

        # Should return 2 Python files
        assert len(files) == 2
        assert files[0][0] == "test.py"
        assert files[1][0] == "folder/nested.py"


def test_github_client_init(mock_env_vars):
    """Test GitHub client initialization."""
    client = GitHubClient("test/repo")
    assert client.repo_name == "test/repo"
    assert client.branch == "test-branch"  # From mock environment

    # Test URL construction
    tree_url = client._get_tree_url()
    assert "test/repo" in tree_url
    assert "test-branch" in tree_url


@patch("src.github_client.GitHubAPIClient.make_request")
def test_github_client_api_error(mock_make_request, mock_env_vars):
    """Test handling of GitHub API errors."""
    # Simulate an API error
    mock_make_request.side_effect = ValueError("API Error")

    client = GitHubClient("test/repo")
    files = client.get_files()

    # Should return empty list on error
    assert files == []
