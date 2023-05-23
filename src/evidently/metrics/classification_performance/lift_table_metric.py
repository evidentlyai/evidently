import dataclasses
from typing import List, Optional

import pandas as pd
from evidently.calculations.classification_performance import (
    PredictionData,
    calculate_lift_table,
    get_prediction_data,
)
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer, default_renderer
from evidently.renderers.html_widgets import (
    TabData,
    WidgetSize,
    table_data,
    widget_tabs,
)
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ClassificationLiftTableResults:
    current_lift_table: Optional[dict] = None
    reference_lift_table: Optional[dict] = None
    top: Optional[dict] = 10


class ClassificationLiftTable(Metric[ClassificationLiftTableResults]):
    """
    Evidently metric with inherited behaviour, provides data for lift analysis

    Parameters
    ----------
    top: Optional[dict] = 10
        Limit top percentiles for displaying in report

    """

    top: int

    def __init__(self, top: Optional[int] = 10) -> None:
        self.top = top

    def calculate(self, data) -> ClassificationLiftTableResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError(("The columns 'target' and 'prediction' " "columns should be present"))
        curr_prediction = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        curr_lift_table = self.calculate_metrics(data.current_data[target_name], curr_prediction)
        ref_lift_table = None
        if data.reference_data is not None:
            ref_prediction = get_prediction_data(
                data.reference_data,
                dataset_columns,
                data.column_mapping.pos_label,
            )
            ref_lift_table = self.calculate_metrics(data.reference_data[target_name], ref_prediction)
        return ClassificationLiftTableResults(
            current_lift_table=curr_lift_table,
            reference_lift_table=ref_lift_table,
            top=self.top,
        )

    def calculate_metrics(self, target_data: pd.Series, prediction: PredictionData):
        labels = prediction.labels
        if prediction.prediction_probas is None:
            raise ValueError("Lift Table can be calculated only on " "binary probabilistic predictions")
        binaraized_target = (target_data.values.reshape(-1, 1) == labels).astype(int)
        lift_table = {}
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
        return lift_table


@default_renderer(wrap_type=ClassificationLiftTable)
class ClassificationLiftTableRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationLiftTable) -> dict:
        current_lift_table = obj.get_result().current_lift_table
        reference_lift_table = obj.get_result().reference_lift_table
        current_lift_table = pd.DataFrame(
            current_lift_table[1],
            columns=[
                "top",
                "count",
                "prob",
                "tp",
                "fp",
                "precision",
                "recall",
                "f1_score",
                "lift",
                "max_lift",
                "relative_lift",
                "percent",
            ],
        )
        if reference_lift_table == None:
            return {
                "current": {
                    "top": list(current_lift_table["top"]),
                    "lift": list(current_lift_table["lift"]),
                    "count": list(current_lift_table["count"]),
                    "prob": list(current_lift_table["prob"]),
                    "tp": list(current_lift_table["tp"]),
                    "fp": list(current_lift_table["fp"]),
                    "precision": list(current_lift_table["precision"]),
                    "recall": list(current_lift_table["recall"]),
                    "f1_score": list(current_lift_table["f1_score"]),
                    "max_lift": list(current_lift_table["max_lift"]),
                    "relative_lift": list(current_lift_table["relative_lift"]),
                    "percent": current_lift_table["percent"][0],
                },
            }
        reference_lift_table = pd.DataFrame(
            reference_lift_table[1],
            columns=[
                "top",
                "count",
                "prob",
                "tp",
                "fp",
                "precision",
                "recall",
                "f1_score",
                "lift",
                "max_lift",
                "relative_lift",
                "percent",
            ],
        )
        return {
            "current": {
                "top": list(current_lift_table["top"]),
                "lift": list(current_lift_table["lift"]),
                "count": list(current_lift_table["count"]),
                "prob": list(current_lift_table["prob"]),
                "tp": list(current_lift_table["tp"]),
                "fp": list(current_lift_table["fp"]),
                "precision": list(current_lift_table["precision"]),
                "recall": list(current_lift_table["recall"]),
                "f1_score": list(current_lift_table["f1_score"]),
                "max_lift": list(current_lift_table["max_lift"]),
                "relative_lift": list(current_lift_table["relative_lift"]),
                "percent": current_lift_table["percent"][0],
            },
            "reference": {
                "top": list(reference_lift_table["top"]),
                "lift": list(reference_lift_table["lift"]),
                "count": list(reference_lift_table["count"]),
                "prob": list(reference_lift_table["prob"]),
                "tp": list(reference_lift_table["tp"]),
                "fp": list(reference_lift_table["fp"]),
                "precision": list(reference_lift_table["precision"]),
                "recall": list(reference_lift_table["recall"]),
                "f1_score": list(reference_lift_table["f1_score"]),
                "max_lift": list(reference_lift_table["max_lift"]),
                "relative_lift": list(reference_lift_table["relative_lift"]),
                "percent": reference_lift_table["percent"][0],
            },
        }

    def render_html(self, obj: ClassificationLiftTable) -> List[BaseWidgetInfo]:
        reference_lift_table = obj.get_result().reference_lift_table
        current_lift_table = obj.get_result().current_lift_table
        top = obj.get_result().top
        columns = [
            "Top(%)",
            "Count",
            "Prob",
            "TP",
            "FP",
            "Precision",
            "Recall",
            "F1 score",
            "Lift",
            "Max lift",
            "Relative lift",
            "Percent",
        ]
        result = []
        size = WidgetSize.FULL
        if current_lift_table is not None:
            if len(current_lift_table.keys()) == 1:
                result.append(
                    table_data(
                        column_names=columns,
                        data=current_lift_table[list(current_lift_table.keys())[0]][:top],
                        title="Current: Lift Table",
                        size=size,
                    )
                )
            else:
                tab_data = []
                for label in current_lift_table.keys():
                    table = table_data(
                        column_names=columns,
                        data=current_lift_table[label],
                        title="",
                        size=size,
                    )
                    tab_data.append(TabData(label, table))
                result.append(widget_tabs(title="Current: Lift Table", tabs=tab_data))
        if reference_lift_table is not None:
            if len(reference_lift_table.keys()) == 1:
                result.append(
                    table_data(
                        column_names=columns,
                        data=reference_lift_table[list(reference_lift_table.keys())[0]][:top],
                        title="Reference: Lift Table",
                        size=size,
                    )
                )
            else:
                tab_data = []
                for label in reference_lift_table.keys():
                    table = table_data(
                        column_names=columns,
                        data=reference_lift_table[label],
                        title="",
                        size=size,
                    )
                    tab_data.append(TabData(label, table))
                result.append(widget_tabs(title="Reference: Lift Table", tabs=tab_data))
        return result
