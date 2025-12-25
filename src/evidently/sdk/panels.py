from typing import List
from typing import Optional

from evidently.sdk.models import DashboardPanelPlot
from evidently.sdk.models import PanelMetric


def text_panel(
    title: str,
    description: Optional[str] = None,
    size: str = "full",
) -> DashboardPanelPlot:
    """Create a text panel for displaying text content.

    Args:
    * `title`: Panel title.
    * `description`: Optional panel description/subtitle.
    * `size`: Panel size (e.g., `"full"`, `"half"`).

    Returns:
    * `DashboardPanelPlot` configured as a text panel.
    """
    return DashboardPanelPlot(
        title=title,
        subtitle=description,
        size=size,
        values=[],
        plot_params={
            "plot_type": "text",
        },
    )


def counter_panel(
    title: str,
    values: List[PanelMetric],
    description: Optional[str] = None,
    size: str = "full",
    aggregation: str = "last",
) -> DashboardPanelPlot:
    """Create a counter panel for displaying metric values as counters.

    Args:
    * `title`: Panel title.
    * `values`: List of `PanelMetric` objects to display.
    * `description`: Optional panel description/subtitle.
    * `size`: Panel size (e.g., `"full"`, `"half"`).
    * `aggregation`: Aggregation method for time series data (e.g., `"last"`, `"sum"`, `"mean"`).

    Returns:
    * `DashboardPanelPlot` configured as a counter panel.
    """
    return DashboardPanelPlot(
        title=title,
        subtitle=description,
        size=size,
        values=values,
        plot_params={
            "plot_type": "counter",
            "aggregation": aggregation,
        },
    )


def line_plot_panel(
    title: str,
    values: List[PanelMetric],
    description: Optional[str] = None,
    size: str = "full",
) -> DashboardPanelPlot:
    """Create a line plot panel for displaying metrics over time.

    Args:
    * `title`: Panel title.
    * `values`: List of `PanelMetric` objects to display.
    * `description`: Optional panel description/subtitle.
    * `size`: Panel size (e.g., `"full"`, `"half"`).

    Returns:
    * `DashboardPanelPlot` configured as a line plot panel.
    """
    return DashboardPanelPlot(
        title=title,
        subtitle=description,
        size=size,
        values=values,
        plot_params={
            "plot_type": "line",
        },
    )


def bar_plot_panel(
    title: str,
    values: List[PanelMetric],
    description: Optional[str] = None,
    size: str = "full",
    stacked: bool = False,
) -> DashboardPanelPlot:
    """Create a bar plot panel for displaying metrics as bars.

    Args:
    * `title`: Panel title.
    * `values`: List of `PanelMetric` objects to display.
    * `description`: Optional panel description/subtitle.
    * `size`: Panel size (e.g., `"full"`, `"half"`).
    * `stacked`: Whether to stack bars on top of each other.

    Returns:
    * `DashboardPanelPlot` configured as a bar plot panel.
    """
    return DashboardPanelPlot(
        title=title,
        subtitle=description,
        size=size,
        values=values,
        plot_params={
            "plot_type": "bar",
            "is_stacked": stacked,
        },
    )


def pie_plot_panel(
    title: str,
    values: List[PanelMetric],
    description: Optional[str] = None,
    size: str = "full",
    aggregation: str = "last",
) -> DashboardPanelPlot:
    """Create a pie chart panel for displaying metrics as a pie chart.

    Args:
    * `title`: Panel title.
    * `values`: List of `PanelMetric` objects to display.
    * `description`: Optional panel description/subtitle.
    * `size`: Panel size (e.g., `"full"`, `"half"`).
    * `aggregation`: Aggregation method for time series data (e.g., `"last"`, `"sum"`, `"mean"`).

    Returns:
    * `DashboardPanelPlot` configured as a pie chart panel.
    """
    return DashboardPanelPlot(
        title=title,
        subtitle=description,
        size=size,
        values=values,
        plot_params={
            "plot_type": "pie",
            "aggregation": aggregation,
        },
    )
