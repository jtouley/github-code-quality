import yaml
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.yaml")

DEFAULT_CONFIG = {
    "analysis": {
        "dry": {
            "enabled": True,
            "weight": 0.6,
            "focus_areas": {
                "logic_reuse": 0.4,
                "data_centralization": 0.3,
                "abstraction_level": 0.3
            },
            "severity_threshold": 0.7
        },
        "solid": {
            "enabled": True,
            "weight": 0.4,
            "principles": {
                "srp": {"enabled": True, "weight": 0.3},
                "ocp": {"enabled": True, "weight": 0.2},
                "lsp": {"enabled": False},
                "isp": {"enabled": False},
                "dip": {"enabled": True, "weight": 0.5}
            },
            "severity_threshold": 0.6
        }
    },
    "prompt_customization": {
        "context_depth": "medium",
        "language_specificity": "python",
        "explanation_detail": "high"
    }
}

def load_config(config_path=CONFIG_PATH):
    """Loads and validates YAML configuration."""
    try:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file) or {}
            return config
    except FileNotFoundError:
        print(f"Warning: Configuration file not found at {config_path}, using defaults.")
        return DEFAULT_CONFIG
    except yaml.YAMLError as e:
        print(f"Error loading YAML configuration: {e}")
        return DEFAULT_CONFIG

config = load_config()