def is_anomalous(current, baseline, threshold):
    #compute the distance between current and baseline
    distance = abs(current - baseline)
    return distance > threshold


class Detector:
    def __init__(self, window, threshold):
        self.window = window
        self.threshold = threshold
        self.is_alerting = False
    
    def update(self, reading):
        if self.is_alerting:
            #Window is Frozen- do not add the reading
            return True


        self.window.add(reading)
        if not self.window.is_full():
            return False
        
        if is_anomalous(reading, self.window.average(), self.threshold):
            self.is_alerting = True
            return True
        
        return False
        #return is_anomalous(reading, self.window.average(), self.threshold)