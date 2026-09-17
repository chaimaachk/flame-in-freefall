# Flame in Freefall: AI-Powered Fire Safety Insights from Microgravity Combustion Data

**Team:** _TBD_
**Challenge:** NASA Space Apps Challenge 2026 — Flame in Freefall
**Track:** Non-App Execution (AI/ML Microgravity Combustion Risk & Detection Paper)

---

## Abstract

_(150–250 words: problem, approach, key result, why it matters for space habitat safety.)_

## 1. Introduction & Motivation

- Why fire behaves differently in microgravity (spherical/hemispherical flame spread, absence of buoyant convection, smoke doesn't rise and stays suspended near the source, different extinguishment dynamics, longer/slower smoldering in some regimes).
- Why this makes early, automated detection more important than in terrestrial habitats (crew may not visually notice smoke the way they would on Earth).
- What this paper contributes: a risk model derived from NASA microgravity combustion data, plus a secure ICS/SCADA-style detection and containment architecture.

## 2. Data

- Dataset(s) used, source, and brief description (instrument, experiment series, what was measured).
- Sampling rate, number of runs/experiments, known limitations (small sample size is typical and should be stated plainly).

## 3. Methodology

### 3.1 Preprocessing
_(cleaning, missing data handling — see `src/preprocessing.py`)_

### 3.2 Feature Engineering
_(flame spread rate, peak heat release rate, time-to-extinction, O2 depletion slope, radiative fraction — see `src/features.py`)_

### 3.3 Model
_(model choice and why, training/validation approach — see `src/model.py`)_

### 3.4 Risk Engine & Safety Decision Logic
_(mapping risk score to NOMINAL/WATCH/WARNING/CRITICAL tiers — see `src/risk_engine.py` and `cybersecurity/detection_logic.md`)_

## 4. Results

- Model performance metrics (precision/recall, ROC AUC, or regression error as appropriate).
- Key figures (insert from `figures/`): raw sensor traces, feature distributions, model performance plots.
- Qualitative discussion: which features were most predictive, and does that match known combustion physics?

## 5. Secure Detection & Containment Architecture

_(Summarize `cybersecurity/architecture.md`, `threat_model.md`, and `detection_logic.md` — include the architecture diagram.)_

- ICS/SCADA framing of the pipeline.
- Threat model summary (sensor spoofing, command injection, DoS, firmware tampering, replay, log tampering).
- Defenses (sensor voting, signed commands, fail-safe defaults, hash-chained audit log).

## 6. Limitations & Future Work

- Dataset size and generalizability.
- Model interpretability vs. accuracy trade-offs.
- Hardware root-of-trust / secure boot as unaddressed residual risk.
- Path to testing against real ISS-representative sensor noise and adversarial conditions.

## 7. Conclusion

_(2–3 sentences tying the ML result and the security architecture back to crew safety impact.)_

## References

_(NASA dataset citation, any papers on microgravity combustion, ICS/SCADA security standards referenced, e.g. NIST SP 800-82.)_
