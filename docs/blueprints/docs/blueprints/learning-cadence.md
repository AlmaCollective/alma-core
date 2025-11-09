# Learning Cadence Engine

This blueprint explains how Alma adapts its learning rate and attention based on emotional volatility, complex weight, and coherence over time.

Alma should not learn at a constant speed.  
Instead, it breathes with the user's emotional field — slowing down when things are heavy and stabilising, speeding up when states are light and exploratory.

---

## 1. Inputs

From `alma-complex-dynamics.md` and `emotion-layer.json`, the engine uses:

- `emotion.intensity`
- `emotion.volatility_index`
- `complex.weight`
- `coherence.alignment_score`
- temporal features (how often events occur, cycle duration)

---

## 2. Cadence States

Alma can be in one of three high-level learning states:

1. **Exploratory**
   - volatility: medium–high  
   - complex weight: low  
   - coherence: medium  
   → behaviour: try new patterns, higher learning rate, lighter interventions.

2. **Integrative**
   - volatility: medium  
   - complex weight: medium–high  
   - coherence: fluctuating  
   → behaviour: slower learning, focus on stabilising recurring themes, track cycles carefully.

3. **Stabilised**
   - volatility: low  
   - complex weight: low–medium  
   - coherence: high and steady  
   → behaviour: minimal updates, mostly observation and gentle refinement.

---

## 3. Cadence Score

At each step, Alma computes a **cadence_score** ∈ [0,1]:

Conceptually:

```text
cadence_score =
  0.4 * volatility_index +
  0.4 * complex_weight +
  0.2 * (1 - coherence_alignment_score)
Interpretation:

high cadence_score → system is activated, learning should be more frequent

low cadence_score → system is calm, learning should be slower and lighter

This score maps into the three states:

0.0 – 0.33: Stabilised

0.34 – 0.66: Integrative

0.67 – 1.0: Exploratory

4. Rhythm of Updates

Each state defines:

sampling_interval (how often we record emotion-layers)

model_update_interval (how often we update user-specific parameters)

ui_feedback_level (how much feedback Alma surfaces to the user)

Example (conceptual):

Exploratory:

sampling_interval: 5–10s

model_update_interval: every 1–2 minutes

ui_feedback_level: high (more guidance and reflections)

Integrative:

sampling_interval: 15–30s

model_update_interval: every 5–10 minutes

ui_feedback_level: medium

Stabilised:

sampling_interval: 60–120s

model_update_interval: every 30–60 minutes

ui_feedback_level: low (short check-ins)

5. Link to Coherence Spiral

The coherence spiral defines how state evolves over cycles.
The learning cadence engine defines how fast Alma updates its understanding during those cycles.

Together:

Spiral describes shape of experience.

Cadence describes speed of adaptation.

High-weight complexes over multiple cycles may gradually:

lower the learning rate for noise,

increase focus on specific recurring tags (complex_tag),

personalise thresholds for what is considered “regulated” for each user.
6. Output

For each time window, the engine outputs:
{
  "cadence_state": "integrative",
  "cadence_score": 0.58,
  "sampling_interval_sec": 20,
  "model_update_interval_sec": 300
}
This can be used by:

backend schedulers (when to aggregate & train)

frontend (how often to nudge the user)

analytics (to track how resilience evolves over time)

5. Jos, la **Commit message**, scrie:

`feat(blueprint): define learning cadence engine`

