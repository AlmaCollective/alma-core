# HUMAN_CADENCE_PROFILE (v0.1)

The Human Cadence Profile defines how Alma interprets biological, behavioral, and contextual rhythms in human systems.  
It provides a universal structure for detecting strain, recovery, stability, and misalignment without pathologizing or judging.

It is applicable to:
- wellbeing,
- cognitive load,
- emotional regulation,
- focus flow,
- daily routine optimisation,
- burnout detection,
- performance stability.

---

## 1. Purpose

Humans operate in rhythms.  
Cadence is a measurable representation of those rhythms.

The Human Cadence Profile translates:
- physiological signals,
- behavioral patterns,
- context,
- micro-reactions,

into universal cadence states that are *non-medical*, *non-diagnostic*, and focused on function + clarity.

---

## 2. Inputs

### 2.1 Physiological Signals
(Depending on device availability.)

- Heart Rate (HR)
- Heart Rate Variability (HRV / RMSSD)
- Breathing rate (BR)
- Skin conductance / GSR
- Movement (IMU: accelerometer/gyroscope)
- Posture metrics
- Sleep/wake cycles
- Temperature (optional)

These signals are always treated as **functional indicators**, not medical markers.

---

### 2.2 Behavioral Signals

- typing rhythm
- step cadence
- voice pace (if available)
- interaction density
- break frequency
- micro-pauses
- gaze stability (where applicable)

---

### 2.3 Contextual Tags

Context is as important as the signal.

Tags may include:
- task type (focus, routine, social, commute, rest)
- location (office, home, outside)
- time of day
- workload level
- emotional self-report (optional)
- social context (alone, talking, crowded)

---

## 3. Windowing and Resolution
WINDOW_SIZE: 120 seconds
SLIDING_STEP: 30 seconds
SAMPLING_RATE: device-dependent (auto-normalized)

A human cadence window captures micro-patterns without being too noisy.

---

## 4. Pattern Types (Human-Oriented)

Alma detects universal patterns:

### • STEADY_RHYTHM  
Stable, predictable, balanced.

### • MICRO_STRESS  
Small spikes in load; fast recovery.

### • SUSTAINED_STRAIN  
Prolonged effort or tension without recovery.

### • JITTER  
Instability, rapid oscillation, disrupted pacing.

### • COLLAPSE_RISK  
Rhythm degradation (cognitive, emotional, or energetic).

Patterns are signal-agnostic — they emerge from correlations, not single metrics.

---

## 5. Cadence States

After mapping patterns → states, Alma uses:


Recommended defaults:

STEADY_FLOW
MICRO_STRESS
SUSTAINED_STRAIN
UNSTABLE_FLOW
COLLAPSE_RISK

States are universal across humans; interpretation is context-aware.

---

## 6. Typical Human Insights

From cadence patterns + context, Alma can infer:

- cognitive load level  
- emotional strain vs. emotional calm  
- recovery quality  
- task alignment (fit/mismatch)  
- mental fatigue buildup  
- micro-burnout cycles  
- overstimulation vs. understimulation  
- flow state signals  
- pacing stability  

---

## 7. Examples (Simplified)

### Example 1 — Focus Task (Deep Work)
**Signals:** steady HR, low movement, high HRV  
**Pattern:** STEADY_RHYTHM  
**State:** STEADY_FLOW  
**Insight:** “Stable focus, good alignment.”

---

### Example 2 — Stress Spike  
**Signals:** HR spike, GSR spike, quick recovery  
**Pattern:** MICRO_STRESS  
**State:** MICRO_STRESS  
**Insight:** “Short stress pulse, recovered fast.”

---

### Example 3 — Cognitive Overload  
**Signals:** HR elevation, HRV suppression, jittery movement  
**Pattern:** SUSTAINED_STRAIN  
**State:** SUSTAINED_STRAIN  
**Insight:** “High cognitive effort; consider a brief break.”

---

### Example 4 — Emotional Turbulence  
**Signals:** jittery HR, unstable pacing, irregular breathing  
**Pattern:** JITTER  
**State:** UNSTABLE_FLOW  
**Insight:** “Instability in rhythm; likely emotional or environmental disturbance.”

---

### Example 5 — Burnout Threshold  
**Signals:** repeated SUSTAINED_STRAIN with no steady recovery  
**Pattern:** COLLAPSE_RISK  
**State:** COLLAPSE_RISK  
**Insight:** “Severe rhythm degradation; immediate rest recommended.”

---

## 8. Ethics & Boundaries

The Human Cadence Profile is designed to be:

- non-medical  
- non-diagnostic  
- non-intrusive  
- consent-based  
- privacy-preserving  
- supportive, not corrective  

No labels. No judgment.  
Cadence = clarity + pacing.

---

## 9. Summary

The Human Cadence Profile provides:

- structured input model  
- universal pattern types  
- cadence states  
- insight examples  
- ethical boundaries  

It enables Alma to support humans with clarity, respect, and simplicity —  
no sensationalism, no overreach, just clean rhythm intelligence.
