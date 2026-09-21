from spider_sense.protocol import encode_packet

def test_encode_packet_matches_spec_example():
    expected = bytes([0xAA, 0x05, 0x31, 0x35, 0x2E, 0x30, 0x33, 0xF7])
    assert encode_packet(15.03) == expected

def test_lenth_field_tracks_payload_size():
    packet = encode_packet(9.5)

    assert packet[1] == 4, "Length field should match the 4-byte payload '9.50' "
    assert len(packet) == 7, "Total Packet is payload + 3 framing bytes"

def test_checksm_is_sum_of_payload_only():
    packet = encode_packet(15.03)
    payload = packet[2:-1]

    assert packet[-1] == sum(payload) & 0xFF