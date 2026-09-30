import pytest

from backend.nea import AirQualityUnavailable, get_latest_pm25


@pytest.mark.asyncio
async def test_live_pm25_requires_server_side_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("DATA_GOV_SG_API_KEY", raising=False)
    with pytest.raises(AirQualityUnavailable, match="not configured"):
        await get_latest_pm25()


@pytest.mark.asyncio
async def test_live_pm25_rejects_unknown_region(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATA_GOV_SG_API_KEY", "test-key")
    with pytest.raises(ValueError, match="Unknown region"):
        await get_latest_pm25("moon")
