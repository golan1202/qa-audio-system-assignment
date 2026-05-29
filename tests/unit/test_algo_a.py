from src.algo_a import AlgoA

def test_algo_a_generates_expected_feature_keys():
    audio_msg = {
        "sensor_id": "s1",
        "timestamp": "2025-01-01T10:00:00Z",
        "audio": [0.1, 0.2, 0.3]
    }

    result = AlgoA.process(audio_msg)

    assert result["sensor_id"] == "s1"
    assert "featureA" in result
    assert "timestamp" in result