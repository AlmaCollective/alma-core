# alma/dejavu_layer.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Literal, Tuple
from datetime import datetime
from .cadence_layer import CadencePoint, CadenceWindowMetrics


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
    # TODO:
    # - if window.confidence_mean < some minimum, return None
    # - otherwise construct DejaVuFeatureVector using:
    #     - hr_mean
    #     - hrv_rmssd
    #     - movement_mean
    #     - confidence_mean
    raise NotImplementedError


def _vector_distance(a: DejaVuFeatureVector, b: DejaVuFeatureVector) -> Number:
    """
    Compute a distance between two feature vectors.
    Use a simple numeric distance (e.g. normalized Euclidean)
    over available fields, skipping those that are None.
    """
    # TODO:
    # - collect pairs of (a_field, b_field) that are both not None
    # - compute squared differences
    # - average them
    # - take sqrt
    # - if no comparable fields, return a large distance
    raise NotImplementedError


def _distance_to_similarity(distance: Number) -> Number:
    """
    Map a non-negative distance to [0, 1] similarity score.
    Smaller distance -> higher similarity.
    """
    # TODO:
    # - use a simple monotonically decreasing mapping, e.g.:
    #   similarity = 1 / (1 + distance)
    # - clamp to [0, 1]
    raise NotImplementedError


def build_feature_history(
    windows: List[CadenceWindowMetrics],
    config: DejaVuConfig
) -> List[DejaVuFeatureVector]:
    """
    Pre-compute feature vectors for all windows that are good enough
    to be used as history.
    """
    # TODO:
    # - convert each window to feature vector with _window_to_feature_vector
    # - drop None
    # - return list
    raise NotImplementedError


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
    # TODO:
    # - convert current window to feature vector (or return empty summary if None)
    # - iterate over history, apply time filters
    # - compute distance & similarity
    # - build DejaVuMatch objects
    # - sort and select top matches
    # - build and return DejaVuSummary
    raise NotImplementedError


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
    # TODO:
    # - if config is None, create a default DejaVuConfig()
    # - build history feature vectors
    # - for each window (starting after we have enough history):
    #     * call find_dejavu_for_window with the history so far
    #     * append summary to results
    # - return list of summaries
    raise NotImplementedError
