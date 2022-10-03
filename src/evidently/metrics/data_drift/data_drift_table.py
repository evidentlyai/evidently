import uuid
from typing import Dict
from typing import List
from typing import Optional

import dataclasses
from dataclasses import dataclass

from evidently.calculations.data_drift import ColumnDataDriftMetrics
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
    number_of_columns: int
    number_of_drifted_columns: int
    share_of_drifted_columns: float
    dataset_drift: bool
    drift_by_columns: Dict[str, ColumnDataDriftMetrics]
    dataset_columns: DatasetColumns


class DataDriftTable(Metric[DataDriftTableResults]):
    columns: Optional[List[str]]
    options: DataDriftOptions

    def __init__(self, columns: Optional[List[str]] = None, options: Optional[DataDriftOptions] = None):
        self.columns = columns
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
            data_drift_options=self.options,
            dataset_columns=dataset_columns,
            columns=self.columns,
        )
        return DataDriftTableResults(
            number_of_columns=result.number_of_columns,
            number_of_drifted_columns=result.number_of_drifted_columns,
            share_of_drifted_columns=result.share_of_drifted_columns,
            dataset_drift=result.dataset_drift,
            drift_by_columns=result.drift_by_columns,
            dataset_columns=result.dataset_columns,
        )


def _generate_column_params(item_id: str, column_name: str, data: ColumnDataDriftMetrics) -> dict:
    if data.current_small_distribution is None or data.reference_small_distribution is None:
        return {}

    current_small_hist = data.current_small_distribution
    ref_small_hist = data.reference_small_distribution
    distr_sim_test = "Detected" if data.drift_detected else "Not Detected"
    parts = [{"title": "Data distribution", "id": f"{item_id}_{column_name}_distribution", "type": "widget"}]
    return {
        "details": {"parts": parts, "insights": []},
        "f1": column_name,
        "f6": data.column_type,
        "stattest_name": data.stattest_name,
        "f3": {"x": list(ref_small_hist[1]), "y": list(ref_small_hist[0])},
        "f4": {"x": list(current_small_hist[1]), "y": list(current_small_hist[0])},
        "f2": distr_sim_test,
        "f5": round(data.drift_score, 6),
    }


@default_renderer(wrap_type=DataDriftTable)
class DataDriftTableRenderer(MetricRenderer):
    def render_json(self, obj: DataDriftTable) -> dict:
        result = dataclasses.asdict(obj.get_result())

        # remove pandas dataset values and other useless for JSON fields
        result.pop("dataset_columns", None)

        for column_name, data in result["drift_by_columns"].items():
            data.pop("current_distribution", None)
            data.pop("reference_distribution", None)
            data.pop("current_small_distribution", None)
            data.pop("reference_small_distribution", None)
            data.pop("current_correlations", None)
            data.pop("reference_correlations", None)

        return result

    def render_html(self, obj: DataDriftTable) -> List[MetricHtmlInfo]:
        results = obj.get_result()
        color_options = ColorOptions()
        target_column = results.dataset_columns.utility_columns.target
        prediction_column = results.dataset_columns.utility_columns.prediction

        # set params data
        params_data = []

        # sort columns by drift score
        all_columns = sorted(
            results.drift_by_columns.keys(),
            key=lambda x: results.drift_by_columns[x].drift_score,
            reverse=True,
        )
        # move target and prediction to the top of the table
        columns = []

        if target_column:
            columns.append(target_column)

            if target_column in all_columns:
                all_columns.remove(target_column)

        if prediction_column and isinstance(prediction_column, str):
            columns.append(prediction_column)

            if prediction_column in all_columns:
                all_columns.remove(prediction_column)

        columns = columns + all_columns

        item_id = str(uuid.uuid4())

        for column_name in columns:
            params_data.append(_generate_column_params(item_id, column_name, results.drift_by_columns[column_name]))

        # set additionalGraphs
        additional_graphs_data = []

        for column_name in columns:
            current_distribution = results.drift_by_columns[column_name].current_distribution
            reference_distribution = results.drift_by_columns[column_name].reference_distribution
            fig = plot_distr(current_distribution, reference_distribution)
            additional_graphs_data.append(
                DetailsInfo(
                    id=f"{item_id}_{column_name}_distribution",
                    title="",
                    info=plotly_figure(title="", figure=fig),
                ),
            )

        drift_percents = round(results.share_of_drifted_columns * 100, 3)
        title_prefix = (
            f"Drift is detected for {drift_percents}% of columns ({results.number_of_drifted_columns}"
            f" out of {results.number_of_columns}). "
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
                        ColumnDefinition("Column", "f1"),
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
