from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import dataclasses
import pandas as pd

from evidently import ColumnMapping
from evidently.calculations.data_integration import get_number_of_all_pandas_missed_values
from evidently.calculations.data_integration import get_number_of_almost_constant_columns
from evidently.calculations.data_integration import get_number_of_almost_duplicated_columns
from evidently.calculations.data_integration import get_number_of_constant_columns
from evidently.calculations.data_integration import get_number_of_duplicated_columns
from evidently.calculations.data_integration import get_number_of_empty_columns
from evidently.calculations.data_quality import get_rows_count
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class DatasetSummary:
    """Columns information in a dataset"""

    target: Optional[str]
    prediction: Optional[Union[str, Sequence[str]]]
    date_column: Optional[str]
    id_column: Optional[str]
    number_of_columns: int
    number_of_rows: int
    number_of_missing_values: int
    number_of_categorical_columns: int
    number_of_numeric_columns: int
    number_of_datetime_columns: int
    number_of_empty_columns: int
    number_of_constant_columns: int
    number_of_almost_constant_columns: int
    number_of_duplicated_columns: int
    number_of_almost_duplicated_columns: int


@dataclasses.dataclass
class DatasetSummaryMetricResult:
    almost_duplicated_threshold: float
    current: DatasetSummary
    reference: Optional[DatasetSummary] = None


class DatasetSummaryMetric(Metric[DatasetSummaryMetricResult]):
    """Common dataset(s) columns/features characteristics"""

    # threshold for calculating the number of almost duplicated columns
    almost_duplicated_threshold: float
    almost_constant_threshold: float

    def __init__(self, almost_duplicated_threshold: float = 0.95, almost_constant_threshold: float = 0.95):
        self.almost_duplicated_threshold = almost_duplicated_threshold
        self.almost_constant_threshold = almost_constant_threshold

    def _calculate_dataset_common_stats(self, dataset: pd.DataFrame, column_mapping: ColumnMapping) -> DatasetSummary:
        columns = process_columns(dataset, column_mapping)
        return DatasetSummary(
            target=columns.utility_columns.target,
            prediction=columns.utility_columns.prediction,
            date_column=columns.utility_columns.date,
            id_column=columns.utility_columns.id_column,
            number_of_columns=len(dataset.columns),
            number_of_rows=get_rows_count(dataset),
            number_of_missing_values=get_number_of_all_pandas_missed_values(dataset),
            number_of_categorical_columns=len(columns.cat_feature_names),
            number_of_numeric_columns=len(columns.num_feature_names),
            number_of_datetime_columns=len(columns.datetime_feature_names),
            number_of_empty_columns=get_number_of_empty_columns(dataset),
            number_of_constant_columns=get_number_of_constant_columns(dataset),
            number_of_almost_constant_columns=get_number_of_almost_constant_columns(
                dataset, self.almost_constant_threshold
            ),
            number_of_duplicated_columns=get_number_of_duplicated_columns(dataset),
            number_of_almost_duplicated_columns=get_number_of_almost_duplicated_columns(
                dataset, self.almost_duplicated_threshold
            ),
        )

    def calculate(self, data: InputData) -> DatasetSummaryMetricResult:
        if self.almost_duplicated_threshold < 0.5 or self.almost_duplicated_threshold > 1:
            raise ValueError("Almost duplicated threshold should be in range [0.5, 1]")

        if self.almost_constant_threshold < 0.5 or self.almost_duplicated_threshold > 1:
            raise ValueError("Almost constant threshold should be in range [0.5, 1]")

        current = self._calculate_dataset_common_stats(data.current_data, data.column_mapping)
        reference = None

        if data.reference_data is not None:
            reference = self._calculate_dataset_common_stats(data.reference_data, data.column_mapping)

        return DatasetSummaryMetricResult(
            current=current,
            reference=reference,
            almost_duplicated_threshold=self.almost_duplicated_threshold,
        )


@default_renderer(wrap_type=DatasetSummaryMetric)
class DatasetSummaryMetricRenderer(MetricRenderer):
    def render_json(self, obj: DatasetSummaryMetric) -> dict:
        return dataclasses.asdict(obj.get_result())

    @staticmethod
    def _get_table(stats: DatasetSummary) -> BaseWidgetInfo:
        return table_data(
            title="",
            column_names=["Value", "Count"],
            data=(
                ("target column", stats.target),
                ("prediction column", stats.prediction),
                ("date column", stats.date_column),
                ("number of columns", stats.number_of_columns),
                ("number of rows", stats.number_of_rows),
                ("missing values", stats.number_of_missing_values),
                ("categorical columns", stats.number_of_categorical_columns),
                ("numeric columns", stats.number_of_numeric_columns),
                ("datetime columns", stats.number_of_datetime_columns),
                ("empty columns", stats.number_of_empty_columns),
                ("constant columns", stats.number_of_constant_columns),
                ("almost constant features", stats.number_of_almost_constant_columns),
                ("duplicated columns", stats.number_of_duplicated_columns),
                ("almost duplicated features", stats.number_of_almost_duplicated_columns),
            ),
        )

    def render_html(self, obj: DatasetSummaryMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        current_table = self._get_table(metric_result.current)

        if metric_result.reference is not None:
            tables = widget_tabs(
                tabs=[
                    TabData(title="Current dataset", widget=current_table),
                    TabData(
                        title="Reference dataset",
                        widget=self._get_table(metric_result.reference),
                    ),
                ]
            )

        else:
            tables = current_table

        return [
            header_text(label="Dataset Summary"),
            tables,
        ]
