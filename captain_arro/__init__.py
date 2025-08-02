"""
Captain Arro - Animated SVG Arrow Generators

A Python library for generating animated SVG arrows for web interfaces.
Provides flow and spread arrow generators with various animation styles.
"""

from .generators.flow.moving_flow_arrow_generator import MovingFlowArrowGenerator
from .generators.flow.spotlight_flow_arrow_generator import SpotlightFlowArrowGenerator
from .generators.spread.bouncing_spread_arrow_generator import BouncingSpreadArrowGenerator
from .generators.spread.spotlight_spread_arrow_generator import SpotlightSpreadArrowGenerator
from .generators.base import AnimatedArrowGeneratorBase
from .constants import ANIMATION_TYPES, FLOW_DIRECTIONS, SPREAD_DIRECTIONS, ArrowTypeEnum

__version__ = "0.1.0"
__author__ = "Helge Esch"


def get_generator_for_arrow_type(arrow_type: ArrowTypeEnum) -> type[AnimatedArrowGeneratorBase]:
    if arrow_type == ArrowTypeEnum.MOVING_FLOW_ARROW:
        return MovingFlowArrowGenerator
    if arrow_type == ArrowTypeEnum.SPOTLIGHT_FLOW_ARROW:
        return SpotlightFlowArrowGenerator
    if arrow_type == ArrowTypeEnum.BOUNCING_SPREAD_ARROW:
        return BouncingSpreadArrowGenerator
    if arrow_type == ArrowTypeEnum.SPOTLIGHT_SPREAD_ARROW:
        return SpotlightSpreadArrowGenerator
    raise ValueError(f'GeneratorEnum {arrow_type} not recognized.')


__all__ = [
    "MovingFlowArrowGenerator",
    "SpotlightFlowArrowGenerator",
    "BouncingSpreadArrowGenerator",
    "SpotlightSpreadArrowGenerator",
    "AnimatedArrowGeneratorBase",
    "ANIMATION_TYPES",
    "FLOW_DIRECTIONS",
    "SPREAD_DIRECTIONS",
    "ArrowTypeEnum",
    "get_generator_for_arrow_type"
]
