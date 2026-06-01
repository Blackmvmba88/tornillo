from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from tests.test_runtime import encode_test_screw


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_detect_endpoint() -> None:
    client = TestClient(app)
    response = client.post(
        "/detect",
        files={"image": ("screw.jpg", encode_test_screw(), "image/jpeg")},
    )
    assert response.status_code == 200
    assert response.json()["detected"] is True


def test_roadmap_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/roadmap")
    payload = response.json()

    assert response.status_code == 200
    assert payload["vision"] == "Physics -> Vision -> Semantics -> Autonomy"
    assert len(payload["phases"]) == 7
    assert payload["phases"][0]["name"] == "Genesis Runtime"
