# alma/interpretation_layer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Literal
from datetime import datetime

from .cadence_layer import CadencePoint, CadenceWindowMetrics
from .dejavu_layer import DejaVuSummary


Number = float


@dataclass
class InterpretationConfig:
    """
    Interpretation rules that convert raw metrics into human-readable states.
    """
    min_confidence: Number = 0.5
    calm_hrv_threshold: Number = 40        # ms RMSSD – rough approximate
    tension_hrv_threshold: Number = 20     # below this → tension
    high_hr_threshold: Number = 95
    low_hr_threshold: Number = 55
    movement_threshold: Number = 200       # accel magnitude (mg)
    trend_window_points: int = 3           # how many cadence points to check for trends


@dataclass
class InterpretationResult:
    """
    High-level human-readable output.
    """
    timestamp: datetime
    labels: List[str]               # ["calm", "overload", "tension pattern", ...]
    details: str                    # short explanation
    confidence: Number
    dejavu: Optional[str] = None    # e.g. "similar to 2h ago (0.87)"


def _interpret_single_point(
    point: CadencePoint,
    config: InterpretationConfig
) -> List[str]:
    """
    Interpret instantaneous state from one cadence point.
    Returns list of labels.
    """
    if point.confidence < config.min_confidence:
        return ["low_confidence"]

    labels: List[str] = []

    # HR-based hints
    hr = point.hr_mean
    if hr is not None:
        if hr > config.high_hr_threshold:
            labels.append("elevated_heart_rate")
        elif hr < config.low_hr_threshold:
            labels.append("low_heart_rate")

    # HRV-based hints
    hrv = point.hrv_rmssd
    if hrv is not None:
        if hrv >= config.calm_hrv_threshold:
            labels.append("calm_indicator")
        elif hrv <= config.tension_hrv_threshold:
            labels.append("tension_indicator")

    # movement
    mov = point.movement_level
    if mov is not None and mov > config.movement_threshold:
        labels.append("active")

    # if nothing stuck, add a neutral tag
    if not labels:
        labels.append("neutral")

    return labels


def _interpret_trend(
    recent_points: List[CadencePoint],
    config: InterpretationConfig
) -> Optional[str]:
    """
    Look at recent cadence points and detect simple trends:
    - increasing calm
    - rising tension
    - overload buildup (hr ↑, hrv ↓)
    """
    if len(recent_points) < config.trend_window_points:
        return None

    # simple linear slope via first/last
    first = recent_points[0]
    last = recent_points[-1]

    def slope(a: Optional[Number], b: Optional[Number]) -> Optional[Number]:
        if a is None or b is None:
            return None
        return b - a

    hr_slope = slope(first.hr_mean, last.hr_mean)
    hrv_slope = slope(first.hrv_rmssd, last.hrv_rmssd)
    mov_slope = slope(first.movement_level, last.movement_level)

    # decide
    if hr_slope is not None and hrv_slope is not None:
        if hr_slope < -2 and hrv_slope > 2:
            return "calming_trend"
        if hr_slope > 2 and hrv_slope < -2:
            return "tension_trend"

    # steady low movement
    if mov_slope is not None and abs(mov_slope) <= 5 and last.movement_level is not None and last.movement_level < config.movement_threshold:
        return "steady_state"

    return None


def _integrate_dejavu(
    summary: Optional[DejaVuSummary],
) -> Optional[str]:
    """
    Convert deja-vu summary into a short string.
    """
    if summary is None or not summary.matches:
        return None
    best = summary.strongest_match
    if best is None:
        return None
    # human-readable delta
    delta = best.current_time - best.past_time
    minutes = int(delta.total_seconds() // 60)
    hours = minutes // 60
    rem_min = minutes % 60
    if hours > 0:
        time_str = f"{hours}h {rem_min}m"
    else:
        time_str = f"{minutes}m"
    return f"similar to {time_str} ago ({best.similarity:.2f})"


def interpret_state(
    cadence_series: List[CadencePoint],
    windows: List[CadenceWindowMetrics],
    dejavu_summaries: List[DejaVuSummary],
    config: Optional[InterpretationConfig] = None
) -> List[InterpretationResult]:
    """
    High-level interpretation pipeline.
    For each cadence point:
        - generate instantaneous labels
        - check trend based on recent points
        - integrate dejavu info
        - produce a compact InterpretationResult
    """
    if config is None:
        config = InterpretationConfig()

    results: List[InterpretationResult] = []

    # pre-index windows and dejavu by timestamp for fast lookup
    window_map = {w.window_end: w for w in windows}
    dejavu_map = {s.window_end: s for s in dejavu_summaries}

    for i, point in enumerate(cadence_series):
        # single point labels
        single_labels = _interpret_single_point(point, config)

        # trend label (use last N points up to i)
        trend_window = cadence_series[max(0, i - config.trend_window_points + 1): i + 1]
        trend_label = _interpret_trend(trend_window, config)

        # build label list
        labels = single_labels.copy()
        if trend_label is not None:
            labels.append(trend_label)

        # details string
        details = ", ".join(labels) if labels else "neutral"

        # confidence for the result: average of point confidence
        confidence = point.confidence

        # dejavu string
        window_key = point.timestamp  # assume point.timestamp == window_end
        dejavu_summary = dejavu_map.get(window_key)
        dejavu_str = _integrate_dejavu(dejavu_summary)

        results.append(
            InterpretationResult(
                timestamp=point.timestamp,
                labels=labels,
                details=details,
                confidence=confidence,
                dejavu=dejavu_str,
            )
        )

    return results
