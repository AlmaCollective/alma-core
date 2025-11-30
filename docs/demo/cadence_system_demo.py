from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta
import json
import random

# --------------------------------------------------
# 1. Data model
# --------------------------------------------------

@dataclass
class CadenceSample:
    timestamp: str
    hr_bpm: float
    rr_bpm: float
    strain: float
    risk: float
    event: Optional[str]


# --------------------------------------------------
# 2. JSON helpers
# --------------------------------------------------

def samples_to_json(samples: List[CadenceSample]) -> str:
    return json.dumps([s.__dict__ for s in samples], indent=2)


# --------------------------------------------------
# 3. Cadence profile simulator
# --------------------------------------------------

class _noise:
    state = 42

def simulate_cadence_profile(minutes: int = 10) -> List[CadenceSample]:
    samples = []
    now = datetime.utcnow()

    for i in range(minutes):
        # fake signals
        hr = random.uniform(60, 100)
        rr = random.uniform(12, 20)
        strain = random.uniform(0.0, 1.0)
        rolling_risk = random.uniform(0.0, 1.0)

        event: Optional[str] = None
        if rolling_risk > 0.85:
            event = "EVENT_SLOW_DOWN"
        elif rolling_risk > 0.65:
            event = "EVENT_MICRO_BREAK_RECOMMENDED"

        samples.append(
            CadenceSample(
                timestamp=(now + timedelta(minutes=i)).isoformat() + "Z",
                hr_bpm=round(hr, 2),
                rr_bpm=round(rr, 2),
                strain=round(strain, 2),
                risk=round(rolling_risk, 2),
                event=event,
            )
        )

    return samples


# --------------------------------------------------
# 4. Printer
# --------------------------------------------------

def print_profile(samples: List[CadenceSample]):
    for s in samples:
        print(
            f"{s.timestamp}  HR={s.hr_bpm}  RR={s.rr_bpm}  "
            f"STRAIN={s.strain}  RISK={s.risk}  EVENT={s.event}"
        )


# --------------------------------------------------
# 5. Main
# --------------------------------------------------

def main(output_json: bool = False) -> None:
    samples = simulate_cadence_profile(minutes=10)

    print_profile(samples)

    if output_json:
        json_str = samples_to_json(samples)
        output_path = "cadence_profile_demo.json"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"\nSaved JSON to {output_path}")


if __name__ == "__main__":
    main(output_json=True)
