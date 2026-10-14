from spider_sense.protocol import encode_packet

temps = [15.03, 9.50, 0.00, -5.00, 100.00, -12.34]

for t in temps:
    packet = encode_packet(t)
    hex_bytes = ", ".join(f"0x{b:02X}" for b in packet)
    expected = round(t * 100)
    print(f"{{{hex_bytes}}}, // {t:.2f} -> {expected}")

    