"""
Basic tests for StreamChat backend endpoints.
Run: pytest tests/test_api.py -v
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from main import app

client = TestClient(app)


def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "uptime_seconds" in data


def test_health_responds_fast():
    import time
    start = time.time()
    client.get("/health")
    elapsed_ms = (time.time() - start) * 1000
    assert elapsed_ms < 200, f"Health check took {elapsed_ms:.0f}ms — must be under 200ms"


def test_reset_returns_session_id():
    response = client.post("/reset", json={"session_id": "test-session-123"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["session_id"] == "test-session-123"


def test_reset_requires_session_id():
    response = client.post("/reset", json={"session_id": ""})
    assert response.status_code == 400


def test_chat_rejects_empty_message():
    response = client.post("/chat", json={"message": "", "history": []})
    assert response.status_code == 400