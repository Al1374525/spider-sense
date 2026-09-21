# Serial protocol

## Purpose

A serial link delivers a continuous stream of bytes with no inherent message boundaries. The receiver may attach to the stream at any point, including partway through a transmission, and has no way to know where it is. This protocol adds framing so that a receiver can locate the start of a message, know how many bytes belong to it, and determine whether it arrived intact.

## Packet format

| Field    | Bytes | Value / meaning |
|----------|-------|-----------------|
| Sync     | 1     | `0xAA`. Marks the start of a packet. Chosen because it lies outside the printable ASCII range and therefore cannot appear inside a text payload. Its binary form, `10101010`, is also easy to identify on a logic analyser. |
| Length   | 1     | Number of payload bytes that follow. Does not include the sync, length, or checksum bytes. |
| Payload  | N     | The temperature reading as ASCII text, e.g. `15.03`. |
| Checksum | 1     | Sum of all payload bytes, truncated to eight bits. |

Total packet size is `N + 3` bytes.

## Example packet

A reading of `15.03`:

| Byte | Hex  | Meaning |
|------|------|---------|
| 0    | `AA` | Sync |
| 1    | `05` | Five payload bytes follow |
| 2    | `31` | `1` |
| 3    | `35` | `5` |
| 4    | `2E` | `.` |
| 5    | `30` | `0` |
| 6    | `33` | `3` |
| 7    | `F7` | Checksum |

On the wire: `AA 05 31 35 2E 30 33 F7` — eight bytes total.

The checksum is the sum of the payload bytes only: `0x31 + 0x35 + 0x2E + 0x30 + 0x33 = 0xF7` (247).

## Checksum

The sender sums the payload bytes and truncates the result to one byte. The receiver performs the same calculation on the bytes it received and compares. A mismatch means the payload was altered in transit.

This matters because corrupted data is otherwise indistinguishable from valid data. A single flipped bit can turn `15.03` into `15.53` or `1503`, and a detector downstream has no way to recognise that as noise rather than a genuine event. Without validation, electrical interference would surface as a temperature anomaly.

The checksum detects corruption; it does not correct it. Invalid packets are discarded, not repaired.

## Error recovery

When the checksum fails, the receiver's position in the stream can no longer be trusted. The length field may itself have been the corrupted byte, so counting forward or backward from the current position produces a different wrong position rather than a correct one.

Recovery is therefore deliberately simple:

1. Discard the partial packet entirely.
2. Read forward one byte at a time.
3. Resume parsing at the next `0xAA`.

One reading is lost. At a sampling rate of one per second, that is a one-second gap.

The sync byte is the only element of the stream that is self-identifying — length, payload, and checksum are only meaningful once position is already known. Resynchronisation must therefore anchor on the sync byte and nothing else.

**False sync bytes.** Corruption could in principle produce a `0xAA` inside a payload, causing the receiver to begin parsing mid-message. The resulting packet will fail its checksum, and recovery repeats. The parser may be briefly wrong, but it cannot remain wrong: each failure advances the scan, and the stream re-synchronises within one or two packets.

The design goal is not a parser that never becomes confused, but one that cannot stay confused.

## Known limitations

- **A sum is a weak checksum.** Two errors that cancel each other out produce the same total and pass validation. CRC-8 detects a much wider class of errors for similar cost and is the natural upgrade.
- **Text payloads are larger than necessary.** `15.03` occupies five bytes as ASCII; the same value as a fixed-point integer would occupy two. Text was chosen because it keeps the payload free of `0xAA` and remains readable during debugging. Binary payloads would require byte-stuffing or escaping to preserve the sync byte's uniqueness.
- **No sequence numbers.** A packet lost in transit leaves no trace, so the receiver cannot distinguish a dropped reading from a slower sample rate.
- **No timestamps.** Readings carry no indication of age, so a stalled sender is indistinguishable from a healthy one until the heartbeat interval elapses.
- **Single-direction.** The receiver cannot request retransmission or acknowledge receipt.