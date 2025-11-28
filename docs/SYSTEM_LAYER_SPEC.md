# System Layer — Universal Specification (v0.1)

The System Layer defines how Alma communicates with the outside world.  
It provides APIs, contracts, connectors, and structure for integrating:

- human-facing apps,
- enterprise systems,
- hardware sensors,
- machine control loops,
- external AIs,
- dashboards and analytics tools.

It is the “interaction surface” of Alma.

---

## 1. Purpose

The System Layer ensures that:

- Alma’s results are accessible through clear, universal interfaces,
- applications can request insights in real time,
- signals from hardware or software can be ingested,
- other systems can connect without needing to understand the internals.

The System Layer protects Alma’s core while making it useful everywhere.

---

## 2. Architecture Overview

The System Layer contains:

### 2.1 Input Connectors  
Connectors:
SensorConnector
SystemEventConnector
HumanInputConnector
BatchDataConnector

### 2.2 Processing Gateway  
Receives signals → forwards them to Cadence + Interpretation layers.

ProcessingGateway:
validate_input()
route_to_cadence()
route_to_interpretation()

### 2.3 Insight API  
External applications use this to access Alma:

InsightAPI:
get_current_state(entity_id)
get_current_insight(entity_id)
get_bottlenecks(scope)
subscribe_to_changes(entity_id)

### 2.4 Output Channels  
Where Alma sends results:

- dashboards  
- mobile apps  
- machine controllers  
- workflow systems  
- messaging systems  
- event streams  

### 2.5 Logging & Audit Layer  
Optional but recommended for enterprise use.

---

## 3. Input Connectors (language-agnostic)

Each connector normalizes incoming data into Alma’s internal formats.

### 3.1 SensorConnector
For hardware (wearables, machines, environmental sensors):


### 2.4 Output Channels  
Where Alma sends results:

- dashboards  
- mobile apps  
- machine controllers  
- workflow systems  
- messaging systems  
- event streams  

### 2.5 Logging & Audit Layer  
Optional but recommended for enterprise use.

---

## 3. Input Connectors (language-agnostic)

Each connector normalizes incoming data into Alma’s internal formats.

### 3.1 SensorConnector
For hardware (wearables, machines, environmental sensors):

SensorConnector:
device_id
data_format
authenticate()
decode_raw()
emit SignalStream

### 3.2 SystemEventConnector
For external systems (ERP, MES, CRM, robotic controllers):


### 3.2 SystemEventConnector
For external systems (ERP, MES, CRM, robotic controllers):

SystemEventConnector:
event_id
metadata
flatten_event()
map_to_context_tags()
emit SignalStream or ContextTag

### 3.3 HumanInputConnector
For manual annotations or user reports:

HumanInputConnector:
user_id
input_type (emotion, pain, workload, note)
timestamp
convert_to_context()

### 3.4 BatchDataConnector
For offline analysis:


### 3.4 BatchDataConnector
For offline analysis:

BatchDataConnector:
load_csv(json,xlsx)
chunk_into_streams()
send_to_processing()

---

## 4. Processing Gateway

A universal abstraction that routes all incoming data.

ProcessingGateway:
function ingest(input):
validated = validate(input)
if validated.is_signal:
forward_to_cadence(validated)
if validated.is_context:
register_context(validated)
if validated.is_event:
update_state(validated)

The gateway ensures:
- no corrupted data enters the core,
- all signals use the same internal structure,
- everything is timestamp-aligned.

---

## 5. Insight API (External-Facing)

This is the main contract other systems use.  
Language-agnostic, but typically exposed as REST / GraphQL / WebSocket.


The gateway ensures:
- no corrupted data enters the core,
- all signals use the same internal structure,
- everything is timestamp-aligned.

---

## 5. Insight API (External-Facing)

This is the main contract other systems use.  
Language-agnostic, but typically exposed as REST / GraphQL / WebSocket.
GET /state/{entity_id}
→ returns current CadenceState

GET /insight/{entity_id}
→ returns Interpretation Insight (summary, cause, effect, priority)

GET /bottlenecks?scope=human|machine|process
→ returns list of Bottlenecks

POST /subscribe
→ stream of updates when state changes

POST /annotate
→ send human input context

Designed to be readable and predictable.

---

## 6. Output Channels

### 6.1 Dashboard Output
Used for operational visibility:

- system overview
- stress map
- rhythm stability map
- bottleneck heatmap
- trend lines

### 6.2 Mobile / Wearable App Output
Human-centered insights:

- micro-stress detection
- recovery suggestions
- rhythm forecasts
- contextual annotations

### 6.3 Machine Controller Output
For factories or automation:

- reduce task rate
- divert queue
- pause machine
- notify operator
- adjust cycle timing

Alma never forces an action — it sends suggestions or flags.

---

## 7. Event Model

Alma emits standardized events:

Event:
id
entity_id
timestamp
event_type (STATE_CHANGE / DELTA / BOTTLENECK)
payload
confidence

Examples:

- STATE_CHANGE: “STEADY_FLOW → SUSTAINED_STRAIN”  
- BOTTLENECK: “station_4, jitter_overload”  
- RECOVERY_EVENT: “recovery after sustained strain, slow but stable”  

---

## 8. Security & Permissions

Core principles:

- minimal data storage  
- anonymizable entity IDs  
- secure connector authentication  
- read/write permissions separated  
- no tracking of identity-level personal data unless user consents  

Alma is designed for **ethics-first** deployment.

---

## 9. System Interaction Example (End-to-End)

1. SensorConnector receives HR + HRV signals  
2. ProcessingGateway validates & aligns  
3. Cadence Layer detects SUSTAINED_STRAIN  
4. Interpretation Layer identifies “high cognitive load”  
5. Insight API posts update  
6. Mobile app shows:  
   “Sustained strain detected during focus task — consider a short break.”  
7. System logs event  
8. Dashboard updates organizational rhythm map

Same flow works for machines, lines, robots.

---

## 10. Summary

The System Layer connects Alma to the world.

It provides:
- universal connectors for signal ingestion,
- a stable processing gateway,
- a clear Insight API,
- output channels for human and machine use,
- event models for integration,
- ethical safeguards.

It is the surface through which Alma becomes part of real systems —  
from human wellbeing to enterprise operations.


Standardized modules for receiving signals:

