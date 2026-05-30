from src.algo_a import AlgoA


def test_audio_to_feature_a_flow(rabbitmq_client,test_logger):
    audio_msg = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "audio": [1, 2, 3]
    }

    # Simulate worker logic
    algo = AlgoA()
    feature_a = algo.process(audio_msg)

    rabbitmq_client.publish("features_a_queue", feature_a)
    received = rabbitmq_client.consume("features_a_queue")

    test_logger.info("Testing if message received")
    assert received["sensor_id"] == audio_msg["sensor_id"]



