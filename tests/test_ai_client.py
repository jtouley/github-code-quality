import os
import pytest
from src.ai_client import AIClient

def test_ai_client_init(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "dummy_key")
    ai_client = AIClient()
    assert ai_client.api_key == "dummy_key"