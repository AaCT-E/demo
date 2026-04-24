# How to Access the AaCT-E Demo

> **Three paths. One purpose. Zero dependencies.**

---

## Path 1: Direct Clone (Reviewers)

For FAA/TSSC reviewers, SBIR evaluators, or anyone auditing the evidence.

```bash
git clone https://github.com/AaCT-E/demo.git
cd demo
git checkout v0.2.0          # Pin to version
python verify_demo.py        # Run assertions
```

**What you get:**
- Deterministic output: same commit → same traces → same decision
- No configuration, no secrets, no network calls
- JSON traces in `outputs/` for inspection

**Time to verify:** < 5 seconds

---

## Path 2: Via StegVerse SDK (Developers)

For developers integrating GCAT/BCAT concepts into applications.

```bash
pip install stegverse-sdk
stegverse demo --repo AaCT-E/demo --tag v0.2.0
```

**What the SDK does:**
- Clones the demo at the specified tag
- Runs `verify_demo.py` in an isolated environment
- Parses traces and surfaces them through the SDK API
- Preserves all provenance metadata (repo, commit, run ID)

**What the SDK does NOT do:**
- Modify scenario files
- Change thresholds or engine logic
- Hide verification failures

See [SDK_INTEGRATION.md](SDK_INTEGRATION.md) for the full contract.

---

## Path 3: HTTP Status Endpoint (Integrators)

For dashboards, CI pipelines, or monitoring systems.

```bash
cd demo
python -m access.web --port 8080
curl http://localhost:8080/status
```

**Response:**
```json
{
  "schema_version": "2.0.0",
  "repo": "AaCT-E/demo",
  "version": "0.2.0",
  "timestamp_utc": "2026-04-24T01:00:00Z",
  "verification_passed": true,
  "scenarios": { ... }
}
```

**Read-only.** No state mutation. No authentication required.

---

## Quick Comparison

| Path | Audience | Dependencies | Latency | Use Case |
|------|----------|-------------|---------|----------|
| Direct clone | Reviewers | Zero | < 5s | Evidence audit |
| SDK | Developers | SDK + demo | < 10s | Integration |
| HTTP endpoint | Systems | Zero | < 5s | Monitoring |

---

## Version Pinning

All three paths support version pinning. The demo is tagged semantically:

- `v0.2.0` — Current: access layer, submission packaging
- `v0.1.0` — Initial: core engine, two scenarios

**Never reference `main` for evidence.** Always use a tag.

---

## Troubleshooting

**"python verify_demo.py fails"**
- Check Python version: `python --version` (requires 3.10+)
- Check you're on the right tag: `git describe --tags`
- Check scenarios exist: `ls scenarios/`

**"SDK can't find the demo"**
- Ensure the SDK is referencing a valid tag, not `main`
- Check network access to GitHub
- See SDK_INTEGRATION.md for debug mode

**"HTTP endpoint returns 404"**
- Only `/status` is served. No other paths.
- Check port: `lsof -i :8080` or equivalent

---

## Citation

If you reference this demo in a paper or proposal:

```bibtex
@software{aacte_demo,
  title = {AaCT-E: Admissibility at Commit-Time Engine},
  url = {https://github.com/AaCT-E/demo},
  version = {0.2.0},
  year = {2026}
}
```
