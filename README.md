# Spider-Sense

An early-warning anomaly detector for slow environmental failures.

Some failures happen quietly. A basement cools overnight and a pipe bursts by morning. A server closet's cooling fails and the hardware cooks over a weekend. The damage isn't caused by the event being undetectable — it's caused by nobody being told while there was still time to act.

Spider-Sense watches an environment, learns what normal looks like, and stays silent until it doesn't.

## Not a thermometer

A thermometer reports a number and leaves the judgment to you. You have to know that 8°C in a basement is a problem, and you have to be looking at the moment it happens.

This system infers its own baseline from recent history and reports only the deviation. It behaves less like a display and more like a smoke alarm: silent until it isn't.

## Architecture

```
Monitor
  ├─ Sensor    → read() returns a temperature
  ├─ Detector  → update(reading) returns a verdict
  │    └─ RollingWindow  (fixed-size history, O(1) insert/evict)
  └─ Alerter   → send(message)

loop:
  reading = sensor.read()
  verdict = detector.update(reading)
  if verdict: alerter.send(...)
  sleep(interval)
```

`Monitor` receives all of its collaborators at construction rather than building them. `Sensor` and `Alerter` are interfaces; `FakeSensor` and `ConsoleAlerter` are the current implementations. A hardware-backed `SerialSensor` can be substituted without modifying the detector, the window, the alerter, or the monitor — which is the point of the abstraction, not a side effect of it.

Detection logic is split deliberately: `Detector` is a class because it holds state across calls, while `is_anomalous()` is a pure function because it doesn't. The pure function is testable in one line with no setup.

## Design decisions

Three failure modes surfaced during development. Each was reproduced before being fixed.

**Baseline poisoning.** The baseline is a rolling average of recent readings. When the temperature dropped and stayed down, the cold readings entered the window and dragged the baseline toward them. The gap collapsed and the alert silenced itself after two samples — while the room was still cold. An adaptive baseline that learns from the anomaly will eventually accept the anomaly as normal.

*Fix:* the window freezes while an alert is active. No new readings are recorded, so the baseline continues to represent pre-event conditions for as long as the event lasts.

**Permanent latch.** Freezing the window fixed the silencing but introduced the opposite failure: once triggered, the alert never stood down, even after conditions returned to normal.

*Fix:* while alerting, the detector compares each reading against the frozen baseline and clears the alert once the reading returns.

**Flapping.** Using a single threshold for both triggering and clearing means a reading hovering at the boundary toggles the alert on and off every sample. An alerting system that behaves this way trains its users to ignore it.

*Fix:* hysteresis. The trigger threshold is higher than the clear threshold, and the dead zone between them absorbs noise. A reading must commit fully in either direction to change the state.

**Self-contaminated baseline.** A subtler variant, found by a test rather than by observation. The reading was added to the window *before* being compared against it, so each reading was partly its own baseline. The triggering sample was therefore baked into the frozen baseline, shifting it by a fifth of the event magnitude and making recovery unreliable. The live demo passed only because sensor noise happened to land favorably; a deterministic test exposed it immediately.

*Fix:* the anomaly check now runs before the reading joins the window.

## Known limitations

**Gradual drift is invisible.** The freeze protects the baseline from anomalies it has detected. It does nothing about a change slow enough that no single reading crosses the threshold — the baseline simply follows the temperature down. Addressing this requires comparing a short-term average against a long-term one rather than against a single adaptive baseline.

**Silence is ambiguous.** A healthy system with nothing to report and a dead system produce identical output. Proof of life requires a periodic heartbeat, which is not yet implemented.

**Readings are untimestamped.** There is no way to distinguish a current reading from a stale one, which matters as soon as the data source can stall.

**Failure modes of a real data source are unhandled.** `FakeSensor.read()` cannot block, fail, or return corrupt data. A serial-backed sensor can do all three.

## Running it

```bash
pip install -r requirements.txt
python main.py     # runs a simulated cold event and recovery
pytest             # runs the test suite
```

The simulator accepts a schedule of offsets keyed by sample number, so failure scenarios that would take hours to reproduce physically run deterministically in seconds. This is also why the tests feed readings directly rather than through the sensor: gaussian noise makes a test non-deterministic, and a test that sometimes passes is worse than no test.

## Roadmap

- **Week 1** — detection engine in Python *(complete)*
- **Week 2** — framed serial protocol with checksums and desync recovery *(complete)*
- **Week 3** — C++ parser over a fixed-size buffer, no dynamic allocation
- **Week 4** — deployment to a microcontroller driving a physical alert
