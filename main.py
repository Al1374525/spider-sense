

from spider_sense.sensors import FakeSensor
import time
#create a sensor with a basment-ish baseline
basement_sensor = FakeSensor(baseline=15)

#Loop about twenty times
for i in range(20):
    #each pass: print the reading, then sleep briefly
    print(f"Reading: {basement_sensor.read():.2f}")
    time.sleep(0.25)
    #around iteration ten, call set_offset(-5.0)
    if i == 10:
        basement_sensor.set_offset(-5.0)