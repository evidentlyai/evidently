from typing import List
from typing import Optional
from typing import Sequence

from evidently.calculations.data_drift import ensure_prediction_column_is_string
from evidently.calculations.stattests import PossibleStatTestType
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ColumnCorrelationsMetric
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnValuePlot
from evidently.metrics import TargetByFeaturesTable
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.utils.data_operations import DatasetColumns


class TargetDriftPreset(MetricPreset):
    columns: Optional[List[str]]
    target_stattest: Optional[PossibleStatTestType]
    prediction_stattest: Optional[PossibleStatTestType]
    target_stattest_threshold: Optional[float]
    prediction_stattest_threshold: Optional[float]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        target_stattest: Optional[PossibleStatTestType] = None,
        prediction_stattest: Optional[PossibleStatTestType] = None,
        target_stattest_threshold: Optional[float] = None,
        prediction_stattest_threshold: Optional[float] = None,
    ):
        super().__init__()
        self.columns = columns
        self.target_stattest = target_stattest
        self.prediction_stattest = prediction_stattest
        self.target_stattest_threshold = target_stattest_threshold
        self.prediction_stattest_threshold = prediction_stattest_threshold

    def generate_metrics(self, data: InputData, columns: DatasetColumns) -> Sequence[Metric]:
        target = columns.utility_columns.target
        prediction = columns.utility_columns.prediction
        result: List[Metric] = []
        columns_by_target = []
        prob_columns: Optional[Sequence[str]] = None

        if target is not None:
            columns_by_target.append(target)
            result.append(
                ColumnDriftMetric(
                    column_name=target,
                    stattest=self.target_stattest,
                    stattest_threshold=self.target_stattest_threshold,
                )
            )

            if data.column_mapping.is_regression_task():
                result.append(ColumnValuePlot(column_name=target))

            result.append(ColumnCorrelationsMetric(column_name=target))

        if prediction is not None:
            if data.column_mapping.is_classification_task():
                prediction_column = ensure_prediction_column_is_string(
                    prediction_column=columns.utility_columns.prediction,
                    current_data=data.current_data,
                    reference_data=data.reference_data,
                )

                if prediction_column is not None:
                    # in case that a new prediction column was created
                    if not isinstance(prediction, str):
                        prob_columns = prediction

                    prediction = prediction_column

            if isinstance(prediction, str):
                columns_by_target.append(prediction)
                result.append(
                    ColumnDriftMetric(
                        column_name=prediction,
                        stattest=self.target_stattest,
                        stattest_threshold=self.target_stattest_threshold,
                    )
                )

                if prob_columns is not None:
                    for prob_column in prob_columns:
                        result.append(ColumnDriftMetric(column_name=prob_column))

                result.append(ColumnCorrelationsMetric(column_name=prediction))

        if columns_by_target:
            result.append(TargetByFeaturesTable())

        return result
