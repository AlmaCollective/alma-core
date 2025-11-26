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
This is the layer that turns numbers into human-readable state.

4. High-Level Pipeline (pipeline.py)

To make integration easy, Alma Core exposes a single high-level API:
from datetime import datetime, timedelta
from alma_core.cadence_layer import RawSample
from alma_core.pipeline import run_alma_core_pipeline, AlmaPipelineConfig

# 1) Build some dummy samples (in real life these come from the device).
now = datetime.utcnow()
samples = [
    RawSample(
        timestamp=now + timedelta(seconds=i * 5),
        hr_bpm=70 + (i % 5),
        rr_ms=850.0,
        accel_mg=100.0,
        signal_quality=0.9,
        battery_pct=80.0,
    )
    for i in range(0, 200)
]

# 2) Configure the pipeline (sane defaults if you don't pass anything).
config = AlmaPipelineConfig(
    cadence_seconds=120,
    window_minutes=10,
)

# 3) Run the full core pipeline.
results = run_alma_core_pipeline(samples, config=config)

# 4) Inspect the high-level interpretation.
for r in results:
    print(r.timestamp.isoformat(), r.labels, r.details, "conf=", r.confidence)
This is what higher layers (Alma Spiral, Alma Emotion AI, UI, etc.) will use.
Folder Structure (high-level)
alma-core/
├─ alma_core/
│  ├─ cadence_layer.py          # canonical 2-minute rhythm + alerts
│  ├─ dejavu_layer.py           # pattern recurrence in time
│  ├─ interpretation_layer.py   # human-readable state labels
│  └─ pipeline.py               # end-to-end API
├─ book-of-feel/                # narrative / conceptual backbone
├─ docs/                        # technical + conceptual docs
└─ README.md                    # this file
Design Principles

Stable APIs, replaceable internals
Each layer can be re-implemented in another language (Rust, Go, TypeScript, etc.) as long as it respects the same data contracts.

Separation of concerns
Cadence ≠ Deja-Vu ≠ Interpretation.
Rhythm → Pattern → Meaning.

No heavy dependencies
Pure Python + standard library in this reference implementation, so others can port it easily.

Human-first
The end product of this core is not just metrics, but readable state that can be connected to human experience and feedback.
