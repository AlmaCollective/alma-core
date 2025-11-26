# Alma Core Pipeline – Cadence → Deja-Vu → Interpretation

This document shows how to use the core Alma layers end-to-end.

```python
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
    for i in range(0, 200)  # ~1000 seconds of data
]

# 2) Configure the pipeline (uses sane defaults if you don't tweak anything).
config = AlmaPipelineConfig(
    cadence_seconds=120,
    window_minutes=10,
)

# 3) Run the full core pipeline.
results = run_alma_core_pipeline(samples, config=config)

# 4) Inspect the high-level interpretation.
for r in results:
    print(r.timestamp.isoformat(), r.labels, r.details, "conf=", r.confidence)
