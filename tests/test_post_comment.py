import pytest
from unittest.mock import MagicMock
from src.post_comment import get_analysis_feedback

def test_get_analysis_feedback_from_analyze_repo(mocker):
    """Mock `analyze_repo()` and verify formatted output from `config.yaml`."""
    mock_results = {
        "src/test_file.py": {"dry_score": 6, "solid_score": 7, "full_analysis": "Example Analysis"}
    }

    # Patch `analyze_repo` in the module where it's called
    mock_analyze = mocker.patch("src.post_comment.analyze_repo", return_value=mock_results)

    feedback = get_analysis_feedback()

    # Ensure the function actually called the mock
    mock_analyze.assert_called_once()

    expected_files = mock_results.keys()
    actual_files_in_feedback = [
        line.split("for ")[-1].strip()
        for line in feedback.split("\n")
        if line.startswith("## Analysis for")
    ]

    assert any(file in actual_files_in_feedback for file in expected_files), (
        f"Expected {list(expected_files)} in feedback, but found: {actual_files_in_feedback}"
    )