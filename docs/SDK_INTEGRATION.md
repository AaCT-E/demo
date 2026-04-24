# SDK Integration Contract

> **How the StegVerse SDK wraps the AaCT-E demo without owning it.**

---

## Philosophy

The demo has a singular purpose: prove commit-time safety enforcement works.
The SDK has a broad purpose: integrate GCAT/BCAT concepts into user workflows.

These must not converge. The SDK observes the demo; it does not operate it.

---

## Read-Only Contract

### The SDK MAY:

1. **Clone** the demo repo at a specific tag
2. **Run** `verify_demo.py` or `python -m access.cli`
3. **Parse** JSON traces from `outputs/`
4. **Display** results through SDK UI/API
5. **Archive** traces with full provenance metadata

### The SDK MUST NOT:

1. **Modify** scenario files (`scenarios/*.json`)
2. **Modify** engine code (`aacte/*.py`)
3. **Modify** thresholds (`min_separation_nm`, `recovery_min_separation_nm`)
4. **Suppress** verification failures
5. **Reference** `main` branch for evidence — only tagged releases

---

## Version Pinning

All SDK interactions must specify a tag:

```python
from stegverse.sdk import DemoRunner

runner = DemoRunner(repo="AaCT-E/demo", tag="v0.2.0")
result = runner.verify()
```

If no tag is specified, the SDK MUST raise an error.

---

## Trace Attribution

Any trace displayed through the SDK must preserve these fields:

| Field | Source | Purpose |
|-------|--------|---------|
| `repo` | `aacte.architecture.json` | Identifies origin |
| `version` | Git tag | Pins behavior |
| `commit_sha` | Git HEAD | Immutable reference |
| `run_id` | CI run or UUID | Distinguishes executions |
| `timestamp_utc` | Runtime | Temporal ordering |

**Example attribution block:**
```json
{
  "provenance": {
    "repo": "AaCT-E/demo",
    "version": "v0.2.0",
    "commit_sha": "abc123...",
    "run_id": "gha-12345",
    "timestamp_utc": "2026-04-24T01:00:00Z"
  }
}
```

---

## Failure Handling

If `verify_demo.py` fails, the SDK MUST:

1. Surface the failure to the user **without modification**
2. Include the full stderr/stdout from the demo run
3. NOT retry, NOT fallback, NOT degrade gracefully
4. Log the failure to StegDB monitoring if configured

**Rationale:** The demo is evidence. A failed verification is meaningful data, not an error to hide.

---

## Isolation Requirements

The SDK must run the demo in an isolated environment:

- **Process isolation:** Demo runs in a subprocess, not imported
- **Filesystem isolation:** Demo cloned to a temp directory, not the SDK's working tree
- **Network isolation:** Demo requires no network; SDK must not inject network dependencies

---

## HTTP Endpoint Wrapping

The SDK may poll the demo's HTTP endpoint (`access/web.py`):

```python
import requests
response = requests.get("http://localhost:8080/status")
status = response.json()
```

The SDK MUST NOT:
- Start the endpoint on behalf of the user without explicit consent
- Cache responses longer than the verification interval
- Modify the endpoint's port or host without user configuration

---

## Compliance Checklist

Before claiming SDK integration with AaCT-E:

- [ ] SDK specifies tag, never `main`
- [ ] SDK preserves all provenance fields
- [ ] SDK surfaces verification failures raw
- [ ] SDK does not modify demo source
- [ ] SDK runs demo in isolated subprocess
- [ ] SDK documentation references this contract

---

## Version History

| Contract Version | Date | Changes |
|-----------------|------|---------|
| 1.0.0 | 2026-04-24 | Initial read-only contract for v0.2.0 |
