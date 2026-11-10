import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"Flask Production App" in res.data

def test_health_endpoint(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert b"healthy" in res.data
