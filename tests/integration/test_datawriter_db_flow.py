import time


def test_datawriter_consumes_queue_and_writes_to_db(
    rabbitmq_client,
    db_connection,
    queue_consumer
):
    msg = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "featureA": {"mean": 1},
        "featureB": {"normalized_mean": 1},
    }

    rabbitmq_client.publish("features_queue", msg)

    # Wait for consumer to process
    time.sleep(0.5)

    cur = db_connection.cursor()
    cur.execute("SELECT * FROM features WHERE sensor_id='s1'")
    row = cur.fetchone()

    assert row is not None
