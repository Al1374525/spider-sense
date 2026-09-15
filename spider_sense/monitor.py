import time

class Monitor:

    def __init__(self, sensor, detector, alerter, interval):
        self.sensor = sensor
        self.detector = detector
        self. alerter = alerter
        self. interval = interval
    
    def run(self, iterations):
        for _ in range(iterations):
            reading = self.sensor.read()
            is_alert = self.detector.update(reading)
            if is_alert:
                self.alerter.send(f"Temperature anomaly: {reading:.2f}") 

            time.sleep(self.interval)