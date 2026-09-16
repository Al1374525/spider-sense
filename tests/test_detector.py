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

def test_detector_does_not_trigger_when_window_is_not_full():
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
    assert result is False, "Detector triggered anomaly before window had sufficient data"

#Test 5
def test_detects_real_drop():
    rolling_window = RollingWindow(5)
    detector = Detector(rolling_window, 2.0, 1.0)
    # five calls to update with values near 15
    for _ in range(5):
        detector.update(15.0)
    #assert that the result is true
    result = detector.update(10.0)
    assert result is True, "Detector failed to trigger anomaly on real drop"

#Test 6 add four more update calles with cold values around 10. Keep the last reasult and assert still true
def test_detector_remains_alerting_after_initial_trigger():
    rolling_window = RollingWindow(5)
    detector = Detector(rolling_window, 2.0, 1.0)
    # Fill the window with normal readings
    for _ in range(5):
        detector.update(15.0)
    
    #The anomaly begins.
    detector.update(10.0) # This should trigger the alert

    #The anomaly continues with more cold readings - baseline must not absorb it.
    for _ in range(4):
        result = detector.update(10.0)
    
    assert result, "Baseline was poisoned: alert stopped while anomaly persisted."