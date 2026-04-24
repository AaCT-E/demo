#!/usr/bin/env python3
"""
AaCT-E Verification Suite

Assertion-based pass/fail verification for all scenarios.
Usage: python verify_demo.py
"""

from pathlib import Path

from aacte.engine import load_scenario, evaluate_scenario


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    unsafe = evaluate_scenario(load_scenario(Path("scenarios") / "unsafe_merge.json"))
    safe = evaluate_scenario(load_scenario(Path("scenarios") / "safe_hold.json"))

    # --- unsafe_merge assertions ---
    assert_true(unsafe["decision"] == "DENY", "unsafe_merge must DENY")
    assert_true(
        unsafe["proposal_min_separation_nm"] < unsafe["threshold_min_separation_nm"],
        "unsafe_merge proposal must violate minimum separation",
    )
    assert_true(
        unsafe["recovery_reachable"] is True,
        "unsafe_merge must retain at least one reachable recovery alternative",
    )
    assert_true(
        len(unsafe["alternatives"]) >= 1,
        "unsafe_merge must record alternatives",
    )

    # --- safe_hold assertions ---
    assert_true(safe["decision"] == "ALLOW", "safe_hold must ALLOW")
    assert_true(
        safe["proposal_min_separation_nm"] >= safe["threshold_min_separation_nm"],
        "safe_hold proposal must preserve minimum separation",
    )
    assert_true(
        len(safe["timeline"]) == safe["horizon_steps"] + 1,
        "timeline length must match horizon",
    )

    # --- cross-check: outputs exist ---
    out_dir = Path("outputs")
    assert_true(
        (out_dir / "unsafe_merge_trace.json").exists(),
        "unsafe_merge trace must be emitted",
    )
    assert_true(
        (out_dir / "safe_hold_trace.json").exists(),
        "safe_hold trace must be emitted",
    )

    print("Verification PASSED")


if __name__ == "__main__":
    main()
