# Alma — Complex Dynamics Model  
*From volatility to coherence*

This document defines how Alma interprets the volatility and persistence of emotions as measurable learning rhythms.

## Emotional Volatility
Volatility reflects the rapid change of emotional intensity within short time windows (e.g., 2–6 minutes).  
It indicates instability and sensitivity to external or internal stimuli.

- `volatility_index` ∈ [0,1]
- high values → reactive emotional state
- low values → regulated, coherent state

## Complex Weight
When a volatile emotion is reinforced by personal memory, body reaction, or cognitive loop, it gains *weight* — forming a **complex**.  
This increases emotional persistence and temporal influence.

- `complex_weight` grows with recurrence_count and duration
- `persistence = volatility_index * complex_weight`

## Adaptive Learning Rhythm
Alma uses emotional persistence to modulate learning cadence:
- transient emotions (low persistence) → fast adaptation
- weighted complexes (high persistence) → slower, integrative rhythm

This allows Alma to “breathe” with emotion instead of reacting to it.

## Integration Points
- Connected with Coherence Spiral for rhythm tracking  
- Stored in JSON format as:
```json
{
  "volatility_index": 0.62,
  "complex_weight": 0.78,
  "persistence": 0.48,
  "coherence_shift": "stabilizing"
}
