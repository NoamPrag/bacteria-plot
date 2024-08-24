import math
from typing import Dict, List, Tuple

from manim import *
from config import Config

_X_RANGE_ADDITION = 2
_Y_RANGE_ADDITION = 0.2

class DataPointsScene(Scene):
    def __init__(
        self,
        data_points: List[Dict[str, float]],
        config: Config,
    ):
        super().__init__()
        self._data_points = data_points

        first_row = data_points[0]

        # by default: most left column is x-axis
        self.config = config
        self._x_data_set_label = list(self._data_points[0].keys())[0]
        self._y_values_labels = {key for key in first_row if key != self._x_data_set_label}

    @property
    def _max_value(self):
        max_value = -math.inf
        for row in self._data_points:
            for key, value in row.items():
                if key == self._x_data_set_label:
                    continue

                max_value = max(max_value, value)
        return max_value

    @property
    def _x_range(self) -> Tuple[float, float, float]:
        x_data_points = [
            data_point[self._x_data_set_label] for data_point in self._data_points
        ]
        min_value, max_value = x_data_points[0], x_data_points[-1]
        return min_value, max_value + _X_RANGE_ADDITION, self.config.axes.x.interval

    def _create_colors(self) -> Dict[str, ManimColor]:
        names_to_colors = {
            "RED": RED,
            "GREEN": GREEN,
            "BLUE": BLUE,
            "PURPLE": PURPLE,
            "WHITE": WHITE,
            "YELLOW": YELLOW,
            "ORANGE": ORANGE,
            "PINK": PINK,
            "TEAL": TEAL,
        }
        get_color = lambda color_name: names_to_colors[color_name] if color_name in names_to_colors else ManimColor(color_name)
        return {label: get_color(color_name) for label, color_name in self.config.data_sets.items()}

    def _plot_row(
        self,
        x_value: float,
        y_values: Dict[str, float],
        ax: Axes,
        colors: Dict[str, ManimColor],
        duration_secs: float,
    ):
        dots = []
        for value_label, y_value in y_values.items():
            coords = ax.coords_to_point(x_value, y_value)

            # TODO: configurable point radius?

            dot = Dot(coords, color=colors[value_label])
            dots.append(dot)

        self.play(*[GrowFromCenter(dot) for dot in dots], run_time=duration_secs)

    def _plot_data_points(
        self,
        ax: Axes,
        colors: Dict[str, ManimColor],
        row_interval_secs: float,
    ):
        for row in self._data_points:
            x_value = row[self._x_data_set_label]
            y_values = {
                key: value for key, value in row.items() if key != self._x_data_set_label
            }
            self._plot_row(x_value, y_values, ax, colors, row_interval_secs)

    def _create_data_labels(self, colors: Dict[str, ManimColor], font_size: int):
        label_group = VGroup()
        index = 0
        text_gap = self.config.labels.gap
        for data_label, color in self.config.data_sets.items():
            label_text = Text(data_label, color=color, font_size=font_size)
            label_text.shift(text_gap * DOWN * index)
            label_group.add(label_text)
            index += 1
        return label_group

    def construct(self):
        y_conf = self.config.axes.y
        ax = Axes(
            x_range=list(self._x_range),
            y_range=[y_conf.range_min, y_conf.range_max + _Y_RANGE_ADDITION, y_conf.interval],
            axis_config={"include_numbers": True},
        )
        # Transform axes to place and size
        ax.scale(0.9)
        ax.shift(LEFT * 0.9)
        ax.shift(DOWN * 0.6)

        AXIS_LABEL_SCALE = 0.7
        axis_labels = ax.get_axis_labels(
            Tex(self.config.axes.x.label).scale(AXIS_LABEL_SCALE),
            Tex(self.config.axes.y.label or "").scale(AXIS_LABEL_SCALE),
        )
        self.add(ax, axis_labels)

        point_interval_secs = self.config.video.duration_seconds / len(self._data_points)

        colors = self._create_colors()
        
        data_labels = self._create_data_labels(colors, font_size=self.config.labels.font_size)
        # Transform data labels to place
        data_labels.shift(RIGHT * 6)
        data_labels.shift(UP * 2)
        self.add(data_labels)
        
        self._plot_data_points(ax, colors, point_interval_secs)

