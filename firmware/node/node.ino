//store the 8 packet bytes in a fixed array of unsigned bytes
uint8_t packet[8] = {0xAA, 0x05, 0x31, 0x35, 0x2E, 0x30, 0x33, 0xF7};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.write(packet, 8);
  
  //wait one second
  delay(1000);

}
