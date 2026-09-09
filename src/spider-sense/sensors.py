import random
#Sensors class for spider_sense system
class Sensor:
    def read(self):
        raise NotImplementedError("Subclasses must implement this method")

class FakeSensor(Sensor):
    def __init__(self, baseline, noise=0.1, offset=0.0):
        self.baseline = baseline
        self.noise = noise 
        self.offset = offset
    
    def set_offset(self, offset):
        self.offset = offset

    def read(self):
        return self.baseline + random.gauss(0, self.noise) + self.offset
