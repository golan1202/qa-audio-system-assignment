def test_rest_api_returns_realtime_data(api_client, rabbitmq_client):
    client, api_base = api_client
    msg = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "featureA": {},
        "featureB": {},
    }

    rabbitmq_client.publish("features_queue", msg)

    resp = client.get(f"{api_base}/features/realtime?sensor_id=s1")
    assert resp.status_code == 200
    assert len(resp.json()) >= 1
