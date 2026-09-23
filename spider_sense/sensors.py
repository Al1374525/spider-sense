import random
from spider_sense.protocol import PacketDecoder
from collections import deque
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


class SerialSensor(Sensor):
    def __init__(self, port, max_queued=50):
        self.port = port
        self.decoder = PacketDecoder()
        self.queue = deque(maxlen=max_queued)

    def read(self):
        #1. Check to see how many bytes are in waiting

        waiting = self.port.in_waiting
        #2. If non are waiting, return None
        if waiting :
            data = self.port.read(waiting)
            self.queue.extend(self.decoder.feed(data))

        if not self.queue:
            return None


        return self.queue.popleft()
    

        




