def test_algo_b_consumes_feature_a_and_produces_feature_b(rabbitmq_client):
    feature_a = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "featureA": {"mean": 10, "length": 5}
    }

    rabbitmq_client.publish("features_a_queue", feature_a)

    result = rabbitmq_client.consume("features_b_queue", timeout=5)

    assert "featureB" in result
    assert result["featureB"]["normalized_mean"] == 2
