SYNC_BYTE = 0xAA


class PacketDecoder:
    def __init__(self):
        self.buffer = bytearray()
        self.SYNC_BYTE = 0xAA
    
    

    def feed(self, data):
     self.buffer.extend(data)
     results = []

     while True:
        index = self.buffer.find(SYNC_BYTE)

        if index == -1:
            self.buffer.clear()
            break
        
        if index > 0:
            del self.buffer[:index]
        
        if len(self.buffer) < 0:
            break
        
        length = self.buffer[1]
        packet_size = length + 3

        if len(self.buffer) < packet_size:
            break
        
        payload = self.buffer[2:2 + length]
        checksum = self.buffer[2 + length]

        if checksum == sum(payload) & 0xFF:
            results.append(float(payload.decode("ascii")))
            del self.buffer[:packet_size]
        else:
            del self.buffer[:1]
     return results




def encode_packet(temperature):
    #format temp to a 2-decimal strig and encode to ASCII bytes
    payload = f'{temperature:.2f}'.encode('ascii')

    #length = how many payload bytes
    length = len(payload)

    #Calculate checksum (sum of payloa bytes, masked to low 8 bits)
    checksum = sum(payload) & 0xFF

    #retun the sync + length + payload + checksum, as bytes
    return bytes([SYNC_BYTE, length]) + payload + bytes([checksum])
