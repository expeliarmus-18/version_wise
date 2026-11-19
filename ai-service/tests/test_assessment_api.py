
from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.api.routes import assessment as assessment_routes
from app.llm.assessment_service import AssessmentValidationError
from app.llm.provider import (
    LLMProviderError,
    LLMProviderUnavailableError,
)
from app.main import app
from app.models.assessment import (
    AssessmentStatus,
    UpgradeAssessment,
)


client = TestClient(app)


VALID_REQUEST = {
    "groupId": "org.springframework.boot",
    "artifactId": "spring-boot-starter-web",
    "currentVersion": "2.7.18",
    "targetVersion": "3.0.0",
    "metadataAvailable": True,
}


def make_assessment():
    return UpgradeAssessment(
        status=AssessmentStatus.INSUFFICIENT_EVIDENCE,
        summary=(
            "The available documentation does not establish "
            "whether this dependency upgrade is compatible."
        ),
        evidence=[],
        limitations=[
            "No traceable documentation evidence was retrieved.",
            "Compatibility cannot be established from missing evidence.",
        ],
    )


def test_assessment_endpoint_returns_structured_assessment(monkeypatch):
    provider = Mock()
    expected_assessment = make_assessment()

    service = Mock()
    service.assess.return_value = expected_assessment

    monkeypatch.setattr(
        assessment_routes,
        "get_llm_provider",
        lambda: provider,
    )
    monkeypatch.setattr(
        assessment_routes,
        "AssessmentService",
        lambda provider: service,
    )

    response = client.post(
        "/api/v1/assess-upgrade",
        json=VALID_REQUEST,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "INSUFFICIENT_EVIDENCE"
    assert data["summary"] == expected_assessment.summary
    assert data["evidence"] == []
    assert len(data["limitations"]) == 2

    service.assess.assert_called_once()


def test_assessment_endpoint_returns_503_without_provider_credentials(
    monkeypatch,
):
    def unavailable_provider():
        raise LLMProviderUnavailableError(
            "OpenAI is unavailable. Configure OPENAI_API_KEY."
        )

    monkeypatch.setattr(
        assessment_routes,
        "get_llm_provider",
        unavailable_provider,
    )

    response = client.post(
        "/api/v1/assess-upgrade",
        json=VALID_REQUEST,
    )

    assert response.status_code == 503
    assert "OPENAI_API_KEY" in response.json()["detail"]


def test_assessment_endpoint_returns_502_on_provider_failure(
    monkeypatch,
):
    provider = Mock()

    service = Mock()
    service.assess.side_effect = LLMProviderError(
        "OpenAI generation failed."
    )

    monkeypatch.setattr(
        assessment_routes,
        "get_llm_provider",
        lambda: provider,
    )
    monkeypatch.setattr(
        assessment_routes,
        "AssessmentService",
        lambda provider: service,
    )

    response = client.post(
        "/api/v1/assess-upgrade",
        json=VALID_REQUEST,
    )

    assert response.status_code == 502
    assert "OpenAI generation failed" in response.json()["detail"]


def test_assessment_endpoint_returns_502_on_invalid_citations(
    monkeypatch,
):
    provider = Mock()

    service = Mock()
    service.assess.side_effect = AssessmentValidationError(
        "Unknown evidence ID: invented-evidence"
    )

    monkeypatch.setattr(
        assessment_routes,
        "get_llm_provider",
        lambda: provider,
    )
    monkeypatch.setattr(
        assessment_routes,
        "AssessmentService",
        lambda provider: service,
    )

    response = client.post(
        "/api/v1/assess-upgrade",
        json=VALID_REQUEST,
    )

    assert response.status_code == 502
    assert "Unknown evidence ID" in response.json()["detail"]


def test_assessment_endpoint_rejects_invalid_request():
    response = client.post(
        "/api/v1/assess-upgrade",
        json={
            "groupId": "org.example",
            "artifactId": "demo",
            "currentVersion": "1.0.0",
        },
    )

    assert response.status_code == 422
