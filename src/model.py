"""
model.py

Trains and evaluates a predictive model that maps combustion
features (src/features.py) to a hazard label or continuous risk
score. Start with a simple, explainable model (Random Forest /
Gradient Boosting) — swap in a time-series model only if the
dataset and timeline support it.
"""

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score


FEATURE_COLUMNS = [
    "flame_spread_rate",
    "peak_heat_release_rate",
    "time_to_extinction",
    "o2_depletion_slope",
    "radiative_fraction",
]


def prepare_xy(feature_table: pd.DataFrame, label_col: str = "hazard_label"):
    """Split a feature table into X (features) and y (label).

    hazard_label should be added manually or derived from metadata
    (e.g. based on known experiment outcomes) — 1 = hazardous event,
    0 = contained/safe event.
    """
    X = feature_table[FEATURE_COLUMNS].fillna(0)
    y = feature_table[label_col]
    return X, y


def train_model(X: pd.DataFrame, y: pd.Series, random_state: int = 42):
    """Train a Random Forest classifier and report validation metrics.

    NOTE: microgravity combustion datasets are typically small —
    use cross-validation rather than a single train/test split if
    you have fewer than ~50 runs, and report metrics honestly.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=random_state, stratify=y if y.nunique() > 1 else None
    )

    clf = RandomForestClassifier(
        n_estimators=200, max_depth=5, random_state=random_state, class_weight="balanced"
    )
    clf.fit(X_train, y_train)

    preds = clf.predict(X_test)
    print(classification_report(y_test, preds))

    if y_test.nunique() > 1:
        try:
            probs = clf.predict_proba(X_test)[:, 1]
            print("ROC AUC:", roc_auc_score(y_test, probs))
        except Exception:
            pass

    return clf


def save_model(clf, path: str = "model.joblib"):
    joblib.dump(clf, path)


def load_model(path: str = "model.joblib"):
    return joblib.load(path)


def predict_risk_score(clf, features_row: dict) -> float:
    """Return a hazard probability (0-1) for a single set of features."""
    X = pd.DataFrame([features_row])[FEATURE_COLUMNS].fillna(0)
    return float(clf.predict_proba(X)[0, 1])


if __name__ == "__main__":
    pass
