
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


VALID_REQUEST = {
    "pom_xml": """
    <project>
        <groupId>com.example</groupId>
        <artifactId>api-demo</artifactId>
        <version>1.0.0</version>
        <dependencies>
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-core</artifactId>
                <version>6.2.0</version>
            </dependency>
        </dependencies>
    </project>
    """
}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_parse_pom_endpoint():
    response = client.post(
        "/api/v1/parse-pom",
        json=VALID_REQUEST,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["project"]["groupId"] == "com.example"
    assert len(data["dependencies"]) == 1
    assert data["dependencies"][0]["artifactId"] == "spring-core"
    assert data["dependencies"][0]["version"] == "6.2.0"
    assert data["dependencies"][0]["versionResolved"] is True


def test_parse_pom_rejects_malformed_xml():
    response = client.post(
        "/api/v1/parse-pom",
        json={"pom_xml": "<project>"},
    )

    assert response.status_code == 422
    assert "Invalid" in response.json()["detail"]


def test_parse_pom_rejects_empty_input():
    response = client.post(
        "/api/v1/parse-pom",
        json={"pom_xml": ""},
    )

    assert response.status_code == 422
