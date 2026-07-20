"""
Smoke tests: confirms the app boots and public routes respond without a DB
write. Run with a test database configured in .env before executing:
    pytest
"""


def test_health_check(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_schemes_list_is_public(client):
    resp = client.get("/api/v1/schemes")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_scheme_create_requires_auth(client):
    resp = client.post("/api/v1/schemes", json={})
    assert resp.status_code == 401


def test_cmrf_list_requires_auth(client):
    resp = client.get("/api/v1/cmrf")
    assert resp.status_code == 401
