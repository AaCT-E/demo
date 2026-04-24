# Changelog

All notable changes to the AaCT-E demo project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.2.0] — 2026-04-24

### Added
- `access/` layer: `cli.py` single-command launcher, `web.py` HTTP endpoint
- `docs/ACCESS.md`: Three-path access guide (direct, SDK, HTTP)
- `docs/SDK_INTEGRATION.md`: Read-only contract for SDK wrapping
- `docs/SUBMISSION.md`: FAA/TSSC/SBIR packaging checklist
- `.github/workflows/release.yml`: Tag-triggered release with trace archive
- `CHANGELOG.md`: This file

### Changed
- `README.md`: Added ACCESS.md link, SDK mention, version badge
- `stegdb_hooks/emit_status.py`: Updated to schema v2.0.0 with `version` field
- `aacte.architecture.json`: Bumped schema to v2.0.0, added `access` entry points

### Frozen
- `aacte/*.py`: Core engine unchanged from v0.1.0
- `scenarios/*.json`: Canonical evidence scenarios unchanged
- `DEMO_SPEC.md`: Specification matches v0.1.0 behavior

---

## [0.1.0] — 2026-04-22

### Added
- Initial commit-time safety enforcement demo
- Core engine: `aacte/` package (models, geometry, actions, simulator, engine)
- Two scenarios: `unsafe_merge` (DENY), `safe_hold` (ALLOW)
- `run_demo.py` and `verify_demo.py`
- `DEMO_SPEC.md`: Complete formal specification
- `aacte.architecture.json`: Ecosystem manifest
- `stegdb_hooks/`: StegDB monitoring integration
- `.github/workflows/verify.yml`: CI across Python 3.10–3.13
- `docs/ECOSYSTEM.md` and `docs/PROCUREMENT.md`
- `CITATION.cff`, `LICENSE` (Apache-2.0), `pyproject.toml`, `Makefile`

### Characteristics
- Zero external dependencies
- Deterministic: same input → same trace → same decision
- Assertion-based verification: self-checking
