"""Transparent exposure indexing; this is not a health-risk model."""
from __future__ import annotations

from typing import Literal, TypedDict


class ExposureResult(TypedDict):
    concentration_ug_m3: float
    duration_hours: float
    setting: str
    concentration_time_index: float
    interpretation: str
    limitation: str


def calculate_exposure(pm25: float, duration_hours: float, setting: str = "outdoor") -> ExposureResult:
    """Return PM2.5 concentration × time, never a disease or mutation probability."""
    if pm25 < 0 or duration_hours <= 0:
        raise ValueError("PM2.5 must be non-negative and duration must be positive.")
    index = round(pm25 * duration_hours, 1)
    return {
        "concentration_ug_m3": pm25,
        "duration_hours": duration_hours,
        "setting": setting,
        "concentration_time_index": index,
        "interpretation": "A transparent concentration-time descriptor for comparing scenarios, not a biological dose or health prediction.",
        "limitation": "Individual inhaled dose depends on ventilation, particle chemistry, time-activity patterns, and many other factors not represented here.",
    }
