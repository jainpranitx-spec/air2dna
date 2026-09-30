"""Small, authenticated client for Singapore NEA PM2.5 data via data.gov.sg."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Literal, TypedDict

import httpx
from dotenv import load_dotenv

PM25_URL = "https://api-open.data.gov.sg/v2/real-time/api/pm25"
REGIONS = {"national", "central", "east", "west", "north", "south"}

# Local convenience only; production should inject this through its secret manager.
load_dotenv(Path(__file__).with_name(".env"))


class LivePM25(TypedDict):
    source: str
    timestamp: str
    updated_at: str
    region: str
    pm25_ug_m3: int | None
    national_pm25_ug_m3: int | None
    unit: Literal["µg/m³"]
    freshness_note: str


class AirQualityUnavailable(Exception):
    """Raised when upstream NEA data cannot be safely supplied to the app."""


async def get_latest_pm25(region: str = "central") -> LivePM25:
    """Fetch a current NEA PM2.5 reading without exposing the API key to browsers."""
    normalized_region = region.lower()
    if normalized_region not in REGIONS:
        raise ValueError(f"Unknown region '{region}'. Choose one of: {', '.join(sorted(REGIONS))}.")

    api_key = os.environ.get("DATA_GOV_SG_API_KEY")
    if not api_key or api_key == "replace_with_data_gov_sg_key":
        raise AirQualityUnavailable("Live air-quality data is not configured.")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(PM25_URL, headers={"x-api-key": api_key})
            response.raise_for_status()
        payload = response.json()
        item = payload["data"]["items"][0]
        readings = item["readings"]["pm25_one_hourly"]
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as error:
        raise AirQualityUnavailable("The NEA live PM2.5 service is temporarily unavailable.") from error

    return {
        "source": "Singapore NEA via data.gov.sg",
        "timestamp": item["timestamp"],
        "updated_at": item["updatedTimestamp"],
        "region": normalized_region,
        "pm25_ug_m3": readings.get(normalized_region),
        "national_pm25_ug_m3": readings.get("national"),
        "unit": "µg/m³",
        "freshness_note": "This is a monitored ambient regional reading, not an individual's exposure dose.",
    }
