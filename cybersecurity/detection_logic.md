# Secure Detection & Override Logic

This document describes, in plain language, the decision logic implemented in
`src/risk_engine.py`, and the safeguards around it referenced in `threat_model.md`.

## Risk tiers

| Tier | Risk score | Action | Automatic? |
|------|-----------|--------|------------|
| NOMINAL | < 0.3 | No action | No |
| WATCH | 0.3 – 0.6 | Increase sensor polling rate, log event | No |
| WARNING | 0.6 – 0.85 | Alert crew/ground control, arm containment systems, wait for confirmation or a corroborating sensor | No (human-in-the-loop) |
| CRITICAL | ≥ 0.85 | Automatic containment: seal compartment, cut ventilation, trigger suppression | **Yes** |

Thresholds are configurable (`RiskThresholds` in `risk_engine.py`) — set from
validation results once the model is trained on real data, not hardcoded
guesses.

## Why only CRITICAL triggers automatic action

- Microgravity fires can escalate faster than a human response cycle, so waiting
  for confirmation at the highest confidence tier would be unsafe.
- At WARNING, the cost of a false positive (unnecessary suppression discharge,
  disrupted operations) is high enough to justify a brief human/corroboration
  step, since the model isn't yet confident enough to act alone.

## Anti-single-point-of-failure rule

No automatic CRITICAL action fires from a single sensor's raw reading — it
requires:
1. The risk score (derived from multiple combined features, not one sensor), **and**
2. Voting agreement across redundant sensors (2-of-3) for the key inputs driving that score.

This directly mitigates the sensor-spoofing threat in `threat_model.md` (#1):
an attacker would need to compromise multiple independent sensors
simultaneously and consistently to force a false CRITICAL action — or to mask
a real one.

## Fail-safe behavior

- Loss of communication from the edge controller is itself escalated to at
  least WATCH level, never treated as "no data = safe."
- Missed risk-evaluation cycles (from DoS or resource exhaustion) trigger the
  watchdog fail-safe state rather than silently continuing in NOMINAL.

## Auditability

Every tier transition, sensor vote, and actuator command is written to the
hash-chained audit log described in `threat_model.md`, enabling post-incident
reconstruction of exactly what the system saw and decided, and detection of
any tampering with that record itself.
