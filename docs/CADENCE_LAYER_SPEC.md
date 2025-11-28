# Cadence Layer — Universal Specification (v0.1)

The Cadence Layer is Alma’s rhythm engine.  
It observes how signals evolve over time and detects where the natural rhythm breaks —  
inside a human, inside a machine, or inside a complex system.

This specification is language-agnostic and can be implemented in any programming language.

---

## 1. Purpose

The Cadence Layer provides:
- a universal method for analyzing time-based signals,
- consistent rules for detecting stress, overload, instability, or collapse,
- a common format for expressing “bottlenecks” in humans or systems.

It is the foundational layer of Alma.

---

## 2. Inputs

### 2.1 Signal Streams
Each signal is a time-series with structure:

SignalStream:
id
timestamps[]
values[]
context_tags[]

Sources may include:
- human physiology (HR, HRV, respiration)
- machine metrics (cycle time, queue length, error rate)
- process variables (load, throughput, delays)

### 2.2 Context Tags
Optional metadata describing:
- entity type (human, machine, workstation, process-step)
- scenario (“rest”, “task”, “shift 2”, “interaction step 4”)
- environment conditions

### 2.3 Configuration
Config:
window_size
step_size
sensitivity_profile

Examples:
- window_size: 60s  
- step_size: 15s  
- sensitivity: low / normal / high  

---

## 3. Outputs

### 3.1 Cadence State
Represents the rhythmic condition of the entity during a given time window.

CadenceState:
label
confidence
supporting_patterns[]

Possible labels:
- STEADY_FLOW  
- MICRO_STRESS  
- SUSTAINED_STRAIN  
- JITTER  
- COLLAPSE_RISK  

### 3.2 Cadence Delta
Describes change from previous state.

CadenceDelta:
previous_state
current_state
magnitude (NONE / SMALL / MAJOR)
direction (BETTER / WORSE / NEUTRAL)

### 3.3 Bottleneck Candidates
Long-term rhythmic disruptions.

Bottleneck:
location
recurring_pattern
severity (LOW / MEDIUM / HIGH)
evidence[]

---

## 4. Core Concepts

### 4.1 Cadence Window
A time slice of a signal stream:

CadenceWindow:
start_time
end_time
signals[]
basic_stats
pattern_flags[]

### 4.2 Universal Patterns
Detected inside each window:

- **Overload Pattern**  
  sustained high level + slow recovery

- **Micro-Stress Pattern**  
  short spikes + fast recovery

- **Jitter Pattern**  
  high volatility + unstable baseline

- **Flat Pattern**  
  abnormally low variability when activity is expected

- **Lag Pattern**  
  delayed reaction to events

These patterns are independent of the entity type.

---

## 5. Algorithm (language-agnostic)

### 5.1 Windowing

windows = slice_into_windows(signal_streams, config.window_size, config.step_size)

### 5.2 Pattern Detection

For each window:
patterns = detect_patterns(window)

### 5.3 Map Patterns → CadenceState

General rules:
- low variance + moderate level → STEADY_FLOW  
- spikes + quick recovery → MICRO_STRESS  
- high level + slow recovery → SUSTAINED_STRAIN  
- high variance + no baseline → JITTER  
- flat response when active → COLLAPSE_RISK  

### 5.4 Compare With Previous Window

delta = compare_with_previous_state(state, cadence_states)

### 5.5 Bottleneck Detection

A bottleneck is detected when:
- the same entity/location produces repeated **MAJOR_SHIFT → WORSE**  
- or remains in SUSTAINED_STRAIN / JITTER / COLLAPSE_RISK for multiple windows.

if is_recurring_shift_to_worse(delta, window.location):
mark_bottleneck_candidate(bottlenecks, window.location, state, delta)

---

## 6. Examples

### 6.1 Human Example (Heart Rate)
Signals:
- HR, HRV, respiration  
Context: “focus task”

Repeated pattern:
- HR spike  
- HRV drop  
- slow recovery  

→ **Human-level bottleneck**: cognitive overload trigger.

### 6.2 Factory Example (Machine Load)
Signals:
- cycle time, queue length  
Context: “station 4 / tool B”

Repeated pattern:
- queue increases  
- cycle time increases  
- jitter spike  

→ **System-level bottleneck**: workstation 4.

---

## 7. Summary

The Cadence Layer:
- transforms raw time-series into states, deltas, and bottlenecks,
- uses universal rules independent of the signal source,
- forms the foundation for Alma’s higher layers.

It is the “rhythm detector” of any complex organism — biological or mechanical.

