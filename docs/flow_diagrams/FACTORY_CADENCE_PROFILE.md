# Factory Cadence Profile — Alma (v0.1)

The Factory Cadence Profile defines how Alma interprets **machine**, **line**, and **system** rhythms inside industrial environments.  
It standardizes what signals matter, how they are processed, and how insights are interpreted in a manufacturing or automation context.

This profile makes Alma directly applicable to:
- assembly lines  
- robotic cells  
- packaging lines  
- CNC stations  
- logistics systems  
- process industry flows  
- warehouses with autonomous robots  
- any environment where timing → throughput

---

# 1. Purpose

Factories run on **rhythm**:  
cycles → queues → delays → bottlenecks → recovery → collapse.

Alma introduces a universal method to *measure, interpret, and de-risk* these rhythms using the Cadence → Interpretation → System Layer pipeline.

---

# 2. Relevant Signals (Machine / Line / System)

Alma expects the following input streams (SignalStream format):

## 2.1 Cycle-Time Series
- duration of each machine cycle  
- jitter between cycles  
- abnormal cycle spikes  
- cycle completion variance  

## 2.2 Queue Length
- items waiting at a workstation  
- inflow/outflow mismatch  
- line saturation events  

## 2.3 Throughput Rate
- units completed per minute/hour  
- rolling throughput variance  

## 2.4 Error & Fault Logs
- minor stops  
- major stops  
- micro-stops (high-frequency noise)  

## 2.5 Energy & Power Consumption
- spikes (overload)  
- dips (underload)  
- phase irregularities on motors  

## 2.6 Machine Sensor Telemetry
- vibration  
- temperature  
- pressure  
- alignment drift  
- robot arm torque load  
- conveyor belt strain  

## 2.7 System Events
- shift changes  
- maintenance windows  
- upstream/downstream stoppages  
- operator interventions  

Every signal is timestamp-aligned and converted to a uniform cadence representation.

---

# 3. Cadence States (Factory Version)

Using the Cadence Layer state machine, factories use these universal states:

### **STEADY_FLOW**
- cycles stable  
- throughput predictable  
- low jitter  
- balanced queues  

### **MICRO_STRESS**
- small but persistent cycle jitter  
- minor stops beginning to accumulate  
- queue variance growing  

### **SUSTAINED_STRAIN**
- cycle times consistently higher  
- throughput dropping  
- queues forming or overflowing  
- energy spikes  

### **JITTER_CHAOS**
- unstable cycles  
- frequent micro-stops  
- multiple competing bottlenecks  
- vibration/torque anomalies  

### **COLLAPSE_RISK**
- imminent failure  
- line blockage  
- cascading delays  
- mechanical degradation + queue saturation  

These states are universal across factories and machines.

---

# 4. Interpretation Rules

The Interpretation Layer attaches meaning to cadence patterns:

## 4.1 Local Interpretation
Inside a single window:
- “Cycle time increased by 17%”  
- “Queue spike detected”  
- “Vibration pattern resembles misalignment”  

## 4.2 Temporal Interpretation
Across windows:
- “Strain rising for the last 6 minutes”  
- “Recovery slow after previous micro-stop”  
- “Repeated slowdown after every tool-change”  

## 4.3 Contextual Interpretation
With system and human context:
- “Operator change → 45-second delay in cycle stabilization”  
- “Material batch variation → machine vibration pattern shift”  

## 4.4 Systemic Interpretation
Multi-machine insights:
- “Bottleneck is upstream, not local”  
- “Machine A overload caused Machine C starvation”  
- “Line imbalance causing cascading jitter waves”  

---

# 5. Bottleneck Logic (Factory Edition)

A bottleneck forms when:

- **State severity ≥ SUSTAINED_STRAIN**  
- **Negative delta persists ≥ 2 consecutive windows**  
- **Queue length slope > cycle completion slope**  
- **Throughput variance > defined threshold**  
- **Jitter > machine tolerance profile**  

Alma classifies severity in 3 tiers:
- Tier 1 — soft bottleneck forming  
- Tier 2 — strong bottleneck  
- Tier 3 — systemic, multi-station bottleneck  

---

# 6. Factory Insights (output objects)

The Interpretation Layer generates:
“Cycle-time elongation caused by upstream queue saturation.”
“Mechanical instability: vibration → misalignment risk.”
“Line imbalance from Station 4 creating cascading strain.”
“Throughput drop predicted in next 6 minutes.”
“Operator-task mismatch increasing cycle variance.”

### **Insight Object Schema**
Insight:
summary
cause
effect
priority (1–5)
confidence (0–1)
recommended_next_step (optional)

---

# 7. Recommended Next Steps (non-authoritative)

Alma never forces actions.  
It suggests, not commands.

Examples:
- “Check alignment on Station 2.”  
- “Reduce feed rate by 5% for 10 minutes.”  
- “Investigate material batch inconsistency.”  
- “Balance workload between Stations 3 and 5.”  
- “Schedule predictive maintenance in next 24h.”  

---

# 8. Example: End-to-End Flow in a Factory

1. Cycle time rises → SignalStream  
2. Windowing detects sustained rise  
3. Pattern detection flags “strain”  
4. Cadence state = SUSTAINED_STRAIN  
5. Delta vs previous windows = worsening  
6. Queue length increasing → bottleneck candidate  
7. Interpretation Layer finds upstream machine mismatch  
8. Insight:  
   “Upstream slowdown causing downstream jitter & queue buildup.”  
9. System Layer outputs to dashboard + controller  
10. Operator adjusts machine → rhythm improves  
11. Feedback loop restarts

---

# 9. Summary

The Factory Cadence Profile makes Alma usable in industrial environments by defining:

- standardized signals  
- universal cadence states  
- interpretation logic  
- bottleneck rules  
- insight schema  
- next-step guidance  

It enables factories to see *rhythm* — not just metrics — and to act before systems break.



### **Insight Examples**
