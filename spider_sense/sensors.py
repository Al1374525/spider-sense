import random
#Sensors class for spider_sense system
class Sensor:
    def read(self):
        raise NotImplementedError("Subclasses must implement this method")

class FakeSensor(Sensor):
    def __init__(self, baseline, noise=0.1, offset=0.0, schedule= None):
        self.baseline = baseline
        self.noise = noise 
        self.offset = offset
        self. schedule = schedule or {}
        self.sample_count = 0

    
    def set_offset(self, offset):
        self.offset = offset

    def read(self):
        if self.sample_count in self.schedule:
            self.offset = self.schedule[self.sample_count]
        self.sample_count += 1
        return self.baseline + random.gauss(0, self.noise) + self.offset
