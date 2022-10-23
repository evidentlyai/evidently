from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd

from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import get_class_separation_plot_data
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ClassificationClassSeparationPlotResults:
    target_name: str
    current_plot: Optional[pd.DataFrame] = None
    reference_plot: Optional[pd.DataFrame] = None


class ClassificationClassSeparationPlot(Metric[ClassificationClassSeparationPlotResults]):
    def calculate(self, data: InputData) -> ClassificationClassSeparationPlotResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        curr_predictions = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        if curr_predictions.prediction_probas is None:
            raise ValueError(
                "ClassificationClassSeparationPlot can be calculated only on binary probabilistic predictions"
            )
        current_plot = curr_predictions.prediction_probas.copy()
        current_plot[target_name] = data.current_data[target_name]
        reference_plot = None
        if data.reference_data is not None:
            ref_predictions = get_prediction_data(data.reference_data, dataset_columns, data.column_mapping.pos_label)
            if ref_predictions.prediction_probas is None:
                raise ValueError(
                    "ClassificationClassSeparationPlot can be calculated only on binary probabilistic predictions"
                )
            reference_plot = ref_predictions.prediction_probas.copy()
            reference_plot[target_name] = data.reference_data[target_name]
        return ClassificationClassSeparationPlotResults(
            current_plot=current_plot,
            reference_plot=reference_plot,
            target_name=target_name,
        )


@default_renderer(wrap_type=ClassificationClassSeparationPlot)
class ClassificationClassSeparationPlotRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationClassSeparationPlot) -> dict:
        return {}

    def render_html(self, obj: ClassificationClassSeparationPlot) -> List[BaseWidgetInfo]:
        current_plot = obj.get_result().current_plot
        reference_plot = obj.get_result().reference_plot
        target_name = obj.get_result().target_name
        if current_plot is None:
            return []
        current_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
        if reference_plot is not None:
            reference_plot.replace([np.inf, -np.inf], np.nan, inplace=True)
        tab_data = get_class_separation_plot_data(
            current_plot, reference_plot, target_name, color_options=self.color_options
        )
        tabs = [TabData(name, widget) for name, widget in tab_data]
        return [header_text(label="Class Separation Quality"), widget_tabs(title="", tabs=tabs)]
