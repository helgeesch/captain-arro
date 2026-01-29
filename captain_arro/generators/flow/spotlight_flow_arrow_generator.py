from typing import Union, Tuple
import uuid

from captain_arro.generators.base import AnimatedArrowGeneratorBase
from captain_arro.constants import FLOW_DIRECTIONS


class SpotlightFlowArrowGenerator(AnimatedArrowGeneratorBase):
    """
    Generates animated SVG arrows with a moving spotlight effect that highlights different parts.
    
    This generator creates arrows that flow in the specified direction while a spotlight effect
    moves along them, creating a dynamic lighting animation. The non-highlighted areas are dimmed
    to create visual contrast. Perfect for drawing attention to specific flow directions or
    creating sophisticated visual indicators.
    
    Example:

        >>> generator = SpotlightFlowArrowGenerator(
        ...     direction="right", 
        ...     color="#8b5cf6",
        ...     spotlight_size=0.3,
        ...     dim_opacity=0.5
        ... )
        >>> svg_content = generator.generate_svg()
    """
    def __init__(
        self,
        color: str = "#2563eb",
        stroke_width: int = 10,
        width: int = 100,
        height: int = 100,
        speed_in_px_per_second: float = 20.0,
        speed_in_duration_seconds: float | None = None,
        direction: FLOW_DIRECTIONS = "right",
        num_arrows: int = 3,
        spotlight_size: float = 0.3,
        spotlight_path_extension_factor: float = 0.5,
        dim_opacity: float = 0.2,
    ) -> None:
        super().__init__(
            color=color,
            stroke_width=stroke_width,
            width=width,
            height=height,
            speed_in_px_per_second=speed_in_px_per_second,
            speed_in_duration_seconds=speed_in_duration_seconds,
            num_arrows=num_arrows,
        )
        self.direction = direction.lower()
        self.spotlight_size = max(0.1, min(1.0, spotlight_size))
        self.spotlight_path_extension_factor = spotlight_path_extension_factor
        self.dim_opacity = max(0.0, min(1.0, dim_opacity))

    def generate_svg(self, unique_id: Union[bool, str] = True) -> str:
        clip_bounds = self._get_clip_bounds()
        animations = self._generate_animations()
        arrow_elements = self._generate_arrow_elements()
        # keep the old name but return mask defs inside
        gradient_defs = self._generate_gradient_defs()

        svg = f"""
        <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <clipPath id="arrowClip">
              <rect x="{clip_bounds['x']}" y="{clip_bounds['y']}" width="{clip_bounds['width']}" height="{clip_bounds['height']}"/>
            </clipPath>
            {gradient_defs}
          </defs>

          <style>
            {animations}
          </style>

          <g clip-path="url(#arrowClip)">
            {arrow_elements}
          </g>
        </svg>
        """

        if unique_id is not False:
            suffix = uuid.uuid4().hex[:6] if unique_id is True else str(unique_id)
            svg = self._apply_unique_suffix(svg, suffix, self._get_unique_id_keys())
        return svg

    def _sweep_axis(self) -> str:
        return "x" if self.direction in ["left", "right"] else "y"

    def _sweep_rect_dims(self) -> Tuple[float, float]:
        if self._sweep_axis() == "x":
            rect_w = self.width * (0.6 + 0.4 * max(0.0, self.spotlight_path_extension_factor))
            rect_h = self.height * 2.0
        else:
            rect_w = self.width * 2.0
            rect_h = self.height * (0.6 + 0.4 * max(0.0, self.spotlight_path_extension_factor))
        return float(rect_w), float(rect_h)

    def _generate_gradient_defs(self) -> str:
        grad_id = "maskGrad"
        mask_id = "sweepMask"
        spotlight_pct = self.spotlight_size * 100.0
        a = max(0.0, min(50.0, (100.0 - spotlight_pct) / 2.0))
        b = 100.0 - a
        rect_w, rect_h = self._sweep_rect_dims()
        rect_x = (self.width - rect_w) / 2.0
        rect_y = (self.height - rect_h) / 2.0
        if self._sweep_axis() == "x":
            grad_axis = 'x1="0" y1="0" x2="1" y2="0"'
        else:
            grad_axis = 'x1="0" y1="0" x2="0" y2="1"'
        return f"""
        <linearGradient id="{grad_id}" {grad_axis}>
          <stop offset="0%" stop-color="black" stop-opacity="0"/>
          <stop offset="{a:.1f}%" stop-color="white" stop-opacity="1"/>
          <stop offset="{b:.1f}%" stop-color="white" stop-opacity="1"/>
          <stop offset="100%" stop-color="black" stop-opacity="0"/>
        </linearGradient>
        <mask id="{mask_id}" maskUnits="userSpaceOnUse" x="0" y="0" width="{self.width}" height="{self.height}">
          <rect class="sweep-rect" x="{rect_x:.2f}" y="{rect_y:.2f}" width="{rect_w:.2f}" height="{rect_h:.2f}" fill="url(#{grad_id})"/>
        </mask>
        """

    def _generate_animations(self) -> str:
        dur = self._duration_seconds()
        rect_w, rect_h = self._sweep_rect_dims()
        if self._sweep_axis() == "x":
            travel = (self.width + rect_w) / 2.0
            if self.direction == "right":
                start_t, end_t = f"translateX(-{travel:.2f}px)", f"translateX({travel:.2f}px)"
            else:
                start_t, end_t = f"translateX({travel:.2f}px)", f"translateX(-{travel:.2f}px)"
        else:
            travel = (self.height + rect_h) / 2.0
            if self.direction == "down":
                start_t, end_t = f"translateY(-{travel:.2f}px)", f"translateY({travel:.2f}px)"
            else:
                start_t, end_t = f"translateY({travel:.2f}px)", f"translateY(-{travel:.2f}px)"
        return f"""
        .arrow-dim polyline {{
          stroke: {self.color};
          stroke-opacity: {self.dim_opacity};
          stroke-width: {self.stroke_width};
          stroke-linecap: round;
          stroke-linejoin: round;
          fill: none;
        }}
        .arrow-hi polyline {{
          stroke: {self.color};
          stroke-width: {self.stroke_width};
          stroke-linecap: round;
          stroke-linejoin: round;
          fill: none;
          mask: url(#sweepMask);
        }}
        @keyframes sweep {{
          0% {{ transform: {start_t}; }}
          100% {{ transform: {end_t}; }}
        }}
        .sweep-rect {{
          animation: sweep {dur:.2f}s linear infinite;
          transform-box: fill-box;
          transform-origin: center;
        }}
        """

    def _generate_arrow_elements(self) -> str:
        spacing = self._calculate_arrow_spacing()
        dim_parts: list[str] = []
        hi_parts: list[str] = []
        for i in range(self.num_arrows):
            position = self._calculate_arrow_position(i, spacing)
            dim_parts.append(f'<polyline points="{position}"/>')
            hi_parts.append(f'<polyline points="{position}"/>')
        return f'''
        <g class="arrow-dim">
          {' '.join(dim_parts)}
        </g>
        <g class="arrow-hi">
          {' '.join(hi_parts)}
        </g>
        '''.strip()

    # --- helpers unchanged from your version ---
    def _duration_seconds(self) -> float:
        if self.speed_in_duration_seconds is not None:
            return float(self.speed_in_duration_seconds)
        distance = self._get_transform_distance() * (1.0 + self.spotlight_path_extension_factor)
        v = max(1e-6, float(self.speed_in_px_per_second))
        return distance / v

    def _calculate_arrow_spacing(self) -> int:
        if self.direction in ["up", "down"]:
            available_space = self.height - 2 * (self.height // 5)
            return max(1, available_space // (self.num_arrows + 1))
        else:
            available_space = self.width - 2 * (self.width // 5)
            return max(1, available_space // (self.num_arrows + 1))

    def _calculate_arrow_position(self, index: int, spacing: int) -> str:
        base_points = self._get_arrow_points()
        if self.direction in ["up", "down"]:
            margin = self.height // 5
            dy = margin + (index + 1) * spacing - self.height // 2
            return self._offset_points(base_points, 0, dy)
        else:
            margin = self.width // 5
            dx = margin + (index + 1) * spacing - self.width // 2
            return self._offset_points(base_points, dx, 0)

    def _offset_points(self, points: str, offset_x: int, offset_y: int) -> str:
        out = []
        for pair in points.split():
            x, y = map(lambda x: int(float(x)), pair.split(","))
            out.append(f"{x + offset_x},{y + offset_y}")
        return " ".join(out)

    def _get_clip_bounds(self) -> dict[str, int]:
        return {"x": 0, "y": 0, "width": self.width, "height": self.height}

    def _get_arrow_points(self) -> str:
        cx = self.width // 2
        cy = self.height // 2
        ox = self.width // 4
        oy = self.height // 4
        if self.direction == "down":
            return f"{cx - ox},{cy - oy // 2} {cx},{cy + oy // 2} {cx + ox},{cy - oy // 2}"
        elif self.direction == "up":
            return f"{cx - ox},{cy + oy // 2} {cx},{cy - oy // 2} {cx + ox},{cy + oy // 2}"
        elif self.direction == "right":
            return f"{cx - ox // 2},{cy - oy} {cx + ox // 2},{cy} {cx - ox // 2},{cy + oy}"
        elif self.direction == "left":
            return f"{cx + ox // 2},{cy - oy} {cx - ox // 2},{cy} {cx + ox // 2},{cy + oy}"
        else:
            raise ValueError(f"Invalid direction: {self.direction}. Use 'up', 'down', 'left', or 'right'.")

    def _get_transform_distance(self) -> float:
        return float(self.height if self.direction in ["up", "down"] else self.width)

    def _get_unique_id_keys(self) -> list[str]:
        return [
            "arrowClip",
            # old gradient id from previous versions (kept for safety)
            "spotlightGradient",
            # new ids for mask-based sweep
            "maskGrad",
            "sweepMask",
        ]


if __name__ == "__main__":
    generator = SpotlightFlowArrowGenerator()

    print("Generated default spotlight flow arrow:")
    print(generator.generate_svg())

    generator.save_to_file("_tmp/spotlight_flow_arrow_default.svg")

    configurations = [
        {"num_arrows": 2, "direction": "right", "color": "#3b82f6", "width": 200, "height": 80,
         "speed_in_duration_seconds": 10.0, "speed_in_px_per_second": None, "spotlight_size": 0.25},
        {"num_arrows": 3, "direction": "up", "color": "#ef4444", "width": 100, "height": 150,
         "speed_in_duration_seconds": 6.0, "speed_in_px_per_second": None, "spotlight_size": 0.01, "dim_opacity": 0.3},
        {"num_arrows": 4, "direction": "left", "color": "#10b981", "width": 180, "height": 60,
         "speed_in_duration_seconds": 3.0, "speed_in_px_per_second": None, "spotlight_size": 0.25},
        {"num_arrows": 5, "direction": "down", "color": "#ef4444", "width": 100, "height": 150,
         "speed_in_duration_seconds": 6.0, "speed_in_px_per_second": None, "spotlight_size": 0.01, "dim_opacity": 0.3},
    ]

    for config in configurations:
        gen = SpotlightFlowArrowGenerator(**config)
        file = f"_tmp/spotlight_flow_arrow_{config['num_arrows']}_{config['direction']}.svg"
        gen.save_to_file(file)
        print(f"Created {file} with {config}")
