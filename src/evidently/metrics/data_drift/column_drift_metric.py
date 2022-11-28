from typing import Dict
from typing import List
from typing import Optional

import dataclasses

from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import GraphData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_graph_tabs
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.utils.data_operations import process_columns
from evidently.utils.types import Numeric
from evidently.utils.visualizations import Distribution
from evidently.utils.visualizations import plot_scatter_for_data_drift


@dataclasses.dataclass
class ColumnDriftMetricResults:
    column_name: str
    column_type: str
    stattest_name: str
    stattest_threshold: float
    drift_score: Numeric
    drift_detected: bool
    current_distribution: Distribution
    reference_distribution: Distribution
    current_scatter: Optional[Dict[str, list]]
    x_name: Optional[str]
    plot_shape: Optional[Dict[str, float]]


class ColumnDriftMetric(Metric[ColumnDriftMetricResults]):
    """Calculate drift metric for a column"""

    column_name: str
    stattest: Optional[PossibleStatTestType]
    stattest_threshold: Optional[float]

    def __init__(
        self,
        column_name: str,
        stattest: Optional[PossibleStatTestType] = None,
        stattest_threshold: Optional[float] = None,
    ):
        self.column_name = column_name
        self.stattest = stattest
        self.stattest_threshold = stattest_threshold

    def get_parameters(self) -> tuple:
        return self.column_name, self.stattest_threshold, self.stattest

    def calculate(self, data: InputData) -> ColumnDriftMetricResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        if self.column_name not in data.current_data:
            raise ValueError(f"Cannot find column '{self.column_name}' in current dataset")

        if self.column_name not in data.reference_data:
            raise ValueError(f"Cannot find column '{self.column_name}' in reference dataset")

        dataset_columns = process_columns(data.reference_data, data.column_mapping)
        options = DataDriftOptions(all_features_stattest=self.stattest, threshold=self.stattest_threshold)
        drift_result = get_one_column_drift(
            current_data=data.current_data,
            reference_data=data.reference_data,
            column_name=self.column_name,
            dataset_columns=dataset_columns,
            options=options,
        )

        return ColumnDriftMetricResults(
            column_name=drift_result.column_name,
            column_type=drift_result.column_type,
            stattest_name=drift_result.stattest_name,
            stattest_threshold=drift_result.threshold,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            current_distribution=drift_result.current_distribution,
            reference_distribution=drift_result.reference_distribution,
            current_scatter=drift_result.current_scatter,
            x_name=drift_result.x_name,
            plot_shape=drift_result.plot_shape,
        )


@default_renderer(wrap_type=ColumnDriftMetric)
class ColumnDriftMetricRenderer(MetricRenderer):
    def render_json(self, obj: ColumnDriftMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        # remove distribution data with pandas dataframes
        result.pop("current_distribution", None)
        result.pop("reference_distribution", None)
        result.pop("current_scatter", None)
        result.pop("x_name", None)
        result.pop("plot_shape", None)
        return result

    def render_html(self, obj: ColumnDriftMetric) -> List[BaseWidgetInfo]:
        result = obj.get_result()

        if result.drift_detected:
            drift = "detected"

        else:
            drift = "not detected"

        drift_score = round(result.drift_score, 3)

        figures = []

        # fig_json = fig.to_plotly_json()
        if result.current_scatter is not None and result.plot_shape is not None and result.x_name is not None:
            scatter_fig = plot_scatter_for_data_drift(
                curr_y=result.current_scatter[result.column_name],
                curr_x=result.current_scatter[result.x_name],
                y0=result.plot_shape["y0"],
                y1=result.plot_shape["y1"],
                y_name=result.column_name,
                x_name=result.x_name,
                color_options=self.color_options,
            )
            figures.append(GraphData.figure("DATA DRIFT", scatter_fig))

        distr_fig = get_distribution_plot_figure(
            current_distribution=result.current_distribution,
            reference_distribution=result.reference_distribution,
            color_options=self.color_options,
        )
        figures.append(GraphData.figure("DATA DISTRIBUTION", distr_fig))
        return [
            counter(
                counters=[
                    CounterData(
                        (
                            f"Data drift {drift}. "
                            f"Drift detection method: {result.stattest_name}. "
                            f"Drift score: {drift_score}"
                        ),
                        f"Drift in column '{result.column_name}'",
                    )
                ],
                title="",
            ),
            plotly_graph_tabs(
                title="",
                figures=figures,
            ),
        ]
