from typing import Optional

import numpy as np
from sklearn.metrics import mean_absolute_error

from evidently.base_metric import InputData
from evidently.base_metric import SimpleMetric
from evidently.metric_results import SimpleMetricResults
from evidently.metric_results import SimpleMetricValues
from evidently.renderers.base_renderer import SimpleMetricRenderer
from evidently.renderers.base_renderer import default_renderer


class MAEMetric(SimpleMetric):
    def calculate(self, data: InputData) -> SimpleMetricResults:
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

        return SimpleMetricResults(
            current=SimpleMetricValues(
                value=mean_absolute_error(target_current, prediction_current),
                std=np.std(np.abs(prediction_current - target_current), ddof=1),
            ),
            reference=reference,
        )


@default_renderer(wrap_type=MAEMetric)
class MAEMetricRenderer(SimpleMetricRenderer):
    label = "Mean Absolute Error (+/- std)"
