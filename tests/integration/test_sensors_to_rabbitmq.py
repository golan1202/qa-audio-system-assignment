def test_sensor_message_reaches_audio_queue(rabbitmq_client):
    msg = {"sensor_id": "s1", "timestamp": "2025-01-01T10:00:00Z", "audio": [1,2,3]}

    rabbitmq_client.publish("audio_queue", msg)
    received = rabbitmq_client.consume("audio_queue", timeout=3)

    assert received["sensor_id"] == "s1"
