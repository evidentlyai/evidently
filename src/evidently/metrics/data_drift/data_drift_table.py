import uuid
from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.data_drift import DataDriftAnalyzerFeatureMetrics
from evidently.calculations.data_drift import DataDriftAnalyzerMetrics
from evidently.calculations.data_drift import calculate_all_drifts_for_metrics
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.options import ColorOptions
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import DetailsInfo
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import ColumnDefinition
from evidently.renderers.html_widgets import ColumnType
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import plotly_figure
from evidently.renderers.html_widgets import rich_table_data
from evidently.renderers.render_utils import plot_distr
from evidently.utils.data_operations import DatasetColumns


@dataclass
class DataDriftMetricsResults:
    options: DataDriftOptions
    columns: DatasetColumns
    metrics: DataDriftAnalyzerMetrics
    distr_for_plots: Dict[str, Dict[str, pd.DataFrame]]


class DataDriftTable(Metric[DataDriftMetricsResults]):
    options: DataDriftOptions

    def __init__(self, options: Optional[DataDriftOptions] = None):
        if options is None:
            self.options = DataDriftOptions()

        else:
            self.options = options

    def get_parameters(self) -> tuple:
        return tuple((self.options,))

    def calculate(self, data: InputData) -> DataDriftMetricsResults:
        result = calculate_all_drifts_for_metrics(data, self.options)
        return DataDriftMetricsResults(
            options=self.options, columns=result.columns, metrics=result.metrics, distr_for_plots=result.distr_for_plots
        )


def _generate_feature_params(item_id: str, name: str, data: DataDriftAnalyzerFeatureMetrics) -> dict:
    current_small_hist = data.current_small_hist
    ref_small_hist = data.ref_small_hist
    feature_type = data.feature_type
    p_value = data.p_value
    distr_sim_test = "Detected" if data.drift_detected else "Not Detected"
    parts = []
    parts.append({"title": "Data distribution", "id": f"{item_id}_{name}_distr", "type": "widget"})
    return {
        "details": {"parts": parts, "insights": []},
        "f1": name,
        "f6": feature_type,
        "stattest_name": data.stattest_name,
        "f3": {"x": list(ref_small_hist[1]), "y": list(ref_small_hist[0])},
        "f4": {"x": list(current_small_hist[1]), "y": list(current_small_hist[0])},
        "f2": distr_sim_test,
        "f5": round(p_value, 6),
    }


@default_renderer(wrap_type=DataDriftTable)
class DataDriftMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataDriftTable) -> dict:
        return dataclasses.asdict(obj.get_result().metrics)

    def render_html(self, obj: DataDriftTable) -> List[MetricHtmlInfo]:
        color_options = ColorOptions()

        data_drift_results = obj.get_result()
        all_features = data_drift_results.columns.get_all_features_list()
        target_column = data_drift_results.columns.utility_columns.target
        prediction_column = data_drift_results.columns.utility_columns.prediction

        # set params data
        params_data = []

        # sort columns by drift score
        df_for_sort = pd.DataFrame()
        df_for_sort["features"] = all_features
        df_for_sort["scores"] = [data_drift_results.metrics.features[feature].p_value for feature in all_features]
        all_features = df_for_sort.sort_values("scores", ascending=False).features.tolist()
        columns = []
        if target_column:
            columns.append(target_column)
            all_features.remove(target_column)
        if prediction_column and isinstance(prediction_column, str):
            columns.append(prediction_column)
            all_features.remove(prediction_column)
        columns = columns + all_features

        item_id = str(uuid.uuid4())
        for feature_name in columns:
            params_data.append(
                _generate_feature_params(item_id, feature_name, data_drift_results.metrics.features[feature_name])
            )

        # set additionalGraphs
        additional_graphs_data = []
        for feature_name in columns:
            curr_distr = obj.get_result().distr_for_plots[feature_name]["current"]
            ref_distr = obj.get_result().distr_for_plots[feature_name]["reference"]
            fig = plot_distr(curr_distr, ref_distr)
            additional_graphs_data.append(
                DetailsInfo(
                    id=f"{item_id}_{feature_name}_distr",
                    title="",
                    info=plotly_figure(title="", figure=fig),
                ),
            )
        n_drifted_features = data_drift_results.metrics.n_drifted_features
        dataset_drift = data_drift_results.metrics.dataset_drift
        n_features = data_drift_results.metrics.n_features
        drift_share = data_drift_results.metrics.share_drifted_features

        title_prefix = (
            f"Drift is detected for {drift_share * 100:.2f}% of features ({n_drifted_features}"
            f" out of {n_features}). "
        )
        title_suffix = "Dataset Drift is detected." if dataset_drift else "Dataset Drift is NOT detected."

        return [
            MetricHtmlInfo(
                "data_drift_title",
                header_text(label="Data Drift Report"),
            ),
            MetricHtmlInfo(
                name="data_drift_table",
                info=rich_table_data(
                    title=title_prefix + title_suffix,
                    columns=[
                        ColumnDefinition("Feature", "f1"),
                        ColumnDefinition("Type", "f6"),
                        ColumnDefinition(
                            "Reference Distribution",
                            "f3",
                            ColumnType.HISTOGRAM,
                            options={"xField": "x", "yField": "y", "color": color_options.primary_color},
                        ),
                        ColumnDefinition(
                            "Current Distribution",
                            "f4",
                            ColumnType.HISTOGRAM,
                            options={"xField": "x", "yField": "y", "color": color_options.primary_color},
                        ),
                        ColumnDefinition("Data Drift", "f2"),
                        ColumnDefinition("Stat Test", "stattest_name"),
                        ColumnDefinition("Drift Score", "f5"),
                    ],
                    data=params_data,
                ),
                details=additional_graphs_data,
            ),
        ]
