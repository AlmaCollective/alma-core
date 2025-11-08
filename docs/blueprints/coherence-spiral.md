# Coherence Spiral — From Emotion Layers to Coherence Score

This blueprint describes how Alma transforms layered emotion data into a coherence score and a learning rhythm.

## 1. Inputs

Alma receives one `emotion-layer` object (see `models/emotion-layer.json`) every few seconds or aggregated over short windows (e.g., 30–120s).

Key fields used:

- `body`: hr, hrv, eda, movement
- `emotion.intensity`
- `emotion.volatility_index`
- `complex.weight`
- `coherence.alignment_score` (previous state, when available)

## 2. Instant Coherence Score

For each window, Alma computes an **instant coherence score**:

- normalize physiological data to [0,1]
- reward balanced HRV and stable movement
- penalize very high volatility and high complex weight

Example (conceptual):

```text
instant_coherence =
  0.4 * body_regulation +
Values are clamped to [0,1].

3. Spiral Over Time

Instead of treating each score in isolation, Alma tracks a spiral:

x-axis: time

y-axis: coherence score

z-axis: complex weight / volatility

This creates a trajectory of how a person returns to themselves after activation.
Patterns in the spiral reveal emotional resilience and recurring loops.

4. Learning Rhythm

Alma adapts its learning cadence based on the spiral:

stable, high coherence → low-frequency updates (system is regulated)

unstable, low coherence + high complex weight → high-frequency sampling and deeper analysis

return to baseline → mark completion of one “coherence cycle”

Each cycle is stored as a unit of experience for the user’s emotional model.

5. Outputs

For each cycle, Alma can output:

average_coherence

cycle_duration_sec

dominant_complex_tag

recovery_profile (fast / slow / fragmented)

These outputs feed UI visualizations and future personalization (e.g., tailored grounding exercises).
  0.3 * (1 - volatility_index) +
  0.3 * (1 - complex_weight)
