from unittest.mock import MagicMock, patch

import pytest

from app.core.config import Settings
from app.llm.factory import get_llm_provider
from app.llm.ollama_provider import OllamaProvider
from app.llm.provider import (
    LLMProviderError,
    LLMProviderUnavailableError,
)


def test_factory_returns_ollama_provider():
    provider = get_llm_provider(Settings())

    assert isinstance(provider, OllamaProvider)


def test_factory_uses_configured_model():
    settings = Settings(
        ollama_model="phi4-mini",
    )

    provider = get_llm_provider(settings)

    assert isinstance(provider, OllamaProvider)
    assert provider.settings.ollama_model == "phi4-mini"


def test_factory_rejects_empty_model():
    settings = Settings(
        ollama_model="",
    )

    with pytest.raises(LLMProviderUnavailableError):
        get_llm_provider(settings)


def test_provider_initializes_model():
    settings = Settings()

    with patch(
        "app.llm.ollama_provider.ChatOllama"
    ) as mock_chat_ollama:
        OllamaProvider(settings)

        mock_chat_ollama.assert_called_once()

        kwargs = mock_chat_ollama.call_args.kwargs

        assert kwargs["model"] == "phi4-mini"
        assert kwargs["temperature"] == 0
        assert kwargs["num_ctx"] == 4096
        assert kwargs["num_predict"] == 512
        assert kwargs["format"] == "json"


def test_provider_wraps_model_errors():
    settings = Settings()

    provider = OllamaProvider(settings)

    provider.model = MagicMock()

    provider.model.invoke.side_effect = RuntimeError(
        "Ollama connection failed"
    )

    with pytest.raises(LLMProviderError):
        provider.generate_assessment(
            "System prompt",
            "User prompt",
        )
