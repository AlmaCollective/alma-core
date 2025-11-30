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
