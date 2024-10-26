import datetime
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from plotly import graph_objs as go

from evidently.base_metric import Metric
from evidently.metric_results import Distribution
from evidently.metric_results import HistogramData
from evidently.model.widget import BaseWidgetInfo
from evidently.pydantic_utils import autoregister
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.ui.dashboards.base import DashboardPanel
from evidently.ui.dashboards.base import PanelValue
from evidently.ui.dashboards.base import assign_panel_id
from evidently.ui.dashboards.utils import CounterAgg
from evidently.ui.dashboards.utils import HistBarMode
from evidently.ui.dashboards.utils import PlotType
from evidently.ui.dashboards.utils import _get_hover_params
from evidently.ui.dashboards.utils import _get_metric_hover
from evidently.ui.type_aliases import ProjectID

if TYPE_CHECKING:
    from evidently.ui.base import DataStorage


@autoregister
class DashboardPanelPlot(DashboardPanel):
    class Config:
        type_alias = "evidently:dashboard_panel:DashboardPanelPlot"

    values: List[PanelValue]
    plot_type: PlotType

    @assign_panel_id
    async def build(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ):
        points = await data_storage.load_points(project_id, self.filter, self.values, timestamp_start, timestamp_end)
        # list[dict[metric, point]]
        all_metrics: Set[Metric] = set(m for data in points for m in data.keys())
        hover_params = _get_hover_params(all_metrics)
        fig = go.Figure(layout={"showlegend": True})
        for val, metric_pts in zip(self.values, points):
            if len(metric_pts) == 0:
                # no matching metrics, show error?
                continue

            for metric, pts in metric_pts.items():
                pts.sort(key=lambda x: x[0])

                hover = _get_metric_hover(hover_params[metric], val)

                if self.plot_type == PlotType.HISTOGRAM:
                    plot = go.Histogram(
                        x=[p[1] for p in pts],
                        name=val.legend,
                        legendgroup=val.legend,
                        hovertemplate=hover,
                    )
                else:
                    cls, args = self.plot_type_cls
                    plot = cls(
                        x=[p[0] for p in pts],
                        y=[p[1] for p in pts],
                        name=val.legend,
                        legendgroup=val.legend,
                        hovertemplate=hover,
                        **args,
                    )
                fig.add_trace(plot)
        return plotly_figure(title=self.title, figure=fig, size=self.size)

    @property
    def plot_type_cls(self):
        if self.plot_type == PlotType.SCATTER:
            return go.Scatter, {"mode": "markers"}
        if self.plot_type == PlotType.BAR:
            return go.Bar, {}
        if self.plot_type == PlotType.LINE:
            return go.Scatter, {}
        raise ValueError(f"Unsupported plot type {self.plot_type}")


@autoregister
class DashboardPanelCounter(DashboardPanel):
    class Config:
        type_alias = "evidently:dashboard_panel:DashboardPanelCounter"

    agg: CounterAgg
    value: Optional[PanelValue] = None
    text: Optional[str] = None

    @assign_panel_id
    async def build(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ):
        if self.agg == CounterAgg.NONE:
            return counter(counters=[CounterData(self.title, self.text or "")], size=self.size)
        if self.value is None:
            raise ValueError("Counters with agg should have value")
        points = (
            await data_storage.load_points(project_id, self.filter, [self.value], timestamp_start, timestamp_end)
        )[0]
        value = self._get_counter_value(points)
        if int(value) != value:
            ct = CounterData.float(self.text or "", value, 3)
        else:
            ct = CounterData.int(self.text or "", int(value))
        return counter(title=self.title, counters=[ct], size=self.size)

    def _get_counter_value(self, points: Dict[Metric, List[Tuple[datetime.datetime, Any]]]) -> float:
        if self.value is None:
            raise ValueError("Counters with agg should have value")
        if self.agg == CounterAgg.LAST:
            if len(points) == 0:
                return 0
            return max(
                ((ts, v) for vs in points.values() for ts, v in vs),
                key=lambda x: x[0],
            )[1]
        if self.agg == CounterAgg.SUM:
            return sum(v or 0 for vs in points.values() for ts, v in vs)
        raise ValueError(f"Unknown agg type {self.agg}")


@autoregister
class DashboardPanelDistribution(DashboardPanel):
    class Config:
        type_alias = "evidently:dashboard_panel:DashboardPanelDistribution"

    value: PanelValue
    barmode: HistBarMode = HistBarMode.STACK

    @assign_panel_id
    async def build(
        self,
        data_storage: "DataStorage",
        project_id: ProjectID,
        timestamp_start: Optional[datetime.datetime],
        timestamp_end: Optional[datetime.datetime],
    ) -> BaseWidgetInfo:
        bins_for_hists: Dict[Metric, List[Tuple[datetime.datetime, Union[HistogramData, Distribution]]]] = (  # type: ignore[assignment]
            await data_storage.load_points_as_type(
                Union[HistogramData, Distribution],  # type: ignore[arg-type]
                project_id,
                self.filter,
                [self.value],
                timestamp_start,
                timestamp_end,
            )
        )[0]
        if len(bins_for_hists) == 0:
            raise ValueError(f"Cannot build hist from {self.value}")
        if len(bins_for_hists) > 1:
            raise ValueError(f"Ambiguious metrics for {self.value}")
        bins_for_hist: List[Tuple[datetime.datetime, HistogramData]] = next(
            [(d, h if isinstance(h, HistogramData) else HistogramData.from_distribution(h)) for d, h in v]
            for v in bins_for_hists.values()
        )

        timestamps: List[datetime.datetime] = []
        names: Set[str] = set()
        values: List[Dict[str, Any]] = []

        for timestamp, hist in bins_for_hist:
            timestamps.append(timestamp)
            data = dict(zip(hist.x, hist.count))
            names.update(data.keys())
            values.append(data)

        names_sorted = list(sorted(names))
        name_to_date_value: Dict[str, List[Any]] = {name: [] for name in names_sorted}
        for timestamp, data in zip(timestamps, values):
            for name in names_sorted:
                name_to_date_value[name].append(data.get(name))
        hovertemplate = "<b>{name}: %{{y}}</b><br><b>Timestamp: %{{x}}</b>"
        fig = go.Figure(
            data=[
                go.Bar(
                    name=name,
                    x=timestamps,
                    y=name_to_date_value.get(name),
                    hovertemplate=hovertemplate.format(name=name),
                )
                for name in names_sorted
            ]
        )
        # Change the bar mode
        fig.update_layout(barmode=self.barmode.value)

        return plotly_figure(title=self.title, figure=fig, size=self.size)
