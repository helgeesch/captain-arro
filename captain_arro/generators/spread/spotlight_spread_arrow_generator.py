from captain_arro.generators.base import AnimatedArrowGeneratorBase
from captain_arro.constants import SPREAD_DIRECTIONS
from typing import Union
import uuid


class SpotlightSpreadArrowGenerator(AnimatedArrowGeneratorBase):
    """
    Generates animated SVG arrows that spread outward from center with spotlight effects.
    
    This generator combines the spreading pattern of bouncing arrows with the dynamic lighting
    effects of spotlight animations. Arrows emanate from the center gap and spread outward
    while a moving spotlight effect travels along them, creating sophisticated visual emphasis.
    The non-highlighted areas are dimmed to enhance the spotlight effect.
    Perfect for drawing attention to distribution patterns or highlighting data flow from a central source.
    
    Example:

        >>> generator = SpotlightSpreadArrowGenerator(
        ...     direction="horizontal",
        ...     color="#6366f1",
        ...     spotlight_size=0.25,
        ...     dim_opacity=0.5,
        ...     center_gap_ratio=0.3
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
            speed_in_duration_seconds: float = None,
            direction: SPREAD_DIRECTIONS = "horizontal",
            num_arrows: int = 4,
            spotlight_size: float = 0.3,
            spotlight_path_extension_factor: float = 0.5,
            dim_opacity: float = 0.2,
            center_gap_ratio: float = 0.2,
    ):
        super().__init__(
            color=color,
            stroke_width=stroke_width,
            width=width,
            height=height,
            speed_in_px_per_second=speed_in_px_per_second,
            speed_in_duration_seconds=speed_in_duration_seconds,
            num_arrows=max(2, num_arrows),
        )
        self.direction = direction.lower()
        self.spotlight_size = max(0.1, min(1.0, spotlight_size))
        self.dim_opacity = max(0.0, min(1.0, dim_opacity))
        self.spotlight_path_extension_factor = spotlight_path_extension_factor
        self.center_gap_ratio = max(0.1, min(0.4, center_gap_ratio))

    def generate_svg(self, unique_id: Union[bool, str] = True) -> str:
        clip_bounds = self._get_clip_bounds()
        animations = self._generate_animations()
        arrow_elements = self._generate_arrow_elements()
        mask_defs = self._generate_mask_defs()
        svg = f"""
        <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <clipPath id="arrowClip">
              <rect x="{clip_bounds['x']}" y="{clip_bounds['y']}" width="{clip_bounds['width']}" height="{clip_bounds['height']}"/>
            </clipPath>
            {mask_defs}
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

    def _axis(self) -> str:
        return "x" if self.direction == "horizontal" else "y"

    def _rect_dims(self) -> Tuple[float, float]:
        if self._axis() == "x":
            w = self.width * (0.6 + 0.4 * max(0.0, self.spotlight_path_extension_factor))
            h = self.height * 2.0
        else:
            w = self.width * 2.0
            h = self.height * (0.6 + 0.4 * max(0.0, self.spotlight_path_extension_factor))
        return float(w), float(h)

    def _duration_seconds(self) -> float:
        if self.speed_in_duration_seconds is not None:
            return float(self.speed_in_duration_seconds)
        if self._axis() == "x":
            dist = self.width + self._rect_dims()[0]
        else:
            dist = self.height + self._rect_dims()[1]
        v = max(1e-6, float(self.speed_in_px_per_second))
        return dist / v

    def _generate_mask_defs(self) -> str:
        spotlight_pct = self.spotlight_size * 100.0
        a = max(0.0, min(50.0, (100.0 - spotlight_pct) / 2.0))
        b = 100.0 - a
        rect_w, rect_h = self._rect_dims()
        rect_x = (self.width - rect_w) / 2.0
        rect_y = (self.height - rect_h) / 2.0
        if self._axis() == "x":
            grad_axis = 'x1="0" y1="0" x2="1" y2="0"'
        else:
            grad_axis = 'x1="0" y1="0" x2="0" y2="1"'
        return f"""
        <linearGradient id="maskGradSpreadA" {grad_axis}>
          <stop offset="0%" stop-color="black" stop-opacity="0"/>
          <stop offset="{a:.1f}%" stop-color="white" stop-opacity="1"/>
          <stop offset="{b:.1f}%" stop-color="white" stop-opacity="1"/>
          <stop offset="100%" stop-color="black" stop-opacity="0"/>
        </linearGradient>
        <linearGradient id="maskGradSpreadB" {grad_axis}>
          <stop offset="0%" stop-color="black" stop-opacity="0"/>
          <stop offset="{a:.1f}%" stop-color="white" stop-opacity="1"/>
          <stop offset="{b:.1f}%" stop-color="white" stop-opacity="1"/>
          <stop offset="100%" stop-color="black" stop-opacity="0"/>
        </linearGradient>
        <mask id="sweepMaskA" maskUnits="userSpaceOnUse" x="0" y="0" width="{self.width}" height="{self.height}">
          <rect class="sweep-rect-a" x="{rect_x:.2f}" y="{rect_y:.2f}" width="{rect_w:.2f}" height="{rect_h:.2f}" fill="url(#maskGradSpreadA)"/>
        </mask>
        <mask id="sweepMaskB" maskUnits="userSpaceOnUse" x="0" y="0" width="{self.width}" height="{self.height}">
          <rect class="sweep-rect-b" x="{rect_x:.2f}" y="{rect_y:.2f}" width="{rect_w:.2f}" height="{rect_h:.2f}" fill="url(#maskGradSpreadB)"/>
        </mask>
        """

    def _generate_animations(self) -> str:
        dur = self._duration_seconds()
        rect_w, rect_h = self._rect_dims()
        if self._axis() == "x":
            travel = (self.width + rect_w) / 2.0
            start_a, end_a = f"translateX(0px)", f"translateX(-{travel:.2f}px)"
            start_b, end_b = f"translateX(0px)", f"translateX({travel:.2f}px)"
        else:
            travel = (self.height + rect_h) / 2.0
            start_a, end_a = f"translateY(0px)", f"translateY(-{travel:.2f}px)"
            start_b, end_b = f"translateY(0px)", f"translateY({travel:.2f}px)"
        return f"""
        .arrow-dim polyline {{
          stroke: {self.color};
          stroke-opacity: {self.dim_opacity};
          stroke-width: {self.stroke_width};
          stroke-linecap: round;
          stroke-linejoin: round;
          fill: none;
        }}
        .arrow-hi-a polyline,
        .arrow-hi-b polyline {{
          stroke: {self.color};
          stroke-width: {self.stroke_width};
          stroke-linecap: round;
          stroke-linejoin: round;
          fill: none;
        }}
        .arrow-hi-a polyline {{ mask: url(#sweepMaskA); }}
        .arrow-hi-b polyline {{ mask: url(#sweepMaskB); }}
        @keyframes sweepA {{ 0% {{ transform: {start_a}; }} 100% {{ transform: {end_a}; }} }}
        @keyframes sweepB {{ 0% {{ transform: {start_b}; }} 100% {{ transform: {end_b}; }} }}
        .sweep-rect-a {{ animation: sweepA {dur:.2f}s linear infinite; transform-box: fill-box; transform-origin: center; }}
        .sweep-rect-b {{ animation: sweepB {dur:.2f}s linear infinite; transform-box: fill-box; transform-origin: center; }}
        """

    def _generate_arrow_elements(self) -> str:
        if self.direction == "horizontal":
            left_positions = self._get_left_arrow_positions()
            right_positions = self._get_right_arrow_positions()
            dim_parts = []
            hi_a_parts = []
            hi_b_parts = []
            for pos in left_positions:
                pts = self._get_left_arrow_points()
                dim_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
                hi_a_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
            for pos in right_positions:
                pts = self._get_right_arrow_points()
                dim_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
                hi_b_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
            return f'''
            <g class="arrow-dim">{''.join(dim_parts)}</g>
            <g class="arrow-hi-a">{''.join(hi_a_parts)}</g>
            <g class="arrow-hi-b">{''.join(hi_b_parts)}</g>
            '''.strip()
        else:
            top_positions = self._get_top_arrow_positions()
            bottom_positions = self._get_bottom_arrow_positions()
            dim_parts = []
            hi_a_parts = []
            hi_b_parts = []
            for pos in top_positions:
                pts = self._get_up_arrow_points()
                dim_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
                hi_a_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
            for pos in bottom_positions:
                pts = self._get_down_arrow_points()
                dim_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
                hi_b_parts.append(f'<g transform="translate({pos["x"]},{pos["y"]})"><polyline points="{pts}"/></g>')
            return f'''
            <g class="arrow-dim">{''.join(dim_parts)}</g>
            <g class="arrow-hi-a">{''.join(hi_a_parts)}</g>
            <g class="arrow-hi-b">{''.join(hi_b_parts)}</g>
            '''.strip()

    def _calculate_arrow_layout(self):
        arrows_per_side = self.num_arrows // 2
        if self.direction == "horizontal":
            arrow_height = int(self.height * 0.8)
            center_gap = int(self.width * self.center_gap_ratio)
            available_width_per_side = (self.width - center_gap) // 2
            arrow_width = max(1, available_width_per_side // max(arrows_per_side, 1))
            return {"arrow_width": arrow_width, "arrow_height": arrow_height, "center_gap": center_gap, "available_width_per_side": available_width_per_side}
        else:
            arrow_width = int(self.width * 0.8)
            center_gap = int(self.height * self.center_gap_ratio)
            available_height_per_side = (self.height - center_gap) // 2
            arrow_height = max(1, available_height_per_side // max(arrows_per_side, 1))
            return {"arrow_width": arrow_width, "arrow_height": arrow_height, "center_gap": center_gap, "available_height_per_side": available_height_per_side}

    def _get_left_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions: list[dict[str, int]] = []
        if self.direction == "horizontal":
            layout = self._calculate_arrow_layout()
            center_x = self.width // 2
            left_edge = center_x - layout["center_gap"] // 2
            for i in range(arrows_per_side):
                cx = left_edge - (layout["arrow_width"] // 2) + (self.stroke_width // 2) - i * layout["arrow_width"]
                positions.append({"x": int(cx), "y": self.height // 2})
        return positions

    def _get_right_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions: list[dict[str, int]] = []
        if self.direction == "horizontal":
            layout = self._calculate_arrow_layout()
            center_x = self.width // 2
            right_edge = center_x + layout["center_gap"] // 2
            for i in range(arrows_per_side):
                cx = right_edge + (layout["arrow_width"] // 2) - (self.stroke_width // 2) + i * layout["arrow_width"]
                positions.append({"x": int(cx), "y": self.height // 2})
        return positions

    def _get_top_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions: list[dict[str, int]] = []
        if self.direction == "vertical":
            layout = self._calculate_arrow_layout()
            center_y = self.height // 2
            top_edge = center_y - layout["center_gap"] // 2
            for i in range(arrows_per_side):
                cy = top_edge - (layout["arrow_height"] // 2) + (self.stroke_width // 2) - i * layout["arrow_height"]
                positions.append({"x": self.width // 2, "y": int(cy)})
        return positions

    def _get_bottom_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions: list[dict[str, int]] = []
        if self.direction == "vertical":
            layout = self._calculate_arrow_layout()
            center_y = self.height // 2
            bottom_edge = center_y + layout["center_gap"] // 2
            for i in range(arrows_per_side):
                cy = bottom_edge + (layout["arrow_height"] // 2) - (self.stroke_width // 2) + i * layout["arrow_height"]
                positions.append({"x": self.width // 2, "y": int(cy)})
        return positions

    def _get_clip_bounds(self) -> dict[str, int]:
        return {"x": 0, "y": 0, "width": self.width, "height": self.height}

    def _get_left_arrow_points(self) -> str:
        layout = self._calculate_arrow_layout()
        ox = layout["arrow_width"] // 2
        oy = layout["arrow_height"] // 2
        return f"{ox},{-oy} {-ox},0 {ox},{oy}"

    def _get_right_arrow_points(self) -> str:
        layout = self._calculate_arrow_layout()
        ox = layout["arrow_width"] // 2
        oy = layout["arrow_height"] // 2
        return f"{-ox},{-oy} {ox},0 {-ox},{oy}"

    def _get_up_arrow_points(self) -> str:
        layout = self._calculate_arrow_layout()
        ox = layout["arrow_width"] // 2
        oy = layout["arrow_height"] // 2
        return f"{-ox},{oy} 0,{-oy} {ox},{oy}"

    def _get_down_arrow_points(self) -> str:
        layout = self._calculate_arrow_layout()
        ox = layout["arrow_width"] // 2
        oy = layout["arrow_height"] // 2
        return f"{-ox},{-oy} 0,{oy} {ox},{-oy}"

    def _get_transform_distance(self) -> float:
        return float(self.height if self.direction == "vertical" else self.width)

    def _get_unique_id_keys(self) -> list[str]:
        return ["arrowClip", "maskGradSpreadA", "maskGradSpreadB", "sweepMaskA", "sweepMaskB"]


if __name__ == "__main__":
    generator = SpotlightSpreadArrowGenerator()

    print("Generated default spotlight spread arrow:")
    print(generator.generate_svg())
    generator.save_to_file("_tmp/spotlight_spread_arrow_default.svg")

    configurations = [
        {"num_arrows": 4, "direction": "vertical", "color": "#ef4444", "width": 100, "height": 150,
         "speed_in_px_per_second": 3.0, "spotlight_size": 0.3, "dim_opacity": 0.1},
        {"num_arrows": 6, "direction": "horizontal", "color": "#3b82f6", "width": 200, "height": 80,
         "speed_in_px_per_second": 2.0, "spotlight_size": 0.4},
        {"num_arrows": 6, "direction": "vertical", "color": "#f59e0b", "width": 100, "height": 200,
         "speed_in_px_per_second": 5.0, "spotlight_size": 0.35, "dim_opacity": 0.15},
        {"num_arrows": 8, "direction": "horizontal", "color": "#10b981", "width": 180, "height": 60,
         "speed_in_px_per_second": 4.0, "spotlight_size": 0.25, "center_gap_ratio": 0.3},
    ]

    for config in configurations:
        gen = SpotlightSpreadArrowGenerator(**config)
        file = f"_tmp/spotlight_spread_arrow_{config['direction']}_{config['num_arrows']}.svg"
        gen.save_to_file(file)
        print(f"Created {file} with {config}")
