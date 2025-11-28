(v0.1 — guiding principles for implementing Alma safely and correctly)
# Implementation Notes for Alma (v0.1)
This document explains how to implement Alma’s architecture in real code, without deviating from the core design.

It provides:
- how the three layers should be structured,
- data contracts,
- recommended algorithms,
- best practices for performance and clarity,
- what to avoid,
- how external AIs (like Kimi2) should interact with the system.

---

# 1. General Principles

1. **Architecture is fixed.**
   Developers must not alter the 3-layer structure.
   They implement it — they do not redesign it.

2. **Language is flexible.**
   Alma can be implemented in:
   - Python (fast prototyping),
   - Rust (high performance, safe concurrency),
   - C++ (industrial),
   - TypeScript (web),
   - C (embedded),
   - Go (services).

3. **Data structures must remain consistent across languages.**

4. **Interpretations are never hard-coded.**
   Interpretation logic is rule-based or statistical, NOT a black-box model.

5. **No ML until the cadence engine is validated.**
   Alma = deterministic patterns first, ML optional later.

---

# 2. Data Contracts (Canonical Structures)

These apply to every programming language.

### 2.1 SignalStream
```json
{
  "entity_id": "string",
  "timestamp": 123456789,
  "signal_type": "HR | HRV | GSR | cycle_time | queue_length | vibration | ...",
  "value": 0.0,
  "metadata": {
}
}
2.2 ContextTag
{
  "entity_id": "string",
  "tag": "task:focus | environment:noise | shift_change | machine:overload",
  "timestamp": 123456789
}
2.3 CadenceState
{
  "entity_id": "string",
  "state": "STEADY_FLOW | MICRO_STRESS | SUSTAINED_STRAIN | JITTER | COLLAPSE_RISK",
  "confidence": 0.0,
  "timestamp": 123456789
}
{
  "entity_id": "string",
  "state": "STEADY_FLOW | MICRO_STRESS | SUSTAINED_STRAIN | JITTER | COLLAPSE_RISK",
  "confidence": 0.0,
  "timestamp": 123456789
}
2.4 Insight
{
  "entity_id": "string",
  "summary": "string",
  "cause": "string",
  "effect": "string",
  "priority": "LOW | MEDIUM | HIGH",
  "confidence": 0.0,
  "timestamp": 123456789
}
3. Cadence Layer – Implementation Notes
3.1 Windowing

Implement sliding windows with configurable size W and step S.

Use ring buffers for performance (Rust/C++ recommended).

Apply timestamp alignment before windowing.

3.2 Feature Extraction

Extract deterministic features:

mean

variance

slope

FFT (optional)

derivative

jitter amplitude

cycle time deltas

HRV metrics if human

3.3 Pattern Detection

Pattern detection uses thresholds + signatures, not ML.

For humans:

HRV dips

HR spikes

GSR peaks

unstable waveform

For machines:

cycle time variance

queue increases

vibration anomalies

Output: pattern label list.

3.4 Cadence State Mapping

Map patterns → canonical cadence states.

Use simple deterministic logic:
if severe_signatures → COLLAPSE_RISK
if repeated_noise → JITTER
if long-duration overload → SUSTAINED_STRAIN
if slight fluctuations → MICRO_STRESS
else → STEADY_FLOW
3.5 Bottleneck Detection

track consecutive strain windows

track worsening deltas

maintain a rolling score (“bottleneck index”)

Output: ranked bottleneck candidates.

4. Interpretation Layer – Implementation Notes
4.1 Multi-Level Interpretation

Level 1 – Local
Use current CadenceState + context.

Level 2 – Temporal
Examine sequences of states across N windows.

Level 3 – Contextual
Join CadenceState with:

task type,

position,

environment,

human reports,

machine type.

Level 4 – Systemic
Join multiple entities using:

dependency graphs,

adjacency maps,

flow diagrams,

upstream/downstream links.

4.2 Insight Construction

Every insight = simple object:

summary

cause

effect

priority

confidence

No probabilistic model required unless added later.

4.3 Never Use “Black Box ML” Here

Interpretation must remain explainable.
ML can assist but cannot override cadence logic.

5. System Layer – Implementation Notes
5.1 API Recommendation

REST for compatibility

GraphQL for flexible querying

WebSocket for real-time updates

5.2 Input Connectors

Each connector must:

authenticate device/system

normalize format

validate timestamps

convert to SignalStream or ContextTag

5.3 Processing Gateway

Simple router:
if input.is_signal → send_to_cadence
if input.is_context → register_context
if input.is_event → log
5.4 Output Channels

Keep them decoupled:

Insight API

Dashboard API

Machine Controller API

Use publish/subscribe for scalability.

6. Performance Notes
6.1 For Humans

HR/HRV sampling: 15–50 Hz recommended

Windows: 6s / 12s / 30s

Low memory footprint required for wearables

6.2 For Factories

cycle_time/queue: 1–10 samples per second

jitter detection: use rolling variance

heavy stations: parallelize windowing

6.3 Multithreading

Cadence Layer should run in parallel for each entity

Interpretation Layer mostly sequential

Use async event loops for System Layer
