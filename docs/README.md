# Alma Core

`alma-core` is the foundational layer of Alma – the part that turns raw physiological signals into structured rhythm, patterns in time, and human-readable interpretations.

It does **not** deal with UI, hardware drivers or feedback modalities.  
It focuses on three questions:

1. *What is the canonical rhythm of the body right now?*  
2. *Has this pattern appeared before?*  
3. *How can we describe this state in simple, meaningful language?*  

---

## Architecture

Alma Core is organized into three main layers:

### 1. Cadence Layer (`cadence_layer.py`)

- Takes `RawSample` objects (HR, RR, movement, signal quality, battery).
- Aggregates them into a **canonical cadence** (default: 2-minute steps).
- Computes:
  - `hr_mean`, `hr_min`, `hr_max`
  - HRV metrics (`hrv_rmssd`, `hrv_sdnn`) when RR data is available
  - movement level
  - signal quality and coverage ratio
  - a 0–1 `confidence` score
- Provides rolling window metrics via `CadenceWindowMetrics` for:
  - 6 minutes
  - 10–12 minutes
  - 30 minutes (configurable)
- Exposes basic debounced alerts:
  - `HR_HIGH`, `HR_LOW`
  - `SIGNAL_LOST`
  - `BATTERY_LOW`

This is the **physiological backbone** of Alma.

---

### 2. Deja-Vu Layer (`dejavu_layer.py`)

- Works on top of `CadenceWindowMetrics`.
- Converts each window into a compact `DejaVuFeatureVector`.
- Compares current state with **past windows** and measures similarity.
- Produces:
  - `DejaVuMatch` objects (current vs. past window, with similarity 0–1)
  - `DejaVuSummary` per window, including the strongest match

The goal is simple:  
> detect when the body is re-entering a familiar pattern (*“this has happened before”*),  
not as mysticism, but as **pattern recurrence in time**.

---

### 3. Interpretation Layer (`interpretation_layer.py`)

- Takes:
  - `CadencePoint` series
  - window metrics
  - Deja-Vu summaries
- Applies simple, tunable rules to generate:
  - instantaneous labels (e.g. `calm_indicator`, `tension_indicator`, `active`)
  - trend labels (e.g. `calming_trend`, `tension_trend`, `steady_state`)
  - optional deja-vu notes (e.g. *"similar to 1h 12m ago (0.83)"*)
- Returns a list of `InterpretationResult` objects:

```python
@dataclass
class InterpretationResult:
    timestamp: datetime
    labels: List[str]
    details: str
    confidence: float
    dejavu: Optional[str] = None
