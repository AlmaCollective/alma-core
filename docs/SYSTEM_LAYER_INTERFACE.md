📌 8. System Layer Interface (API Overview) – v0.1
### 8. System Layer Interface (API Overview)

The System Layer exposes a minimal, stable, and secure API.
All routes follow a read-mostly pattern — external clients can query
information, but cannot alter internal states.

The API surface is intentionally small to guarantee:
- predictable integration,
- version stability,
- safety by design.

Below are the core endpoints for v0.1.
8.1 /state – Get Current System State
GET /state
Response:
{
  "status": "OK",
  "system_state": SystemState
}
Rules:

read-only

returns last stable state

no sensitive raw data exposed (cadence, strain → normalized values only)

8.2 /events – Stream Outbound Events
GET /events?since=<ISO8601>
Response:
{
  "status": "OK",
  "events": [ EventEnvelope, ... ]
}
Notes:

pagination via since

events are append-only

signature-verified

8.3 /telemetry – Opt-in Anonymized Telemetry
POST /telemetry
Payload:
TelemetryPacket
Rules:

optional

rate-limited

anonymized

cannot influence internal state (strict one-way)

8.4 /input – Inbound Data Envelope
POST /input
Payload:
InputEnvelope
System Behavior:

validate schema

validate signature

validate timing

reject anything unsafe

integrate only through authorized channels

If error → return structured rejection.

8.5 /health – System Health Check
GET /health
Response:
{
  "status": "OK",
  "uptime": <seconds>,
  "latency": <ms>,
  "last_error": <string or null>
}
Used by:

factories

cloud orchestrations

dev environments

8.6 Rate Limits

/state → max 1 request / second

/events → max 5 requests / second

/input → rejects bursts > 30 requests / second

/telemetry → one packet / minute

Purpose: prevent overload & secure deterministic compute cost.

8.7 Versioning Model
Clients negotiate version via header:
X-Alma-Version: "1.0"
If unsupported:

return ERROR_UNSUPPORTED_VERSION

suggest fallback
📌 8.8 Security Headers & Signatures (v0.1)
### 8.8 Security Headers & Signatures (v0.1)

Every API call to Alma's System Layer must include explicit security metadata.
Without these headers, requests are rejected automatically.

---

#### **Required Headers**

1. `X-Alma-Version`
   - Specifies API version.
   - Example: `X-Alma-Version: 1.0`

2. `X-Alma-Client-ID`
   - Unique identity of the caller (device, app, service).

3. `X-Alma-Timestamp`
   - ISO8601 timestamp when the request was generated.
   - Reject if time drift > 30 seconds.

4. `X-Alma-Signature`
   - HMAC-SHA256 signature over:
     - payload (if POST)
     - timestamp
     - client ID
   - Generated using the client’s shared secret.

---

#### **Signature Verification Rules**

- Payload + timestamp + client ID are concatenated in canonical format.
- The server computes its own HMAC using the client’s secret.
- If signatures differ → reject with `ERROR_SIGNATURE_INVALID`.
- If timestamp too old → reject with `ERROR_TIMESTAMP_DRIFT`.
- If client ID unknown → reject with `ERROR_UNKNOWN_CLIENT`.

---

#### **Replay Protection**

The System Layer keeps a rolling window of used signatures.
If a signature appears again → automatic block:
- reject request,
- log security alert,
- increment client’s risk score.

---

#### **Why This Matters**

Security headers ensure:
- no spoofing,
- no tampering,
- no replay attacks,
- no unauthorized access,
- deterministic trust boundaries.

This design protects Alma’s internal state while allowing integrations without exposing sensitive internals.

📌 8.9 Example API Use Cases (v0.1)
### 8.9 Example API Use Cases (v0.1)

This section illustrates how external systems can safely interact with
Alma’s System Layer using the defined API surface.

---

#### 8.9.1 Wearable + Companion App (Individual User)

**Scenario:**  
A user wears an Alma-compatible device. The phone app wants to show
the current state and recent events.

**Flow:**

1. App polls the current state:

   ```http
   GET /state
   X-Alma-Version: 1.0
   X-Alma-Client-ID: companion-app
   X-Alma-Timestamp: 2025-11-30T10:15:00Z
   X-Alma-Signature: <hmac>
System Layer returns:
{
  "status": "OK",
  "system_state": {
    "timestamp": "2025-11-30T10:14:59Z",
    "session_id": "sess_123",
    "cadence_state": "STEADY",
    "cadence_index": 0.62,
    "interpretation_tag": "FOCUSED",
    "signal_quality": 0.91,
    "errors": []
  }
}
App then fetches recent events for history view:
GET /events?since=2025-11-30T10:00:00Z
...
Returned EventEnvelopes are rendered as a timeline:

“STEADY WINDOW”

“APPROACHING EDGE”

“RECOVERY”

The app never sees raw biosignals, only structured, safe states.

8.9.2 Factory Use Case (Machine Slowdown)

Scenario:
A factory line wants to slow a machine when human strain crosses a threshold.

Flow:

A local controller periodically calls:
GET /state
X-Alma-Version: 1.0
X-Alma-Client-ID: factory-controller
...
GET /state
X-Alma-Version: 1.0
X-Alma-Client-ID: factory-controller
...
It reads:
"cadence_state": "STRAIN",
"cadence_index": 0.81
If cadence_index > 0.8 and signal_quality > 0.7:

controller reduces machine speed by 20%

logs the decision on its side

No external system is allowed to:

change cadence_state,

override safety rules,

write into Alma’s internal states.

The control loop lives entirely outside Alma, using /state as a
trusted, read-only input.
8.9.3 Clinical / Research Dashboard

Scenario:
A research dashboard wants to track long-term patterns for a supervised study.

Flow:

A backend service calls /events periodically:
GET /events?since=2025-11-01T00:00:00Z
X-Alma-Version: 1.0
X-Alma-Client-ID: research-backend
...
It receives a list of EventEnvelope objects (anonymized IDs, no PII).

For aggregated analytics, Alma may opt-in to send telemetry:
POST /telemetry
X-Alma-Client-ID: device-gateway
...
{
  "packet_id": "pkt_456",
  "state_snapshot": { ... },
  "device_info": { "hw_rev": "A1", "fw": "1.2.3" },
  "metrics": { "cpu": 0.33, "latency_ms": 18 }
}
POST /telemetry
X-Alma-Client-ID: device-gateway
...
{
  "packet_id": "pkt_456",
  "state_snapshot": { ... },
  "device_info": { "hw_rev": "A1", "fw": "1.2.3" },
  "metrics": { "cpu": 0.33, "latency_ms": 18 }
}
The research system:

generates statistics,

never sends commands back into Alma through /telemetry,

never accesses raw biosignals.

Alma remains the source of truth for state, while external systems
remain consumers, not controllers, of that state.

These use cases demonstrate how Alma’s System Layer:

stays small and predictable,

protects the inner core,

allows powerful integrations without exposing raw physiology.
### 9.7 ASCII Architecture Diagram (v0.1)

A simplified view of Alma’s layered architecture:

```text
            +-----------------------------+
            |       Application Layer     |
            |  (apps, dashboards, AIs)    |
            +--------------+--------------+
                           ^
                           |  APIs (/state, /events, /health, ...)
                           |
                  +--------+---------+
                  |    System Layer  |
                  | (safety, routing,|
                  |  contracts, API) |
                  +--------+---------+
                           ^
                           |  SystemState, EventEnvelope
                           |
           +---------------+----------------+
           |      Interpretation Layer      |
           |  (meaning, tags, state logic)  |
           +---------------+----------------+
                           ^
                           |  CadenceState, confidence
                           |
           +---------------+----------------+
           |        Signal Layer            |
           | (HR, HRV, cadence, stability,  |
           |  motion, Signal Quality Engine)|
           +---------------+----------------+
                           ^
                           |  raw sensor data
                           |
           +---------------+----------------+
           |        Hardware Layer          |
           | (sensors: PPG, IMU, temp, GSR, |
           |  haptic actuator, BLE)         |
           +--------------------------------+
The System Layer acts as the protective shell between Alma’s inner core
(Signal + Interpretation) and the outer world (applications, machines, AIs).





