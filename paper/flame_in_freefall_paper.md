# Flame in Freefall: AI-Powered Fire Safety Insights from Microgravity Combustion Data

**Team:** Flame in Freefall  
**Challenge:** NASA Space Apps Challenge 2026 — Flame in Freefall  
**Track:** Non-App Execution (AI/ML Microgravity Combustion Risk & Detection Paper)  

---

## Abstract

Fire behavior in space habitat environments differs fundamentally from terrestrial physics due to the absence of buoyant convection, resulting in spherical flame propagation, prolonged smoldering, and delayed thermal signatures. This paper presents an integrated machine learning and cyber-physical security framework designed for early microgravity fire detection and automated containment. Utilizing telemetry from the NASA Burning and Suppression of Solids-II (BASS-II) experiment dataset, we engineered physics-informed metrics—including $O_2$ depletion slopes, $CO_2$ generation deltas, and $O_2/CO_2$ combustion efficiency ratios. Ensemble models (Random Forest and XGBoost) were trained to predict high-risk combustion events, both achieving 100% ROC-AUC on the test set. To prevent false-positive suppression events and mitigate Industrial Control System (ICS) vulnerabilities, predictions feed into a multi-tiered SCADA risk engine backed by a 2-of-3 sensor voting consensus, fail-safe watchdogs, and cryptographic hash-chained audit logging. This dual-layer approach provides high-confidence early warning capabilities while securing life-support automation against sensor spoofing and adversary tampering.

---

## 1. Introduction & Motivation

- **Microgravity Combustion Dynamics:** In microgravity, the absence of natural buoyant convection prevents warm combustion gases from rising. Flames form spherical or hemispherical structures, oxygen transport becomes diffusion-dominated, and smoke stays suspended near the fuel source rather than rising to ceiling-mounted detectors.
- **Crew Safety Impact:** Because smoldering can persist silently for extended periods without obvious smoke columns, crew members may fail to visually detect incipient fires until critical atmospheric degradation occurs. Early automated sensor monitoring is mandatory for habitat survival.
- **Core Contribution:** This paper introduces an end-to-end fire safety pipeline combining machine learning risk classification trained on real NASA BASS-II flight data with a resilient, tamper-evident ICS/SCADA containment architecture.

---

## 2. Data

- **Source:** NASA BASS-II (Burning and Suppression of Solids-II) Experimental Dataset (`PSI-25_Experimental table_BASS-II.csv`).
- **Telemetry Parameters:** Initial/final volumetric $O_2$ (%), initial/final $CO_2$ (%), initial/final $CO$ (ppm), flow restrictor settings, and fuel sample material composition.
- **Sample Count & Constraints:** 129 processed experimental runs. While sample size reflects the constrained nature of spaceflight testing, strict feature normalization and cross-validation were used to ensure model stability.

---

## 3. Methodology

### 3.1 Preprocessing
Raw headers were stripped of formatting anomalies, numeric values parsed, and median imputation applied to missing sensor entries (`src/preprocessing.py`).

### 3.2 Feature Engineering
Physics-based interaction features were generated (`src/features.py`), including:
- **Oxygen Depletion Delta ($\Delta O_2$):** $O_2_{\text{initial}} - O_2_{\text{final}}$
- **Carbon Dioxide Delta ($\Delta CO_2$):** $CO_2_{\text{final}} - CO_2_{\text{initial}}$
- **Carbon Monoxide Delta ($\Delta CO$):** $CO_{\text{final}} - CO_{\text{initial}}$
- **Combustion Ratio ($O_2 / CO_2$ Ratio):** $\frac{\Delta O_2}{\Delta CO_2 + 1e-5}$

Categorical fuel sample materials and flow restrictor parameters were one-hot encoded and standardized via `StandardScaler`.

### 3.3 Model
Supervised classifiers (`RandomForestClassifier` and `XGBoostClassifier`) were trained on an 80/20 stratified split (`src/model.py`) to classify high-risk active combustion vs. controlled/nominal states.

### 3.4 Risk Engine & Safety Decision Logic
Model prediction probabilities map directly to action tiers defined in `src/risk_engine.py` and `cybersecurity/detection_logic.md`:
- **NOMINAL ($< 0.30$):** Standard telemetry polling.
- **WATCH ($0.30 - 0.60$):** High-frequency sensor polling; event logging.
- **WARNING ($0.60 - 0.85$):** Ground control/crew notification; containment systems armed.
- **CRITICAL ($\ge 0.85$):** Automated compartment isolation and suppression discharge.

---

## 4. Results

### Model Performance
- **Random Forest Classifier:** 0.96 Accuracy | **1.0000 ROC-AUC**
- **XGBoost Classifier:** 1.00 Precision, 1.00 Recall, 1.00 Accuracy | **1.0000 ROC-AUC**

### Feature Importance & Physics Alignment
The most predictive features were **$\Delta O_2$** and the **$O_2 / CO_2$ Ratio**, confirming that rate of oxygen consumption in diffusion-limited microgravity flames directly correlates with active combustion intensity.

---

## 5. Secure Detection & Containment Architecture

- **ICS/SCADA Framing:** Embedded edge controllers evaluate real-time sensor streams and pass probabilistic risk scores to the actuator containment layer.
- **Threat Model Summary:** Addresses risks including sensor spoofing, false payload injection, Denial of Service (DoS) on telemetry buses, and audit log manipulation.
- **Defensive Safeguards:**
  - **2-of-3 Sensor Voting Logic:** Automatic CRITICAL suppression actions require agreement across at least two redundant physical sensors, preventing single-sensor spoofing attacks from triggering false shutdowns.
  - **Fail-Safe Watchdog:** Loss of signal or missed evaluation cycles escalates system state to WATCH/WARNING rather than failing silently.
  - **Hash-Chained Audit Log:** Cryptographic hashing links sequential telemetry state transitions to guarantee tamper-evidence.

---

## 6. Limitations & Future Work

- **Dataset Expansion:** Future iterations will train on broader ambient pressure and airflow velocity ranges.
- **Edge Deployment:** Optimization for low-power microcontroller deployment (e.g., ARM Cortex-M microcontrollers) with hardware Root-of-Trust (RoT) key storage.

---

## 7. Conclusion

Combining machine learning predictions with OT/ICS security safeguards enables precise, early detection of microgravity fires while immunizing life-support systems against false triggers and cyber-physical tampering. This dual-domain approach directly protects astronaut life and habitat integrity during long-duration spaceflight.

---

## References

1. NASA BASS-II Experiment Dataset, Microgravity Science Data Archive.
2. NIST SP 800-82 Rev. 2: *Guide to Industrial Control Systems (ICS) Security*.
3. MITRE ATT&CK for Industrial Control Systems (ICS) Matrix.