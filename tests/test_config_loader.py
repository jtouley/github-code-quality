import pytest
import os
import yaml
from src.config_loader import load_config

@pytest.fixture
def temp_config_file(tmp_path):
    """Creates a temporary YAML config file for testing."""
    config_path = tmp_path / "test_config.yaml"
    sample_config = {
        "analysis": {
            "dry": {"enabled": True, "weight": 0.6},
            "solid": {"enabled": True, "weight": 0.4}
        },
        "prompt_customization": {
            "context_depth": "medium",
            "language_specificity": "python",
            "explanation_detail": "high"
        },
        "feedback_format": {
            "include_dry_score": True,
            "include_solid_score": True,
            "message_template": "## Analysis for {file}\\n\\n### DRY Score: {dry_score}/10\\n{dry_analysis}\\n"
        }
    }

    with open(config_path, "w") as f:
        yaml.dump(sample_config, f)
    
    return config_path

def test_load_valid_config(temp_config_file):
    """Test if the config loader successfully loads a valid config file."""
    config = load_config(str(temp_config_file))
    assert "analysis" in config
    assert config["analysis"]["dry"]["weight"] == 0.6
    assert config["analysis"]["solid"]["weight"] == 0.4
    assert "feedback_format" in config
    assert "message_template" in config["feedback_format"]

def test_load_missing_config():
    """Test fallback behavior when the config file is missing."""
    config = load_config("non_existent_config.yaml")
    assert "analysis" in config  # Should return default config
    assert config["analysis"]["dry"]["weight"] == 0.6  # Verify default value

def test_invalid_yaml(tmp_path):
    """Test behavior when an invalid YAML file is provided."""
    bad_config_path = tmp_path / "invalid_config.yaml"
    with open(bad_config_path, "w") as f:
        f.write("invalid_yaml: :::")  # Corrupt YAML format

    config = load_config(str(bad_config_path))
    assert "analysis" in config  # Should fall back to default config
    assert config["analysis"]["dry"]["weight"] == 0.6  # Verify default fallback