# Threat Model — Fire Detection ICS/SCADA Pipeline

## Assets to protect

- Integrity of sensor readings (temperature, O2, heat flux, flame/smoke).
- Integrity and availability of the risk-scoring pipeline (edge controller).
- Integrity of actuator command channel (vent shutoff, suppression, power cutoff, compartment seal).
- Availability of the SCADA/HMI dashboard for crew/ground control.
- Audit log integrity (for post-incident investigation and for detecting tampering itself).

## Threat actors / scenarios

| # | Threat | Description | Impact |
|---|--------|-------------|--------|
| 1 | Sensor spoofing / false data injection | Attacker (or malfunction) feeds fabricated readings to suppress a real fire signature or trigger a false alarm | Missed real event, or unnecessary shutdown/resource waste |
| 2 | Command injection | Unauthorized party sends actuator commands directly (bypassing the risk engine) | Unwanted suppression discharge, venting, or power cutoff — safety and mission risk |
| 3 | Denial-of-service on edge controller | Flooding or resource exhaustion prevents timely risk evaluation | Detection delay during an actual event |
| 4 | Firmware/software tampering | Malicious or corrupted update to edge controller logic or model weights | Silent disabling of detection, or biased risk scoring |
| 5 | Communications interception/replay | Old "all clear" sensor data replayed to mask a live event | Detection suppressed during an active fire |
| 6 | Log tampering | Attacker or fault erases/alters the audit trail after an incident | Loss of forensic capability, hides root cause |

## Defenses (mapped to threats)

1. **Sensor spoofing (→1, →5)**: redundant, physically diverse sensors per zone with 2-of-3 voting logic; a secondary anomaly-detection model flags sensor readings that are statistically inconsistent with each other or with known physical combustion behavior (e.g., temperature rising with no corresponding O2 drop).
2. **Command injection (→2)**: actuator commands must be cryptographically signed by the edge controller; actuators reject unsigned or replayed commands (nonce/timestamp checks).
3. **DoS resilience (→3)**: edge controller runs the risk engine locally with hard resource/time budgets; sensor polling and risk evaluation are prioritized over non-critical SCADA traffic; a watchdog forces fail-safe state if evaluation cycles are missed.
4. **Firmware integrity (→4)**: signed firmware/model updates only, applied through a verified update channel; hash-check on boot; no remote unauthenticated write access to the edge controller.
5. **Replay protection (→5)**: timestamped, sequenced sensor messages; edge controller rejects out-of-sequence or stale data.
6. **Log integrity (→6)**: append-only, hash-chained audit log (each entry includes hash of the previous entry) stored redundantly; anomalies in the log itself (gaps, hash mismatches) raise a WATCH-level alert.

## Residual risk

- A fully compromised edge controller with valid signing keys is out of scope for these defenses alone; this would require hardware root-of-trust / secure boot, noted here as a limitation and future-work item rather than solved in this project.
