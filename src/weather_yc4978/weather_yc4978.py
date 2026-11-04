
"""Weather station utilities for QMSS G5072."""

import math

import pandas as pd

ABSOLUTE_ZERO_C = -273.15
MIN_PLAUSIBLE_C = -90.0
MAX_PLAUSIBLE_C = 60.0


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit.

Examples
--------
>>> celsius_to_fahrenheit(20)
68.0
"""
    if isinstance(celsius, bool) or not isinstance(celsius, (int, float)):
        raise TypeError("celsius must be a number")
    if celsius < ABSOLUTE_ZERO_C:
        raise ValueError("temperature cannot be below absolute zero")
    return celsius * 9 / 5 + 32


def summarize_temperatures(temps: list[float]) -> dict[str, float]:
    """Summarize temperature readings, ignoring NaN values.

    Examples
    --------
    >>> summarize_temperatures([10.0, 20.0, 30.0])
    {'mean': 20.0, 'min': 10.0, 'max': 30.0, 'n_missing': 0}
    """
    valid = [t for t in temps if not math.isnan(t)]
    if not valid:
        raise ValueError("no valid temperature readings")
    return {
        "mean": sum(valid) / len(valid),
        "min": min(valid),
        "max": max(valid),
        "n_missing": len(temps) - len(valid),
    }


def clean_readings(df: pd.DataFrame) -> pd.DataFrame:
    """Clean station readings and add Fahrenheit temperatures."""
    cleaned = df.dropna(subset=["temp_c"])
    in_range = cleaned["temp_c"].between(MIN_PLAUSIBLE_C, MAX_PLAUSIBLE_C)
    cleaned = cleaned[in_range].copy()
    cleaned["temp_f"] = cleaned["temp_c"] * 9 / 5 + 32
    return cleaned.sort_values(["station", "date"]).reset_index(drop=True)
