
"""Provider interface for structured LLM assessment generation."""

from typing import Protocol

from app.models.llm_assessment import LLMAssessmentDraft


class LLMProviderError(RuntimeError):
    """Raised when an LLM provider fails to generate a response."""


class LLMProviderUnavailableError(LLMProviderError):
    """Raised when the requested LLM provider is not configured."""


class LLMProvider(Protocol):
    """Interface implemented by concrete and mocked LLM providers."""

    def generate_assessment(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMAssessmentDraft:
        """Generate a validated structured assessment draft."""
        ...
