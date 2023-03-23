from typing import List
from typing import Optional

import numpy as np
import pandas as pd

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metric_results import ColumnScatter
from evidently.metric_results import column_scatter_from_df
from evidently.metric_results import df_from_column_scatter
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import TabData
from evidently.renderers.html_widgets import get_class_separation_plot_data
from evidently.renderers.html_widgets import header_text
from evidently.renderers.html_widgets import widget_tabs
from evidently.utils.data_operations import process_columns


class ClassificationClassSeparationPlotResults(MetricResult):
    class Config:
        smart_union = True
        dict_exclude_fields = {"current", "reference"}
        pd_exclude_fields = {"current", "reference"}

    target_name: str
    current: Optional[ColumnScatter] = None
    reference: Optional[ColumnScatter] = None


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
            current=column_scatter_from_df(current_plot, True),
            reference=column_scatter_from_df(reference_plot, True),
            target_name=target_name,
        )


@default_renderer(wrap_type=ClassificationClassSeparationPlot)
class ClassificationClassSeparationPlotRenderer(MetricRenderer):
    def render_html(self, obj: ClassificationClassSeparationPlot) -> List[BaseWidgetInfo]:
        current_plot = obj.get_result().current
        reference_plot = obj.get_result().reference
        target_name = obj.get_result().target_name
        if current_plot is None:
            return []
        # todo changing data here, consider doing this in calculation
        current_df = df_from_column_scatter(current_plot)
        current_df.replace([np.inf, -np.inf], np.nan, inplace=True)
        reference_df = None
        if reference_plot is not None:
            reference_df = df_from_column_scatter(reference_plot)
            reference_df.replace([np.inf, -np.inf], np.nan, inplace=True)

        tab_data = get_class_separation_plot_data(
            current_df,
            reference_df,
            target_name,
            color_options=self.color_options,
        )
        tabs = [TabData(name, widget) for name, widget in tab_data]
        return [
            header_text(label="Class Separation Quality"),
            widget_tabs(title="", tabs=tabs),
        ]
