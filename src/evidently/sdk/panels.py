from typing import List
from typing import Optional

from evidently.sdk.models import DashboardPanelPlot
from evidently.sdk.models import PanelMetric


def text_panel(
    title: str,
    description: Optional[str] = None,
    size: str = "full",
) -> DashboardPanelPlot:
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
    aggregation: str = "last",
) -> DashboardPanelPlot:
    return DashboardPanelPlot(
        title=title,
        subtitle=description,
        size=size,
        values=values,
        plot_params={
            "plot_type": "line",
        },
    )
