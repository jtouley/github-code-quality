import pytest
from src.ai_client import AIClient


# This fixture sets the OPENAI_API_KEY before each test runs.
@pytest.fixture(autouse=True)
def set_dummy_openai_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")


def test_ai_client_init():
    ai_client = AIClient()
    assert ai_client.api_key == "dummy_key"
