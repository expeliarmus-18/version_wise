"""Local Ollama provider for structured upgrade assessments."""

import json
import logging

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from pydantic import ValidationError

from app.core.config import Settings
from app.llm.provider import LLMProviderError
from app.models.llm_assessment import LLMAssessmentDraft


logger = logging.getLogger(__name__)


class OllamaProvider:
    """Generate structured assessments using a local Ollama model."""

    def __init__(self, settings: Settings):
        self.settings = settings

        self.model = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=0,
            num_ctx=settings.ollama_num_ctx,
            num_predict=settings.ollama_num_predict,
            format="json",
        )

    def generate_assessment(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> LLMAssessmentDraft:
        """Generate and validate a structured assessment."""

        constrained_system_prompt = (
            "/no_think\n"
            "You are generating a structured dependency upgrade assessment "
            "for VersionWise.\n\n"
            "STRICT OUTPUT REQUIREMENTS:\n"
            "- Return exactly one JSON object.\n"
            "- Do not return Markdown, code fences, explanations, or text "
            "outside JSON.\n"
            "- Follow the supplied JSON schema exactly.\n"
            "- Include every field in the output structure.\n"
            "- Never invent evidence or evidence IDs.\n"
            "- Use only the supplied evidence.\n"
            "- If evidence is insufficient, status MUST be "
            "INSUFFICIENT_EVIDENCE.\n"
            "- When evidence is insufficient, all finding arrays MUST be empty.\n"
            "- Use empty arrays when there are no findings.\n"
            "- Every finding must contain title, description, severity, "
            "and evidence_ids.\n"
            "- Valid severity values: INFO, LOW, MODERATE, HIGH, CRITICAL, "
            "UNKNOWN.\n"
            "- Valid status values: RECOMMENDED, NOT_RECOMMENDED, "
            "INSUFFICIENT_EVIDENCE.\n"
            "- The limitations field MUST always be an array of strings, "
            "never a single string.\n\n"
            "REQUIRED JSON STRUCTURE:\n"
            "{\n"
            '  "status": "INSUFFICIENT_EVIDENCE",\n'
            '  "summary": "Assessment summary",\n'
            '  "evidence_ids": [],\n'
            '  "compatibility_findings": [],\n'
            '  "breaking_changes": [],\n'
            '  "migration_concerns": [],\n'
            '  "security_findings": [],\n'
            '  "limitations": []\n'
            "}\n\n"
            "When evidence is insufficient, do not attempt to assess "
            "compatibility, breaking changes, migration concerns, or security "
            "findings. Return empty arrays for all finding categories and "
            "explain the limitation in the summary and limitations.\n\n"
            + system_prompt
        )

        try:
            response = self.model.invoke(
                [
                    SystemMessage(content=constrained_system_prompt),
                    HumanMessage(content=user_prompt),
                ]
            )

            content = response.content

            if not isinstance(content, str):
                raise LLMProviderError(
                    "Ollama returned a non-text assessment response."
                )

            content = content.strip()

            # Defensive cleanup for occasional Markdown fences.
            if content.startswith("```"):
                lines = content.splitlines()

                if lines and lines[0].startswith("```"):
                    lines = lines[1:]

                if lines and lines[-1].startswith("```"):
                    lines = lines[:-1]

                content = "\n".join(lines).strip()

            # Parse JSON before Pydantic validation so we can normalize
            # occasional inconsistencies from the local LLM.
            data = json.loads(content)

            # Normalize limitations when the model returns a single string
            # instead of the expected list of strings.
            if isinstance(data.get("limitations"), str):
                data["limitations"] = [data["limitations"]]

            return LLMAssessmentDraft.model_validate(data)

        except (json.JSONDecodeError, ValidationError) as exc:
            logger.exception(
                "Ollama returned an invalid assessment structure."
            )

            raise LLMProviderError(
                "Ollama returned an invalid structured assessment."
            ) from exc

        except LLMProviderError:
            raise

        except Exception as exc:
            logger.exception(
                "Ollama assessment generation failed."
            )

            raise LLMProviderError(
                "Local LLM assessment generation failed."
            ) from exc