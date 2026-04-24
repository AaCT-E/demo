from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Aircraft:
    """Immutable aircraft state."""
    id: str
    x_nm: float
    y_nm: float
    heading_deg: float
    speed_kts: float


@dataclass(frozen=True)
class Scenario:
    """Immutable scenario definition."""
    name: str
    dt_sec: int
    horizon_steps: int
    min_separation_nm: float
    recovery_min_separation_nm: float
    proposal_aircraft_id: str
    proposed_action: str
    alternative_actions: List[str]
    aircraft: List[Aircraft]
