"""Runtime configuration for VersionWise AI service."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    ollama_model: str = "phi4-mini"
    ollama_base_url: str = "http://localhost:11434"
    ollama_timeout_seconds: int = 120
    ollama_num_ctx: int = 4096
    ollama_num_predict: int = 512

    @property
    def ollama_configured(self) -> bool:
        return bool(
            self.ollama_model
            and self.ollama_model.strip()
            and self.ollama_base_url
            and self.ollama_base_url.strip()
        )


def get_settings() -> Settings:
    timeout_raw = os.getenv("OLLAMA_TIMEOUT_SECONDS", "120")
    num_ctx_raw = os.getenv("OLLAMA_NUM_CTX", "4096")
    num_predict_raw = os.getenv("OLLAMA_NUM_PREDICT", "512")

    try:
        timeout = int(timeout_raw)
        num_ctx = int(num_ctx_raw)
        num_predict = int(num_predict_raw)
    except ValueError as exc:
        raise ValueError("Invalid Ollama configuration value.") from exc

    if timeout < 1:
        raise ValueError("OLLAMA_TIMEOUT_SECONDS must be positive.")

    if num_ctx < 1:
        raise ValueError("OLLAMA_NUM_CTX must be positive.")

    if num_predict < 1:
        raise ValueError("OLLAMA_NUM_PREDICT must be positive.")

    return Settings(
        ollama_model=os.getenv("OLLAMA_MODEL", "phi4-mini"),
        ollama_base_url=os.getenv(
            "OLLAMA_BASE_URL",
            "http://localhost:11434",
        ),
        ollama_timeout_seconds=timeout,
        ollama_num_ctx=num_ctx,
        ollama_num_predict=num_predict,
    )
