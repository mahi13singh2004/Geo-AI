import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_upload_invalid_file_type(tmp_path):
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    
    with open(test_file, "rb") as f:
        response = client.post(
            "/api/v1/files/",
            files={"file": ("test.txt", f, "text/plain")}
        )
    assert response.status_code == 400


def test_get_nonexistent_file():
    response = client.get("/api/v1/files/nonexistent-id/")
    assert response.status_code == 404


def test_get_nonexistent_measurements():
    response = client.get("/api/v1/files/nonexistent-id/measurements/")
    assert response.status_code == 404
