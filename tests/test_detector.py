import pytest
from spider_sense.detector import is_anomalous

def test_is_anomalous_detects_large_drop():
    assert is_anomalous(10, 15, 2)
   

def test_isanomalous_ignores_small_fluctuation():
    assert not is_anomalous(15.1, 15.0, 2)

def test_gap_equal_to_threshold_is_not_anomalous():
    assert not is_anomalous(13, 15, 2)
