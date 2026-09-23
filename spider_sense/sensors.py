import random
from spider_sense.protocol import PacketDecoder
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
    def __init__(self, port):
        self.port = port
        self.decoder = PacketDecoder()

    def read(self):
        #1. Check to see how many bytes are in waiting

        waiting = self.port.in_waiting
        #2. If non are waiting, return None
        if waiting == 0:
            return None
        #3.Read exactly that many bytes 
        data = self.port.read(waiting)

        #4 feed them into the decoder
        results = self.decoder.feed(data)

        #5 if the results returned any temp, return the last one
        if results:
            return results[-1] #Grabs the last item in the list

        return None

        




