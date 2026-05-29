from src.data_writer import write_feature_to_db

def test_data_writer_inserts_record(db_connection):
    feature = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "featureA": {"mean": 1.0},
        "featureB": {"normalized_mean": 1.0},
    }

    write_feature_to_db(db_connection, feature)

    cur = db_connection.cursor()
    cur.execute("SELECT sensor_id FROM features WHERE sensor_id='s1'")
    row = cur.fetchone()

    assert row is not None
