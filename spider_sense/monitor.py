import time

class Monitor:

    def __init__(self, sensor, detector, alerter, interval, heartbeat_interval=10):
        self.sensor = sensor
        self.detector = detector
        self. alerter = alerter
        self. interval = interval
        self.heartbeat_interval = heartbeat_interval
        self.heart_counter = 0
    
    def run(self, iterations):
        for _ in range(iterations):
            reading = self.sensor.read()
            is_alert = self.detector.update(reading)
            if is_alert:
                self.alerter.send(f"Temperature anomaly: {reading:.2f}") 
                self.heart_counter = 0
            elif self.heart_counter >= self.heartbeat_interval:
                self.alerter.status(f" normal, reading {reading:.2f}")
                self.heart_counter = 0
            else:
                self.heart_counter += 1

            time.sleep(self.interval)