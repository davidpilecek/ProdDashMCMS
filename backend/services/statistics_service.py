from datetime import datetime


def _build_stats(segments: list[dict]) -> dict:
    if not segments:
        return {
            "tonnes": 0.0,
            "hours": 0.0,
            "rate": 0.0,
        }

    tonnes = sum(
        float(segment["massTotal"])
        for segment in segments
    )

    hours = sum(
        float(segment["runTime"])
        for segment in segments
    ) / 3600

    return {
        "tonnes": tonnes,
        "hours": hours,
        "rate": tonnes / hours if hours > 0 else 0.0,
    }


def calculate_production_statistics(
    segments: list[dict],
    selected_segment_id: str,
) -> dict:

    parsed_segments = [
        (
            segment,
            datetime.fromisoformat(
                segment["startTime"]
            ),
        )
        for segment in segments
    ]

    selected_segment, selected_start_time = next(
        (
            (segment, start_time)
            for segment, start_time in parsed_segments
            if segment["segmentId"] == selected_segment_id
        ),
        (None, None),
    )

    if selected_segment is None or selected_start_time is None:
        raise ValueError(
            f"Segment not found: {selected_segment_id}"
        )

    selected_day = selected_start_time.date()
    selected_month = selected_start_time.month
    selected_year = selected_start_time.year

    day_segments = [
        segment
        for segment, start_time in parsed_segments
        if start_time.date() == selected_day
    ]

    month_segments = [
        segment
        for segment, start_time in parsed_segments
        if (
            start_time.month == selected_month
            and start_time.year == selected_year
        )
    ]

    return {
        "segment": _build_stats(
            [selected_segment]
        ),
        "day": _build_stats(
            day_segments
        ),
        "month": _build_stats(
            month_segments
        ),
    }