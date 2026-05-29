import pytest
from src.algo_b import AlgoB

def test_algo_b_basic_processing():
    algo = AlgoB()
    input_data = {"value": 10}

    result = algo.process(input_data)

    assert "result" in result
    assert isinstance(result["result"], (int, float))

def test_algo_b_handles_invalid_input():
    algo = AlgoB()

    with pytest.raises(ValueError):
        algo.process(None)

def test_algo_b_edge_case_zero():
    algo = AlgoB()
    input_data = {"value": 0}

    result = algo.process(input_data)

    assert result["result"] == 0
