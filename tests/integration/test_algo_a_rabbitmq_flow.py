def test_audio_to_feature_a_flow(rabbitmq_client):
    audio_msg = {...}
    rabbitmq_client.publish("audio_queue", audio_msg)

    # Wait for processing
    messages = rabbitmq_client.consume("features_a_queue", timeout=5)

    assert len(messages) == 1
    assert messages[0]["sensor_id"] == audio_msg["sensor_id"]
