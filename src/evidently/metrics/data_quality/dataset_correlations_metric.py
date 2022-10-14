from typing import List
from typing import Optional
from typing import Sequence
from typing import Union

import dataclasses
import numpy as np
import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import table_data


@dataclasses.dataclass
class DataCorrelation:
    num_features: Optional[List[str]]
    correlation_matrix: pd.DataFrame
    target_prediction_correlation: Optional[float] = None
    abs_max_target_features_correlation: Optional[float] = None
    abs_max_prediction_features_correlation: Optional[float] = None
    abs_max_correlation: Optional[float] = None
    abs_max_num_features_correlation: Optional[float] = None


@dataclasses.dataclass
class DataQualityCorrelationMetricsResults:
    current: DataCorrelation
    reference: Optional[DataCorrelation]


class DatasetCorrelationsMetric(Metric[DataQualityCorrelationMetricsResults]):
    """Calculate different correlations with target, predictions and features"""

    method: str

    def __init__(self, method: str = "pearson") -> None:
        self.method = method

    def _get_correlations(
        self,
        dataset: pd.DataFrame,
        target_name: Optional[str],
        prediction_name: Optional[Union[str, Sequence[str]]],
        num_features: Optional[List[str]],
        is_classification_task: bool,
    ) -> DataCorrelation:
        correlation_matrix = dataset.corr(method=self.method)
        correlation_matrix_for_plot = correlation_matrix.copy()
        # fill diagonal with 1 values for getting abs max values
        np.fill_diagonal(correlation_matrix.values, 0)

        if num_features is None:
            num_features = [i for i in correlation_matrix if i not in [target_name, prediction_name]]

        if (
            isinstance(prediction_name, str)
            and prediction_name in correlation_matrix
            and target_name in correlation_matrix
        ):
            target_prediction_correlation = correlation_matrix.loc[prediction_name, target_name]

        else:
            target_prediction_correlation = None

        if target_name in correlation_matrix:
            abs_max_target_features_correlation = correlation_matrix.loc[target_name, num_features].abs().max()

        else:
            abs_max_target_features_correlation = None

        if isinstance(prediction_name, str) and prediction_name in correlation_matrix:
            abs_max_prediction_features_correlation = correlation_matrix.loc[prediction_name, num_features].abs().max()

        else:
            abs_max_prediction_features_correlation = None

        if is_classification_task is not None:
            corr_features = num_features

        else:
            corr_features = num_features + [target_name, prediction_name]

        abs_max_correlation = correlation_matrix.loc[corr_features, corr_features].abs().max().max()

        if pd.isnull(abs_max_correlation):
            abs_max_correlation = None

        abs_max_num_features_correlation = correlation_matrix.loc[num_features, num_features].abs().max().max()

        if pd.isnull(abs_max_num_features_correlation):
            abs_max_num_features_correlation = None

        if pd.isnull(target_prediction_correlation):
            target_prediction_correlation = None

        return DataCorrelation(
            num_features=num_features,
            correlation_matrix=correlation_matrix_for_plot,
            target_prediction_correlation=target_prediction_correlation,
            abs_max_target_features_correlation=abs_max_target_features_correlation,
            abs_max_prediction_features_correlation=abs_max_prediction_features_correlation,
            abs_max_correlation=abs_max_correlation,
            abs_max_num_features_correlation=abs_max_num_features_correlation,
        )

    def calculate(self, data: InputData) -> DataQualityCorrelationMetricsResults:
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        num_features: Optional[List[str]] = data.column_mapping.numerical_features
        is_classification_task = data.column_mapping.is_classification_task()

        current_correlations = self._get_correlations(
            dataset=data.current_data,
            target_name=target_name,
            prediction_name=prediction_name,
            num_features=num_features,
            is_classification_task=is_classification_task,
        )

        if data.reference_data is not None:
            reference_correlation: Optional[DataCorrelation] = self._get_correlations(
                dataset=data.reference_data,
                target_name=target_name,
                prediction_name=prediction_name,
                num_features=num_features,
                is_classification_task=is_classification_task,
            )

        else:
            reference_correlation = None

        return DataQualityCorrelationMetricsResults(
            current=current_correlations,
            reference=reference_correlation,
        )


@default_renderer(wrap_type=DatasetCorrelationsMetric)
class DataQualityCorrelationMetricsRenderer(MetricRenderer):
    def render_json(self, obj: DatasetCorrelationsMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result["current"].pop("correlation_matrix", None)

        if result["reference"]:
            result["reference"].pop("correlation_matrix", None)

        return result

    @staticmethod
    def _get_table_stat(dataset_name: str, correlation: DataCorrelation) -> BaseWidgetInfo:
        if correlation.abs_max_correlation is None:
            abs_max_correlation = "None"

        else:
            abs_max_correlation = np.round(correlation.abs_max_correlation, 3)

        if correlation.abs_max_num_features_correlation is None:
            abs_max_num_features_correlation = "None"

        else:
            abs_max_num_features_correlation = np.round(correlation.abs_max_num_features_correlation, 3)

        matched_stat = [
            ("Abs max correlation", abs_max_correlation),
            ("Abs max num features correlation", abs_max_num_features_correlation),
        ]

        if correlation.abs_max_target_features_correlation is not None:
            matched_stat.append(
                ("Abs max target features correlation", np.round(correlation.abs_max_target_features_correlation, 3))
            )
        if correlation.abs_max_prediction_features_correlation is not None:
            matched_stat.append(
                (
                    "Abs max prediction features correlation",
                    np.round(correlation.abs_max_prediction_features_correlation, 3),
                )
            )

        matched_stat_headers = ["Metric", "Value"]
        return table_data(
            title=f"{dataset_name.capitalize()}: Correlation statistic",
            column_names=matched_stat_headers,
            data=matched_stat,
        )

    def render_html(self, obj: DatasetCorrelationsMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()

        result = [
            header_text(label="Data Correlation Metrics"),
            self._get_table_stat(dataset_name="current", correlation=metric_result.current),
        ]

        if metric_result.reference is not None:
            result.append(self._get_table_stat(dataset_name="reference", correlation=metric_result.reference))

        return result
