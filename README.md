# AaCT-E — Admissibility at Commit-Time Engine

[![CI](https://github.com/AaCT-E/demo/actions/workflows/verify.yml/badge.svg)](https://github.com/AaCT-E/demo/actions/workflows/verify.yml)
[![Version](https://img.shields.io/badge/version-0.2.0-blue)](https://github.com/AaCT-E/demo/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)]()

> **Minimal, runnable prototype of commit-time safety enforcement for AI-assisted aviation decisions.**
>
> This repo is a Phase-I-style evidence artifact: one narrow claim, executable in seconds, verifiable by assertion.

---

## What This Proves

At the exact moment an action would become operationally real, the system evaluates whether recovery remains available and **denies** the action if it would push the system into an unrecoverable or separation-violating state.

| Internal Concept | Procurement Translation |
|------------------|------------------------|
| GCAT / BCAT | Commit-time safety enforcement |
| Admissibility | Recoverability-preserving action permission |
| Actuator boundary | Commit point |
| Fail-closed | Deny on unsafe projection |
| Trajectory invariant | Projected minimum separation across horizon |

---

## How to Access

Three paths, one purpose, zero dependencies:

| Path | Audience | Command |
|------|----------|---------|
| **Direct clone** | Reviewers | `git clone` → `python verify_demo.py` |
| **Via SDK** | Developers | `stegverse demo --repo AaCT-E/demo --tag v0.2.0` |
| **HTTP endpoint** | Systems | `python -m access.web --port 8080` |

See [docs/ACCESS.md](docs/ACCESS.md) for full details.

---

## Zero-Dependency Run

```bash
git clone --branch v0.2.0 https://github.com/AaCT-E/demo.git
cd demo
python run_demo.py
python verify_demo.py
```

**No `pip install`. No `requirements.txt` to resolve. No external packages.**

---

## Repo Contents

| Path | Purpose |
|------|---------|
| `run_demo.py` | Execute all scenarios, emit JSON traces |
| `verify_demo.py` | Assertion-based pass/fail verification |
| `aacte/` | Core engine (frozen since v0.1.0) |
| `scenarios/` | Scenario inputs (frozen since v0.1.0) |
| `access/` | Single-purpose entry points (cli, web) |
| `outputs/` | Generated traces after execution |
| `DEMO_SPEC.md` | Exact specification (frozen) |
| `aacte.architecture.json` | Ecosystem architecture manifest |
| `stegdb_hooks/` | StegDB monitoring integration |
| `.github/workflows/verify.yml` | CI verification |
| `.github/workflows/release.yml` | Tag-triggered release packaging |
| `docs/ACCESS.md` | How to access the demo |
| `docs/SDK_INTEGRATION.md` | SDK wrapping contract |
| `docs/SUBMISSION.md` | FAA/TSSC/SBIR packaging guide |
| `docs/ECOSYSTEM.md` | Ecosystem guide |
| `docs/PROCUREMENT.md` | Procurement translation |
| `CHANGELOG.md` | Version history |

---

## Expected Results

### `unsafe_merge`
- **Decision:** `DENY`
- **Why:** Proposed turn reduces minimum separation to ~1.20 nm (below 3.0 nm threshold)
- **Recovery:** `TURN_LEFT_30` remains reachable at ~4.11 nm — a safer alternative exists

### `safe_hold`
- **Decision:** `ALLOW`
- **Why:** Maintaining heading preserves ~8.06 nm minimum separation (above threshold)
- **Recovery:** Both alternatives also preserve safe separation

---

## Ecosystem Context

AaCT-E is part of the **GCAT/BCAT** research-to-procurement pipeline:

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  GCAT-BCAT-Engine   │────▶│  GCAT-BCAT-Engine   │────▶│    AaCT-E/demo      │
│  (Formal Theory)    │     │  /Publisher           │     │  (Executable Demo)    │
│  Proofs, Metrics    │     │  Papers, Submissions  │     │  Procurement Evidence │
└─────────────────────┘     └─────────────────────┘     └─────────────────────┘
            │                                               │
            └───────────────────────────────────────────────┘
                              StegVerse Ecosystem
                    ┌─────────┐    ┌─────────┐    ┌─────────┐
                    │ StegDB  │    │  SDK    │    │  Site   │
                    │ Monitor │    │ Validate│    │ Publish │
                    └─────────┘    └─────────┘    └─────────┘
```

- **Upstream theory:** [GCAT-BCAT-Engine](https://github.com/GCAT-BCAT-Engine)
- **Paper publishing & social media:** [GCAT-BCAT-Engine/Publisher](https://github.com/GCAT-BCAT-Engine/Publisher)
- **Entity sandbox & monitoring:** [StegVerse-Labs/StegDB](https://github.com/StegVerse-Labs/StegDB)
- **User-facing validation:** [StegVerse-Labs/SDK](https://github.com/StegVerse-Labs/SDK)

---

## Verification Criteria

The demo is complete when:

1. ✅ `python run_demo.py` completes without error
2. ✅ `python verify_demo.py` prints `Verification PASSED`
3. ✅ `unsafe_merge` yields `DENY`
4. ✅ `safe_hold` yields `ALLOW`
5. ✅ Each scenario emits a JSON trace in `outputs/`
6. ✅ The trace records at least one alternative action evaluation
7. ✅ The trace explicitly records whether recovery remained reachable

---

## Citation

```bibtex
@software{aacte_demo,
  title = {AaCT-E: Admissibility at Commit-Time Engine},
  url = {https://github.com/AaCT-E/demo},
  version = {0.2.0},
  year = {2026}
}
```

See [`CITATION.cff`](CITATION.cff) for full metadata.

---

## License

Apache-2.0. See [`LICENSE`](LICENSE).
