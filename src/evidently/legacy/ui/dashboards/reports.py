import datetime
from collections import defaultdict
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Set
from typing import Tuple
from typing import Union

from plotly import graph_objs as go

from evidently.legacy.base_metric import Metric
from evidently.legacy.metric_results import Distribution
from evidently.legacy.metric_results import HistogramData
from evidently.legacy.metric_results import Label
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import plotly_figure
from evidently.legacy.ui.dashboards.base import DashboardPanel
from evidently.legacy.ui.dashboards.base import PanelValue
from evidently.legacy.ui.dashboards.base import assign_panel_id
from evidently.legacy.ui.dashboards.utils import CounterAgg
from evidently.legacy.ui.dashboards.utils import HistBarMode
from evidently.legacy.ui.dashboards.utils import PlotType
from evidently.legacy.ui.dashboards.utils import _get_hover_params
from evidently.legacy.ui.dashboards.utils import _get_metric_hover
from evidently.legacy.ui.type_aliases import DataPointsAsType
from evidently.legacy.ui.type_aliases import PointInfo
from evidently.legacy.ui.type_aliases import ProjectID
from evidently.legacy.ui.type_aliases import SnapshotID
from evidently.pydantic_utils import autoregister
from evidently.pydantic_utils import register_type_alias

if TYPE_CHECKING:
    from evidently.legacy.ui.base import DataStorage


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
                pts.sort(key=lambda x: x.timestamp)
                hover = _get_metric_hover(hover_params[metric], val)
                hover_args = {
                    "name": val.legend,
                    "legendgroup": val.legend,
                    "hovertemplate": hover,
                    "customdata": [
                        {"metric_fingerprint": metric.get_fingerprint(), "snapshot_id": str(p.snapshot_id)} for p in pts
                    ],
                }

                if self.plot_type == PlotType.HISTOGRAM:
                    plot = go.Histogram(x=[p.value for p in pts], **hover_args)
                else:
                    cls, args = self.plot_type_cls
                    plot = cls(
                        x=[p.timestamp for p in pts],
                        y=[p.value for p in pts],
                        **hover_args,
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

    def _get_counter_value(self, points: Dict[Metric, List[PointInfo]]) -> float:
        if self.value is None:
            raise ValueError("Counters with agg should have value")
        if self.agg == CounterAgg.LAST:
            if len(points) == 0:
                return 0
            return max(
                ((pi.timestamp, pi.value) for vs in points.values() for pi in vs),
                key=lambda x: x[0],
            )[1]
        if self.agg == CounterAgg.SUM:
            return sum(pi.value or 0 for vs in points.values() for pi in vs)
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
        bins_for_hists_data: DataPointsAsType[
            Union[HistogramData, Distribution, dict]
        ] = await data_storage.load_points_as_type(
            Union[HistogramData, Distribution, dict],  # type: ignore[arg-type]
            project_id,
            self.filter,
            [self.value],
            timestamp_start,
            timestamp_end,
        )
        bins_for_hists = bins_for_hists_data[0]  # dict metric -> list of point infos
        if len(bins_for_hists) == 0:
            raise ValueError(f"Cannot build hist from {self.value}")
        if len(bins_for_hists) > 1:
            raise ValueError(f"Ambiguious metrics for {self.value}")
        metric = next(iter(bins_for_hists.keys()))
        fingerprint = metric.get_fingerprint()
        bins_for_hist: List[Tuple[datetime.datetime, SnapshotID, HistogramData]] = next(
            [
                (
                    d.timestamp,
                    d.snapshot_id,
                    HistogramData.from_any(d.value),
                )
                for d in v
            ]
            for v in bins_for_hists.values()
        )

        timestamps: List[datetime.datetime] = []
        names: Set[Label] = set()
        values: List[Dict[Label, Any]] = []
        snapshot_ids = []

        for timestamp, snapshot_id, hist in bins_for_hist:
            timestamps.append(timestamp)
            data = dict(zip(hist.x, hist.count))
            values.append(data)
            names.update(data.keys())
            snapshot_ids.append(snapshot_id)

        names_sorted = list(sorted([x for x in names if x is not None])) + ([None] if None in names else [])
        name_to_date_value: Dict[Label, List[Any]] = defaultdict(list)
        name_to_snapshot_id: Dict[Label, List[SnapshotID]] = defaultdict(list)
        for timestamp, snapshot_id, data in zip(timestamps, snapshot_ids, values):
            for name in names_sorted:
                name_to_date_value[name].append(data.get(name))
                name_to_snapshot_id[name].append(snapshot_id)

        hovertemplate = "<b>{name}: %{{y}}</b><br><b>Timestamp: %{{x}}</b>"
        fig = go.Figure(
            data=[
                go.Bar(
                    name=name,
                    x=timestamps,
                    y=name_to_date_value[name],
                    hovertemplate=hovertemplate.format(name=name),
                    customdata=[
                        {"metric_fingerprint": fingerprint, "snapshot_id": str(snapshot_id)}
                        for snapshot_id in name_to_snapshot_id[name]
                    ],
                )
                for name in names_sorted
            ]
        )
        # Change the bar mode
        fig.update_layout(barmode=self.barmode.value)

        return plotly_figure(title=self.title, figure=fig, size=self.size)


DashboardPanelHistogram = DashboardPanelDistribution
register_type_alias(
    DashboardPanel, DashboardPanelHistogram.__get_classpath__(), "evidently:dashboard_panel:DashboardPanelHistogram"
)
