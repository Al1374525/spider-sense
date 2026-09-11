def is_anomalous(current, baseline, threshold):
    #compute the distance between current and baseline
    distance = abs(current - baseline)
    return distance > threshold


class Detector:
    def __init__(self, window, threshold):
        self.window = window
        self.threshold = threshold
    
    def update(self, reading):
        self.window.add(reading)
        if not self.window.is_full():
            return False
        return is_anomalous(reading, self.window.average(), self.threshold)