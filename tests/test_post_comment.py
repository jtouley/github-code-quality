from unittest.mock import MagicMock, patch
from src.post_comment import (
    get_analysis_feedback,
    FeedbackFormatter,
    FeedbackProvider,
    GitHubPRCommenter,
)


def test_feedback_formatter():
    """Test the feedback formatter with sample data."""
    formatter = FeedbackFormatter()

    # Sample result for a file
    result = {
        "dry_score": 8,
        "solid_score": 7,
        "full_analysis": "This is a test analysis",
    }

    # Format feedback for a file
    formatted = formatter.format_file_feedback("test_file.py", result)

    # Verify the formatted output
    assert "test_file.py" in formatted
    assert "8/10" in formatted or "8" in formatted  # Different template formats


@patch("src.post_comment.analyze_repo")
@patch("src.post_comment.FeedbackFormatter.format_file_feedback")
def test_feedback_provider_from_analysis(mock_format, mock_analyze_repo):
    """Test getting feedback from analysis."""
    mock_results = {
        "src/test_file.py": {
            "dry_score": 6,
            "solid_score": 7,
            "full_analysis": "Example Analysis",
        }
    }

    # Setup the mock to return our test results and formatted feedback
    mock_analyze_repo.return_value = mock_results
    mock_format.return_value = "## Analysis for src/test_file.py\n\n### DRY Score: 6/10\n### SOLID Score: 7/10\nExample Analysis\n"

    # Create a provider and get feedback
    provider = FeedbackProvider()
    feedback = provider.get_from_analysis()

    # Verify the mock was called
    mock_analyze_repo.assert_called_once()

    # Verify the feedback contains expected content
    assert "src/test_file.py" in feedback
    assert "6" in feedback  # The dry score
    assert "7" in feedback  # The solid score


@patch("os.path.exists")
@patch("builtins.open")
def test_feedback_provider_from_file(mock_open, mock_exists):
    """Test getting feedback from a file."""
    # Setup mocks
    mock_exists.return_value = True
    mock_file = MagicMock()
    mock_file.__enter__.return_value.read.return_value = "File feedback content"
    mock_open.return_value = mock_file

    # Create a provider and get feedback
    provider = FeedbackProvider()
    feedback = provider.get_from_file()

    # Verify the feedback is from the file
    assert feedback == "File feedback content"


@patch("src.post_comment.FeedbackProvider.get_from_analysis")
@patch("src.post_comment.FeedbackProvider.get_from_file")
def test_get_analysis_feedback_fallback(mock_get_from_file, mock_get_from_analysis):
    """Test fallback behavior when analysis fails."""
    # Setup mocks - analysis fails, file works
    mock_get_from_analysis.return_value = None
    mock_get_from_file.return_value = "Fallback feedback"

    # Get feedback
    feedback = get_analysis_feedback()

    # Verify both methods were called and we got the fallback
    mock_get_from_analysis.assert_called_once()
    mock_get_from_file.assert_called_once()
    assert feedback == "Fallback feedback"


@patch("src.post_comment.GitHubPRCommenter._extract_pr_number")
@patch("os.getenv")
def test_github_pr_commenter_validation(mock_getenv, mock_extract_pr):
    """Test PR commenter validation."""
    # Setup environment variables to be missing
    mock_getenv.side_effect = lambda key, default=None: {
        "GITHUB_REPOSITORY": None,
        "GITHUB_REF": None,
        "GITHUB_TOKEN": None,
    }.get(key, default)

    # Mock the _extract_pr_number method to avoid the TypeError
    mock_extract_pr.return_value = None

    # Create a commenter
    commenter = GitHubPRCommenter()

    # Validation should fail
    assert commenter._validate() is False


@patch("requests.post")
@patch("src.post_comment.GitHubPRCommenter._extract_pr_number")
@patch("os.getenv")
def test_github_pr_commenter_post(mock_getenv, mock_extract_pr, mock_post):
    """Test posting a PR comment."""
    # Setup environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        "GITHUB_REPOSITORY": "test/repo",
        "GITHUB_REF": "refs/pull/123/merge",
        "GITHUB_TOKEN": "test-token",
    }.get(key, default)

    # Mock the _extract_pr_number method to return a known PR number
    mock_extract_pr.return_value = "123"

    # Setup successful response
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_post.return_value = mock_response

    # Create a commenter and post a comment
    commenter = GitHubPRCommenter()
    commenter.repo = "test/repo"  # Set the repo directly
    commenter.pr_number = "123"  # Set the PR number directly
    result = commenter.post_comment("Test comment")

    # Verify the post was successful
    assert result is True
    mock_post.assert_called_once()

    # Verify the call arguments differently
    call_args = mock_post.call_args[0][0]  # Get the URL directly from positional args
    assert "test/repo" in call_args
    assert "123" in call_args
