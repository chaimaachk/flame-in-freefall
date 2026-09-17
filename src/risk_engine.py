"""
risk_engine.py

Converts a model risk score (src/model.py) into a discrete safety
decision. This is the logical bridge between "ML Risk Prediction"
and "ICS/SCADA Simulation" in the pipeline described in the README.

Keep these thresholds explicit and documented — they are exactly
what the cybersecurity/detection_logic.md file needs to describe
and defend.
"""

from dataclasses import dataclass


@dataclass
class RiskThresholds:
    watch: float = 0.3     # log + increase monitoring frequency
    warn: float = 0.6      # alert crew, prepare containment
    critical: float = 0.85  # automatic containment / cutoff


@dataclass
class SafetyDecision:
    level: str
    risk_score: float
    action: str
    automatic: bool


def evaluate_risk(risk_score: float, thresholds: RiskThresholds = RiskThresholds()) -> SafetyDecision:
    """Map a continuous risk score to a safety decision + action.

    Design principle: automatic hardware cutoffs only trigger at the
    highest confidence tier; mid-tier risk raises alerts for human
    confirmation, avoiding false-positive shutdowns from a single
    noisy sensor reading (see cybersecurity/threat_model.md).
    """
    if risk_score >= thresholds.critical:
        return SafetyDecision(
            level="CRITICAL",
            risk_score=risk_score,
            action="Automatic containment: seal compartment, cut ventilation, trigger suppression.",
            automatic=True,
        )
    if risk_score >= thresholds.warn:
        return SafetyDecision(
            level="WARNING",
            risk_score=risk_score,
            action="Alert crew/ground control, arm containment systems, await confirmation or 2nd sensor corroboration.",
            automatic=False,
        )
    if risk_score >= thresholds.watch:
        return SafetyDecision(
            level="WATCH",
            risk_score=risk_score,
            action="Increase sensor polling rate, log event, no active intervention.",
            automatic=False,
        )
    return SafetyDecision(
        level="NOMINAL",
        risk_score=risk_score,
        action="No action.",
        automatic=False,
    )


if __name__ == "__main__":
    for score in [0.1, 0.4, 0.7, 0.9]:
        print(score, "->", evaluate_risk(score))
