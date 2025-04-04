from typing import List
from typing import Optional

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import CounterData
from evidently.legacy.renderers.html_widgets import counter
from evidently.legacy.renderers.html_widgets import header_text


class DataQualityStabilityMetricResult(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:DataQualityStabilityMetricResult"

    number_not_stable_target: Optional[int] = None
    number_not_stable_prediction: Optional[int] = None


class DataQualityStabilityMetric(Metric[DataQualityStabilityMetricResult]):
    class Config:
        type_alias = "evidently:metric:DataQualityStabilityMetric"

    """Calculates stability by target and prediction"""

    def calculate(self, data: InputData) -> DataQualityStabilityMetricResult:
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        columns = [column for column in data.current_data.columns if column not in (target_name, prediction_name)]

        if not columns:
            return DataQualityStabilityMetricResult(number_not_stable_target=0, number_not_stable_prediction=0)

        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]

        number_not_stable_target = None
        number_not_stable_prediction = None

        if target_name in data.current_data:
            number_not_stable_target = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [target_name], keep=False)].index
            ).shape[0]

        if prediction_name in data.current_data:
            number_not_stable_prediction = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [prediction_name], keep=False)].index
            ).shape[0]

        return DataQualityStabilityMetricResult(
            number_not_stable_target=number_not_stable_target, number_not_stable_prediction=number_not_stable_prediction
        )


@default_renderer(wrap_type=DataQualityStabilityMetric)
class DataQualityStabilityMetricRenderer(MetricRenderer):
    def render_html(self, obj: DataQualityStabilityMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Data Stability Metrics"),
            counter(
                counters=[
                    CounterData("Not stable target", str(metric_result.number_not_stable_target)),
                    CounterData(
                        "Not stable prediction",
                        str(metric_result.number_not_stable_prediction),
                    ),
                ]
            ),
        ]
        return result
