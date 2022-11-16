from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns
from evidently.utils.visualizations import plot_scatter


@dataclasses.dataclass
class RegressionPredictedVsActualScatterResults:
    current_scatter: Dict[str, pd.Series]
    reference_scatter: Optional[Dict[str, pd.Series]]


class RegressionPredictedVsActualScatter(Metric[RegressionPredictedVsActualScatterResults]):
    def calculate(self, data: InputData) -> RegressionPredictedVsActualScatterResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        curr_df = data.current_data
        ref_df = data.reference_data
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        if not isinstance(prediction_name, str):
            raise ValueError("Expect one column for prediction. List of columns was provided.")
        curr_df = self._make_df_for_plot(curr_df, target_name, prediction_name, None)
        current_scatter = {}
        current_scatter["predicted"] = curr_df[prediction_name]
        current_scatter["actual"] = curr_df[target_name]
        reference_scatter: Optional[dict] = None
        if data.reference_data is not None:
            ref_df = self._make_df_for_plot(ref_df, target_name, prediction_name, None)
            reference_scatter = {}
            reference_scatter["predicted"] = ref_df[prediction_name]
            reference_scatter["actual"] = ref_df[target_name]
        return RegressionPredictedVsActualScatterResults(
            current_scatter=current_scatter, reference_scatter=reference_scatter
        )

    def _make_df_for_plot(self, df, target_name: str, prediction_name: str, datetime_column_name: Optional[str]):
        result = df.replace([np.inf, -np.inf], np.nan)
        if datetime_column_name is not None:
            result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name, datetime_column_name])
            return result.sort_values(datetime_column_name)
        result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name])
        return result.sort_index()


@default_renderer(wrap_type=RegressionPredictedVsActualScatter)
class RegressionPredictedVsActualScatterRenderer(MetricRenderer):
    def render_json(self, obj: RegressionPredictedVsActualScatter) -> dict:
        return {}

    def render_html(self, obj: RegressionPredictedVsActualScatter) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current_scatter = result.current_scatter
        reference_scatter = None
        if result.reference_scatter is not None:
            reference_scatter = result.reference_scatter
        fig = plot_scatter(
            curr=current_scatter,
            ref=reference_scatter,
            x="actual",
            y="predicted",
            xaxis_name="Actual value",
            yaxis_name="Predicted value",
            color_options=self.color_options,
        )
        return [
            header_text(label="Predicted vs Actual"),
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            ),
        ]
