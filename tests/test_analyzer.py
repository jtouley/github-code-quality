import sys
from unittest.mock import patch, MagicMock
from src.analyzer import AnalysisResultHandler, CodeAnalyzer, analyze_repo


def test_analysis_result_handler_extract_scores():
    """Test extracting scores from analysis text."""
    with patch("src.analyzer.load_config") as mock_load_config:
        mock_load_config.return_value = {}

        handler = AnalysisResultHandler()

        # Sample analysis text
        analysis = (
            "### DRY Analysis\n"
            "**Score: 8/10**\n"
            "This is a sample analysis.\n\n"
            "### SOLID Analysis\n"
            "**Score: 7/10**\n"
            "This is another sample analysis."
        )

        # Extract scores
        dry_score, solid_score = handler.extract_scores(analysis)

        # Verify the scores
        assert dry_score == 8
        assert solid_score == 7


def test_analysis_result_handler_format_result():
    """Test formatting an analysis result."""
    with patch("src.analyzer.load_config") as mock_load_config:
        mock_load_config.return_value = {}

        handler = AnalysisResultHandler()

        # Sample analysis text
        analysis = (
            "### DRY Analysis\n"
            "**Score: 8/10**\n"
            "This is a sample analysis.\n\n"
            "### SOLID Analysis\n"
            "**Score: 7/10**\n"
            "This is another sample analysis."
        )

        # Format the result
        result = handler.format_result("test_file.py", analysis)

        # Verify the formatted result
        assert result["dry_score"] == 8
        assert result["solid_score"] == 7
        assert result["full_analysis"] == analysis


@patch("builtins.open")
@patch("src.analyzer.load_config")
def test_analysis_result_handler_save_results(mock_load_config, mock_open):
    """Test saving results to a file with fully mocked dependencies."""
    sys.stdout.write("Test starting\n")
    sys.stdout.flush()

    # Mock the configuration to avoid actual file loading
    mock_load_config.return_value = {
        "feedback_format": {"message_template": "Test template"}
    }
    sys.stdout.write("Config mocked\n")
    sys.stdout.flush()

    # Create a mock file object
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file
    sys.stdout.write("File mock created\n")
    sys.stdout.flush()

    # Create a simple handler with minimal setup
    try:
        handler = AnalysisResultHandler(output_file="test_output.md")
        sys.stdout.write("Handler created\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"Error creating handler: {str(e)}\n")
        sys.stdout.flush()
        raise

    # Create simple test data
    results = {"test.py": {"dry_score": 8, "solid_score": 7, "full_analysis": "Test"}}
    sys.stdout.write("About to call save_results\n")
    sys.stdout.flush()

    # Call the method under test
    try:
        handler.save_results(results)
        sys.stdout.write("save_results completed\n")
        sys.stdout.flush()
    except Exception as e:
        sys.stdout.write(f"Error in save_results: {str(e)}\n")
        sys.stdout.flush()
        raise

    # Basic verification
    mock_open.assert_called_once()
    assert mock_file.write.called
    sys.stdout.write("Test completed\n")
    sys.stdout.flush()


@patch("src.analyzer.GitHubClient")
@patch("src.analyzer.AIClient")
@patch("src.analyzer.load_config")
@patch("src.analyzer.os.getenv")
def test_code_analyzer_validate_environment(
    mock_getenv, mock_load_config, mock_ai_client, mock_github_client
):
    """Test environment validation with mocked dependencies."""
    # Mock configuration
    mock_load_config.return_value = {}

    # Set up environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        "ENABLE_ANALYSIS": "true",
        "REPO": "test/repo",
        "GITHUB_TOKEN": "dummy_token",  # Add this to avoid the GitHubClient error
    }.get(key, default)

    # Create an analyzer and validate environment
    analyzer = CodeAnalyzer()
    env_vars = analyzer._validate_environment()

    # Verify the environment variables
    assert env_vars is not None
    assert env_vars["repo"] == "test/repo"


@patch("src.analyzer.load_config")
@patch("src.analyzer.os.getenv")
def test_code_analyzer_validate_environment_disabled(mock_getenv, mock_load_config):
    """Test environment validation when analysis is disabled."""
    # Mock configuration
    mock_load_config.return_value = {}

    # Set up environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        "ENABLE_ANALYSIS": "false",
        "REPO": "test/repo",
    }.get(key, default)

    # Create an analyzer and validate environment
    analyzer = CodeAnalyzer()
    env_vars = analyzer._validate_environment()

    # Verify that environment validation fails
    assert env_vars is None


@patch("src.analyzer.GitHubClient")
@patch("src.analyzer.AIClient")
@patch("src.analyzer.AnalysisResultHandler")
@patch("src.analyzer.load_config")
@patch("src.analyzer.os.getenv")
def test_code_analyzer_analyze_repo(
    mock_getenv,
    mock_load_config,
    mock_result_handler,
    mock_ai_client,
    mock_github_client,
):
    """Test analyzing a repository with fully mocked dependencies."""
    # Mock configuration
    mock_load_config.return_value = {}

    # Set up environment variables
    mock_getenv.side_effect = lambda key, default=None: {
        "ENABLE_ANALYSIS": "true",
        "REPO": "test/repo",
        "GITHUB_TOKEN": "dummy_token",  # Add this to avoid the GitHubClient error
    }.get(key, default)

    # Set up GitHub client mock
    mock_github_instance = MagicMock()
    mock_github_instance.get_files.return_value = [("test_file.py", "# Sample code")]
    mock_github_client.return_value = mock_github_instance

    # Set up AI client mock
    mock_ai_instance = MagicMock()
    mock_ai_instance.analyze_code.return_value = (
        "### DRY Analysis\n"
        "**Score: 8/10**\n"
        "This is a sample analysis.\n\n"
        "### SOLID Analysis\n"
        "**Score: 7/10**\n"
        "This is another sample analysis."
    )
    mock_ai_client.return_value = mock_ai_instance

    # Set up result handler mock
    mock_handler_instance = MagicMock()
    mock_handler_instance.format_result.return_value = {
        "dry_score": 8,
        "solid_score": 7,
        "full_analysis": "Sample analysis",
    }
    mock_handler_instance.save_results.side_effect = lambda x: x  # Return input
    mock_result_handler.return_value = mock_handler_instance

    # Create an analyzer and analyze the repo
    analyzer = CodeAnalyzer()
    results = analyzer.analyze_repo()

    # Verify the results
    assert "test_file.py" in results


@patch("src.analyzer.CodeAnalyzer")
def test_analyze_repo_function(mock_code_analyzer):
    """Test the analyze_repo function."""
    # Set up mock
    mock_instance = MagicMock()
    mock_instance.analyze_repo.return_value = {"test_file.py": "result"}
    mock_code_analyzer.return_value = mock_instance

    # Call the function
    result = analyze_repo()

    # Verify the result
    assert result == {"test_file.py": "result"}
    mock_instance.analyze_repo.assert_called_once()
