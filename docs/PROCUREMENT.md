# Procurement Translation Guide

## For FAA / TSSC Reviewers

This repository is a **Phase I evidence artifact**. It is not an operational ATC system. It proves one narrow claim that underpins a larger safety formalism.

### The Claim

> At the exact moment an action would become operationally real, the system can evaluate whether recovery remains available and deny the action if it would push the system into an unrecoverable or separation-violating state.

### How to Verify It

```bash
git clone https://github.com/AaCT-E/demo.git
cd demo
python run_demo.py      # See scenarios execute
python verify_demo.py   # See assertions pass
```

No external dependencies. No configuration. No network required.

### What You Will See

- **Scenario A (`unsafe_merge`)**: A proposed unsafe turn is **denied**. A safer alternative is identified.
- **Scenario B (`safe_hold`)**: A proposed safe hold is **allowed**.

Both scenarios emit JSON traces in `outputs/` that you can inspect, diff, or feed into your own tools.

### Connection to Broader Work

This demo implements the commit-time safety mechanism described in the GCAT/BCAT formalism (see [GCAT-BCAT-Engine/Publisher](https://github.com/GCAT-BCAT-Engine/Publisher) for papers). The formalism defines:
- **GCAT**: Global Confinement Assurance Test — can the system stay safe?
- **BCAT**: Boundary Confinement Assurance Test — can the system recover?

This demo shows both in action: the gate denies when GCAT fails, and checks BCAT via alternative actions.

### Questions?

Open an issue at [github.com/AaCT-E/demo/issues](https://github.com/AaCT-E/demo/issues) or contact the GCAT-BCAT-Engine maintainers.

---

## For SBIR Evaluators

### Technical Merit
- Zero dependencies: demonstrates minimal attack surface
- Deterministic: same input → same trace → same decision
- Verifiable: `verify_demo.py` is self-checking; CI runs daily

### Commercialization Path
- The commit-time gate pattern applies to any safety-critical system with discrete action points (drones, autonomous vehicles, industrial robotics)
- The GCAT/BCAT formalism provides IP protection through mathematical novelty
- StegVerse SDK provides a commercialization wrapper for non-aviation markets

### Phase II Expansion
- Multi-aircraft scenarios (3+, pairwise + global separation)
- 3D kinematics (climb/descent)
- Real-time performance benchmarking
- Integration with existing ATC simulation frameworks
