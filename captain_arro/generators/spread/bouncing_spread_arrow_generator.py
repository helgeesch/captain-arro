from captain_arro.generators.base import AnimatedArrowGeneratorBase
from captain_arro.constants import ANIMATION_TYPES, SPREAD_DIRECTIONS


class BouncingSpreadArrowGenerator(AnimatedArrowGeneratorBase):
    def __init__(
            self,
            color: str = "#2563eb",
            stroke_width: int = 2,
            width: int = 300,
            height: int = 150,
            speed: float = 10.0,
            direction: SPREAD_DIRECTIONS = "vertical",
            num_arrows: int = 6,
            animation: ANIMATION_TYPES = "ease-in-out",
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
        self.animation = animation
        self.center_gap_ratio = max(0.1, min(0.4, center_gap_ratio))

    def generate_svg(self) -> str:
        """Override to customize the arrow groups and animations."""
        clip_bounds = self._get_clip_bounds()
        animations = self._generate_animations()
        arrow_elements = self._generate_arrow_elements()

        return f"""
        <svg width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <clipPath id="arrowClip">
              <rect x="{clip_bounds['x']}" y="{clip_bounds['y']}" width="{clip_bounds['width']}" height="{clip_bounds['height']}"/>
            </clipPath>
          </defs>

          <style>
            .arrow {{
              stroke: {self.color};
              stroke-width: {self.stroke_width};
              stroke-linecap: round;
              stroke-linejoin: round;
              fill: none;
            }}

            .group-left {{
              animation: moveLeft {self._calculate_animation_duration():.2f}s {self.animation} infinite alternate;
            }}

            .group-right {{
              animation: moveRight {self._calculate_animation_duration():.2f}s {self.animation} infinite alternate;
            }}

            .group-top {{
              animation: moveTop {self._calculate_animation_duration():.2f}s {self.animation} infinite alternate;
            }}

            .group-bottom {{
              animation: moveBottom {self._calculate_animation_duration():.2f}s {self.animation} infinite alternate;
            }}

            {animations}
          </style>

          <g clip-path="url(#arrowClip)">
        {arrow_elements}
          </g>
        </svg>
        """

    def _generate_arrow_elements(self) -> str:
        arrows_per_side = self.num_arrows // 2
        elements = []

        left_arrows = []
        right_arrows = []
        top_arrows = []
        bottom_arrows = []

        if self.direction == "horizontal":
            left_positions = self._get_left_arrow_positions()
            right_positions = self._get_right_arrow_positions()

            for i, pos in enumerate(left_positions):
                arrow_points = self._get_left_arrow_points()
                left_arrows.append(
                    f'      <g style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n        <polyline points="{arrow_points}"/>\n      </g>')

            for i, pos in enumerate(right_positions):
                arrow_points = self._get_right_arrow_points()
                right_arrows.append(
                    f'      <g style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n        <polyline points="{arrow_points}"/>\n      </g>')

            if left_arrows:
                elements.append(f'    <g class="arrow group-left">\n{chr(10).join(left_arrows)}\n    </g>')
            if right_arrows:
                elements.append(f'    <g class="arrow group-right">\n{chr(10).join(right_arrows)}\n    </g>')

        else:
            top_positions = self._get_top_arrow_positions()
            bottom_positions = self._get_bottom_arrow_positions()

            for i, pos in enumerate(top_positions):
                arrow_points = self._get_up_arrow_points()
                top_arrows.append(
                    f'      <g style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n        <polyline points="{arrow_points}"/>\n      </g>')

            for i, pos in enumerate(bottom_positions):
                arrow_points = self._get_down_arrow_points()
                bottom_arrows.append(
                    f'      <g style="transform: translate({pos["x"]}px, {pos["y"]}px)">\n        <polyline points="{arrow_points}"/>\n      </g>')

            if top_arrows:
                elements.append(f'    <g class="arrow group-top">\n{chr(10).join(top_arrows)}\n    </g>')
            if bottom_arrows:
                elements.append(f'    <g class="arrow group-bottom">\n{chr(10).join(bottom_arrows)}\n    </g>')

        return "\n    \n".join(elements)

    def _get_left_arrow_positions(self) -> list[dict[str, int]]:
        arrows_per_side = self.num_arrows // 2
        positions = []

        if self.direction == "horizontal":
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

        if self.direction == "horizontal":
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

        if self.direction == "vertical":
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

        if self.direction == "vertical":
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

    def _get_transform_distance(self) -> int:
        if self.direction == "vertical":
            available_space = self.height - 2 * (self.height // 8)
            return int(available_space * 0.15)
        else:
            available_space = self.width - 2 * (self.width // 8)
            return int(available_space * 0.15)

    def _calculate_animation_duration(self) -> float:
        transform_distance = self._get_transform_distance()
        return transform_distance / self.speed

    def _generate_animations(self) -> str:
        distance = self._get_transform_distance()

        if self.direction == "horizontal":
            return f"""
        @keyframes moveLeft {{
          0% {{ transform: translateX(0px); }}
          100% {{ transform: translateX({distance}px); }}
        }}

        @keyframes moveRight {{
          0% {{ transform: translateX(0px); }}
          100% {{ transform: translateX(-{distance}px); }}
        }}"""
        else:
            return f"""
        @keyframes moveTop {{
          0% {{ transform: translateY(0px); }}
          100% {{ transform: translateY({distance}px); }}
        }}

        @keyframes moveBottom {{
          0% {{ transform: translateY(0px); }}
          100% {{ transform: translateY(-{distance}px); }}
        }}"""


if __name__ == "__main__":
    generator = BouncingSpreadArrowGenerator()

    print("Generated default bouncing spread arrow:")
    print(generator.generate_svg())
    generator.save_to_file("_tmp/bouncing_spread_arrow_default.svg")

    configurations = [
        {"direction": "horizontal", "color": "#3b82f6", "num_arrows": 1, "width": 300, "height": 300,
         "animation": "ease-in-out"},
        {"direction": "vertical", "color": "#ef4444", "num_arrows": 4, "width": 80, "height": 150,
         "animation": "ease-in"},
        {"direction": "horizontal", "color": "#10b981", "num_arrows": 8, "stroke_width": 12, "width": 180, "height": 60,
         "center_gap_ratio": 0.3},
        {"direction": "vertical", "color": "#f59e0b", "num_arrows": 6, "stroke_width": 8, "speed": 25.0, "width": 100,
         "height": 200}
    ]

    for config in configurations:
        gen = BouncingSpreadArrowGenerator(**config)
        file = f"_tmp/bouncing_spread_arrow_{config['direction']}_{config['num_arrows']}.svg"
        gen.save_to_file(file)
        print(f"Created {file} with {config}")
