"""
features.py

Derives combustion risk metrics from cleaned time-series data
(data/processed/) for use in modeling (src/model.py) and the
risk engine (src/risk_engine.py).

Expected input columns (after preprocessing.standardize_columns):
    time_s, temperature_c, o2_pct, radiative_heat_flux,
    flame_area (optional), pressure (optional)
"""

import numpy as np
import pandas as pd


def flame_spread_rate(df: pd.DataFrame, area_col: str = "flame_area") -> float:
    """Approximate flame spread rate as d(area)/dt, averaged over the
    growth phase (from ignition to peak area)."""
    if area_col not in df.columns:
        return np.nan
    peak_idx = df[area_col].idxmax()
    growth = df.loc[: peak_idx]
    if len(growth) < 2:
        return np.nan
    dt = growth["time_s"].iloc[-1] - growth["time_s"].iloc[0]
    d_area = growth[area_col].iloc[-1] - growth[area_col].iloc[0]
    return d_area / dt if dt > 0 else np.nan


def peak_heat_release_rate(df: pd.DataFrame, flux_col: str = "radiative_heat_flux") -> float:
    """Maximum radiative heat flux recorded during the event."""
    return df[flux_col].max() if flux_col in df.columns else np.nan


def time_to_extinction(df: pd.DataFrame, flux_col: str = "radiative_heat_flux",
                        threshold: float = 0.05) -> float:
    """Time from peak heat flux until the signal drops below
    `threshold` fraction of the peak (approximate extinction point)."""
    if flux_col not in df.columns:
        return np.nan
    peak = df[flux_col].max()
    peak_idx = df[flux_col].idxmax()
    post_peak = df.loc[peak_idx:]
    below = post_peak[post_peak[flux_col] <= threshold * peak]
    if below.empty:
        return np.nan
    return below["time_s"].iloc[0] - df["time_s"].loc[peak_idx]


def o2_depletion_slope(df: pd.DataFrame, o2_col: str = "o2_pct") -> float:
    """Linear slope of O2 concentration over time during the event
    (steeper negative slope = faster oxygen consumption = higher risk)."""
    if o2_col not in df.columns:
        return np.nan
    slope, _ = np.polyfit(df["time_s"], df[o2_col], 1)
    return slope


def radiative_fraction(df: pd.DataFrame, flux_col: str = "radiative_heat_flux",
                        total_energy_col: str = None) -> float:
    """Fraction of total energy release that is radiative, if a total
    energy column is available. Returns NaN otherwise (placeholder for
    when the dataset includes total heat release rate)."""
    if total_energy_col is None or total_energy_col not in df.columns:
        return np.nan
    total = df[total_energy_col].sum()
    radiative = df[flux_col].sum() if flux_col in df.columns else np.nan
    return radiative / total if total else np.nan


def extract_features(df: pd.DataFrame) -> dict:
    """Compute the full feature set for one combustion event/run."""
    return {
        "flame_spread_rate": flame_spread_rate(df),
        "peak_heat_release_rate": peak_heat_release_rate(df),
        "time_to_extinction": time_to_extinction(df),
        "o2_depletion_slope": o2_depletion_slope(df),
        "radiative_fraction": radiative_fraction(df),
    }


def build_feature_table(processed_files: list) -> pd.DataFrame:
    """Run extract_features over multiple processed run files and
    assemble one row per run/experiment."""
    rows = []
    for path in processed_files:
        df = pd.read_csv(path)
        feats = extract_features(df)
        feats["source_file"] = path
        rows.append(feats)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pass
