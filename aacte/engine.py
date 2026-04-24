from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from aacte.actions import apply_action
from aacte.models import Aircraft, Scenario
from aacte.simulator import (
    clone_aircraft_list,
    simulate_timeline,
    projected_min_separation,
)


def load_scenario(path: Path) -> Scenario:
    """Load a scenario from JSON file."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    aircraft = [Aircraft(**a) for a in raw["aircraft"]]
    return Scenario(
        name=raw["name"],
        dt_sec=raw["dt_sec"],
        horizon_steps=raw["horizon_steps"],
        min_separation_nm=raw["min_separation_nm"],
        recovery_min_separation_nm=raw["recovery_min_separation_nm"],
        proposal_aircraft_id=raw["proposal_aircraft_id"],
        proposed_action=raw["proposed_action"],
        alternative_actions=raw["alternative_actions"],
        aircraft=aircraft,
    )


def _apply_action_to_target(
    aircraft_list: List[Aircraft], target_id: str, action: str
) -> List[Aircraft]:
    """Apply an action to a specific aircraft by ID."""
    updated = []
    found = False
    for aircraft in clone_aircraft_list(aircraft_list):
        if aircraft.id == target_id:
            updated.append(apply_action(aircraft, action))
            found = True
        else:
            updated.append(aircraft)
    if not found:
        raise ValueError(f"Target aircraft not found: {target_id}")
    return updated


def _evaluate_action(scenario: Scenario, action: str) -> Dict:
    """Evaluate a single action: simulate horizon, return metrics."""
    acted = _apply_action_to_target(
        scenario.aircraft,
        scenario.proposal_aircraft_id,
        action,
    )
    timeline = simulate_timeline(acted, scenario.dt_sec, scenario.horizon_steps)
    min_sep = projected_min_separation(timeline)
    return {
        "action": action,
        "projected_min_separation_nm": round(min_sep, 6),
        "timeline": timeline,
    }


def evaluate_scenario(scenario: Scenario) -> Dict:
    """
    Commit-time gate evaluation.

    Returns a dict with decision, proposal metrics, alternative evaluations,
    and full timeline for the proposed action.
    """
    proposal_eval = _evaluate_action(scenario, scenario.proposed_action)
    proposal_min_sep = proposal_eval["projected_min_separation_nm"]
    decision = "ALLOW" if proposal_min_sep >= scenario.min_separation_nm else "DENY"

    alternatives = []
    recovery_reachable = False
    for action in scenario.alternative_actions:
        alt_eval = _evaluate_action(scenario, action)
        alt_min_sep = alt_eval["projected_min_separation_nm"]
        reachable = alt_min_sep >= scenario.recovery_min_separation_nm
        recovery_reachable = recovery_reachable or reachable
        alternatives.append(
            {
                "action": action,
                "projected_min_separation_nm": alt_min_sep,
                "recovery_reachable": reachable,
            }
        )

    return {
        "scenario": scenario.name,
        "dt_sec": scenario.dt_sec,
        "horizon_steps": scenario.horizon_steps,
        "decision": decision,
        "proposal_aircraft_id": scenario.proposal_aircraft_id,
        "proposed_action": scenario.proposed_action,
        "proposal_min_separation_nm": proposal_min_sep,
        "threshold_min_separation_nm": scenario.min_separation_nm,
        "recovery_min_separation_nm": scenario.recovery_min_separation_nm,
        "recovery_reachable": recovery_reachable,
        "alternatives": alternatives,
        "timeline": proposal_eval["timeline"],
    }
