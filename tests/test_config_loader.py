import pytest
import yaml
from src.config_loader import load_config, ConfigManager


@pytest.fixture
def temp_config_file(tmp_path):
    """Creates a temporary YAML config file for testing."""
    config_path = tmp_path / "test_config.yaml"
    sample_config = {
        "analysis": {
            "dry": {"enabled": True, "weight": 0.8},  # Custom value
            "solid": {"enabled": True, "weight": 0.2},  # Custom value
        },
        "prompt_customization": {
            "context_depth": "high",  # Changed from default
            "language_specificity": "python",
            "explanation_detail": "high",
        },
        "feedback_format": {
            "include_dry_score": True,
            "include_solid_score": True,
            "message_template": "## Analysis for {file}\\n\\n### DRY Score: {dry_score}/10\\n{dry_analysis}\\n",
        },
    }

    with open(config_path, "w") as f:
        yaml.dump(sample_config, f)

    return config_path


@pytest.fixture
def temp_default_config(tmp_path):
    """Creates a temporary default YAML config file for testing."""
    defaults_dir = tmp_path / "config"
    defaults_dir.mkdir(exist_ok=True)
    config_path = defaults_dir / "defaults.yaml"

    sample_config = {
        "analysis": {
            "dry": {"enabled": True, "weight": 0.7},
            "solid": {"enabled": True, "weight": 0.3},
        },
        "prompt_customization": {
            "context_depth": "medium",
            "language_specificity": "python",
            "explanation_detail": "high",
        },
        "feedback_format": {"include_dry_score": True, "include_solid_score": True},
    }

    with open(config_path, "w") as f:
        yaml.dump(sample_config, f)

    return tmp_path


@pytest.fixture
def config_manager_with_defaults(temp_default_config, monkeypatch):
    """Returns a ConfigManager with mock default config path."""

    def mock_get_default_config_path(self):
        return temp_default_config / "config" / "defaults.yaml"

    # Monkey patch the method to return our test defaults path
    monkeypatch.setattr(
        ConfigManager,
        "_get_default_config",
        lambda self: ConfigManager._load_yaml_file(
            self, temp_default_config / "config" / "defaults.yaml"
        ),
    )

    return ConfigManager()


def test_load_valid_config(temp_config_file, config_manager_with_defaults, monkeypatch):
    """Test if the config loader successfully loads a valid config file."""
    # Patch the default config path for this test
    monkeypatch.setattr(
        ConfigManager, "_get_default_config_path", lambda self: temp_config_file
    )

    config = load_config(temp_config_file)

    # Check if values from the test config override defaults
    assert config["analysis"]["dry"]["weight"] == 0.8  # Custom value from test_config
    assert config["analysis"]["solid"]["weight"] == 0.2  # Custom value from test_config
    assert config["prompt_customization"]["context_depth"] == "high"  # Custom value


def test_config_manager_defaults(config_manager_with_defaults):
    """Test the ConfigManager with default settings."""
    config = config_manager_with_defaults.get_config()

    # Check default values
    assert config["analysis"]["dry"]["weight"] == 0.6
    assert config["analysis"]["solid"]["weight"] == 0.4
    assert config["prompt_customization"]["context_depth"] == "medium"


def test_config_manager_custom_path(
    temp_config_file, config_manager_with_defaults, monkeypatch
):
    """Test the ConfigManager with a custom config path."""
    # Create a ConfigManager with our test config
    manager = ConfigManager(temp_config_file)

    # Patch the _get_default_config method for this manager
    original_method = manager._get_default_config
    manager._get_default_config = (
        lambda: config_manager_with_defaults._get_default_config()
    )

    config = manager.get_config()

    # Restore original method
    manager._get_default_config = original_method

    # Custom values should override defaults
    assert config["analysis"]["dry"]["weight"] == 0.8
    assert config["analysis"]["solid"]["weight"] == 0.2
    assert config["prompt_customization"]["context_depth"] == "high"


def test_validate_config(config_manager_with_defaults):
    """Test configuration validation."""
    # Valid config should pass validation
    valid_config = {"analysis": {}, "prompt_customization": {}, "feedback_format": {}}
    assert config_manager_with_defaults._validate_config(valid_config) is True

    # Invalid config (missing required section) should fail validation
    invalid_config = {
        "analysis": {},
        "prompt_customization": {}
        # Missing feedback_format
    }
    assert config_manager_with_defaults._validate_config(invalid_config) is False


def test_merge_configs(config_manager_with_defaults):
    """Test merging of configuration dictionaries."""
    base = {"a": 1, "b": {"c": 2, "d": 3}}

    override = {
        "b": {"c": 4, "e": 5},  # Override existing value  # Add new nested value
        "f": 6,  # Add new top-level value
    }

    merged = config_manager_with_defaults._merge_configs(base, override)

    # Check merged values
    assert merged["a"] == 1  # Unchanged
    assert merged["b"]["c"] == 4  # Overridden
    assert merged["b"]["d"] == 3  # Unchanged nested
    assert merged["b"]["e"] == 5  # New nested
    assert merged["f"] == 6  # New top-level
