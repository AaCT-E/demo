#!/usr/bin/env python3
"""
access/cli.py — Single-command launcher for AaCT-E demo

Usage:
    python -m access.cli           # Run demo + print formatted status
    python -m access.cli --json    # Emit structured JSON status
    python -m access.cli --verify  # Run verification only
    python -m access.cli --serve   # Start web endpoint (stdin/stdout mode)

This is an observation layer. It runs the demo; it does not
modify scenarios, thresholds, or engine code.
"""

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone

# Add parent to path so we can import aacte
sys.path.insert(0, str(Path(__file__).parent.parent))

from aacte.engine import load_scenario, evaluate_scenario

SCENARIOS = ["unsafe_merge", "safe_hold"]


def run_demo() -> dict:
    """Execute all scenarios and return structured results."""
    results = {}
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)

    for name in SCENARIOS:
        scenario = load_scenario(Path("scenarios") / f"{name}.json")
        result = evaluate_scenario(scenario)
        out_path = out_dir / f"{name}_trace.json"
        out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
        results[name] = result

    return results


def verify(results: dict) -> bool:
    """Assertion-based verification."""
    unsafe = results["unsafe_merge"]
    safe = results["safe_hold"]

    checks = [
        (unsafe["decision"] == "DENY", "unsafe_merge must DENY"),
        (unsafe["proposal_min_separation_nm"] < unsafe["threshold_min_separation_nm"],
         "unsafe_merge must violate separation"),
        (unsafe["recovery_reachable"] is True,
         "unsafe_merge must retain recovery"),
        (safe["decision"] == "ALLOW", "safe_hold must ALLOW"),
        (safe["proposal_min_separation_nm"] >= safe["threshold_min_separation_nm"],
         "safe_hold must preserve separation"),
    ]

    all_passed = True
    for condition, msg in checks:
        if not condition:
            print(f"FAIL: {msg}")
            all_passed = False

    return all_passed


def format_status(results: dict) -> str:
    """Human-readable status summary."""
    lines = [
        "═" * 60,
        "  AaCT-E Demo Status",
        "═" * 60,
        f"  Version:    0.2.0",
        f"  Timestamp:  {datetime.now(timezone.utc).isoformat()}",
        f"  Scenarios:  {len(results)}",
        "",
    ]
    for name, data in results.items():
        decision = data["decision"]
        sep = data["proposal_min_separation_nm"]
        rec = data["recovery_reachable"]
        icon = "🟢" if decision == "ALLOW" else "🔴"
        lines.append(f"  {icon} {name:20s} {decision:6s}  min_sep={sep:.3f}nm  recovery={rec}")

    lines.extend(["", "  Run 'python verify_demo.py' for full assertions.", "═" * 60])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="AaCT-E Access Layer")
    parser.add_argument("--json", action="store_true", help="Emit JSON status")
    parser.add_argument("--verify", action="store_true", help="Run verification only")
    parser.add_argument("--serve", action="store_true", help="Start web endpoint")
    args = parser.parse_args()

    if args.serve:
        from access.web import main as web_main
        web_main()
        return

    results = run_demo()

    if args.verify:
        passed = verify(results)
        sys.exit(0 if passed else 1)

    if args.json:
        status = {
            "schema_version": "2.0.0",
            "repo": "AaCT-E/demo",
            "version": "0.2.0",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "scenarios": results,
        }
        print(json.dumps(status, indent=2))
    else:
        print(format_status(results))


if __name__ == "__main__":
    main()
