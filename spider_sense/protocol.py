SYNC_BYTE = 0xAA

def encode_packet(temperature):
    #format temp to a 2-decimal strig and encode to ASCII bytes
    payload = f'{temperature:.2f}'.encode('ascii')

    #length = how many payload bytes
    length = len(payload)

    #Calculate checksum (sum of payloa bytes, masked to low 8 bits)
    checksum = sum(payload) & 0xFF

    #retun the sync + length + payload + checksum, as bytes
    return bytes([SYNC_BYTE, length]) + payload + bytes([checksum])
