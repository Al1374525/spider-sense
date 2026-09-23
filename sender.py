import serial
import time
from spider_sense.sensors import FakeSensor
from spider_sense.protocol import PacketDecoder, encode_packet

port = serial.serial_for_url("loop://", baudrate=115200, timeout=1)

#create a FakeSensor with a basement baseline
sensor = FakeSensor(baseline=15)

#create a packetDecoder
decoder = PacketDecoder()

for _ in range(20):
    reading = sensor.read()
    packet = encode_packet(reading)
    port.write(packet)
    #will change later
    print(f"sent   {reading:.2f} as {packet.hex(' ')}")

    waiting = port.in_waiting
    if waiting:
        data = port.read(waiting)
        for temp in decoder.feed(data):
            print(f"received {temp:.2f}")
    time.sleep(0.25)
port.close()