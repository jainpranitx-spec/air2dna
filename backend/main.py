"""HTTP boundary for AIR2DNA's deterministic scientific engines."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from science.exposure import calculate_exposure
from science.mutation import annotate_substitution
from science.pathways import build_trace
from backend.nea import AirQualityUnavailable, get_latest_pm25

app = FastAPI(title="AIR2DNA API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExposureRequest(BaseModel):
    pm25: float = Field(ge=0, le=2000)
    pm10: float | None = Field(default=None, ge=0, le=3000)
    no2: float | None = Field(default=None, ge=0, le=2000)
    ozone: float | None = Field(default=None, ge=0, le=2000)
    duration_hours: float = Field(gt=0, le=168)
    location: str = "Singapore"
    scenario_name: str = "Custom scenario"
    setting: str = "outdoor"


class MutationRequest(BaseModel):
    sequence: str = Field(min_length=3, max_length=30000)
    position: int = Field(ge=1)
    alternate: str = Field(min_length=1, max_length=1)


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/air-quality/latest")
async def latest_air_quality(
    region: str = Query(default="central", description="Singapore NEA reporting region"),
) -> dict:
    """Return the latest NEA PM2.5 reading through a server-side authenticated proxy."""
    try:
        return await get_latest_pm25(region)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except AirQualityUnavailable as error:
        raise HTTPException(status_code=503, detail=str(error)) from error


@app.post("/api/trace")
def trace(request: ExposureRequest) -> dict:
    exposure = calculate_exposure(request.pm25, request.duration_hours, request.setting)
    return {"exposure": exposure, "pathway": build_trace("oxidative")}


@app.post("/api/mutation")
def mutation(request: MutationRequest) -> dict:
    try:
        return annotate_substitution(request.sequence, request.position, request.alternate)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
