from collections import deque

class RollingWindow:
    def __init__(self, size):
        self.window = deque(maxlen=size)
        self.size = size
    #append to the deque. One line
    
    def add(self, reading):
        self.window.append(reading)
    #sum the deque, divide by how many items are in
    def average(self):
        if not self.window:
            raise ValueError("Cannot average an empty window")
        return sum(self.window)/len(self.window)
    
    #return whethert the cpint has reached the maximum size
    def is_full(self):
        return len(self.window) == self.size