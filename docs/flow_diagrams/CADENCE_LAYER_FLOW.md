# Cadence Layer — Flow Diagram (v0.1)

## Mermaid Diagram

```mermaid
flowchart TD

A[Signal Streams] --> B[Processing Gateway]
B --> C[Windowing Module<br>(Slice into time windows)]
C --> D[Pattern Detection]
D --> E[Cadence State Mapping]
E --> F[Cadence Delta Calculation]
F --> G[Bottleneck Detection]
G --> H[Output: CadenceState<br>CadenceDelta<br>BottleneckCandidates]
Textual Flow

Input

SignalStreams (HR, HRV, queue length, cycle time, etc.)

ContextTags (human/machine, task, environment)

Config (window size, sliding step)

Processing Gateway

Validates incoming data

Normalizes format

Aligns timestamps

Windowing Module

Splits signals into overlapping windows

Computes basic statistics for each window

Pattern Detection

Identifies overload, micro-stress, jitter, flat, lag

Flags pattern types inside each window

Cadence State Mapping

Maps patterns → universal cadence states

(STEADY_FLOW, MICRO_STRESS, SUSTAINED_STRAIN, JITTER, COLLAPSE_RISK)

Cadence Delta Calculation

Compares state with previous window

Determines magnitude and direction of change

Bottleneck Detection

Recurring negative deltas

Sustained high-severity states

Marks bottleneck candidates

Outputs

CadenceState

CadenceDelta

BottleneckCandidates
