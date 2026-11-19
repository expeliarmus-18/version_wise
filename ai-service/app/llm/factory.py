"""Factory for the configured LLM provider."""

from app.core.config import Settings, get_settings
from app.llm.ollama_provider import OllamaProvider
from app.llm.provider import (
    LLMProvider,
    LLMProviderUnavailableError,
)


def get_llm_provider(
    settings: Settings | None = None,
) -> LLMProvider:
    """Return the configured local Ollama provider."""

    settings = settings or get_settings()

    if not settings.ollama_configured:
        raise LLMProviderUnavailableError(
            "Ollama is unavailable. Configure OLLAMA_MODEL "
            "and OLLAMA_BASE_URL."
        )

    return OllamaProvider(settings)
