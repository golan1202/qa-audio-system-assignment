import pytest


def test_health_check(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"

def test_realtime_endpoint_unit(api_client):
    payload = {"sensor_id": 1, "value": 42}

    response = api_client.post("/realtime", json=payload)

    assert response.status_code == 200
    assert "processed" in response.json

def test_historical_endpoint_unit(api_client):
    response = api_client.get("/historical?sensor_id=1")

    assert response.status_code == 200
    assert isinstance(response.json, list)
