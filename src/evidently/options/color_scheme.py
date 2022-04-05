from dataclasses import dataclass

RED = "#ed0400"
GREY = "#4d4d4d"
COLOR_DISCRETE_SEQUENCE = ["#ed0400", "#0a5f38", "#6c3461", "#71aa34", "#d8dcd6", "#6b8ba4"]


@dataclass
class ColorOptions:
    """Collection of colors for data visualization"""

    current_data_color = RED
    reference_data_color = GREY
    color_sequence = COLOR_DISCRETE_SEQUENCE
    fill_color = "LightGreen"
    zero_line_color = "green"
    non_visible_color = "white"
    underestimation_color = "#6574f7"
    overestimation_color = "#ee5540"
    majority_color = "#1acc98"
