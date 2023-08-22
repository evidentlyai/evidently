from typing import Text

import pandas as pd

from evidently import ColumnMapping
from evidently.metric_preset import TargetDriftPreset
from evidently.metrics import RegressionAbsPercentageErrorPlot
from evidently.metrics import RegressionErrorDistribution
from evidently.metrics import RegressionErrorNormality
from evidently.metrics import RegressionErrorPlot
from evidently.metrics import RegressionPredictedVsActualPlot
from evidently.metrics import RegressionPredictedVsActualScatter
from evidently.metrics import RegressionQualityMetric
from evidently.metrics import RegressionTopErrorMetric
from evidently.report import Report


def get_column_mapping(**kwargs) -> ColumnMapping:

    column_mapping = ColumnMapping()
    column_mapping.target = kwargs["target_col"]
    column_mapping.prediction = kwargs["prediction_col"]
    column_mapping.numerical_features = kwargs["num_features"]
    column_mapping.categorical_features = kwargs["cat_features"]

    return column_mapping


def build_model_performance_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
) -> Text:

    model_performance_report = Report(
        metrics=[
            RegressionQualityMetric(),
            RegressionPredictedVsActualScatter(),
            RegressionPredictedVsActualPlot(),
            RegressionErrorPlot(),
            RegressionAbsPercentageErrorPlot(),
            RegressionErrorDistribution(),
            RegressionErrorNormality(),
            RegressionTopErrorMetric(),
        ]
    )
    model_performance_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )
    report_path = "reports/model_performance.html"
    model_performance_report.save_html(report_path)

    return report_path


def build_target_drift_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping,
) -> Text:

    target_drift_report = Report(metrics=[TargetDriftPreset()])
    target_drift_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping,
    )
    report_path = "reports/target_drift.html"
    target_drift_report.save_html(report_path)

    return report_path
