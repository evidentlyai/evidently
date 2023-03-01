from typing import List
from typing import Optional

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import get_one_column_drift
from evidently.calculations.stattests import PossibleStatTestType
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.utils.data_operations import process_columns
from evidently.utils.visualizations import plot_scatter_for_data_drift


class ColumnDriftMetricResults(ColumnDataDriftMetrics):  # ???
    pass

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
            stattest_threshold=drift_result.stattest_threshold,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            current=drift_result.current,
            scatter=drift_result.scatter,
            reference=drift_result.reference
        )


@default_renderer(wrap_type=ColumnDriftMetric)
class ColumnDriftMetricRenderer(MetricRenderer):
    def render_json(self, obj: ColumnDriftMetric) -> dict:
        return obj.get_result().dict(
            exclude={"current", "reference", "scatter"})

    def render_html(self, obj: ColumnDriftMetric) -> List[BaseWidgetInfo]:
        result = obj.get_result()

        if result.drift_detected:
            drift = "detected"

        else:
            drift = "not detected"

        drift_score = round(result.drift_score, 3)

        tabs = []

        # fig_json = fig.to_plotly_json()
        if result.scatter is not None:
            scatter_fig = plot_scatter_for_data_drift(
                curr_y=result.scatter.scatter[result.column_name],
                curr_x=result.scatter.scatter[result.scatter.x_name],
                y0=result.scatter.plot_shape["y0"],
                y1=result.scatter.plot_shape["y1"],
                y_name=result.column_name,
                x_name=result.scatter.x_name,
                color_options=self.color_options,
            )
            tabs.append(TabData("DATA DRIFT", plotly_figure(title="", figure=scatter_fig)))

        if result.current.distribution is not None and result.reference.distribution is not None:
            distr_fig = get_distribution_plot_figure(
                current_distribution=result.current.distribution,
                reference_distribution=result.reference.distribution,
                color_options=self.color_options,
            )
            # figures.append(GraphData.figure("DATA DISTRIBUTION", distr_fig))
            tabs.append(TabData("DATA DISTRIBUTION", plotly_figure(title="", figure=distr_fig)))

        if (
            result.current.examples is not None
            and result.reference.examples is not None
            and result.current.words is not None
            and result.reference.words is not None
        ):
            current_table_words = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.current.words],
            )
            reference_table_words = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.reference.words],
            )
            current_table_examples = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.current.examples],
            )
            reference_table_examples = table_data(
                title="",
                column_names=["", ""],
                data=[[el, ""] for el in result.reference.examples],
            )

            tabs = [
                TabData(title="current: characteristic words", widget=current_table_words),
                TabData(title="reference: characteristic words", widget=reference_table_words),
                TabData(title="current: characteristic examples", widget=current_table_examples),
                TabData(title="reference: characteristic examples", widget=reference_table_examples),
            ]
        render_result = [
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
            )
        ]
        if len(tabs) > 0:
            render_result.append(
                widget_tabs(
                    title="",
                    tabs=tabs,
                )
            )

        return render_result
