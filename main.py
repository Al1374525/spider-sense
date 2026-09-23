

from spider_sense.sensors import SerialSensor
#from spider_sense.sensors import FakeSensor
from spider_sense.window import RollingWindow
from spider_sense.detector import Detector
from spider_sense.alerters import ConsoleAlerter
from spider_sense.monitor import Monitor
import time
import serial 

#Opening up a port
port = serial.serial_for_url("loop://", baudrate=115200, timeout=1)
#create a sensor with a basment-ish baseline
basement_sensor = SerialSensor(port)

#Create a rolling windo of 5
window = RollingWindow(5)

#creating a detector object
detector = Detector( window ,2.0, 1.0)

#Alert Object
alerter = ConsoleAlerter()

# monitor object
monitor = Monitor(basement_sensor, detector, alerter, 0.25, heartbeat_interval=5)


monitor.run(30)


