#!/usr/bin/env python3
"""
AaCT-E Demo Runner

Executes all scenarios and emits JSON traces to outputs/.
Usage: python run_demo.py
"""

from pathlib import Path
import json

from aacte.engine import load_scenario, evaluate_scenario

SCENARIOS = ["unsafe_merge", "safe_hold"]


def main() -> None:
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    for name in SCENARIOS:
        scenario = load_scenario(Path("scenarios") / f"{name}.json")
        result = evaluate_scenario(scenario)
        out_path = out_dir / f"{name}_trace.json"
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(
            f"{name}: {result['decision']} | "
            f"proposal_min_sep={result['proposal_min_separation_nm']:.3f} nm | "
            f"recovery_reachable={result['recovery_reachable']}"
        )


if __name__ == "__main__":
    main()
