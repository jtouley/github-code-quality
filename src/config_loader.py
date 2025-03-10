import yaml
import os
from src.utils import log


class ConfigManager:
    """Manages configuration loading, validation, and access."""

    def __init__(self, config_path=None):
        """Initialize with an optional custom config path."""
        self.config_path = config_path or self._get_default_config_path()
        self.config = None

    def _get_default_config_path(self):
        """Get the default path to the config file."""
        return os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")

    def _load_yaml_file(self, filepath):
        """Load and parse a YAML configuration file."""
        try:
            with open(filepath, "r") as file:
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            message = f"Warning: Configuration file not found at {filepath}"
            log(message)
            return {}
        except yaml.YAMLError as e:
            message = f"Error loading YAML configuration from {filepath}: {e}"
            log(message)
            return {}

    def _get_default_config(self):
        """Load the default configuration from the config/defaults.yaml file."""
        default_config_path = os.path.join(
            os.path.dirname(__file__), "..", "config", "defaults.yaml"
        )
        default_config = self._load_yaml_file(default_config_path)
        if not default_config:
            log("Warning: Default configuration not found. Using empty configuration.")
        return default_config

    def _validate_config(self, config):
        """Validate the configuration and ensure it has the required structure."""
        # Check essential configuration elements
        required_sections = ["analysis", "prompt_customization", "feedback_format"]
        for section in required_sections:
            if section not in config:
                log(f"Warning: Missing required configuration section: {section}")
                return False

        # Further validation could be added here
        return True

    def _merge_configs(self, base_config, override_config):
        """Recursively merge configuration dictionaries."""
        merged = base_config.copy()

        for key, value in override_config.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                # Recursively merge nested dictionaries
                merged[key] = self._merge_configs(merged[key], value)
            else:
                # Override or add the value
                merged[key] = value

        return merged

    def load_config(self):
        """Load, validate, and merge configuration with defaults."""
        # Load default configuration first
        default_config = self._get_default_config()

        # Load user configuration
        user_config = self._load_yaml_file(self.config_path)

        # Merge configurations, with user config overriding defaults
        self.config = self._merge_configs(default_config, user_config)

        # Validate the merged configuration
        if not self._validate_config(self.config):
            log(
                "Warning: Configuration validation failed. Some features may not work correctly."
            )

        return self.config

    def get_config(self):
        """Get the configuration, loading it if necessary."""
        if self.config is None:
            return self.load_config()
        return self.config


def load_config(config_path=None):
    """Load and return the configuration."""
    return ConfigManager(config_path).get_config()
