import dataclasses
import re

import numpy
import pytest

from evidently.base_metric import Metric
from evidently.metrics.classification_performance.class_balance_metric import ClassificationClassBalance
from evidently.metrics.classification_performance.class_separation_metric import ClassificationClassSeparationPlot
from evidently.metrics.classification_performance.classification_dummy_metric import ClassificationDummyMetric
from evidently.metrics.classification_performance.classification_quality_metric import ClassificationQualityMetric
from evidently.metrics.classification_performance.confusion_matrix_metric import ClassificationConfusionMatrix
from evidently.metrics.classification_performance.pr_curve_metric import ClassificationPRCurve
from evidently.metrics.classification_performance.pr_table_metric import ClassificationPRTable
from evidently.metrics.classification_performance.probability_distribution_metric import ClassificationProbDistribution
from evidently.metrics.classification_performance.quality_by_class_metric import ClassificationQualityByClass
from evidently.metrics.classification_performance.quality_by_feature_table import ClassificationQualityByFeatureTable
from evidently.metrics.classification_performance.roc_curve_metric import ClassificationRocCurve
from evidently.metrics.data_drift.column_drift_metric import ColumnDriftMetric
from evidently.metrics.data_drift.column_value_plot import ColumnValuePlot
from evidently.metrics.data_drift.data_drift_table import DataDriftTable
from evidently.metrics.data_drift.dataset_drift_metric import DatasetDriftMetric
from evidently.metrics.data_drift.embeddings_drift import EmbeddingsDriftMetric
from evidently.metrics.data_drift.target_by_features_table import TargetByFeaturesTable
from evidently.metrics.data_drift.text_descriptors_drift_metric import TextDescriptorsDriftMetric
from evidently.metrics.data_drift.text_domain_classifier_drift_metric import TextDomainClassifierDriftMetric
from evidently.metrics.data_drift.text_metric import Comment
from evidently.metrics.data_integrity.column_missing_values_metric import ColumnMissingValuesMetric
from evidently.metrics.data_integrity.column_regexp_metric import ColumnRegExpMetric
from evidently.metrics.data_integrity.column_summary_metric import ColumnSummaryMetric
from evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetric
from evidently.metrics.data_quality.column_correlations_metric import ColumnCorrelationsMetric
from evidently.metrics.data_quality.column_distribution_metric import ColumnDistributionMetric
from evidently.metrics.data_quality.column_quantile_metric import ColumnQuantileMetric
from evidently.metrics.data_quality.column_value_list_metric import ColumnValueListMetric
from evidently.metrics.data_quality.column_value_range_metric import ColumnValueRangeMetric
from evidently.metrics.data_quality.conflict_prediction_metric import ConflictPredictionMetric
from evidently.metrics.data_quality.conflict_target_metric import ConflictTargetMetric
from evidently.metrics.data_quality.dataset_correlations_metric import DatasetCorrelationsMetric
from evidently.metrics.data_quality.stability_metric import DataQualityStabilityMetric
from evidently.metrics.data_quality.text_descriptors_correlation_metric import TextDescriptorsCorrelationMetric
from evidently.metrics.data_quality.text_descriptors_distribution import TextDescriptorsDistribution
from evidently.metrics.regression_performance.abs_perc_error_in_time import RegressionAbsPercentageErrorPlot
from evidently.metrics.regression_performance.error_bias_table import RegressionErrorBiasTable
from evidently.metrics.regression_performance.error_distribution import RegressionErrorDistribution
from evidently.metrics.regression_performance.error_in_time import RegressionErrorPlot
from evidently.metrics.regression_performance.error_normality import RegressionErrorNormality
from evidently.metrics.regression_performance.predicted_and_actual_in_time import RegressionPredictedVsActualPlot
from evidently.metrics.regression_performance.predicted_vs_actual import RegressionPredictedVsActualScatter
from evidently.metrics.regression_performance.regression_dummy_metric import RegressionDummyMetric
from evidently.metrics.regression_performance.regression_performance_metrics import RegressionPerformanceMetrics
from evidently.metrics.regression_performance.regression_quality import RegressionQualityMetric
from evidently.metrics.regression_performance.top_error import RegressionTopErrorMetric
from evidently.report import Report
from tests.multitest.conftest import find_all_subclasses
from tests.multitest.datasets import TestDataset


@dataclasses.dataclass
class TestMetric:
    name: str
    metric: Metric


metric_fixtures = []


def metric(f):
    metric_fixtures.append(f())
    return f


@metric
def regression_error_plot():
    return TestMetric("regression_error_plot", RegressionErrorPlot())


@metric
def classification_class_separation_plot():
    return TestMetric("classification_class_separation_plot", ClassificationClassSeparationPlot())


@metric
def classification_p_r_table():
    return TestMetric("classification_p_r_table", ClassificationPRTable())


@metric
def comment():
    return TestMetric("comment", Comment(""))


@metric
def classification_p_r_curve():
    return TestMetric("classification_p_r_curve", ClassificationPRCurve())


# @metric
# def column_missing_values_metric():
#     return TestMetric("column_missing_values_metric", ColumnMissingValuesMetric())


@metric
def regression_abs_percentage_error_plot():
    return TestMetric("regression_abs_percentage_error_plot", RegressionAbsPercentageErrorPlot())


#
# @metric
# def column_correlations_metric():
#     return TestMetric("column_correlations_metric", ColumnCorrelationsMetric())


@metric
def regression_performance_metrics():
    return TestMetric("regression_performance_metrics", RegressionPerformanceMetrics())


@metric
def regression_quality_metric():
    return TestMetric("regression_quality_metric", RegressionQualityMetric())


# @metric
# def text_descriptors_distribution():
#     return TestMetric("text_descriptors_distribution", TextDescriptorsDistribution())


@metric
def regression_top_error_metric():
    return TestMetric("regression_top_error_metric", RegressionTopErrorMetric())


@metric
def regression_dummy_metric():
    return TestMetric("regression_dummy_metric", RegressionDummyMetric())


@metric
def dataset_correlations_metric():
    return TestMetric("dataset_correlations_metric", DatasetCorrelationsMetric())


@metric
def conflict_target_metric():
    return TestMetric("conflict_target_metric", ConflictTargetMetric())


@metric
def classification_quality_by_class():
    return TestMetric("classification_quality_by_class", ClassificationQualityByClass())


@metric
def data_drift_table():
    return TestMetric("data_drift_table", DataDriftTable())


# @metric
# def column_value_plot():
#     return TestMetric("column_value_plot", ColumnValuePlot())


# @metric
# def column_summary_metric():
#     return TestMetric("column_summary_metric", ColumnSummaryMetric())


# @metric
# def text_descriptors_correlation_metric():
#     return TestMetric("text_descriptors_correlation_metric", TextDescriptorsCorrelationMetric())


@metric
def classification_class_balance():
    return TestMetric("classification_class_balance", ClassificationClassBalance())


@metric
def dataset_drift_metric():
    return TestMetric("dataset_drift_metric", DatasetDriftMetric())


@metric
def dataset_summary_metric():
    return TestMetric("dataset_summary_metric", DatasetSummaryMetric())


@metric
def regression_predicted_vs_actual_plot():
    return TestMetric("regression_predicted_vs_actual_plot", RegressionPredictedVsActualPlot())


# @metric
# def embeddings_drift_metric():
#     return TestMetric("embeddings_drift_metric", EmbeddingsDriftMetric())


# @metric
# def text_domain_classifier_drift_metric():
#     return TestMetric("text_domain_classifier_drift_metric", TextDomainClassifierDriftMetric())


# @metric
# def column_distribution_metric():
#     return TestMetric("column_distribution_metric", ColumnDistributionMetric())


# @metric
# def column_value_list_metric():
#     return TestMetric("column_value_list_metric", ColumnValueListMetric())


# @metric
# def column_value_range_metric():
#     return TestMetric("column_value_range_metric", ColumnValueRangeMetric())


@metric
def regression_error_bias_table():
    return TestMetric("regression_error_bias_table", RegressionErrorBiasTable())


@metric
def regression_error_normality():
    return TestMetric("regression_error_normality", RegressionErrorNormality())


@metric
def classification_confusion_matrix():
    return TestMetric("classification_confusion_matrix", ClassificationConfusionMatrix())


@metric
def classification_roc_curve():
    return TestMetric("classification_roc_curve", ClassificationRocCurve())


@metric
def regression_error_distribution():
    return TestMetric("regression_error_distribution", RegressionErrorDistribution())


@metric
def target_by_features_table():
    return TestMetric("target_by_features_table", TargetByFeaturesTable())


# @metric
# def text_descriptors_drift_metric():
#     return TestMetric("text_descriptors_drift_metric", TextDescriptorsDriftMetric())


# @metric
# def column_reg_exp_metric():
#     return TestMetric("column_reg_exp_metric", ColumnRegExpMetric())


@metric
def classification_quality_metric():
    return TestMetric("classification_quality_metric", ClassificationQualityMetric())


@metric
def classification_quality_by_feature_table():
    return TestMetric("classification_quality_by_feature_table", ClassificationQualityByFeatureTable())


# @metric
# def column_drift_metric():
#     return TestMetric("column_drift_metric", ColumnDriftMetric())


@metric
def classification_prob_distribution():
    return TestMetric("classification_prob_distribution", ClassificationProbDistribution())


@metric
def classification_dummy_metric():
    return TestMetric("classification_dummy_metric", ClassificationDummyMetric())


@metric
def conflict_prediction_metric():
    return TestMetric("conflict_prediction_metric", ConflictPredictionMetric())


@metric
def data_quality_stability_metric():
    return TestMetric("data_quality_stability_metric", DataQualityStabilityMetric())


# @metric
# def column_quantile_metric():
#     return TestMetric("column_quantile_metric", ColumnQuantileMetric())


@metric
def regression_predicted_vs_actual_scatter():
    return TestMetric("regression_predicted_vs_actual_scatter", RegressionPredictedVsActualScatter())


@metric
def dataset_missing_values_metric():
    return TestMetric("dataset_missing_values_metric", DatasetMissingValuesMetric())


def should_run_and_result(tmetric: TestMetric, tdataset: TestDataset):
    # todo: filter by tags or something, also
    return True, None


@pytest.mark.parametrize("raw_data", [True, False], ids=["raw_data", "agg_data"])
def test_metric(tmetric: TestMetric, tdataset: TestDataset, raw_data, tmp_path):
    should_run, exception = should_run_and_result(tmetric, tdataset)
    if not should_run:
        pytest.skip()

    report = Report(metrics=[tmetric.metric], options={"render": {"raw_data": raw_data}})

    if exception is not None:
        with pytest.raises(exception):
            report.run(reference_data=tdataset.reference, current_data=tdataset.current)
        return

    report.run(reference_data=tdataset.reference, current_data=tdataset.current)
    report._inner_suite.raise_for_error()
    assert report.show()
    assert report.json()

    path = str(tmp_path / "report.json")
    report._save(path)
    report2 = Report._load(path)
    numpy.testing.assert_equal(report2.as_dict(), report.as_dict())  # has nans
    report2.show()
    report2.save_html(str(tmp_path / "report.html"))


def test_all_metrics_tested():
    all_metric_classes = find_all_subclasses(Metric)
    missing = []
    for metric_class in all_metric_classes:
        if not any(m.metric.__class__ is metric_class for m in metric_fixtures):
            missing.append(metric_class)

    suggestion_template = """
@metric
def {snake_case}():
    return TestMetric("{snake_case}", {cls}()) 
    """
    suggestion = "\n".join(
        suggestion_template.format(cls=m.__name__, snake_case=re.sub(r"(?<!^)(?=[A-Z])", "_", m.__name__).lower())
        for m in missing
    )
    imports = "\n".join("from {module} import {cls}".format(cls=m.__name__, module=m.__module__) for m in missing)
    print(imports)
    print(suggestion)
    assert len(missing) == 0, f"Missing metric fixtures for {missing}."
