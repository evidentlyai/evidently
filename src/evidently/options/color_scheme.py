from dataclasses import dataclass

RED = "#ed0400"
GREY = "#4d4d4d"
COLOR_DISCRETE_SEQUENCE = ["#ed0400", "#0a5f38", "#6c3461", "#71aa34", "#d8dcd6", "#6b8ba4"]


@dataclass
class ColorOptions:
    """Collection of colors for data visualization

    - primary_color - basic color for data visualization.
        Uses by default for all bars and lines for widgets with one dataset and as a default for current data.
    - secondary_color - basic color for second data visualization if we have two data sets, for example, reference data.
    - current_data_color - color for all current data, by default primary color is used
    - reference_data_color - color for reference data, by default secondary color is used
    - color_sequence - set of colors for drawing a number of lines in one graph, in for data quality, for example
    - fill_color - fill color for areas in line graphs
    - zero_line_color - color for base, zero line in line graphs
    - non_visible_color - color for technical, not visible dots or points for better scalability
    - underestimation_color - color for underestimation line in regression
    - overestimation_color - color for overestimation line in regression
    - majority_color - color for majority line in regression
    """
    primary_color = RED
    secondary_color = GREY
    current_data_color = None
    reference_data_color = None
    color_sequence = COLOR_DISCRETE_SEQUENCE
    fill_color = "LightGreen"
    zero_line_color = "green"
    non_visible_color = "white"
    underestimation_color = "#6574f7"
    overestimation_color = "#ee5540"
    majority_color = "#1acc98"

    def get_current_data_color(self):
        return self.current_data_color or self.primary_color

    def get_reference_data_color(self):
        return self.reference_data_color or self.secondary_color
