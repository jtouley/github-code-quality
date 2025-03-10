import pytest
from src.ai_client import AIClient, AIClientConfig, PromptGenerator


# This fixture sets the OPENAI_API_KEY before each test runs.
@pytest.fixture(autouse=True)
def set_dummy_openai_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")


def test_ai_client_init():
    """Test AI client initialization with environment variable."""
    ai_client = AIClient()
    assert ai_client.api_key == "dummy_key"


def test_ai_client_missing_key(monkeypatch):
    """Test AI client raises error with missing API key."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="OPENAI_API_KEY is not set"):
        AIClient()


def test_ai_client_config():
    """Test AI client configuration loading."""
    config = AIClientConfig()
    model_settings = config.get_model_settings()

    # Verify model settings have expected keys
    assert "model" in model_settings
    assert "temperature" in model_settings
    assert "max_tokens" in model_settings


def test_prompt_generator():
    """Test prompt generator creates valid prompts."""
    config = AIClientConfig()
    generator = PromptGenerator(config)

    # Generate a prompt for a simple code snippet
    code = "def hello():\n    print('Hello, world!')"
    prompt = generator.generate_code_analysis_prompt(code)

    # Verify the prompt contains key elements
    assert "DRY Analysis" in prompt
    assert "SOLID Analysis" in prompt
    assert code in prompt
    assert "Response Format" in prompt
