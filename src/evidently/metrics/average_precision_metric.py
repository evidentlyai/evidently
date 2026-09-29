from typing import List
from typing import Optional

from sklearn.metrics import average_precision_score

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.utils.data_operations import process_columns


class ClassificationAveragePrecisionResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ClassificationAveragePrecisionResult"

    current_value: Optional[float] = None
    reference_value: Optional[float] = None


class ClassificationAveragePrecision(Metric[ClassificationAveragePrecisionResult]):
    class Config:
        type_alias = "evidently:metric:ClassificationAveragePrecision"

    def calculate(self, data: InputData) -> ClassificationAveragePrecisionResult:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction

        if target_name is None or prediction_name is None:
            raise ValueError("Target and Prediction columns must be specified for Average Precision.")

        def _calculate_ap(df):
            if df is None:
                return None
            target = df[target_name]
            prediction = df[prediction_name]
            if len(target) == 0:
                return None
            try:
                return float(average_precision_score(target, prediction))
            except Exception:
                return None

        current_ap = _calculate_ap(data.current_data)
        reference_ap = _calculate_ap(data.reference_data)

        return ClassificationAveragePrecisionResult(
            current_value=current_ap,
            reference_value=reference_ap,
        )


@default_renderer(wrap_type=ClassificationAveragePrecision)
class ClassificationAveragePrecisionRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationAveragePrecision) -> List[BaseWidgetInfo]:
        return []