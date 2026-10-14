"""Tests des endpoints Flask."""
import json


def test_health(app_client):
    r = app_client.get("/api/health")
    assert r.status_code == 200
    data = r.get_json()
    assert data["status"] in ("ok", "degraded")
    assert "encryption" in data
    assert "db" in data


def test_index_returns_html(app_client):
    r = app_client.get("/")
    assert r.status_code == 200
    assert b"WIFI" in r.data


def test_diagnostics(app_client):
    r = app_client.get("/api/diagnostics")
    assert r.status_code == 200
    data = r.get_json()
    assert "os" in data
    assert "adapter_active" in data


def test_history_empty(app_client):
    r = app_client.get("/api/history")
    assert r.status_code == 200
    assert r.get_json() == []


def test_history_clear(app_client):
    r = app_client.delete("/api/history")
    assert r.status_code == 200
    assert r.get_json()["ok"] is True


def test_logs_empty(app_client):
    r = app_client.get("/api/logs")
    assert r.status_code == 200
    assert r.get_json() == []


def test_preferences_roundtrip(app_client):
    # Écrit
    r = app_client.post("/api/preferences",
                        json={"theme": "dark", "lang": "fr"})
    assert r.status_code == 200

    # Relit
    r = app_client.get("/api/preferences")
    data = r.get_json()
    assert data["theme"] == "dark"
    assert data["lang"] == "fr"


def test_stats_initial(app_client):
    r = app_client.get("/api/stats")
    assert r.status_code == 200
    data = r.get_json()
    assert data["total_scans"] == 0
    assert data["known_networks"] == 0


def test_connect_requires_ssid(app_client):
    r = app_client.post("/api/connect", json={})
    assert r.status_code == 400


def test_known_list_empty(app_client):
    r = app_client.get("/api/known")
    assert r.status_code == 200
    assert r.get_json() == []