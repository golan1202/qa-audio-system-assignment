from src.algo_b import AlgoB

def test_algo_b_consumes_feature_a_and_produces_feature_b(rabbitmq_client):
    feature_a = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "featureA": {"mean": 10, "length": 5}
    }

    # Simulate worker logic
    algo = AlgoB()
    feature_b = algo.process(feature_a)

    rabbitmq_client.publish("features_b_queue", feature_b)

    received = rabbitmq_client.consume("features_b_queue")

    assert "featureB" in received
    assert received["featureB"]["normalized_mean"] == 2
