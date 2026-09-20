# ICS/SCADA Architecture — Microgravity Fire Detection & Response

## Pipeline as an Industrial Control System

```
[Field Sensors]                [Edge Controller / PLC]        [SCADA / HMI]              [Actuators]
Temp, O2, Heat Flux,   --->    Local aggregation, risk    --->  Operator/crew       --->  Vent shutoff
Flame/Smoke sensors            engine evaluation                dashboard, alerts         Suppression system
(redundant, voted)             (src/risk_engine.py)              Manual override           Power cutoff to zone
                                                                                             Compartment seal
```

## Layers

1. **Field layer (sensors)** — redundant sensor sets per compartment (at minimum 2-of-3 voting for any automatic action) to avoid single-point spoofing or malfunction triggering a false shutdown.
2. **Edge/control layer** — runs preprocessing + the ML risk model + `risk_engine.py` decision logic close to the sensors, so detection doesn't depend on a live link to a central system.
3. **Supervisory layer (SCADA/HMI)** — crew/ground control dashboard: current risk levels per zone, alert history, manual override controls.
4. **Actuation layer** — ventilation shutoff, fire suppression discharge, zone power cutoff, compartment sealing.

## Control Flow

1. Sensors report at fixed interval (increased automatically at WATCH level — see `risk_engine.py`).
2. Edge controller computes combustion features + risk score.
3. `evaluate_risk()` maps score to NOMINAL / WATCH / WARNING / CRITICAL.
4. WARNING → SCADA raises alert, arms actuators, waits for confirmation or corroborating sensor data.
5. CRITICAL → automatic actuation (no human-in-the-loop delay, since time-to-harm in microgravity fires is short).
6. All state transitions are logged immutably for post-event audit (see `threat_model.md` for why this matters).

## Design principles

- **Fail-safe default**: loss of sensor communication is treated as elevated risk, not nominal.
- **Least trust in a single input**: no single sensor reading can trigger CRITICAL-level automatic action alone.
- **Local autonomy**: edge controller can make the CRITICAL call without waiting on SCADA/ground link latency.
- **Human override always available**, but never required to stop a runaway automatic response fast enough to matter.


---

## Visual Architecture Diagram


graph TD
    subgraph Layer1 [1. Field Layer - Sensors]
        S1[Temp / Heat Flux]
        S2[O2 / CO2 Telemetry]
        S3[Flame / Smoke Sensors]
    end

    subgraph Layer2 [2. Edge/Control Layer - PLC]
        FE[Feature Extraction]
        ML[ML Risk Prediction]
        RE[risk_engine.py Evaluation]
        VOT{2-of-3 Sensor Voting}
        
        S1 & S2 & S3 --> FE --> ML --> RE --> VOT
    end

    subgraph Layer3 [3. Supervisory Layer - SCADA/HMI]
        DASH[Crew Dashboard & Alerts]
        OVER[Manual Override Controls]
        LOG[Immutable Audit Logging]
    end

    subgraph Layer4 [4. Actuation Layer]
        A1[Nominal / Log Event]
        A2[Watch / Increase Polling Rate]
        A3[Warning / Alert Crew & Arm Actuators]
        A4[CRITICAL / Auto Compartment Seal & Suppression]
    end

    VOT -- Telemetry State --> DASH & LOG
    OVER -. Override Command .-> Layer4
    
    VOT -- Score < 0.30 --> A1
    VOT -- 0.30 <= Score < 0.60 --> A2
    VOT -- 0.60 <= Score < 0.85 --> A3
    VOT -- Score >= 0.85 + Consensus --> A4