import time
import uuid
import random
from datetime import datetime

# ---------------------------
# 1. Cadence Stream Simulator
# ---------------------------

def generate_cadence_sample():
    """Simulates a single cadence measurement."""
    return {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "cadence_index": round(random.uniform(0.3, 0.9), 3),
        "signal_quality": round(random.uniform(0.7, 1.0), 3)
    }


# ---------------------------
# 2. Interpretation Logic
# ---------------------------

def interpret_cadence(cadence_index):
    if cadence_index < 0.45:
        return "CALM"
    elif cadence_index < 0.65:
        return "STEADY"
    elif cadence_index < 0.8:
        return "FOCUSED"
    else:
        return "STRAIN"


# ---------------------------
# 3. SystemState Builder
# ---------------------------

def build_system_state(sample):
    return {
        "timestamp": sample["timestamp"],
        "session_id": "sess_" + uuid.uuid4().hex[:6],
        "cadence_state": interpret_cadence(sample["cadence_index"]),
        "cadence_index": sample["cadence_index"],
        "interpretation_tag": interpret_cadence(sample["cadence_index"]),
        "signal_quality": sample["signal_quality"],
        "errors": []
    }


# ---------------------------
# 4. EventEmitter
# ---------------------------

def emit_event(state):
    """Creates a high-level event from current SystemState."""
    uid = uuid.uuid4().hex[:8]
    return {
        "event_id": uid,
        "event_type": state["cadence_state"],
        "state_snapshot": state,
        "issued_at": datetime.utcnow().isoformat() + "Z",
        "signature": "dummy_signature_" + uid
    }


# ---------------------------
# 5. End-to-end Demo
# ---------------------------

if __name__ == "__main__":
    print("\n=== Alma Cadence → SystemState → Event Demo ===\n")

    for i in range(5):
        sample = generate_cadence_sample()
        state = build_system_state(sample)
        event = emit_event(state)

        print("Cadence Sample:", sample)
        print("SystemState:   ", state)
        print("Event:         ", event)
        print("-" * 60)

        time.sleep(1)
