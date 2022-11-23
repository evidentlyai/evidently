import json
from typing import List
from typing import Optional
from typing import Union

import dataclasses
import numpy as np
import pandas as pd
from plotly import graph_objs as go
from plotly.subplots import make_subplots
from scipy.stats import probplot

from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class RegressionErrorNormalityResults:
    current_error: pd.Series
    reference_error: Optional[pd.Series]


class RegressionErrorNormality(Metric[RegressionErrorNormalityResults]):
    def calculate(self, data: InputData) -> RegressionErrorNormalityResults:
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
        current_error = curr_df[prediction_name] - curr_df[target_name]
        reference_error = None
        if ref_df is not None:
            ref_df = self._make_df_for_plot(ref_df, target_name, prediction_name, None)
            reference_error = ref_df[prediction_name] - ref_df[target_name]
        return RegressionErrorNormalityResults(current_error=current_error, reference_error=reference_error)

    def _make_df_for_plot(self, df, target_name: str, prediction_name: str, datetime_column_name: Optional[str]):
        result = df.replace([np.inf, -np.inf], np.nan)
        if datetime_column_name is not None:
            result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name, datetime_column_name])
            return result.sort_values(datetime_column_name)
        result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name])
        return result.sort_index()


@default_renderer(wrap_type=RegressionErrorNormality)
class RegressionErrorNormalityRenderer(MetricRenderer):
    def render_json(self, obj: RegressionErrorNormality) -> dict:
        return {}

    def render_html(self, obj: RegressionErrorNormality) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current_error = result.current_error
        reference_error = result.reference_error
        color_options = self.color_options
        cols = 1
        subplot_titles: Union[list, str] = ""

        if reference_error is not None:
            cols = 2
            subplot_titles = ["current", "reference"]

        fig = make_subplots(rows=1, cols=cols, shared_yaxes=False, subplot_titles=subplot_titles)
        curr_qq_lines = probplot(current_error, dist="norm", plot=None)
        curr_theoretical_q_x = np.linspace(curr_qq_lines[0][0][0], curr_qq_lines[0][0][-1], 100)
        sample_quantile_trace = go.Scatter(
            x=curr_qq_lines[0][0],
            y=curr_qq_lines[0][1],
            mode="markers",
            name="Dataset Quantiles",
            legendgroup="Dataset Quantiles",
            marker=dict(size=6, color=color_options.primary_color),
        )

        theoretical_quantile_trace = go.Scatter(
            x=curr_theoretical_q_x,
            y=curr_qq_lines[1][0] * curr_theoretical_q_x + curr_qq_lines[1][1],
            mode="lines",
            name="Theoretical Quantiles",
            legendgroup="Theoretical Quantiles",
            marker=dict(size=6, color=color_options.secondary_color),
        )
        fig.add_trace(sample_quantile_trace, 1, 1)
        fig.add_trace(theoretical_quantile_trace, 1, 1)
        fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=1)
        if reference_error is not None:
            ref_qq_lines = probplot(reference_error, dist="norm", plot=None)
            ref_theoretical_q_x = np.linspace(ref_qq_lines[0][0][0], ref_qq_lines[0][0][-1], 100)
            sample_quantile_trace = go.Scatter(
                x=ref_qq_lines[0][0],
                y=ref_qq_lines[0][1],
                mode="markers",
                name="Dataset Quantiles",
                legendgroup="Dataset Quantiles",
                showlegend=False,
                marker=dict(size=6, color=color_options.primary_color),
            )

            theoretical_quantile_trace = go.Scatter(
                x=ref_theoretical_q_x,
                y=ref_qq_lines[1][0] * ref_theoretical_q_x + ref_qq_lines[1][1],
                mode="lines",
                name="Theoretical Quantiles",
                legendgroup="Theoretical Quantiles",
                showlegend=False,
                marker=dict(size=6, color=color_options.secondary_color),
            )
            fig.add_trace(sample_quantile_trace, 1, 2)
            fig.add_trace(theoretical_quantile_trace, 1, 2)
            fig.update_xaxes(title_text="Theoretical Quantiles", row=1, col=2)
        fig.update_layout(yaxis_title="Dataset Quantiles")
        fig = json.loads(fig.to_json())

        return [
            header_text(label="Error Normality"),
            BaseWidgetInfo(
                title="",
                size=2,
                type="big_graph",
                params={"data": fig["data"], "layout": fig["layout"]},
            ),
        ]
