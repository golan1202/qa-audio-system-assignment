

def test_health_check(api_client):
    client, api_base = api_client
    response = client.get(f"{api_base}/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_realtime_endpoint_unit(api_client):
    payload = {"sensor_id": 1, "value": 42}
    client, api_base = api_client
    response = client.post(f"{api_base}/realtime", json=payload)

    assert response.status_code == 200
    assert "processed" in response.json


def test_historical_endpoint_unit(api_client):
    client, api_base = api_client
    response = client.get(f"{api_base}/historical?sensor_id=1")

    assert response.status_code == 200
    assert isinstance(response.json, list)
