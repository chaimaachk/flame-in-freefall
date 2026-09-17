"""
preprocessing.py

Functions for loading and cleaning raw microgravity combustion data
(data/raw/) into a consistent tabular/time-series format
(data/processed/).

Expected raw data: time-series sensor logs with columns that may
include timestamp, temperature, O2 concentration, radiative heat
flux, flame spread / area, and pressure. Adjust the column mapping
in `load_raw` once the actual challenge dataset schema is known.
"""

import pandas as pd


def load_raw(path: str) -> pd.DataFrame:
    """Load a single raw combustion data file into a DataFrame.

    TODO: update to match the actual NASA dataset format
    (CSV, delimited text, or another format) once confirmed.
    """
    df = pd.read_csv(path)
    return df


def standardize_columns(df: pd.DataFrame, column_map: dict) -> pd.DataFrame:
    """Rename raw columns to a standard internal schema.

    column_map example:
        {
            "Time_s": "time_s",
            "Temp_C": "temperature_c",
            "O2_pct": "o2_pct",
            "HeatFlux_Wm2": "radiative_heat_flux",
        }
    """
    return df.rename(columns=column_map)


def handle_missing(df: pd.DataFrame, method: str = "interpolate") -> pd.DataFrame:
    """Handle missing/irregular sensor readings.

    method: "interpolate" (default), "ffill", or "drop"
    """
    if method == "interpolate":
        return df.interpolate(limit_direction="both")
    if method == "ffill":
        return df.ffill().bfill()
    if method == "drop":
        return df.dropna()
    raise ValueError(f"Unknown method: {method}")


def clean_dataset(raw_path: str, column_map: dict, out_path: str) -> pd.DataFrame:
    """Full pipeline: load -> standardize -> handle missing -> save."""
    df = load_raw(raw_path)
    df = standardize_columns(df, column_map)
    df = handle_missing(df)
    df.to_csv(out_path, index=False)
    return df


if __name__ == "__main__":
    # Example usage once real data + column map are available:
    # clean_dataset(
    #     raw_path="data/raw/experiment_001.csv",
    #     column_map={"Time_s": "time_s", "Temp_C": "temperature_c"},
    #     out_path="data/processed/experiment_001_clean.csv",
    # )
    pass
