from science.exposure import calculate_exposure


def test_concentration_time_descriptor_is_transparent() -> None:
    result = calculate_exposure(150, 8)
    assert result["concentration_time_index"] == 1200
    assert "not a biological dose" in result["interpretation"]


def test_invalid_exposure_is_rejected() -> None:
    try:
        calculate_exposure(-1, 8)
    except ValueError:
        return
    raise AssertionError("Expected invalid PM2.5 to fail")
