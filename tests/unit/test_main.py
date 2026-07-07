import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Enterprise Hiring Assistant API"
    assert "docs" in response.json()
    assert "version" in response.json()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_docs_available():
    response = client.get("/api/docs")
    assert response.status_code == 200


def test_redoc_available():
    response = client.get("/api/redoc")
    assert response.status_code == 200
