
from services.statistics_service import (
    calculate_production_statistics,
)

import pytest

def make_segment(
    segment_id,
    start_time,
    run_time,
    mass_total,
):
    return {
        "segmentId": segment_id,
        "prodId": "PROD_001",
        "usrId": "N/A",
        "startTime": start_time,
        "stopTime": start_time,
        "runTime": run_time,
        "massTotal": mass_total,
    }



segments = [
    make_segment(
        "SEG_1",
        "2026-01-10T08:00:00",
        3600,
        10.0,
    ),
    make_segment(
        "SEG_2",
        "2026-01-10T10:00:00",
        1800,
        5.0,
    ),
    make_segment(
        "SEG_3",
        "2026-01-10T14:00:00",
        7200,
        20.0,
    ),
    make_segment(
        "SEG_4",
        "2026-01-11T08:00:00",
        3600,
        8.0,
    ),
]

def test_segment_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["segment"]["tonnes"] == 10.0
    assert result["segment"]["hours"] == 1.0
    assert result["segment"]["rate"] == 10.0

def test_day_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-11T08:00:00",
            7200,
            20.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["day"]["tonnes"] == 15.0
    assert result["day"]["hours"] == 1.5
    assert result["day"]["rate"] == 10.0

def test_month_statistics():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-11T08:00:00",
            7200,
            20.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["month"]["tonnes"] == 35.0
    assert result["month"]["hours"] == 3.5
    assert result["month"]["rate"] == 10.0

def test_other_month_is_excluded():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-11T08:00:00",
            3600,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-02-01T08:00:00",
            3600,
            100.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["month"]["tonnes"] == 15.0
    assert result["month"]["hours"] == 2.0
    assert result["month"]["rate"] == 7.5

def test_other_day_is_excluded():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
        make_segment(
            "SEG_2",
            "2026-01-10T10:00:00",
            1800,
            5.0,
        ),
        make_segment(
            "SEG_3",
            "2026-01-11T08:00:00",
            3600,
            100.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["day"]["tonnes"] == 15.0
    assert result["day"]["hours"] == 1.5

def test_invalid_segment_id():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            3600,
            10.0,
        ),
    ]

    with pytest.raises(ValueError):
        calculate_production_statistics(
            segments,
            "DOES_NOT_EXIST",
        )

def test_zero_runtime():

    segments = [
        make_segment(
            "SEG_1",
            "2026-01-10T08:00:00",
            0,
            10.0,
        ),
    ]

    result = calculate_production_statistics(
        segments,
        "SEG_1",
    )

    assert result["segment"]["tonnes"] == 10.0
    assert result["segment"]["hours"] == 0.0
    assert result["segment"]["rate"] == 0.0