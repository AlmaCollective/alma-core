# alma/dejavu_layer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
import math

from .cadence_layer import CadenceWindowMetrics

Number = float


@dataclass
class DejaVuConfig:
    window_minutes: int = 10
    min_history_minutes: int = 60
    min_gap_minutes: int = 15
    similarity_threshold: Number = 0.8
    min_confidence_mean: Number = 0.6
    max_matches_per_window: int = 3


@dataclass
class DejaVuFeatureVector:
    timestamp: datetime
    hr_mean: Optional[Number]
    hrv_rmssd: Optional[Number]
    movement_mean: Optional[Number]
    confidence_mean: Number


@dataclass
class DejaVuMatch:
    current_time: datetime
    past_time: datetime
    similarity: Number
    duration_minutes: int
    notes: Optional[str] = None


@dataclass
class DejaVuSummary:
    window_start: datetime
    window_end: datetime
    matches: List[DejaVuMatch]
    strongest_match: Optional[DejaVuMatch]


def _window_to_feature_vector(
    window: CadenceWindowMetrics,
    config: DejaVuConfig,
) -> Optional[DejaVuFeatureVector]:
    """
    Convert a window into a feature vector.
    Return None if confidence is too low.
    """
    if window.confidence_mean < config.min_confidence_mean:
        return None
    return DejaVuFeatureVector(
        timestamp=window.window_end,
        hr_mean=window.hr_mean,
        hrv_rmssd=window.hrv_rmssd,
        movement_mean=window.movement_mean,
        confidence_mean=window.confidence_mean,
    )


def _vector_distance(a: DejaVuFeatureVector, b: DejaVuFeatureVector) -> Number:
    """
    Simple numeric distance between two windows, using available fields.
    """
    fields = [('hr_mean', True), ('hrv_rmssd', True), ('movement_mean', True), ('confidence_mean', False)]
    diffs = []
    for fname, signed in fields:
        va = getattr(a, fname)
        vb = getattr(b, fname)
        if va is not None and vb is not None:
            # tanh normalisation to [-1, 1] (or [0,1] for confidence)
            if signed:
                na, nb = math.tanh(va), math.tanh(vb)
            else:
                na, nb = max(0.0, min(1.0, va)), max(0.0, min(1.0, vb))
            diffs.append(na - nb)
    if not diffs:
        return 1e9
    return math.sqrt(sum(d * d for d in diffs) / len(diffs))


def _distance_to_similarity(distance: Number) -> Number:
    """
    Map distance >=0 to similarity in [0, 1].
    Smaller distance -> higher similarity.
    """
    return max(0.0, min(1.0, 1.0 / (1.0 + distance)))


def build_feature_history(
    windows: List[CadenceWindowMetrics],
    config: Optional[DejaVuConfig] = None,
) -> List[DejaVuFeatureVector]:
    """
    Build feature vectors for all windows that pass confidence filters.
    """
    if config is None:
        config = DejaVuConfig()
    out = []
    for w in windows:
        fv = _window_to_feature_vector(w, config)
        if fv is not None:
            out.append(fv)
    return out


def find_dejavu_for_window(
    current: CadenceWindowMetrics,
    history: List[DejaVuFeatureVector],
    config: Optional[DejaVuConfig] = None,
) -> DejaVuSummary:
    """
    For the current window, find similar past windows.
    """
    if config is None:
        config = DejaVuConfig()

    current_vec = _window_to_feature_vector(current, config)
    if current_vec is None:
        return DejaVuSummary(
            window_start=current.window_start,
            window_end=current.window_end,
            matches=[],
            strongest_match=None,
        )

    now = current_vec.timestamp
    gap = timedelta(minutes=config.min_gap_minutes)
    min_age = timedelta(minutes=config.min_history_minutes)

    matches: List[DejaVuMatch] = []
    for past_vec in history:
        age = now - past_vec.timestamp
        if age < gap:
            continue
        # (min_age filter optional; here we apply it strictly)
        if age > min_age:
            continue
        sim = _distance_to_similarity(_vector_distance(current_vec, past_vec))
        if sim >= config.similarity_threshold:
            matches.append(
                DejaVuMatch(
                    current_time=now,
                    past_time=past_vec.timestamp,
                    similarity=sim,
                    duration_minutes=config.window_minutes,
                    notes=None,
                )
            )

    matches.sort(key=lambda m: m.similarity, reverse=True)
    matches = matches[: config.max_matches_per_window]
    strongest = matches[0] if matches else None

    return DejaVuSummary(
        window_start=current.window_start,
        window_end=current.window_end,
        matches=matches,
        strongest_match=strongest,
    )


def run_dejavu_pipeline(
    windows: List[CadenceWindowMetrics],
    config: Optional[DejaVuConfig] = None,
) -> List[DejaVuSummary]:
    """
    Main entry point for the Deja-Vu layer.
    """
    if config is None:
        config = DejaVuConfig()

    summaries: List[DejaVuSummary] = []
    history: List[DejaVuFeatureVector] = []

    # incremental history build
    for w in windows:
        # allow search only after we have some history
        if len(history) > 0:
            summary = find_dejavu_for_window(w, history, config)
            summaries.append(summary)
        # add current to history for next iterations
        fv = _window_to_feature_vector(w, config)
        if fv is not None:
            history.append(fv)

    return summaries
