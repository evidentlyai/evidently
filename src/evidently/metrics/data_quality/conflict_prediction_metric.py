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
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ConflictPredictionMetricResults:
    number_not_stable_prediction: int
    share_not_stable_prediction: float
    number_not_stable_prediction_ref: Optional[int] = None
    share_not_stable_prediction_ref: Optional[float] = None


class ConflictPredictionMetric(Metric[ConflictPredictionMetricResults]):
    def calculate(self, data: InputData) -> ConflictPredictionMetricResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        prediction_name = dataset_columns.utility_columns.prediction
        if prediction_name is None:
            raise ValueError("The prediction column should be presented")
        columns = dataset_columns.get_all_features_list()
        if len(columns) == 0:
            raise ValueError("Prediction conflict is not defined. No features provided")
        if isinstance(prediction_name, str):
            prediction_columns = [prediction_name]
        elif isinstance(prediction_name, list):
            prediction_columns = prediction_name
        duplicates = data.current_data[data.current_data.duplicated(subset=columns, keep=False)]
        number_not_stable_prediction = duplicates.drop(
            data.current_data[data.current_data.duplicated(subset=columns + prediction_columns, keep=False)].index
        ).shape[0]
        share_not_stable_prediction = round(number_not_stable_prediction / data.current_data.shape[0], 3)
        # reference
        number_not_stable_prediction_ref = None
        share_not_stable_prediction_ref = None
        if data.reference_data is not None:
            duplicates_ref = data.reference_data[data.reference_data.duplicated(subset=columns, keep=False)]
            number_not_stable_prediction_ref = duplicates_ref.drop(
                data.reference_data[
                    data.reference_data.duplicated(subset=columns + prediction_columns, keep=False)
                ].index
            ).shape[0]
            share_not_stable_prediction_ref = round(number_not_stable_prediction_ref / data.reference_data.shape[0], 3)
        return ConflictPredictionMetricResults(
            number_not_stable_prediction=number_not_stable_prediction,
            share_not_stable_prediction=share_not_stable_prediction,
            number_not_stable_prediction_ref=number_not_stable_prediction_ref,
            share_not_stable_prediction_ref=share_not_stable_prediction_ref,
        )


@default_renderer(wrap_type=ConflictPredictionMetric)
class ConflictPredictionMetricRenderer(MetricRenderer):
    def render_json(self, obj: ConflictPredictionMetric) -> dict:
        return dataclasses.asdict(obj.get_result())

    def render_html(self, obj: ConflictPredictionMetric) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        counters = [
            CounterData(
                "number of conflicts (current)",
                self._get_string(metric_result.number_not_stable_prediction, metric_result.share_not_stable_prediction),
            )
        ]
        if (
            metric_result.number_not_stable_prediction_ref is not None
            and metric_result.share_not_stable_prediction_ref is not None
        ):
            counters.append(
                CounterData(
                    "number of conflicts (reference)",
                    self._get_string(
                        metric_result.number_not_stable_prediction_ref, metric_result.share_not_stable_prediction_ref
                    ),
                )
            )
        result = [
            header_text(label="Conflicts in Prediction"),
            counter(counters=counters),
        ]
        return result

    @staticmethod
    def _get_string(number: int, ratio: float) -> str:
        return f"{number} ({ratio * 100}%)"
