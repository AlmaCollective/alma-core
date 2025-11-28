(v0.1 — canonical profile for human signals & emotional/cognitive rhythm)
# Human Cadence Profile (v0.1)
This profile defines how Alma reads, interprets, and maps cadence in humans — across emotional, cognitive, physical, and behavioral layers.

It specifies:
- which physiological & contextual signals matter,
- how patterns are identified,
- how cadence states reflect human wellbeing,
- and how insights are constructed in a non-invasive, non-judgmental way.

---

# 1. Purpose

The Human Cadence Profile gives Alma a universal framework to understand human rhythm.

Goals:
- detect micro-changes in emotional/cognitive load,
- identify stress, recovery, stability, or overload patterns,
- provide gentle, supportive insights,
- help humans see themselves without shame or judgment.

---

# 2. Core Signal Types (Human)

Alma reads human rhythm through four categories of signals:

---

## 2.1 Physiological Signals

### Heart-based metrics:
- **HR (Heart Rate)**
- **HRV (RMSSD, SDNN, LF/HF)**
- **Pulse waveform morphology**

### Stress-response metrics:
- **GSR/EDA (Electrodermal activity)**
- **Skin temperature**
- **Respiration rate** (or inferred from HR modulation)
- **Movement jitter / micro-movements**

These reflect:
- arousal,
- recovery,
- cognitive load,
- emotional activation,
- micro-stress events.

---

## 2.2 Movement & Behavior Signals

- IMU patterns (accelerometer, gyro)
- posture changes
- restlessness vs stillness
- directional patterns (pacing, fidgeting)
- presence/absence of motion

These reflect:
- focus,
- agitation,
- fatigue,
- embodied stress.

---

## 2.3 Cognitive & Emotional Signals (contextual)

Not read directly — **but inferred** from:
- task type,
- workload,
- timing,
- interaction contexts,
- human notes / self-reports,
- historical patterns.

Examples:
- “Working on a demanding task”
- “After a conflict”
- “During commute”
- “Shift change”
- “During break”

---

## 2.4 Environmental Context

- noise levels (optional)
- temperature (optional)
- time of day
- sleep schedule (if provided)
- social context (crowded / isolated)

---

# 3. Pattern Detection (Human Version)

Alma identifies universal human rhythm patterns:

---

## 3.1 Steady Rhythm
- stable HRV
- smooth waveform
- low movement jitter
- consistent breathing

→ **STEADY_FLOW**

---

## 3.2 Micro-Stress
- subtle HRV dips
- short HR spikes
- slight EDA increases
- brief movement noise

→ **MICRO_STRESS**

---

## 3.3 Sustained Strain
- HRV remains low
- HR elevated for multiple windows
- breathing irregular
- repeated minor stress events
- cognitive load inferred from context

→ **SUSTAINED_STRAIN**

---

## 3.4 Emotional or Cognitive Jitter
- alternating HRV dips + spikes
- emotional oscillation
- movement inconsistency
- agitation/restlessness

→ **JITTER**

---

## 3.5 Collapse Risk
- extreme low HRV + high HR
- multiple micro-stress events stacking
- loss of rhythm coherence
- signs of autonomic overload

→ **COLLAPSE_RISK**

*(Alma does not diagnose medical conditions.  
It reads **rhythm**, not illness.)*

---

# 4. Bottleneck Detection (Human)

A human bottleneck is a **stuck rhythm**.

Detected when:
1. sustained strain persists,
2. jitter repeats across time,
3. recovery is absent,
4. context suggests chronic overload,
5. physiological patterns decouple from expected behavior.

Examples:
- “Cognitive bottleneck during prolonged focus.”
- “Emotional bottleneck after conflict.”
- “Stress buildup across the day with no recovery window.”

Alma highlights patterns — never labels the person.

---

# 5. Cadence State Mapping (Human)

| Cadence State      | Human Meaning |
|--------------------|---------------|
| STEADY_FLOW        | calm focus, emotional coherence |
| MICRO_STRESS       | small pressures, manageable load |
| SUSTAINED_STRAIN   | prolonged stress, mental narrowing |
| JITTER             | emotional turbulence, cognitive instability |
| COLLAPSE_RISK      | overload, exhaustion warning |

---

# 6. Outputs Specific to Humans

### 6.1 Micro-Insights  
- “Subtle strain detected during this task.”  
- “Brief stress spike — no action needed.”  
- “Improving recovery pattern.”

### 6.2 Macro-Insights  
- “Sustained strain during late evening tasks.”  
- “Recurring jitter patterns after social interactions.”  
- “Morning stability followed by afternoon overload.”

### 6.3 Recovery Signals  
- “Natural recovery detected.”  
- “Rhythm stabilizing.”  
- “Return to baseline.”

### 6.4 Gentle Suggestions (optional)  
Never commands, always soft cues:
- “Take a moment to breathe.”  
- “Short pause may help reset your rhythm.”  
- “This seems to be a long effort — pace yourself.”  

---

# 7. Ethical Principles

- No judgment.  
- No pathologizing normal human emotions.  
- No forced compliance.  
- No behavior manipulation.  
- User controls what data is shared.  
- Insights are supportive, never invasive.

Alma is a mirror of rhythm, not a judge of identity.

---

# 8. Summary

The Human Cadence Profile defines:
- what signals matter,
- how human rhythm is mapped,
- how cadence states reflect emotional/cognitive load,
- how insights are generated gently, ethically, clearly.

It is the foundation for Alma as a personal guide into inner coherence.
