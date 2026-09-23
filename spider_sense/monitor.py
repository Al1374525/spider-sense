import time

class Monitor:

    def __init__(self, sensor, detector, alerter, interval, heartbeat_interval=10, missed_read_limit=20):
        self.sensor = sensor
        self.detector = detector
        self. alerter = alerter
        self. interval = interval
        self.heartbeat_interval = heartbeat_interval
        self.missed_read_limit = missed_read_limit
        self.heart_counter = 0
        self.missed_reads = 0
    
    def run(self, iterations):
        for _ in range(iterations):

            try:
                reading = self.sensor.read()
                if reading is None:
                    self.missed_reads += 1
                    if self.missed_reads >= self.missed_read_limit:
                        self.alerter.send("No data from sensor")
                        self.missed_reads = 0
                    continue
                self.missed_reads = 0
                is_alert = self.detector.update(reading)
                if is_alert:
                    self.alerter.send(f"Temperature anomaly: {reading:.2f}") 
                    self.heart_counter = 0
                elif self.heart_counter >= self.heartbeat_interval:
                    self.alerter.status(f" normal, reading {reading:.2f}")
                    self.heart_counter = 0
                else:
                    self.heart_counter += 1  

            finally:
                time.sleep(self.interval)
            
                