"""
Constants used across arrow generators.
"""

from typing import Literal
from enum import Enum

# Animation types
ANIMATION_TYPES = Literal["linear", "ease", "ease-in", "ease-out", "ease-in-out"]

# Direction types
FLOW_DIRECTIONS = Literal["right", "left", "up", "down"]
SPREAD_DIRECTIONS = Literal["horizontal", "vertical"]


class ArrowTypeEnum(Enum):
    MOVING_FLOW_ARROW = 'moving_flow_arrow'
    SPOTLIGHT_FLOW_ARROW = 'spotlight_flow_arrow'
    BOUNCING_SPREAD_ARROW = 'bouncing_spread_arrow'
    SPOTLIGHT_SPREAD_ARROW = 'spotlight_spread_arrow'
