"""
Base class for arrow generators.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


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
        speed: float = 20.0,
        num_arrows: int = 4,
    ):
        self.color = color
        self.width = width
        self.height = height
        self.speed = speed
        self.num_arrows = max(1, num_arrows)
        self.stroke_width = max(2, stroke_width)
    
    @abstractmethod
    def _generate_arrow_elements(self) -> str:
        """Generate the arrow elements for the SVG."""
        pass
    
    @abstractmethod
    def _generate_animations(self) -> str:
        """Generate the CSS animations for the SVG."""
        pass
    
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