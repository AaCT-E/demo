from aacte.geometry import normalize_heading_deg
from aacte.models import Aircraft

ACTION_DELTAS = {
    "MAINTAIN": 0.0,
    "TURN_LEFT_15": -15.0,
    "TURN_RIGHT_15": 15.0,
    "TURN_LEFT_30": -30.0,
    "TURN_RIGHT_30": 30.0,
}


def apply_action(aircraft: Aircraft, action: str) -> Aircraft:
    """Return a new Aircraft with the action applied to heading."""
    if action not in ACTION_DELTAS:
        raise ValueError(f"Unsupported action: {action}")
    delta = ACTION_DELTAS[action]
    return Aircraft(
        id=aircraft.id,
        x_nm=aircraft.x_nm,
        y_nm=aircraft.y_nm,
        heading_deg=normalize_heading_deg(aircraft.heading_deg + delta),
        speed_kts=aircraft.speed_kts,
    )
