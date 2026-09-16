def is_anomalous(current, baseline, threshold):
    #compute the distance between current and baseline
    distance = abs(current - baseline)
    return distance > threshold


class Detector:
    def __init__(self, window, threshold, clear_threshold):
        self.window = window
        self.threshold = threshold
        self.is_alerting = False
        #gap must fall below this to stand down
        self.clear_threshold = clear_threshold
    
    def update(self, reading):
        if self.is_alerting:
            #Window is Frozen- do not add the reading
            gap = abs(reading - self.window.average())
            if gap < self.clear_threshold:
                self.is_alerting = False
            return True


        self.window.add(reading)
        #below we are testing out if self.window.is_full()
        if not self.window.is_full():
            return False
        
        if is_anomalous(reading, self.window.average(), self.threshold):
            self.is_alerting = True
            return True
        
        return False
        #return is_anomalous(reading, self.window.average(), self.threshold)