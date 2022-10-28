from evidently.calculations.classification_performance import get_prediction_data
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metrics import ClassificationClassBalance
from evidently.metrics import ClassificationClassSeparationPlot
from evidently.metrics import ClassificationConfusionMatrix
from evidently.metrics import ClassificationPerformanceMetrics
from evidently.metrics import ClassificationPRCurve
from evidently.metrics import ClassificationProbDistribution
from evidently.metrics import ClassificationPRTable
from evidently.metrics import ClassificationQualityByClass
from evidently.metrics import ClassificationQualityByFeatureTable
from evidently.metrics import ClassificationQualityMetric
from evidently.metrics import ClassificationRocCurve
from evidently.metrics.base_metric import InputData
from evidently.utils.data_operations import DatasetColumns


class ClassificationPerformance(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        return [ClassificationPerformanceMetrics()]


class ClassificationPreset(MetricPreset):
    def generate_metrics(self, data: InputData, columns: DatasetColumns):
        result = [
            ClassificationQualityMetric(),
            ClassificationClassBalance(),
            ClassificationConfusionMatrix(),
            ClassificationQualityByClass(),
        ]
        curr_predictions = get_prediction_data(data.current_data, columns, data.column_mapping.pos_label)

        if curr_predictions.prediction_probas is not None:
            result.extend(
                [
                    ClassificationClassSeparationPlot(),
                    ClassificationProbDistribution(),
                    ClassificationRocCurve(),
                    ClassificationPRCurve(),
                    ClassificationPRTable(),
                ]
            )

        result.append(ClassificationQualityByFeatureTable())
        return result
