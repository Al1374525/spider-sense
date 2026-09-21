from spider_sense.protocol import encode_packet, PacketDecoder


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


from spider_sense.protocol import encode_packet, PacketDecoder


def test_decoder_reads_complete_packet():
    decoder = PacketDecoder()
    packet = encode_packet(15.03)

    assert decoder.feed(packet) == [15.03]


def test_decoder_waits_for_partial_packet():
    decoder = PacketDecoder()
    packet = encode_packet(15.03)

    assert decoder.feed(packet[:4]) == [], "Should not decode an incomplete packet"
    assert decoder.feed(packet[4:]) == [15.03], "Should decode once the rest arrives"


def test_decoder_rejects_bad_checksum():
    decoder = PacketDecoder()
    packet = bytearray(encode_packet(15.03))
    packet[-1] ^= 0xFF

    assert decoder.feed(bytes(packet)) == [], "Corrupt packet must be discarded"


def test_decoder_resyncs_after_garbage():
    decoder = PacketDecoder()
    garbage = bytes([0x12, 0x34, 0x56])

    assert decoder.feed(garbage + encode_packet(15.03)) == [15.03]


def test_decoder_reads_two_packets_in_one_feed():
    decoder = PacketDecoder()
    data = encode_packet(15.03) + encode_packet(9.5)

    assert decoder.feed(data) == [15.03, 9.5]