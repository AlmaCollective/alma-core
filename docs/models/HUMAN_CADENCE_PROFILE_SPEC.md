# Alma – Human Cadence Profile (v0.1)

This profile defines the **default human cadence ranges** that Alma uses to
interpret biosignals into discrete states for safety and performance.

It is **not medical**. It is an engineering profile for:
- adult users (18–60)
- light-to-heavy physical work
- no known acute cardiac conditions

All values are **starting points** and must be calibrated per site.

---

## 1. Input signals

Alma’s cadence profile uses:

- **HR_BPM** – heart rate (beats per minute)
- **RR_MS** – average R–R interval (ms) over the cadence window
- **ACCEL_MG** – body acceleration magnitude (mg)
- **SIGNAL_QUALITY** – 0.0–1.0 (PPG/ECG quality)
- **CADENCE_WINDOW_SEC** – default: 120 s
- **ROLLING_WINDOW_MIN** – default: 10 min

Only samples with `SIGNAL_QUALITY ≥ 0.7` are considered for state transitions.

---

## 2. Cadence states

Alma maps the raw signals into 5 states:

1. `STATE_CALM` – baseline, safe
2. `STATE_FOCUSED` – engaged, stable
3. `STATE_STRAIN` – elevated load, watch
4. `STATE_RISK` – unsafe trend, action needed
5. `STATE_UNKNOWN` – not enough data / bad signal

The **pipeline** outputs both the current state and a **confidence score** (0–1).

---

## 3. Baseline estimation

For each user, Alma builds a rolling baseline over the first **7 days**:

- `BASE_HR_BPM` – median HR at rest-like activity  
- `BASE_RR_MS` – median RR at rest  
- `BASE_ACC_MG` – median acceleration at rest

Until the baseline is stable, Alma uses conservative defaults:
- `BASE_HR_BPM = 75`
- `BASE_RR_MS = 900`
- `BASE_ACC_MG = 50`

---

## 4. State rules (v0.1)

All thresholds are **relative to baseline**.

### 4.1 STATE_CALM

Conditions (over last 2 min, majority of samples):

- `HR_BPM` within `BASE_HR_BPM ± 10`
- `RR_MS` within `BASE_RR_MS ± 120`
- `ACCEL_MG < BASE_ACC_MG + 150`

Confidence:
- start at `0.6`
- +0.1 if signal_quality > 0.85
- +0.1 if same state persisted ≥ 6 min  
→ capped at `0.95`

Use: “normal” operation, no flag.

---

### 4.2 STATE_FOCUSED

Conditions:

- `HR_BPM` between `BASE_HR_BPM + 5` and `BASE_HR_BPM + 25`
- **HRV slightly reduced**: `RR_MS` between `BASE_RR_MS - 200` and `BASE_RR_MS`
- movement moderate: `ACCEL_MG < BASE_ACC_MG + 300`

Confidence:
- `0.5` base
- +0.2 if trend of HR_BPM is flat (±3 bpm over last 6 min)
- +0.1 if user stayed out of STRAIN/RISK for ≥ 30 min

Use: “good focus / engaged work”.

---

### 4.3 STATE_STRAIN

Early warning zone.

Conditions (any **two** of):

- `HR_BPM > BASE_HR_BPM + 25` for ≥ 2 consecutive cadence windows
- `RR_MS < BASE_RR_MS - 250`
- high movement: `ACCEL_MG > BASE_ACC_MG + 400`
- **upward trend**: HR_BPM increased ≥ 10 bpm in last 10 min

Confidence:
- `0.6` base
- +0.2 if condition holds for ≥ 10 min
- −0.2 if signal_quality < 0.8

Use:
- internal flag for dashboard
- optional soft nudge: “micro-break suggested”.

---

### 4.4 STATE_RISK

Escalation zone – **automation should slow down**.

Conditions (any **one** of):

- `HR_BPM > BASE_HR_BPM + 40` for ≥ 2 windows (≥ 4 min)
- `HR_BPM > 130 bpm` (absolute) for ≥ 1 window
- `RR_MS < BASE_RR_MS - 350` for ≥ 2 windows
- oscillation between STRAIN and CALM ≥ 3 times in last 20 min
  (pattern of instability)

Confidence:
- `0.7` base
- +0.2 if at least 2 conditions are true
- +0.1 if same state for ≥ 10 min

When STATE_RISK is active **and** confidence ≥ 0.75:

- the **system layer** raises a `SLOW_DOWN` flag to the PLC / robot
- optional: trigger local alert (light / haptic)

---

### 4.5 STATE_UNKNOWN

Used when:

- `SIGNAL_QUALITY < 0.7` for > 50% of samples in last window
- less than 30% of expected samples arrived (sensor off, battery low)

In this case Alma:
- does **not** change the last known state
- outputs `confidence = 0.0` for the current window
- optionally raises `SIGNAL_LOSS` event to the system layer.

---

## 5. Events for the System Layer

From this profile, Alma exposes the following **events** upward:

- `EVENT_MICRO_BREAK_RECOMMENDED`
  - transition: CALM/FOCUSED → STRAIN (confidence ≥ 0.7)
- `EVENT_SLOW_DOWN`
  - state: RISK (confidence ≥ 0.75) sustained for ≥ 2 windows
- `EVENT_SIGNAL_LOSS`
  - state: UNKNOWN for ≥ 3 consecutive windows
- `EVENT_RECOVERY`
  - transition: RISK/STRAIN → CALM/FOCUSED sustained ≥ 10 min

These events are **stateless** for the caller: the system layer does not need
to know the full history, only what Alma emits.

---

## 6. Calibration notes

- All thresholds must be **tuned per factory** with real pilots.
- Profiles can be specialised (e.g. night-shift, heat-exposed workers,
  older workers).
- This v0.1 profile is intentionally conservative: it prefers **false positives**
  over missed risks.
