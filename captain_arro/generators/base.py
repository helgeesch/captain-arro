"""
Base class for arrow generators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Union


class AnimatedArrowGeneratorBase(ABC):
    """
    Abstract base class for all animated arrow generators.
    
    Provides common functionality and interface for arrow generation.
    """
    
    def __init__(
        self,
        color: str = "#2563eb",
        stroke_width: int = 10,
        width: int = 100,
        height: int = 100,
        speed_in_px_per_second: float = None,
        speed_in_duration_seconds: float = None,
        num_arrows: int = 4,
    ):
        self.color = color
        self.width = width
        self.height = height
        self.num_arrows = max(1, num_arrows)
        self.stroke_width = max(2, stroke_width)
        
        if (speed_in_px_per_second is None) and (speed_in_duration_seconds is None):
            raise ValueError("One speed option must be defined: speed_in_px_per_second or speed_in_duration_seconds")
        if (speed_in_px_per_second is not None) and (speed_in_duration_seconds is not None):
            raise ValueError("Only one speed option can be defined: speed_in_px_per_second or speed_in_duration_seconds")

        self.speed_in_px_per_second = speed_in_px_per_second
        self._speed_in_duration_seconds = speed_in_duration_seconds

    @property
    def speed_in_duration_seconds(self) -> float:
        """Get the speed in duration seconds, calculating it if needed."""
        if self._speed_in_duration_seconds is not None:
            return self._speed_in_duration_seconds
        else:
            # Calculate from speed_in_px_per_second
            transform_distance = self._get_transform_distance()
            return transform_distance / self.speed_in_px_per_second

    @abstractmethod
    def _generate_arrow_elements(self) -> str:
        """Generate the arrow elements for the SVG."""
        pass
    
    @abstractmethod
    def _generate_animations(self) -> str:
        """Generate the CSS animations for the SVG."""
        pass
    
    @abstractmethod
    def _get_transform_distance(self) -> float:
        """Get the transform distance for animation calculations."""
        pass
    
    def _calculate_animation_duration(self) -> float:
        """Calculate the appropriate animation duration based on speed options."""
        return self.speed_in_duration_seconds
    
    def generate_svg(self) -> str:
        """Generate the complete SVG string."""
        clip_bounds = self._get_clip_bounds()
        animations = self._generate_animations()
        arrow_elements = self._generate_arrow_elements()
        
        return f"""
        <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <clipPath id="arrowClip">
              <rect x="{clip_bounds['x']}" y="{clip_bounds['y']}" width="{clip_bounds['width']}" height="{clip_bounds['height']}"/>
            </clipPath>
            {self._generate_gradient_defs() if hasattr(self, '_generate_gradient_defs') else ''}
          </defs>
        
          <style>
            .arrow {{
              stroke: {self.color};
              stroke-width: {self.stroke_width};
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }}
            
            {self._generate_arrow_classes() if hasattr(self, '_generate_arrow_classes') else ''}
            
            {animations}
          </style>
        
          <g clip-path="url(#arrowClip)">
            {arrow_elements}
          </g>
        </svg>
        """
    
    def _get_clip_bounds(self) -> Dict[str, int]:
        """Get the clipping bounds for the SVG."""
        # Use full canvas area - no margins
        return {
            "x": 0,
            "y": 0,
            "width": self.width,
            "height": self.height
        }
    
    def save_to_file(self, file_path: str) -> None:
        """Save the generated SVG to a file."""
        svg_content = self.generate_svg()
        with open(file_path, 'w') as file:
            file.write(svg_content)