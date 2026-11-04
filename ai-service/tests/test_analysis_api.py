from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_valid_analysis_request_returns_structured_result():
    response = client.post("/api/v1/analyze-upgrade", json={
        "groupId": "org.example",
        "artifactId": "demo",
        "currentVersion": "1.2.3",
        "targetVersion": "2.0.0",
        "metadataAvailable": True,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["riskScore"] == 40
    assert data["riskCategory"] == "HIGH"
    assert data["comparison"] == "upgrade"
    assert data["factors"][0]["ruleId"] == "MAJOR_CHANGE"
    assert data["scoreIsProbability"] is False


def test_missing_version_is_rejected():
    response = client.post("/api/v1/analyze-upgrade", json={
        "groupId": "org.example", "artifactId": "demo",
        "currentVersion": "1.0.0",
    })
    assert response.status_code == 422


def test_unknown_comparison_returns_structured_uncertainty():
    response = client.post("/api/v1/analyze-upgrade", json={
        "groupId": "org.example", "artifactId": "demo",
        "currentVersion": "1.0.0-custom", "targetVersion": "1.1.0",
    })
    assert response.status_code == 200
    assert response.json()["comparison"] == "unknown"
