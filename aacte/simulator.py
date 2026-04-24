from __future__ import annotations

from dataclasses import asdict
from typing import List, Dict

from aacte.geometry import heading_to_unit_vector, separation_nm
from aacte.models import Aircraft


def clone_aircraft_list(aircraft_list: List[Aircraft]) -> List[Aircraft]:
    """Deep-copy a list of aircraft states."""
    return [
        Aircraft(
            id=a.id,
            x_nm=a.x_nm,
            y_nm=a.y_nm,
            heading_deg=a.heading_deg,
            speed_kts=a.speed_kts,
        )
        for a in aircraft_list
    ]


def step_aircraft(aircraft: Aircraft, dt_sec: int) -> Aircraft:
    """Advance one aircraft by dt_sec at constant speed and heading."""
    dx_unit, dy_unit = heading_to_unit_vector(aircraft.heading_deg)
    distance_nm = aircraft.speed_kts * dt_sec / 3600.0
    return Aircraft(
        id=aircraft.id,
        x_nm=aircraft.x_nm + dx_unit * distance_nm,
        y_nm=aircraft.y_nm + dy_unit * distance_nm,
        heading_deg=aircraft.heading_deg,
        speed_kts=aircraft.speed_kts,
    )


def compute_min_pairwise_separation(aircraft_list: List[Aircraft]) -> float:
    """Minimum separation across all unordered pairs."""
    min_sep = float("inf")
    n = len(aircraft_list)
    for i in range(n):
        for j in range(i + 1, n):
            sep = separation_nm(aircraft_list[i], aircraft_list[j])
            if sep < min_sep:
                min_sep = sep
    return min_sep


def simulate_timeline(
    aircraft_list: List[Aircraft], dt_sec: int, horizon_steps: int
) -> List[Dict]:
    """Simulate forward and return per-step state + min separation."""
    timeline = []
    current = clone_aircraft_list(aircraft_list)
    for step in range(horizon_steps + 1):
        timeline.append(
            {
                "step": step,
                "aircraft": [asdict(a) for a in current],
                "min_pairwise_separation_nm": compute_min_pairwise_separation(current),
            }
        )
        if step < horizon_steps:
            current = [step_aircraft(a, dt_sec) for a in current]
    return timeline


def projected_min_separation(timeline: List[Dict]) -> float:
    """Worst-case minimum separation across the entire timeline."""
    return min(frame["min_pairwise_separation_nm"] for frame in timeline)
