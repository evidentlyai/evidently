from typing import List
from typing import Optional

import numpy as np
from sklearn.metrics import mean_absolute_error

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.metric_results import SimpleMetricValues
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import CounterData
from evidently.renderers.html_widgets import counter
from evidently.renderers.html_widgets import header_text


class MAEMetricResults(MetricResult):
    current: SimpleMetricValues
    reference: Optional[SimpleMetricValues]


class MAEMetric(Metric[MAEMetricResults]):
    def calculate(self, data: InputData) -> MAEMetricResults:
        target = data.data_definition.get_target_column()
        prediction_data = data.data_definition.get_prediction_columns()
        if target is None or prediction_data is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        prediction = prediction_data.predicted_values
        if prediction is None:
            raise ValueError("Expect one numerical column for prediction.")
        _, target_current, target_reference = data.get_data(target.column_name)
        _, prediction_current, prediction_reference = data.get_data(prediction.column_name)

        reference: Optional[SimpleMetricValues] = None
        if target_reference is not None and prediction_reference is not None:
            reference = SimpleMetricValues(
                value=mean_absolute_error(target_reference, prediction_reference),
                std=np.std(np.abs(prediction_reference - target_reference), ddof=1),
            )

        return MAEMetricResults(
            current=SimpleMetricValues(
                value=mean_absolute_error(target_current, prediction_current),
                std=np.std(np.abs(prediction_current - target_current), ddof=1),
            ),
            reference=reference,
        )


@default_renderer(wrap_type=MAEMetric)
class MAEMetricRenderer(MetricRenderer):
    def render_html(self, obj: MAEMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        counters = [
            CounterData(
                "Current data",
                f"{round(metric_result.current.value, 2)} ({round(metric_result.current.std, 2)})",
            ),
        ]
        if metric_result.reference is not None:
            counters.append(
                CounterData(
                    "Reference data",
                    f"{round(metric_result.reference.value, 2)} ({round(metric_result.reference.std, 2)})",
                ),
            )
        result = [
            header_text(label="Mean Absolute Error (+/- std)"),
            counter(title="", counters=counters),
        ]

        return result
