# Exact Simulation Demo Spec — AaCT-E

## 1. Objective

Demonstrate a minimal execution-boundary governance mechanism for AI-assisted aviation decisions.

The demo must show:

1. A proposed action is evaluated at the **commit point**, not only before simulation start.
2. The decision uses **current state plus short-horizon trajectory projection**.
3. The gate **denies** an action that would create an unsafe or unrecoverable state.
4. The gate **allows** an action when recoverability and separation are preserved.
5. The system emits a **reproducible machine-readable trace**.

---

## 2. Scope

**Phase I demonstration.** Not an operational ATC model.

**Included:**
- 2D kinematic simulation
- Fixed time step
- Constant speed aircraft
- Heading-change actions
- Pairwise separation evaluation
- Commit-time allow/deny gate
- JSON evidence output

**Excluded:**
- Weather, climb/descent, communication latency, human factors
- Full FAA separation logic, certified conflict detection
- Optimization across many aircraft

---

## 3. State Model

### Aircraft state
| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `x_nm` | float | x-position (nautical miles) |
| `y_nm` | float | y-position (nautical miles) |
| `heading_deg` | float | Heading [0, 360) |
| `speed_kts` | float | Constant speed (knots) |

### Scenario parameters
| Field | Type | Description |
|-------|------|-------------|
| `dt_sec` | int | Simulation time step (seconds) |
| `horizon_steps` | int | Number of forward steps to project |
| `min_separation_nm` | float | Safety threshold (nm) |
| `recovery_min_separation_nm` | float | Recovery threshold (nm) |
| `proposal_aircraft_id` | string | Aircraft proposing action |
| `proposed_action` | string | Action to evaluate |
| `alternative_actions` | string[] | Safer alternatives to check |

---

## 4. Dynamics

At each step:
- Heading determines direction of motion
- Speed is constant
- Position updated by:
  - `distance_nm = speed_kts * dt_sec / 3600`
  - `x += distance_nm * cos(heading)`
  - `y += distance_nm * sin(heading)`

### Action effects
| Action | Heading delta |
|--------|---------------|
| `MAINTAIN` | 0° |
| `TURN_LEFT_15` | −15° |
| `TURN_RIGHT_15` | +15° |
| `TURN_LEFT_30` | −30° |
| `TURN_RIGHT_30` | +30° |

Heading wraps in `[0, 360)`.

---

## 5. Commit-Time Gate

### Input
- Current scenario state
- Target aircraft
- Proposed action
- Allowed alternative actions
- Safety thresholds

### Evaluation rules

**Proposed action:**
1. Apply action to proposal aircraft at commit point.
2. Simulate all aircraft forward over horizon.
3. Compute projected minimum pairwise separation.

**Deny if:** `projected_min_separation < min_separation_nm`

**Allow if:** `projected_min_separation >= min_separation_nm`

### Recoverability evidence

For each alternative action:
- Simulate same horizon
- Compute projected minimum separation

**Recovery reachable if:** `projected_min_separation >= recovery_min_separation_nm`

**Trace must record:**
- Whether proposal is allowed
- Minimum separation under proposal
- All alternative evaluations
- Whether at least one recovery action remained reachable

---

## 6. Required Scenarios

### Scenario A — `unsafe_merge`
**Goal:** Proposed action must be denied.

**Setup:** Two aircraft on near-conflict geometry. Proposal turns primary toward intruder.

**Expected:**
- Decision: `DENY`
- Proposal minimum separation below threshold
- At least one alternative marked reachable

### Scenario B — `safe_hold`
**Goal:** Proposed action must be allowed.

**Setup:** Safe geometry. Maintain heading preserves separation.

**Expected:**
- Decision: `ALLOW`
- Proposal minimum separation above threshold

---

## 7. Output Artifacts

### A. Scenario trace JSON
File: `outputs/<scenario_name>_trace.json`

Required fields:
| Field | Type | Description |
|-------|------|-------------|
| `scenario` | string | Scenario name |
| `decision` | "ALLOW" \| "DENY" | Gate decision |
| `proposal_aircraft_id` | string | Target aircraft |
| `proposed_action` | string | Evaluated action |
| `proposal_min_separation_nm` | float | Worst-case separation under proposal |
| `threshold_min_separation_nm` | float | Safety threshold |
| `recovery_min_separation_nm` | float | Recovery threshold |
| `recovery_reachable` | bool | At least one alternative is safe |
| `alternatives` | object[] | Per-alternative evaluations |
| `timeline` | object[] | Per-step state + separation |

### B. Console summary
One-line per scenario:
```
<scenario>: <decision> | proposal_min_sep=<value> nm | recovery_reachable=<bool>
```

---

## 8. Verification Criteria

The demo is complete when:

1. `python run_demo.py` completes without error.
2. `python verify_demo.py` completes without error.
3. `unsafe_merge` yields `DENY`.
4. `safe_hold` yields `ALLOW`.
5. Each scenario emits JSON trace in `outputs/`.
6. Trace records at least one alternative action evaluation.
7. Trace explicitly records whether recovery remained reachable.

---

## 9. Why This Matters

This demo isolates the central claim behind the formalism:

> A system can govern action at the point of commitment by evaluating whether safety and recoverability remain preserved in the current state, rather than relying only on preapproved authority, static policy, or post-hoc audit.

This is the bridge from **GCAT/BCAT theory** to **procurement evidence**.

---

## 10. Ecosystem Integration

This spec is implemented by the `AaCT-E/demo` repository and monitored by the StegVerse StegDB pipeline. Architecture governance is declared in `aacte.architecture.json`.
