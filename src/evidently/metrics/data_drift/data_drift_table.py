import dataclasses
from dataclasses import dataclass
from typing import Dict, List, Optional

from evidently.base_metric import InputData, Metric
from evidently.calculations.data_drift import (
    ColumnDataDriftMetrics,
    get_drift_for_columns,
)
from evidently.calculations.stattests import PossibleStatTestType
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.renderers.base_renderer import MetricRenderer, default_renderer
from evidently.renderers.html_widgets import (
    ColumnDefinition,
    ColumnType,
    RichTableDataRow,
    RowDetails,
    header_text,
    plotly_figure,
    rich_table_data,
    table_data,
)
from evidently.renderers.render_utils import get_distribution_plot_figure
from evidently.utils.data_operations import DatasetColumns, process_columns
from evidently.utils.visualizations import plot_scatter_for_data_drift


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

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        text_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        text_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
    ):
        self.columns = columns
        self.options = DataDriftOptions(
            all_features_stattest=stattest,
            cat_features_stattest=cat_stattest,
            num_features_stattest=num_stattest,
            text_features_stattest=text_stattest,
            per_feature_stattest=per_column_stattest,
            all_features_threshold=stattest_threshold,
            cat_features_threshold=cat_stattest_threshold,
            num_features_threshold=num_stattest_threshold,
            text_features_threshold=text_stattest_threshold,
            per_feature_threshold=per_column_stattest_threshold,
        )

    def get_parameters(self) -> tuple:
        return None if self.columns is None else tuple(self.columns), self.options

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
            data.pop("current_scatter", None)
            data.pop("x_name", None)
            data.pop("plot_shape", None)

        return result

    def _generate_column_params(
        self, column_name: str, data: ColumnDataDriftMetrics
    ) -> Optional[RichTableDataRow]:
        details = RowDetails()
        if data.column_type == "text":
            if (
                data.typical_examples_cur is not None
                and data.typical_examples_ref is not None
                and data.typical_words_cur is not None
                and data.typical_words_ref is not None
            ):
                current_table_words = table_data(
                    title="",
                    column_names=["", ""],
                    data=[[el, ""] for el in data.typical_words_cur],
                )
                details.with_part(
                    "current: characteristic words", info=current_table_words
                )
                reference_table_words = table_data(
                    title="",
                    column_names=["", ""],
                    data=[[el, ""] for el in data.typical_words_ref],
                )
                details.with_part(
                    "reference: characteristic words", info=reference_table_words
                )
                current_table_examples = table_data(
                    title="",
                    column_names=["", ""],
                    data=[[el, ""] for el in data.typical_examples_cur],
                )
                details.with_part(
                    "current: characteristic examples", info=current_table_examples
                )
                reference_table_examples = table_data(
                    title="",
                    column_names=["", ""],
                    data=[[el, ""] for el in data.typical_examples_ref],
                )
                details.with_part(
                    "reference: characteristic examples", info=reference_table_examples
                )

            data_drift = "Detected" if data.drift_detected else "Not Detected"

            # tabs = [
            #     TabData(title="Carent Dataset: characteristic WORDS", widget=current_table_words),
            #     TabData(title="Reference Dataset: characteristic WORDS", widget=reference_table_words),
            #     TabData(title="Carent Dataset: characteristic EXAMPLES", widget=current_table_examples),
            #     TabData(title="Reference Dataset: characteristic EXAMPLES", widget=reference_table_examples),
            # ]
            return RichTableDataRow(
                details=details,
                fields={
                    "column_name": column_name,
                    "column_type": data.column_type,
                    "stattest_name": data.stattest_name,
                    # "reference_distribution": {},
                    # "current_distribution": {},
                    "data_drift": data_drift,
                    "drift_score": round(data.drift_score, 6),
                },
            )

        else:
            if (
                data.current_small_distribution is None
                or data.reference_small_distribution is None
                or data.current_distribution is None
                or data.reference_distribution is None
            ):
                return None

            current_small_hist = data.current_small_distribution
            ref_small_hist = data.reference_small_distribution
            data_drift = "Detected" if data.drift_detected else "Not Detected"
            if (
                data.column_type == "num"
                and data.current_scatter is not None
                and data.x_name is not None
                and data.plot_shape is not None
            ):
                scatter_fig = plot_scatter_for_data_drift(
                    curr_y=data.current_scatter[data.column_name],
                    curr_x=data.current_scatter[data.x_name],
                    y0=data.plot_shape["y0"],
                    y1=data.plot_shape["y1"],
                    y_name=data.column_name,
                    x_name=data.x_name,
                    color_options=self.color_options,
                )
                scatter = plotly_figure(title="", figure=scatter_fig)
                details.with_part("DATA DRIFT", info=scatter)
            fig = get_distribution_plot_figure(
                current_distribution=data.current_distribution,
                reference_distribution=data.reference_distribution,
                color_options=self.color_options,
            )
            distribution = plotly_figure(title="", figure=fig)
            details.with_part("DATA DISTRIBUTION", info=distribution)
            return RichTableDataRow(
                details=details,
                fields={
                    "column_name": column_name,
                    "column_type": data.column_type,
                    "stattest_name": data.stattest_name,
                    "reference_distribution": {
                        "x": list(ref_small_hist[1]),
                        "y": list(ref_small_hist[0]),
                    },
                    "current_distribution": {
                        "x": list(current_small_hist[1]),
                        "y": list(current_small_hist[0]),
                    },
                    "data_drift": data_drift,
                    "drift_score": round(data.drift_score, 6),
                },
            )

    def render_html(self, obj: DataDriftTable) -> List[BaseWidgetInfo]:
        results = obj.get_result()
        color_options = self.color_options
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
        if target_column in all_columns:
            columns.append(target_column)
            all_columns.remove(target_column)
        if isinstance(prediction_column, str) and prediction_column in all_columns:
            columns.append(prediction_column)
            all_columns.remove(prediction_column)

        columns = columns + all_columns

        for column_name in columns:
            column_params = self._generate_column_params(
                column_name, results.drift_by_columns[column_name]
            )

            if column_params is not None:
                params_data.append(column_params)

        drift_percents = round(results.share_of_drifted_columns * 100, 3)

        return [
            header_text(label="Data Drift Summary"),
            rich_table_data(
                title=f"Drift is detected for {drift_percents}% of columns "
                f"({results.number_of_drifted_columns} out of {results.number_of_columns}).",
                columns=[
                    ColumnDefinition("Column", "column_name"),
                    ColumnDefinition("Type", "column_type"),
                    ColumnDefinition(
                        "Reference Distribution",
                        "reference_distribution",
                        ColumnType.HISTOGRAM,
                        options={
                            "xField": "x",
                            "yField": "y",
                            "color": color_options.primary_color,
                        },
                    ),
                    ColumnDefinition(
                        "Current Distribution",
                        "current_distribution",
                        ColumnType.HISTOGRAM,
                        options={
                            "xField": "x",
                            "yField": "y",
                            "color": color_options.primary_color,
                        },
                    ),
                    ColumnDefinition("Data Drift", "data_drift"),
                    ColumnDefinition("Stat Test", "stattest_name"),
                    ColumnDefinition("Drift Score", "drift_score"),
                ],
                data=params_data,
            ),
        ]
