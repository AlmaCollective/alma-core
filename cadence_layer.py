
# alma/dejavu_layer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Literal, Tuple
from datetime import datetime, timedelta
from .cadence_layer import CadencePoint, CadenceWindowMetrics
import math


Number = float


@dataclass
class DejaVuConfig:
    """
    Configuration for the Deja-Vu mechanism.

    This is intentionally simple for now and can be tuned later
    without breaking the API.
    """
    window_minutes: int = 10
    min_history_minutes: int = 60          # how far back we need history
    min_gap_minutes: int = 15              # avoid matching with the immediate past
    similarity_threshold: Number = 0.8     # 0–1, higher = stricter
    min_confidence_mean: Number = 0.6      # ignore low-confidence windows
    max_matches_per_window: int = 3        # to avoid flooding


@dataclass
class DejaVuFeatureVector:
    """
    Feature representation of a window, ready for similarity comparison.
    """
    timestamp: datetime           # window_end or representative time
    hr_mean: Optional[Number]
    hrv_rmssd: Optional[Number]
    movement_mean: Optional[Number]
    confidence_mean: Number


@dataclass
class DejaVuMatch:
    """
    One deja-vu match: current window vs a similar past window.
    """
    current_time: datetime
    past_time: datetime
    similarity: Number            # 0–1
    duration_minutes: int
    notes: Optional[str] = None   # e.g. "calm repeated", "overload pattern"


@dataclass
class DejaVuSummary:
    """
    High-level summary for a given time window.
    """
    window_start: datetime
    window_end: datetime
    matches: List[DejaVuMatch]
    strongest_match: Optional[DejaVuMatch]


def _window_to_feature_vector(
    window: CadenceWindowMetrics
) -> Optional[DejaVuFeatureVector]:
    """
    Convert a CadenceWindowMetrics into a compact feature vector.
    Return None if window is too low-confidence to be used.
    """
    if window.confidence_mean < 0.6:   # config.min_confidence_mean would be nicer, but signature fixed
        return None
    return DejaVuFeatureVector(
        timestamp=window.window_end,
        hr_mean=window.hr_mean,
        hrv_rmssd=window.hrv_rmssd,
        movement_mean=window.movement_mean,
        confidence_mean=window.confidence_mean
    )


def _vector_distance(a: DejaVuFeatureVector, b: DejaVuFeatureVector) -> Number:
    """
    Compute a distance between two feature vectors.
    Use a simple numeric distance (e.g. normalized Euclidean)
    over available fields, skipping those that are None.
    """
    fields = ['hr_mean', 'hrv_rmssd', 'movement_mean', 'confidence_mean']
    diffs = []
    for f in fields:
        va = getattr(a, f)
        vb = getattr(b, f)
        if va is not None and vb is not None:
            # normalise each to [0,1] range using a gentle sigmoid
            # (confidence already in [0,1])
            if f == 'confidence_mean':
                diffs.append(va - vb)
            else:
                # tanh clamp to [-1,1] then scale to unit interval
                na = math.tanh(va)
                nb = math.tanh(vb)
                diffs.append(na - nb)
    if not diffs:
        return 1e6   # large distance if no comparable fields
    return math.sqrt(sum(d * d for d in diffs) / len(diffs))


def _distance_to_similarity(distance: Number) -> Number:
    """
    Map a non-negative distance to [0, 1] similarity score.
    Smaller distance -> higher similarity.
    """
    return max(0.0, min(1.0, 1.0 / (1.0 + distance)))


def build_feature_history(
    windows: List[CadenceWindowMetrics],
    config: DejaVuConfig
) -> List[DejaVuFeatureVector]:
    """
    Pre-compute feature vectors for all windows that are good enough
    to be used as history.
    """
    hist = []
    for w in windows:
        fv = _window_to_feature_vector(w)
        if fv is not None:
            hist.append(fv)
    return hist


def find_dejavu_for_window(
    current: CadenceWindowMetrics,
    history: List[DejaVuFeatureVector],
    config: DejaVuConfig
) -> DejaVuSummary:
    """
    For a given current window, search history for similar past windows.

    Rules:
    - skip history points that are:
        * too recent (within min_gap_minutes)
        * too far (before min_history_minutes, if we want to restrict)
    - compute similarity to all remaining history vectors
    - keep only those >= similarity_threshold
    - sort by similarity desc
    - truncate to max_matches_per_window
    """
    current_fv = _window_to_feature_vector(current)
    if current_fv is None:
        return DejaVuSummary(
            window_start=current.window_start,
            window_end=current.window_end,
            matches=[],
            strongest_match=None
        )

    now = current_fv.timestamp
    gap = timedelta(minutes=config.min_gap_minutes)
    min_age = timedelta(minutes=config.min_history_minutes)

    matches: List[DejaVuMatch] = []
    for past_fv in history:
        age = now - past_fv.timestamp
        if age < gap:
            continue
        if age > min_age:
            continue   # could be relaxed later; here we obey the config names
        sim = _distance_to_similarity(_vector_distance(current_fv, past_fv))
        if sim >= config.similarity_threshold:
            matches.append(
                DejaVuMatch(
                    current_time=now,
                    past_time=past_fv.timestamp,
                    similarity=sim,
                    duration_minutes=config.window_minutes,
                    notes=None
                )
            )

    # sort desc
    matches.sort(key=lambda m: m.similarity, reverse=True)
    matches = matches[:config.max_matches_per_window]

    strongest = matches[0] if matches else None
    return DejaVuSummary(
        window_start=current.window_start,
        window_end=current.window_end,
        matches=matches,
        strongest_match=strongest
    )


def run_dejavu_pipeline(
    windows: List[CadenceWindowMetrics],
    config: Optional[DejaVuConfig] = None
) -> List[DejaVuSummary]:
    """
    High-level pipeline:

    INPUT:
        - list of CadenceWindowMetrics (sorted by time)
    OUTPUT:
        - list of DejaVuSummary, one per window, possibly with 0+ matches

    This is the main entry point higher layers will use.
    """
    if config is None:
        config = DejaVuConfig()

    summaries: List[DejaVuSummary] = []
    history: List[DejaVuFeatureVector] = []

    # build history incrementally (only windows *before* current)
    for i, w in enumerate(windows):
        # minimal history requirement: at least one window older than min_gap
        # we cheat by using index: once we have a few windows we start
        if i == 0:
            summaries.append(
                DejaVuSummary(window_start=w.window_start, window_end=w.window_end, matches=[], strongest_match=None)
            )
            fv = _window_to_feature_vector(w)
            if fv is not None:
                history.append(fv)
            continue

        # use history *so far* (strictly past windows)
        summary = find_dejavu_for_window(w, history, config)
        summaries.append(summary)

        # add current to history for next iterations
        fv = _window_to_feature_vector(w)
        if fv is not None:
            history.append(fv)

    return summaries
