from typing import List
from typing import Optional

import dataclasses

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text


@dataclasses.dataclass
class DataQualityStabilityMetricResult:
    number_not_stable_target: Optional[int] = None
    number_not_stable_prediction: Optional[int] = None


class DataQualityStabilityMetric(Metric[DataQualityStabilityMetricResult]):
    """Calculates stability by target and prediction"""

    def calculate(self, data: InputData) -> DataQualityStabilityMetricResult:
        result = DataQualityStabilityMetricResult()
        target_name = data.column_mapping.target
        prediction_name = data.column_mapping.prediction
        columns = [column for column in data.current_data.columns if column not in (target_name, prediction_name)]

        if not columns:
            result.number_not_stable_target = 0
            result.number_not_stable_prediction = 0
            return result

        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]

        if target_name in data.current_data:
            result.number_not_stable_target = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [target_name], keep=False)].index
            ).shape[0]

        if prediction_name in data.current_data:
            result.number_not_stable_prediction = duplicates.drop(
                data.current_data[data.current_data.duplicated(subset=columns + [prediction_name], keep=False)].index
            ).shape[0]

        return result


@default_renderer(wrap_type=DataQualityStabilityMetric)
class DataQualityStabilityMetricRenderer(MetricRenderer):
    def render_json(self, obj: DataQualityStabilityMetric) -> dict:
        return dataclasses.asdict(obj.get_result())

    def render_html(self, obj: DataQualityStabilityMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            header_text(label="Data Stability Metrics"),
            counter(
                counters=[
                    CounterData("Not stable target", str(metric_result.number_not_stable_target)),
                    CounterData("Not stable prediction", str(metric_result.number_not_stable_prediction)),
                ]
            ),
        ]
        return result
