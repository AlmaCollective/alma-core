"""
cadence_profile_demo.py

Small demo that simulates Alma's human cadence profile over ~60 minutes
and prints the resulting states and events.

This is NOT medical software. It is an engineering demo only.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional
import random
import statistics
from datetime import datetime, timedelta


# ---------------------------------------------------------------------
# 1. Basic types
# ---------------------------------------------------------------------

class CadenceState(Enum):
    CALM = auto()
    FOCUSED = auto()
    STRAIN = auto()
    RISK = auto()
    UNKNOWN = auto()


@dataclass
class RawSample:
    timestamp: datetime
    hr_bpm: float
    rr_ms: float
    accel_mg: float
    signal_quality: float


@dataclass
class CadenceResult:
    timestamp: datetime
    state: CadenceState
    confidence: float
    events: List[str]


# ---------------------------------------------------------------------
# 2. Default baseline and thresholds (v0.1)
# ---------------------------------------------------------------------

BASE_HR_BPM = 75
BASE_RR_MS = 900
BASE_ACC_MG = 50

CADENCE_WINDOW_SEC = 120       # 2 min windows
ROLLING_WINDOW_MIN = 10        # 10 min trend window


# ---------------------------------------------------------------------
# 3. Core state logic (simplified v0.1)
# ---------------------------------------------------------------------

def infer_state(samples: List[RawSample]) -> CadenceResult:
    """
    Infer cadence state for the LAST window, using all samples provided.
    `samples` should cover at least the last 10 minutes for trends.
    """

    if not samples:
        now = datetime.utcnow()
        return CadenceResult(now, CadenceState.UNKNOWN, 0.0, ["EVENT_SIGNAL_LOSS"])

    latest = samples[-1]
    now = latest.timestamp

    # Filter last 2 minutes (current window)
    window_start = now - timedelta(seconds=CADENCE_WINDOW_SEC)
    window = [s for s in samples if s.timestamp >= window_start]

    if not window:
        return CadenceResult(now, CadenceState.UNKNOWN, 0.0, ["EVENT_SIGNAL_LOSS"])

    # Check signal quality
    good = [s for s in window if s.signal_quality >= 0.7]
    if len(good) < len(window) * 0.5:
        return CadenceResult(now, CadenceState.UNKNOWN, 0.0, ["EVENT_SIGNAL_LOSS"])

    # Aggregate metrics for current window
    hr_vals = [s.hr_bpm for s in good]
    rr_vals = [s.rr_ms for s in good]
    accel_vals = [s.accel_mg for s in good]

    hr_mean = statistics.fmean(hr_vals)
    rr_mean = statistics.fmean(rr_vals)
    accel_mean = statistics.fmean(accel_vals)

    # Trend over last 10 min
    trend_start = now - timedelta(minutes=ROLLING_WINDOW_MIN)
    trend_window = [s for s in samples if s.timestamp >= trend_start and s.signal_quality >= 0.7]
    if len(trend_window) >= 2:
        hr_trend = trend_window[-1].hr_bpm - trend_window[0].hr_bpm
    else:
        hr_trend = 0.0

    # --- State rules (simplified, aligned with HUMAN_CADENCE_PROFILE_SPEC v0.1) ---

    state = CadenceState.CALM
    confidence = 0.5
    events: List[str] = []

    # RISK
    if (
        hr_mean > BASE_HR_BPM + 40
        or hr_mean > 130
        or rr_mean < BASE_RR_MS - 350
    ):
        state = CadenceState.RISK
        confidence = 0.7
        if hr_mean > BASE_HR_BPM + 45 or rr_mean < BASE_RR_MS - 400:
            confidence += 0.1
        events.append("EVENT_SLOW_DOWN")

    # STRAIN
    elif (
        (hr_mean > BASE_HR_BPM + 25)
        or (rr_mean < BASE_RR_MS - 250)
        or (accel_mean > BASE_ACC_MG + 400)
        or (hr_trend >= 10)
    ):
        state = CadenceState.STRAIN
        confidence = 0.65
        events.append("EVENT_MICRO_BREAK_RECOMMENDED")

    # FOCUSED
    elif (
        BASE_HR_BPM + 5 <= hr_mean <= BASE_HR_BPM + 25
        and BASE_RR_MS - 200 <= rr_mean <= BASE_RR_MS
        and accel_mean < BASE_ACC_MG + 300
    ):
        state = CadenceState.FOCUSED
        confidence = 0.6
        if abs(hr_trend) <= 3:
            confidence += 0.1

    # CALM
    else:
        state = CadenceState.CALM
        confidence = 0.6

    # Clamp confidence
    confidence = max(0.0, min(1.0, confidence))

    return CadenceResult(now, state, confidence, events)


# ---------------------------------------------------------------------
# 4. Simple simulator
# ---------------------------------------------------------------------

def simulate_stream(
    minutes: int = 60,
    base_hr: int = BASE_HR_BPM,
    seed: Optional[int] = 42,
) -> List[CadenceResult]:
    """
    Simulates `minutes` of data with phases:
    - calm
    - focused work
    - strain
    - short risk episode
    Returns cadence results for each cadence window.
    """
    if seed is not None:
        random.seed(seed)

    start = datetime.utcnow()
    samples: List[RawSample] = []
    results: List[CadenceResult] = []

    total_seconds = minutes * 60
    step = 5  # sample every 5 seconds

    for i in range(0, total_seconds, step):
        t = start + timedelta(seconds=i)

        # Phase selection based on time
        minute = i // 60
        if minute < 10:
            phase = "CALM"
        elif minute < 30:
            phase = "FOCUSED"
        elif minute < 50:
            phase = "STRAIN"
        else:
            phase = "RISK"

        # Generate HR / RR / movement per phase
        if phase == "CALM":
            hr = random.gauss(base_hr, 3)
            accel = abs(random.gauss(BASE_ACC_MG + 80, 40))
        elif phase == "FOCUSED":
            hr = random.gauss(base_hr + 15, 5)
            accel = abs(random.gauss(BASE_ACC_MG + 180, 60))
        elif phase == "STRAIN":
            hr = random.gauss(base_hr + 30, 8)
            accel = abs(random.gauss(BASE_ACC_MG + 350, 80))
        else:  # RISK
            hr = random.gauss(base_hr + 50, 10)
            accel = abs(random.gauss(BASE_ACC_MG + 450, 90))

        # RR ~ 60000 / HR with some noise
        rr = 60000.0 / max(hr, 40) + random.gauss(0, 30)

        # Signal quality – occasionally bad
        if random.random() < 0.03:
            sq = random.uniform(0.3, 0.6)
        else:
            sq = random.uniform(0.8, 1.0)

        sample = RawSample(
            timestamp=t,
            hr_bpm=hr,
            rr_ms=rr,
            accel_mg=accel,
            signal_quality=sq,
        )
        samples.append(sample)

        # Every cadence window, compute result
        if i > 0 and i % CADENCE_WINDOW_SEC == 0:
            res = infer_state(samples)
            results.append(res)

    return results


# ---------------------------------------------------------------------
# 5. CLI entry point
# ---------------------------------------------------------------------

def main():
    results = simulate_stream(minutes=60)

    print("Time\t\tState\tConf.\tEvents")
    print("-" * 60)
    for r in results:
        time_str = r.timestamp.strftime("%H:%M:%S")
        state_str = r.state.name
        conf_str = f"{r.confidence:.2f}"
        events_str = ",".join(r.events) if r.events else "-"
        print(f"{time_str}\t{state_str}\t{conf_str}\t{events_str}")


if __name__ == "__main__":
    main()
