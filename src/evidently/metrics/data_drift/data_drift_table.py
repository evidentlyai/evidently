import uuid
from typing import List
from typing import Optional

import dataclasses
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.calculations.data_drift import DatasetDriftMetrics
from evidently.calculations.data_drift import get_drift_for_columns
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
from evidently.utils.data_operations import process_columns


@dataclass
class DataDriftTableResults:
    options: DataDriftOptions
    columns: DatasetColumns
    metrics: DatasetDriftMetrics


class DataDriftTable(Metric[DataDriftTableResults]):
    options: DataDriftOptions

    def __init__(self, options: Optional[DataDriftOptions] = None):
        if options is None:
            self.options = DataDriftOptions()

        else:
            self.options = options

    def get_parameters(self) -> tuple:
        return tuple((self.options,))

    def calculate(self, data: InputData) -> DataDriftTableResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        dataset_columns = process_columns(data.reference_data, data.column_mapping)
        result = get_drift_for_columns(
            current_data=data.current_data,
            reference_data=data.reference_data,
            options=self.options,
            dataset_columns=dataset_columns,
        )
        return DataDriftTableResults(options=self.options, columns=result.columns, metrics=result.metrics)


def _generate_feature_params(item_id: str, name: str, data: ColumnDataDriftMetrics) -> dict:
    if data.current_small_distribution is None or data.reference_small_distribution is None:
        return {}

    current_small_hist = data.current_small_distribution
    ref_small_hist = data.reference_small_distribution
    feature_type = data.column_type
    drift_score = data.drift_score
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
        "f5": round(drift_score, 6),
    }


@default_renderer(wrap_type=DataDriftTable)
class DataDriftTableRenderer(MetricRenderer):
    def render_json(self, obj: DataDriftTable) -> dict:
        result = dataclasses.asdict(obj.get_result().metrics)
        result.pop("features", None)
        return result

    def render_html(self, obj: DataDriftTable) -> List[MetricHtmlInfo]:
        results = obj.get_result()
        color_options = ColorOptions()
        all_features = results.columns.get_all_features_list()
        target_column = results.columns.utility_columns.target
        prediction_column = results.columns.utility_columns.prediction

        # set params data
        params_data = []

        # sort columns by drift score
        df_for_sort = pd.DataFrame()
        df_for_sort["features"] = all_features
        df_for_sort["scores"] = [results.metrics.features[feature].drift_score for feature in all_features]
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
            params_data.append(_generate_feature_params(item_id, feature_name, results.metrics.features[feature_name]))

        # set additionalGraphs
        additional_graphs_data = []
        for feature_name in columns:
            curr_distr = results.metrics.features[feature_name].current_distribution
            ref_distr = results.metrics.features[feature_name].reference_distribution
            fig = plot_distr(curr_distr, ref_distr)
            additional_graphs_data.append(
                DetailsInfo(
                    id=f"{item_id}_{feature_name}_distr",
                    title="",
                    info=plotly_figure(title="", figure=fig),
                ),
            )
        n_drifted_features = results.metrics.n_drifted_features
        n_features = results.metrics.n_features
        drift_share = results.metrics.share_drifted_features

        title_prefix = (
            f"Drift is detected for {drift_share * 100:.2f}% of features ({n_drifted_features}"
            f" out of {n_features}). "
        )

        return [
            MetricHtmlInfo(
                "data_drift_title",
                header_text(label="Data Drift Report"),
            ),
            MetricHtmlInfo(
                name="data_drift_table",
                info=rich_table_data(
                    title=title_prefix,
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
