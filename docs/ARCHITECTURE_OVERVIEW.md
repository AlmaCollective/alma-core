## 9. Architecture Overview (v0.1)

Alma is designed as a layered system that translates human physiological
signals into safe, meaningful, and actionable states — without ever
overriding the human body’s own cadence.

This document provides a high-level view of Alma’s architecture:
- what the main layers are,
- how they interact,
- where the System Layer fits,
- how the system can be deployed and extended.

---

### 9.1 Architectural Goals

Alma’s architecture is built around a small set of non-negotiable goals:

1. **Safety-first**
   - No unsafe haptics.
   - No decisions based on low-confidence data.
   - Predictable failure modes (Safe Mode, Guarded Mode).

2. **Determinism**
   - Same inputs → same outputs.
   - No hidden randomness in core layers.

3. **Modularity**
   - Each layer has a single responsibility.
   - Layers can be updated independently.

4. **Privacy by Design**
   - Raw biosignals stay at the edge.
   - Only processed, normalized states move upward.

5. **Deploy Anywhere**
   - Works on-device, on-premise, or in the cloud.
   - Same contracts across all deployments.

---

### 9.2 Core Layers

Alma is composed of four main layers:

1. **Hardware Layer (Edge)**
   - Sensors: PPG, IMU, temperature, GSR (optional).
   - Outputs: haptic motor / actuator, LEDs (optional), BLE.
   - Constraints: low power, low compute, thermal safety.

2. **Signal Layer (Physiology Engine)**
   - Cleans and transforms raw signals into:
     - heart rate, HRV, cadence index,
     - phase stability windows,
     - motion and posture patterns.
   - Contains the Signal Quality Engine (SQE) and confidence scoring.

3. **Interpretation Layer (Meaning Engine)**
   - Consumes CadenceState + context.
   - Produces semantic tags such as:
     - “CALM”, “STEADY”, “STRAIN”, “APPROACHING_EDGE”, “RECOVERY”.
   - Handles pattern detection, history windows, and state transitions.

4. **System Layer (Integration & Safety Shell)**
   - The API boundary around Alma’s inner core.
   - Responsibilities:
     - connectivity, power, safety, failover,
     - routing of events in and out,
     - contracts, error model, security.
   - Does not invent new physiology or meaning — it governs access.

5. **Application Layer (Outer World)**
   - Mobile apps, dashboards, factory UIs, 3rd-party AIs.
   - Reads Alma’s states and events.
   - May act on them (e.g., nudges, machine slowdowns) without
     touching the inner core.

---

### 9.3 Data Flow (End-to-End)

High-level data flow can be summarized as:

1. **Sensing**
   - Hardware Layer captures raw signals (PPG, IMU, etc.).
   - Local firmware performs minimal preprocessing.

2. **Physiological Processing**
   - Signal Layer converts raw streams into:
     - cadence metrics,
     - stability windows,
     - stress edges,
     - motion signatures.
   - SQE assigns confidence scores and filters out noise.

3. **Interpretation**
   - Interpretation Layer receives:
     - CadenceState,
     - context (time of day, recent history),
     - signal confidence.
   - Emits InterpretationResults with:
     - tags,
     - severity,
     - optional recommendations.

4. **System Layer Orchestration**
   - System Layer:
     - validates and routes events,
     - enforces safety and rate limits,
     - manages connectivity and power,
     - exposes APIs for apps and services.

5. **Feedback & Control**
   - Haptic Engine receives safe, approved patterns from the core.
   - Application Layer may adapt UI, workloads, or machine control loops
     based on Alma events.

---

### 9.4 Deployment Topologies

Alma supports multiple deployment models:

#### 9.4.1 Edge-Centric (Wearable / Local)

- Signal + Interpretation Layer run on or near the device.
- System Layer runs on a phone or local gateway.
- Application Layer is a companion app.
- Best for:
  - personal regulation,
  - privacy-critical use cases,
  - low-latency feedback.

#### 9.4.2 Hybrid (Factory / Clinic)

- Signal Layer partly runs at the edge.
- Interpretation + System Layer run on a local server.
- Application Layer is dashboards and local tools.
- Best for:
  - industrial monitoring,
  - safety-critical environments,
  - limited or unreliable connectivity.

#### 9.4.3 Cloud-Centric (Analytics / Research)

- Devices stream derived features to the cloud System Layer.
- Signal Layer may run on edge or in the cloud.
- Interpretation, System, and Application Layers run in managed services.
- Best for:
  - large-scale analytics,
  - model refinement,
  - multi-site deployments.

In every topology, the **System Layer remains the single integration surface**
for external systems.

---

### 9.5 Non-Goals

Alma’s architecture is explicitly **not** designed to:

- Perform generalized emotion recognition or “mind reading”.
- Replace clinical diagnostics.
- Share raw biosignals without explicit consent.
- Allow external code to inject logic into core layers.

These are intentional constraints that protect users and keep the system
aligned with its purpose.

---

### 9.6 Summary

Alma’s architecture is a layered, safety-first stack that:

- starts from the body,
- stabilizes physiology into cadence,
- interprets it into clear states,
- exposes only safe, structured outputs to the outside world.

The System Layer acts as the protective shell:
- enforcing rules,
- exposing APIs,
- managing risk.

This separation allows Alma to evolve over time without losing trust,
safety, or clarity of purpose.
