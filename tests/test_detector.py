import pytest
from spider_sense.detector import is_anomalous
from spider_sense.detector import Detector
from spider_sense.window import RollingWindow

def test_is_anomalous_detects_large_drop():
    assert is_anomalous(10, 15, 2)
   

def test_isanomalous_ignores_small_fluctuation():
    assert not is_anomalous(15.1, 15.0, 2)

def test_gap_equal_to_threshold_is_not_anomalous():
    assert not is_anomalous(13, 15, 2)

def test_detector_does_not_triggernt_when_windowntnt_is_not_full():
    """
    Ensures that the detector returns False on a large drop 
    if the rolling window has not yet accumulated enough data.
    """
    # 1. Build a RollingWindow(5) and a Detector(window, 2.0, 1.0)
    test_window = RollingWindow(5)
    test_detector = Detector(test_window, 2.0, 1.0)

 # 2. Call update(15.0) once
    test_detector.update(15)

     # 3. Call update(10.0) — wildly cold
    result = test_detector.update(1.0)

    #Assert result is False
    assert result is False "Detector triggered anomaly before window had sufficient data"