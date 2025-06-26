from captain_arro.generators.base import AnimatedArrowGeneratorBase
from captain_arro.constants import SPREAD_DIRECTIONS


class SpotlightSpreadArrowGenerator(AnimatedArrowGeneratorBase):
    def __init__(
            self,
            color: str = "#2563eb",
            stroke_width: int = 10,
            width: int = 100,
            height: int = 100,
            speed: float = 20.0,
            direction: SPREAD_DIRECTIONS = "horizontal",
            num_arrows: int = 4,
            spotlight_size: float = 0.3,
            dim_opacity: float = 0.2,
            center_gap_ratio: float = 0.2,
    ):
        super().__init__(
            color=color,
            stroke_width=stroke_width,
            width=width,
            height=height,
            speed=speed,
            num_arrows=max(2, num_arrows)
        )
        self.direction = direction.lower()
        self.spotlight_size = max(0.1, min(1.0, spotlight_size))
        self.dim_opacity = max(0.0, min(1.0, dim_opacity))
        self.center_gap_ratio = max(0.1, min(0.4, center_gap_ratio))

    def generate_svg(self) -> str:
        """Override to customize arrow styles with directional gradients."""
        clip_bounds = self._get_clip_bounds()
        animations = self._generate_animations()
        arrow_elements = self._generate_arrow_elements()
        gradient_defs = self._generate_gradient_defs()

        return f"""
        <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <clipPath id="arrowClip">
              <rect x="{clip_bounds['x']}" y="{clip_bounds['y']}" width="{clip_bounds['width']}" height="{clip_bounds['height']}"/>
            </clipPath>
            {gradient_defs}
          </defs>

          <style>
            .arrow-left {{
              stroke: url(#spotlightGradientLeft);
              stroke-width: {self.stroke_width};
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }}

            .arrow-right {{
              stroke: url(#spotlightGradientRight);
              stroke-width: {self.stroke_width};
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }}

            .arrow-top {{
              stroke: url(#spotlightGradientTop);
              stroke-width: {self.stroke_width};
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }}

            .arrow-bottom {{
              stroke: url(#spotlightGradientBottom);
              stroke-width: {self.stroke_width};
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }}
            
            {animations}
          </style>

          <g clip-path="url(#arrowClip)">
            {arrow_elements}
          </g>
        </svg>
        """

    def _generate_gradient_defs(self) -> str:
        duration = self._calculate_animation_duration()
        spotlight_percent = self.spotlight_size * 100
        dim_before = (100 - spotlight_percent) / 2
        dim_after = dim_before + spotlight_percent

        if self.direction == "horizontal":
            center_x = self.width // 2
            left_gradient = f"""
        <linearGradient id="spotlightGradientLeft" x1="0" y1="0" x2="{self.width}" y2="0" gradientUnits="userSpaceOnUse">
          <animateTransform
            attributeName="gradientTransform"
            type="translate"
            values="{center_x} 0; -{self.width} 0"
            dur="{duration:.2f}s"
            repeatCount="indefinite"/>
          <stop offset="0%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="{dim_before:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="50%" stop-color="{self.color}" stop-opacity="1"/>
          <stop offset="{dim_after:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="100%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
        </linearGradient>"""

            right_gradient = f"""
        <linearGradient id="spotlightGradientRight" x1="-{self.width}" y1="0" x2="0" y2="0" gradientUnits="userSpaceOnUse">
          <animateTransform
            attributeName="gradientTransform"
            type="translate"
            values="-{center_x} 0; {self.width} 0"
            dur="{duration:.2f}s"
            repeatCount="indefinite"/>
          <stop offset="0%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="{dim_before:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="50%" stop-color="{self.color}" stop-opacity="1"/>
          <stop offset="{dim_after:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="100%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
        </linearGradient>"""

            return left_gradient + "\n" + right_gradient

        else:
            center_y = self.height // 2
            top_gradient = f"""
        <linearGradient id="spotlightGradientTop" x1="0" y1="0" x2="0" y2="{self.height}" gradientUnits="userSpaceOnUse">
          <animateTransform
            attributeName="gradientTransform"
            type="translate"
            values="0 {center_y}; 0 -{self.height}"
            dur="{duration:.2f}s"
            repeatCount="indefinite"/>
          <stop offset="0%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="{dim_before:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="50%" stop-color="{self.color}" stop-opacity="1"/>
          <stop offset="{dim_after:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="100%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
        </linearGradient>"""

            bottom_gradient = f"""
        <linearGradient id="spotlightGradientBottom" x1="0" y1="-{self.height}" x2="0" y2="0" gradientUnits="userSpaceOnUse">
          <animateTransform
            attributeName="gradientTransform"
            type="translate"
            values="0 -{center_y}; 0 {self.height}"
            dur="{duration:.2f}s"
            repeatCount="indefinite"/>
          <stop offset="0%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="{dim_before:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="50%" stop-color="{self.color}" stop-opacity="1"/>
          <stop offset="{dim_after:.1f}%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
          <stop offset="100%" stop-color="{self.color}" stop-opacity="{self.dim_opacity}"/>
        </linearGradient>"""

            return top_gradient + "\n" + bottom_gradient

    def _generate_arrow_elements(self) -> str:
        elements = []

        if self.direction == "horizontal":
            left_positions = self._get_left_arrow_positions()
            right_positions = self._get_right_arrow_positions()

            for pos in left_positions:
                arrow_points = self._get_left_arrow_points()
                elements.append(
                    f'    <g class="arrow-left" style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n      <polyline points="{arrow_points}"/>\n    </g>')

            for pos in right_positions:
                arrow_points = self._get_right_arrow_points()
                elements.append(
                    f'    <g class="arrow-right" style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n      <polyline points="{arrow_points}"/>\n    </g>')

        else:
            top_positions = self._get_top_arrow_positions()
            bottom_positions = self._get_bottom_arrow_positions()

            for pos in top_positions:
                arrow_points = self._get_up_arrow_points()
                elements.append(
                    f'    <g class="arrow-top" style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n      <polyline points="{arrow_points}"/>\n    </g>')

            for pos in bottom_positions:
                arrow_points = self._get_down_arrow_points()
                elements.append(
                    f'    <g class="arrow-bottom" style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n      <polyline points="{arrow_points}"/>\n    </g>')

        return "\n    \n".join(elements)

    def _get_left_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions = []

        available_width = self.width - 2 * (self.width // 8)
        center_gap = available_width * self.center_gap_ratio
        side_width = (available_width - center_gap) // 2

        spacing = side_width // (arrows_per_side + 1) if arrows_per_side > 1 else side_width // 2
        start_x = self.width // 8

        for i in range(arrows_per_side):
            x = start_x + (i + 1) * spacing
            positions.append({"x": x, "y": self.height // 2})

        return positions

    def _get_right_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions = []

        available_width = self.width - 2 * (self.width // 8)
        center_gap = available_width * self.center_gap_ratio
        side_width = (available_width - center_gap) // 2

        spacing = side_width // (arrows_per_side + 1) if arrows_per_side > 1 else side_width // 2
        start_x = self.width // 2 + (available_width * self.center_gap_ratio) // 2

        for i in range(arrows_per_side):
            x = start_x + (i + 1) * spacing
            positions.append({"x": x, "y": self.height // 2})

        return positions

    def _get_top_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions = []

        available_height = self.height - 2 * (self.height // 8)
        center_gap = available_height * self.center_gap_ratio
        side_height = (available_height - center_gap) // 2

        spacing = side_height // (arrows_per_side + 1) if arrows_per_side > 1 else side_height // 2
        start_y = self.height // 8

        for i in range(arrows_per_side):
            y = start_y + (i + 1) * spacing
            positions.append({"x": self.width // 2, "y": y})

        return positions

    def _get_bottom_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions = []

        available_height = self.height - 2 * (self.height // 8)
        center_gap = available_height * self.center_gap_ratio
        side_height = (available_height - center_gap) // 2

        spacing = side_height // (arrows_per_side + 1) if arrows_per_side > 1 else side_height // 2
        start_y = self.height // 2 + (available_height * self.center_gap_ratio) // 2

        for i in range(arrows_per_side):
            y = start_y + (i + 1) * spacing
            positions.append({"x": self.width // 2, "y": y})

        return positions

    def _get_clip_bounds(self) -> dict[str, int]:
        if self.direction == "vertical":
            margin_y = self.height // 10
            return {
                "x": 0,
                "y": margin_y,
                "width": self.width,
                "height": self.height - 2 * margin_y
            }
        else:
            margin_x = self.width // 10
            return {
                "x": margin_x,
                "y": 0,
                "width": self.width - 2 * margin_x,
                "height": self.height
            }

    def _get_left_arrow_points(self) -> str:
        offset_x = self.width // 20
        offset_y = self.height // 20
        return f"{offset_x},{-offset_y} {-offset_x},0 {offset_x},{offset_y}"

    def _get_right_arrow_points(self) -> str:
        offset_x = self.width // 20
        offset_y = self.height // 20
        return f"{-offset_x},{-offset_y} {offset_x},0 {-offset_x},{offset_y}"

    def _get_up_arrow_points(self) -> str:
        offset_x = self.width // 20
        offset_y = self.height // 20
        return f"{-offset_x},{offset_y} 0,{-offset_y} {offset_x},{offset_y}"

    def _get_down_arrow_points(self) -> str:
        offset_x = self.width // 20
        offset_y = self.height // 20
        return f"{-offset_x},{-offset_y} 0,{offset_y} {offset_x},{-offset_y}"

    def _calculate_animation_duration(self) -> float:
        if self.direction == "vertical":
            total_distance = self.height
        else:
            total_distance = self.width
        return total_distance / self.speed


if __name__ == "__main__":
    generator = SpotlightSpreadArrowGenerator()

    print("Generated default spotlight spread arrow:")
    print(generator.generate_svg())
    generator.save_to_file("_tmp/spotlight_spread_arrow_default.svg")

    configurations = [
        {"direction": "horizontal", "color": "#3b82f6", "num_arrows": 6, "width": 200, "height": 80,
         "speed": 80.0, "spotlight_size": 0.4},
        {"direction": "vertical", "color": "#ef4444", "num_arrows": 4, "width": 100, "height": 150,
         "speed": 60.0, "spotlight_size": 0.3, "dim_opacity": 0.1},
        {"direction": "horizontal", "color": "#10b981", "num_arrows": 8, "width": 180, "height": 60,
         "speed": 100.0, "spotlight_size": 0.25, "center_gap_ratio": 0.3},
        {"direction": "vertical", "color": "#f59e0b", "num_arrows": 6, "width": 100, "height": 200,
         "speed": 90.0, "spotlight_size": 0.35, "dim_opacity": 0.15}
    ]

    for config in configurations:
        gen = SpotlightSpreadArrowGenerator(**config)
        file = f"_tmp/spotlight_spread_arrow_{config['direction']}_{config['num_arrows']}.svg"
        gen.save_to_file(file)
        print(f"Created {file} with {config}")
