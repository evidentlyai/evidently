from typing import List
from typing import Optional

import dataclasses
import pandas as pd
import plotly.figure_factory as ff
import sklearn

from evidently.metrics.base_metric import InputData
from evidently.metrics.classification_performance.base_classification_metric import ThresholdClassificationMetric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.data_operations import DatasetColumns
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ClassificationQualityByClassResult:
    columns: DatasetColumns
    current_metrics: dict
    reference_metrics: Optional[dict]


class ClassificationQualityByClass(ThresholdClassificationMetric[ClassificationQualityByClassResult]):
    def calculate(self, data: InputData) -> ClassificationQualityByClassResult:
        columns = process_columns(data.current_data, data.column_mapping)
        target, prediction = self.get_target_prediction_data(
            data.current_data,
            column_mapping=data.column_mapping,
        )
        metrics_matrix = sklearn.metrics.classification_report(
            target,
            prediction.predictions,
            output_dict=True,
        )
        ref_metrics = None
        if data.reference_data is not None:
            ref_target, ref_prediction = self.get_target_prediction_data(
                data.reference_data,
                column_mapping=data.column_mapping,
            )
            ref_metrics = sklearn.metrics.classification_report(
                ref_target,
                ref_prediction.predictions,
                output_dict=True,
            )
        return ClassificationQualityByClassResult(
            columns=columns,
            current_metrics=metrics_matrix,
            reference_metrics=ref_metrics,
        )


@default_renderer(wrap_type=ClassificationQualityByClass)
class ClassificationQualityByClassRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationQualityByClass) -> List[BaseWidgetInfo]:
        metric_result = obj.get_result()
        result = [
            _plot_metrics(
                metric_result.columns,
                metric_result.current_metrics,
                "Current: Quality Metrics by Class",
                WidgetSize.FULL if metric_result.reference_metrics is None else WidgetSize.HALF,
            )
        ]
        if metric_result.reference_metrics is not None:
            result.append(
                _plot_metrics(
                    metric_result.columns,
                    metric_result.current_metrics,
                    "Reference: Quality Metrics by Class",
                    WidgetSize.HALF,
                )
            )
        return result

    def render_json(self, obj) -> dict:
        return {}


def _plot_metrics(
    columns: DatasetColumns,
    metrics_matrix: dict,
    title: str,
    size: WidgetSize,
):
    metrics_frame = pd.DataFrame(metrics_matrix)

    z = metrics_frame.iloc[:-1, :-3].values

    x = columns.target_names if columns.target_names else metrics_frame.columns.tolist()[:-3]

    y = ["precision", "recall", "f1-score"]

    # change each element of z to type string for annotations
    z_text = [[str(round(y, 3)) for y in x] for x in z]

    # set up figure
    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text, colorscale="bluered", showscale=True)
    fig.update_layout(xaxis_title="Class", yaxis_title="Metric")

    return plotly_figure(
        title=title,
        figure=fig,
        size=size,
    )
