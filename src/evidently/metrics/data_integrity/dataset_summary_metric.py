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
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data
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
    number_of_constant_columns: int
    number_of_almost_constant_columns: int
    number_of_duplicated_columns: int
    number_of_almost_duplicated_columns: int
    number_of_empty_rows: int
    number_of_empty_columns: int
    number_of_duplicated_rows: int
    columns_type: dict
    nans_by_columns: dict
    number_uniques_by_columns: dict


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
            number_of_empty_rows=dataset.isna().all(1).sum(),
            number_of_duplicated_rows=dataset.duplicated().sum(),
            columns_type=dict(dataset.dtypes.to_dict()),
            nans_by_columns=dataset.isna().sum().to_dict(),
            number_uniques_by_columns=dict(dataset.nunique().to_dict()),
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
        result = dataclasses.asdict(obj.get_result())
        if "reference" in result and result["reference"]:
            result["reference"].pop("columns_type", None)

        if "current" in result and result["current"]:
            result["current"].pop("columns_type", None)

        return result

    @staticmethod
    def _get_table(metric_result: DatasetSummaryMetricResult) -> BaseWidgetInfo:
        column_names = ["Metric", "Current"]
        rows = (
            ["id column", metric_result.current.id_column],
            ["target column", metric_result.current.target],
            ["prediction column", metric_result.current.prediction],
            ["date column", metric_result.current.date_column],
            ["number of columns", metric_result.current.number_of_columns],
            ["number of rows", metric_result.current.number_of_rows],
            ["missing values", metric_result.current.number_of_missing_values],
            ["categorical columns", metric_result.current.number_of_categorical_columns],
            ["numeric columns", metric_result.current.number_of_numeric_columns],
            ["datetime columns", metric_result.current.number_of_datetime_columns],
            ["empty columns", metric_result.current.number_of_empty_columns],
            ["constant columns", metric_result.current.number_of_constant_columns],
            ["almost constant features", metric_result.current.number_of_almost_constant_columns],
            ["duplicated columns", metric_result.current.number_of_duplicated_columns],
            ["almost duplicated features", metric_result.current.number_of_almost_duplicated_columns],
        )
        if metric_result.reference is not None:
            column_names.append("Reference")
            rows[0].append(metric_result.reference.id_column)
            rows[1].append(metric_result.reference.target)
            rows[2].append(metric_result.reference.prediction)
            rows[3].append(metric_result.reference.date_column)
            rows[4].append(metric_result.reference.number_of_columns)
            rows[5].append(metric_result.reference.number_of_rows)
            rows[6].append(metric_result.reference.number_of_missing_values)
            rows[7].append(metric_result.reference.number_of_categorical_columns)
            rows[8].append(metric_result.reference.number_of_numeric_columns)
            rows[9].append(metric_result.reference.number_of_datetime_columns)
            rows[10].append(metric_result.reference.number_of_empty_columns)
            rows[11].append(metric_result.reference.number_of_constant_columns)
            rows[12].append(metric_result.reference.number_of_almost_constant_columns)
            rows[13].append(metric_result.reference.number_of_duplicated_columns)
            rows[14].append(metric_result.reference.number_of_almost_duplicated_columns)

        return table_data(title="", column_names=column_names, data=rows)

    def render_html(self, obj: DatasetSummaryMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        return [
            header_text(label="Dataset Summary"),
            self._get_table(metric_result),
        ]
