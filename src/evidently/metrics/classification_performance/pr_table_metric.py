from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import calculate_pr_table
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import table_data
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import widget_tabs
from evidently.model.widget import BaseWidgetInfo


@dataclasses.dataclass
class ClassificationPRTableResults:
    current_pr_table: Optional[dict] = None
    reference_pr_table: Optional[dict] = None


class ClassificationPRTable(Metric[ClassificationPRTableResults]):
    def calculate(self, data: InputData) -> ClassificationPRTableResults:
        curr_prediction = get_prediction_data(data.current_data, data.column_mapping)
        curr_pr_table = self.calculate_metrics(data.current_data[data.column_mapping.target], curr_prediction)
        ref_pr_table = None
        if data.reference_data is not None:
            ref_prediction = get_prediction_data(data.reference_data, data.column_mapping)
            ref_pr_table = self.calculate_metrics(data.reference_data[data.column_mapping.target], ref_prediction)
        return ClassificationPRTableResults(
            current_pr_table=curr_pr_table,
            reference_pr_table=ref_pr_table,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData):
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("PR Table can be calculated only on binary probabilistic predictions")
        binaraized_target = (target_data.values.reshape(-1, 1) == labels).astype(int)
        pr_table = {}
        if len(labels) <= 2:
            binaraized_target = pd.DataFrame(binaraized_target[:, 0])
            binaraized_target.columns = ["target"]

            binded = list(zip(binaraized_target["target"].tolist(), prediction.prediction_probas[labels[0]].tolist()))
            pr_table[labels[0]] = calculate_pr_table(binded)
        else:
            binaraized_target = pd.DataFrame(binaraized_target)
            binaraized_target.columns = labels

            for label in labels:
                binded = list(zip(binaraized_target[label].tolist(), prediction.prediction_probas[label]))
                pr_table[label] = calculate_pr_table(binded)
        return pr_table


@default_renderer(wrap_type=ClassificationPRTable)
class ClassificationPRTableRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationPRTable) -> dict:
        return {}

    def render_html(self, obj: ClassificationPRTable) -> List[BaseWidgetInfo]:
        reference_pr_table = obj.get_result().reference_pr_table
        current_pr_table = obj.get_result().current_pr_table
        columns = ["Top(%)", "Count", "Prob", "TP", "FP", "Precision", "Recall"]
        result = []
        size = WidgetSize.FULL
        if reference_pr_table is not None:
            size = WidgetSize.HALF
        if current_pr_table is not None:
            if len(current_pr_table.keys()) == 1:
                result.append(
                    table_data(column_names=columns, data=current_pr_table[list(current_pr_table.keys())[0]],
                               title="Current: Precision-Recall Table", size=size)
                )
            else:
                tab_data = []
                for label in current_pr_table.keys():
                    table = table_data(column_names=columns, data=current_pr_table[label],
                                       title="", size=size)
                    tab_data.append(TabData(label, table))
                result.append(widget_tabs(title="Current: Precision-Recall Table", tabs=tab_data))
        if reference_pr_table is not None:
            if len(reference_pr_table.keys()) == 1:
                result.append(
                    table_data(column_names=columns, data=reference_pr_table[list(reference_pr_table.keys())[0]],
                               title="Reference: Precision-Recall Table", size=size)
                )
            else:
                tab_data = []
                for label in reference_pr_table.keys():
                    table = table_data(column_names=columns, data=reference_pr_table[label],
                                       title="", size=size)
                    tab_data.append(TabData(label, table))
                result.append(widget_tabs(title="Reference: Precision-Recall Table", tabs=tab_data))
        return result
