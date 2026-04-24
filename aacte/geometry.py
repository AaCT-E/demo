import math
from aacte.models import Aircraft


def normalize_heading_deg(value: float) -> float:
    """Wrap heading to [0, 360)."""
    return value % 360.0


def heading_to_unit_vector(heading_deg: float) -> tuple[float, float]:
    """Convert heading to (dx, dy) unit vector."""
    radians = math.radians(heading_deg)
    return math.cos(radians), math.sin(radians)


def separation_nm(a: Aircraft, b: Aircraft) -> float:
    """Euclidean distance between two aircraft in nautical miles."""
    return math.hypot(a.x_nm - b.x_nm, a.y_nm - b.y_nm)
