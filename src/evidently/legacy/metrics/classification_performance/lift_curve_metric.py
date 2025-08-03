from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import pandas as pd

from evidently.legacy.base_metric import InputData
from evidently.legacy.base_metric import Metric
from evidently.legacy.base_metric import MetricResult
from evidently.legacy.calculations.classification_performance import calculate_lift_table
from evidently.legacy.calculations.classification_performance import get_prediction_data
from evidently.legacy.core import IncludeTags
from evidently.legacy.metric_results import Label
from evidently.legacy.metric_results import LiftCurve
from evidently.legacy.metric_results import LiftCurveData
from evidently.legacy.metric_results import PredictionData
from evidently.legacy.model.widget import BaseWidgetInfo
from evidently.legacy.renderers.base_renderer import MetricRenderer
from evidently.legacy.renderers.base_renderer import default_renderer
from evidently.legacy.renderers.html_widgets import TabData
from evidently.legacy.renderers.html_widgets import get_lift_plot_data
from evidently.legacy.renderers.html_widgets import header_text
from evidently.legacy.renderers.html_widgets import widget_tabs
from evidently.legacy.utils.data_operations import process_columns


class ClassificationLiftCurveResults(MetricResult):
    class Config:
        type_alias = "evidently:metric_result:ClassificationLiftCurveResults"
        pd_include = False

        field_tags = {"current_lift_curve": {IncludeTags.Current}, "reference_lift_curve": {IncludeTags.Reference}}

    current_lift_curve: Optional[LiftCurve] = None
    reference_lift_curve: Optional[LiftCurve] = None


class ClassificationLiftCurve(Metric[ClassificationLiftCurveResults]):
    class Config:
        type_alias = "evidently:metric:ClassificationLiftCurve"

    def calculate(self, data: InputData) -> ClassificationLiftCurveResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' should be present")
        curr_predictions = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        curr_lift_curve = self.calculate_metrics(data.current_data[target_name], curr_predictions)
        ref_lift_curve = None
        if data.reference_data is not None:
            ref_predictions = get_prediction_data(
                data.reference_data,
                dataset_columns,
                data.column_mapping.pos_label,
            )
            ref_lift_curve = self.calculate_metrics(data.reference_data[target_name], ref_predictions)
        return ClassificationLiftCurveResults(
            current_lift_curve=curr_lift_curve,
            reference_lift_curve=ref_lift_curve,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData) -> LiftCurve:
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("Lift Curve can be calculated only on binary probabilistic predictions")
        binaraized_target = (target_data.to_numpy().reshape(-1, 1) == labels).astype(int)
        lift_curve: LiftCurve = {}
        lift_table: Dict[Label, Any] = {}
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]

            binded = list(
                zip(
                    binaraized_target["target"].tolist(),
                    prediction.prediction_probas.iloc[:, 0].tolist(),
                )
            )
            lift_table[prediction.prediction_probas.columns[0]] = calculate_lift_table(binded)

            lift_curve[prediction.prediction_probas.columns[0]] = LiftCurveData(
                lift=[i[8] for i in lift_table[prediction.prediction_probas.columns[0]]],
                top=[i[0] for i in lift_table[prediction.prediction_probas.columns[0]]],
                count=[i[1] for i in lift_table[prediction.prediction_probas.columns[0]]],
                prob=[i[2] for i in lift_table[prediction.prediction_probas.columns[0]]],
                tp=[i[3] for i in lift_table[prediction.prediction_probas.columns[0]]],
                fp=[i[4] for i in lift_table[prediction.prediction_probas.columns[0]]],
                precision=[i[5] for i in lift_table[prediction.prediction_probas.columns[0]]],
                recall=[i[6] for i in lift_table[prediction.prediction_probas.columns[0]]],
                f1_score=[i[7] for i in lift_table[prediction.prediction_probas.columns[0]]],
                max_lift=[i[9] for i in lift_table[prediction.prediction_probas.columns[0]]],
                relative_lift=[i[10] for i in lift_table[prediction.prediction_probas.columns[0]]],
                percent=[i[11] for i in lift_table[prediction.prediction_probas.columns[0]]],
            )
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels

            for label in labels:
                binded = list(
                    zip(
                        binaraized_target[label].tolist(),
                        prediction.prediction_probas[label],
                    )
                )
                lift_table[label] = calculate_lift_table(binded)

            for label in labels:
                lift_curve[label] = LiftCurveData(
                    lift=[i[8] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    top=[i[0] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    count=[i[1] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    prob=[i[2] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    tp=[i[3] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    fp=[i[4] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    precision=[i[5] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    recall=[i[6] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    f1_score=[i[7] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    max_lift=[i[9] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    relative_lift=[i[10] for i in lift_table[prediction.prediction_probas.columns[0]]],
                    percent=[i[11] for i in lift_table[prediction.prediction_probas.columns[0]]],
                )
        return lift_curve


@default_renderer(wrap_type=ClassificationLiftCurve)
class ClassificationLiftCurveRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationLiftCurve) -> List[BaseWidgetInfo]:
        current_lift_curve: Optional[LiftCurve] = obj.get_result().current_lift_curve
        reference_lift_curve: Optional[LiftCurve] = obj.get_result().reference_lift_curve
        if current_lift_curve is None:
            return []

        tab_data = get_lift_plot_data(
            current_lift_curve,
            reference_lift_curve,
            color_options=self.color_options,
        )
        if len(tab_data) == 1:
            return [header_text(label="Lift Curve"), tab_data[0][1]]
        tabs = [TabData(name, widget) for name, widget in tab_data]
        return [
            header_text(label="Lift Curve"),
            widget_tabs(title="", tabs=tabs),
        ]
