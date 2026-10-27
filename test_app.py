import pytest

from app import app


@pytest.fixture
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_dashboard(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Server Monitoring Dashboard" in response.data


def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "status": "ok",
        "application": "server-monitor",
    }


def test_metrics(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    data = response.get_json()
    assert data["operating_system"] == "Windows"

    for name in ("cpu_percent", "memory_percent", "disk_percent"):
        assert isinstance(data[name], (int, float))
        assert 0 <= data[name] <= 100