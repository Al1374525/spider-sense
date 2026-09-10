

from spider_sense.sensors import FakeSensor
from spider_sense.window import RollingWindow
import time
#create a sensor with a basment-ish baseline
basement_sensor = FakeSensor(baseline=15)

#Create a rolling windo of 5
window = RollingWindow(5)
#Loop about twenty times
for i in range(20):
    #Assign the reading to a variable- something like reading = basement_sensor.read()
    reading = basement_sensor.read()

    window.add(reading)

    #each pass: print the reading, then sleep briefly
    print(f"Reading: {reading:.2f}  Baseline: {window.average():.2f}")
    time.sleep(0.25)
    #around iteration ten, call set_offset(-5.0)
    if i == 10:
        basement_sensor.set_offset(-5.0)
    #call read() once, store it in a variable



