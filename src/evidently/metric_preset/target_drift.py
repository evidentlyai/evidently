from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence

from evidently import TaskType
from evidently.calculations.data_drift import ensure_prediction_column_is_string
from evidently.calculations.stattests import PossibleStatTestType
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ColumnCorrelationsMetric
from evidently.metrics import ColumnDriftMetric
from evidently.metrics import ColumnValuePlot
from evidently.metrics import TargetByFeaturesTable
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.utils.data_drift_utils import resolve_stattest_threshold
from evidently.utils.data_operations import DatasetColumns


class TargetDriftPreset(MetricPreset):
    """Metric preset for Target Drift analysis.

    Contains metrics:
    - ColumnDriftMetric - for target and prediction if present in datasets.
    - ColumnValuePlot - if task is regression.
    - ColumnCorrelationsMetric - for target and prediction if present in datasets.
    - TargetByFeaturesTable
    """

    columns: Optional[List[str]]
    stattest: Optional[PossibleStatTestType]
    cat_stattest: Optional[PossibleStatTestType]
    num_stattest: Optional[PossibleStatTestType]
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]]
    stattest_threshold: Optional[float]
    cat_stattest_threshold: Optional[float]
    num_stattest_threshold: Optional[float]
    per_column_stattest_threshold: Optional[Dict[str, float]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
    ):
        super().__init__()
        self.columns = columns
        self.stattest = stattest
        self.cat_stattest = cat_stattest
        self.num_stattest = num_stattest
        self.per_column_stattest = per_column_stattest
        self.stattest_threshold = stattest_threshold
        self.cat_stattest_threshold = cat_stattest_threshold
        self.num_stattest_threshold = num_stattest_threshold
        self.per_column_stattest_threshold = per_column_stattest_threshold

    def generate_metrics(self, data: InputData, columns: DatasetColumns) -> Sequence[Metric]:
        target = columns.utility_columns.target
        prediction = columns.utility_columns.prediction
        result: List[Metric] = []
        columns_by_target = []
        prob_columns: Optional[Sequence[str]] = None

        if target is not None:
            columns_by_target.append(target)

            stattest, threshold = resolve_stattest_threshold(
                target,
                "cat" if columns.task == TaskType.CLASSIFICATION_TASK else "num",
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.per_column_stattest_threshold,
            )
            result.append(
                ColumnDriftMetric(
                    column_name=target,
                    stattest=stattest,
                    stattest_threshold=threshold,
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
                stattest, threshold = resolve_stattest_threshold(
                    prediction,
                    "cat" if columns.task == TaskType.CLASSIFICATION_TASK else "num",
                    self.stattest,
                    self.cat_stattest,
                    self.num_stattest,
                    self.per_column_stattest,
                    self.stattest_threshold,
                    self.cat_stattest_threshold,
                    self.num_stattest_threshold,
                    self.per_column_stattest_threshold,
                )
                result.append(
                    ColumnDriftMetric(
                        column_name=prediction,
                        stattest=stattest,
                        stattest_threshold=threshold,
                    )
                )

                if prob_columns is not None:
                    for prob_column in prob_columns:
                        stattest, threshold = resolve_stattest_threshold(
                            prob_column,
                            "num",
                            self.stattest,
                            self.cat_stattest,
                            self.num_stattest,
                            self.per_column_stattest,
                            self.stattest_threshold,
                            self.cat_stattest_threshold,
                            self.num_stattest_threshold,
                            self.per_column_stattest_threshold,
                        )
                        result.append(
                            ColumnDriftMetric(
                                column_name=prob_column,
                                stattest=stattest,
                                stattest_threshold=threshold,
                            )
                        )

                result.append(ColumnCorrelationsMetric(column_name=prediction))

        if columns_by_target:
            result.append(TargetByFeaturesTable())

        return result
