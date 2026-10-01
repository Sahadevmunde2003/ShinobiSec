"""Regression tests for ShinobiSec's local defensive-analysis APIs."""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest

import app as shinobisec


@pytest.fixture()
def client(tmp_path):
    """Provide an isolated Flask client and SQLite history database."""
    database = tmp_path / "assessments.sqlite3"
    shinobisec.app.config.update(TESTING=True, DATABASE=str(database))
    with shinobisec.app.test_client() as test_client:
        yield test_client, database


def test_history_starts_empty_and_validates_limit(client):
    test_client, _ = client

    response = test_client.get("/api/history")
    assert response.status_code == 200
    assert response.get_json() == {"ok": True, "assessments": []}

    response = test_client.get("/api/history?limit=invalid")
    assert response.status_code == 400
    assert response.get_json()["error"] == "History limit must be a number."


@pytest.mark.parametrize(
    ("endpoint", "payload", "module", "target_label"),
    [
        ("/api/sharingan", {"text": "Failed password for root from 203.0.113.50"}, "Sharingan", "Security log input"),
        ("/api/amaterasu", {"text": "mimikatz connected to 8.8.8.8"}, "Amaterasu", "Defensive IOC input"),
        ("/api/shadow-clone", {"text": "Failed password from 8.8.8.8"}, "Shadow Clone", "Defensive analysis input"),
    ],
)
def test_successful_local_analysis_is_saved_as_metadata(client, endpoint, payload, module, target_label):
    test_client, database = client

    response = test_client.post(endpoint, json=payload)
    assert response.status_code == 200
    assert response.get_json()["ok"] is True

    history = test_client.get("/api/history?limit=1").get_json()["assessments"]
    assert len(history) == 1
    assert history[0]["module"] == module
    assert history[0]["target"] == target_label
    assert history[0]["finding_count"] >= 0

    with sqlite3.connect(database) as connection:
        stored_values = connection.execute(
            "SELECT module, target, finding_count, severity_counts, created_at FROM assessment_history"
        ).fetchall()
    assert len(stored_values) == 1
    assert payload["text"] not in str(stored_values)


def test_history_returns_newest_entries_first(client):
    test_client, _ = client
    test_client.post("/api/sharingan", json={"text": "Accepted password for analyst"})
    test_client.post("/api/amaterasu", json={"text": "mimikatz"})

    history = test_client.get("/api/history?limit=1000").get_json()["assessments"]
    assert [entry["module"] for entry in history] == ["Amaterasu", "Sharingan"]
