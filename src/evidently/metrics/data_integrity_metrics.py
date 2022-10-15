from itertools import combinations
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
from dataclasses import dataclass

from evidently.calculations.data_integration import get_number_of_empty_columns
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data


@dataclass
class DataIntegrityMetricsValues:
    number_of_columns: int
    number_of_rows: int
    number_of_nans: int
    number_of_columns_with_nans: int
    number_of_rows_with_nans: int
    number_of_constant_columns: int
    number_of_empty_rows: int
    number_of_empty_columns: int
    number_of_duplicated_rows: int
    number_of_duplicated_columns: int
    columns_type: dict
    nans_by_columns: dict
    number_uniques_by_columns: dict
    counts_of_values: dict


@dataclass
class DataIntegrityMetricsResults:
    current: DataIntegrityMetricsValues
    reference: Optional[DataIntegrityMetricsValues] = None


class DataIntegrityMetrics(Metric[DataIntegrityMetricsResults]):
    @staticmethod
    def _get_integrity_metrics_values(dataset: pd.DataFrame, columns: tuple) -> DataIntegrityMetricsValues:
        counts_of_values = {}

        for column_name in dataset.columns:
            feature = dataset[column_name]
            df_counts = feature.value_counts(dropna=False).reset_index()
            df_counts.columns = ["x", "count"]
            counts_of_values[column_name] = df_counts

        return DataIntegrityMetricsValues(
            number_of_columns=len(columns),
            number_of_rows=dataset.shape[0],
            number_of_nans=dataset.isna().sum().sum(),
            number_of_columns_with_nans=dataset.isna().any().sum(),
            number_of_rows_with_nans=dataset.isna().any(axis=1).sum(),
            number_of_constant_columns=len(dataset.columns[dataset.nunique() <= 1]),  # type: ignore
            number_of_empty_rows=dataset.isna().all(1).sum(),
            number_of_empty_columns=get_number_of_empty_columns(dataset),
            number_of_duplicated_rows=dataset.duplicated().sum(),
            number_of_duplicated_columns=sum([1 for i, j in combinations(dataset, 2) if dataset[i].equals(dataset[j])]),
            columns_type=dict(dataset.dtypes.to_dict()),
            nans_by_columns=dataset.isna().sum().to_dict(),
            number_uniques_by_columns=dict(dataset.nunique().to_dict()),
            counts_of_values=counts_of_values,
        )

    def calculate(self, data: InputData) -> DataIntegrityMetricsResults:
        columns = []

        for col in [data.column_mapping.target, data.column_mapping.datetime, data.column_mapping.id]:
            if col is not None:
                columns.append(col)

        for features in [
            data.column_mapping.numerical_features,
            data.column_mapping.categorical_features,
            data.column_mapping.datetime_features,
        ]:
            if features is not None:
                columns.extend(features)

        if data.column_mapping.prediction is not None:
            if isinstance(data.column_mapping.prediction, str):
                columns.append(data.column_mapping.prediction)

            elif isinstance(data.column_mapping.prediction, str):
                columns += data.column_mapping.prediction

        # even with empty column_mapping we will have 3 default values
        if len(columns) <= 3:
            columns = data.current_data.columns

            if data.reference_data is not None:
                columns = np.union1d(columns, data.reference_data.columns)

        current_columns = np.intersect1d(columns, data.current_data.columns)

        curr_data = data.current_data[current_columns]
        current = self._get_integrity_metrics_values(curr_data, current_columns)

        if data.reference_data is not None:
            reference_columns = np.intersect1d(columns, data.reference_data.columns)
            ref_data = data.reference_data[reference_columns]
            reference: Optional[DataIntegrityMetricsValues] = self._get_integrity_metrics_values(
                ref_data, reference_columns
            )

        else:
            reference = None

        return DataIntegrityMetricsResults(current=current, reference=reference)


@default_renderer(wrap_type=DataIntegrityMetrics)
class DataIntegrityMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DataIntegrityMetrics) -> dict:
        result = dataclasses.asdict(obj.get_result())
        if "current" in result:
            result["current"].pop("counts_of_values", None)

            result["current"]["columns_type"] = [str(t) for t in result["current"]["columns_type"]]

        if "reference" in result and result["reference"]:
            result["reference"].pop("counts_of_values", None)
            result["reference"]["columns_type"] = [str(t) for t in result["reference"]["columns_type"]]

        return result

    @staticmethod
    def _get_metrics_table(dataset_name: str, metrics: DataIntegrityMetricsValues) -> BaseWidgetInfo:
        headers = ("Quality Metric", "Value")
        stats = (
            ("Number of columns", metrics.number_of_columns),
            ("Number of rows", metrics.number_of_rows),
            ("Number of NaNs", metrics.number_of_nans),
            ("Number of columns with NaNs", metrics.number_of_columns_with_nans),
            ("Number of rows with NaNs", metrics.number_of_rows_with_nans),
            ("Number of constant columns", metrics.number_of_constant_columns),
            ("Number of empty rows", metrics.number_of_empty_rows),
            ("Number of empty columns", metrics.number_of_empty_columns),
            ("Number of duplicated rows", metrics.number_of_duplicated_rows),
            ("Number of duplicated columns", metrics.number_of_duplicated_columns),
        )

        return table_data(column_names=headers, data=stats)

    def render_html(self, obj: DataIntegrityMetrics) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()

        result = [
            header_text(label="Data Integrity"),
            self._get_metrics_table(dataset_name="current", metrics=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_metrics_table(dataset_name="reference", metrics=metric_result.reference))

        return result
