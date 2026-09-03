"""Smoke tests: verify the app boots and serves its core routes.

These are intentionally minimal. Their job is to make dependency upgrades
verifiable in CI: if a bump breaks app startup or the homepage render, these
fail fast.
"""

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_homepage_renders() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    # The projects section is rendered from the database.
    assert "Projects" in response.text


def test_favicon_served() -> None:
    response = client.get("/favicon.svg")
    assert response.status_code == 200
    assert "image/svg+xml" in response.headers["content-type"]
