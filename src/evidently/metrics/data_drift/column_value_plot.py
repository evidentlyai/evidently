from typing import List
from typing import Optional

import numpy as np
import pandas as pd
from pandas.api.types import is_numeric_dtype
from plotly import graph_objs as go

from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.metric_results import ColumnScatter
from evidently.metric_results import column_scatter_from_df
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import WidgetSize
from evidently.renderers.html_widgets import plotly_figure
from evidently.utils.data_operations import process_columns


class ColumnValuePlotResults(MetricResult):
    class Config:
        smart_union = True
        dict_include = False
        pd_include = False

    column_name: str
    datetime_column_name: Optional[str]
    current: ColumnScatter
    reference: ColumnScatter


class ColumnValuePlot(Metric[ColumnValuePlotResults]):
    column_name: str

    def __init__(self, column_name: str):
        self.column_name = column_name

    def calculate(self, data: InputData) -> ColumnValuePlotResults:
        if self.column_name not in data.current_data.columns:
            raise ValueError(f"Column '{self.column_name}' should present in the current dataset")

        if data.reference_data is None:
            raise ValueError("Reference data should be present")

        if self.column_name not in data.reference_data.columns:
            raise ValueError(f"Column '{self.column_name}' should present in the reference dataset")

        dataset_columns = process_columns(data.current_data, data.column_mapping)
        if not (
            self.column_name in dataset_columns.num_feature_names
            or (
                self.column_name == dataset_columns.utility_columns.target
                and (data.column_mapping.task == "regression" or is_numeric_dtype(data.current_data[self.column_name]))
            )
            or (
                isinstance(dataset_columns.utility_columns.prediction, str)
                and self.column_name == dataset_columns.utility_columns.prediction
                and (data.column_mapping.task == "regression" or is_numeric_dtype(data.current_data[self.column_name]))
            )
        ):
            raise ValueError("Expected numerical feature")
        datetime_column_name = dataset_columns.utility_columns.date
        curr_df = data.current_data
        ref_df = data.reference_data
        curr_df = self._make_df_for_plot(curr_df, self.column_name, datetime_column_name)
        ref_df = self._make_df_for_plot(ref_df, self.column_name, datetime_column_name)
        return ColumnValuePlotResults(
            column_name=self.column_name,
            datetime_column_name=datetime_column_name,
            current=column_scatter_from_df(curr_df, True),
            reference=column_scatter_from_df(ref_df, True),
        )

    def _make_df_for_plot(self, df, column_name: str, datetime_column_name: Optional[str]):
        result = df.replace([np.inf, -np.inf], np.nan)
        if datetime_column_name is not None:
            result.dropna(
                axis=0,
                how="any",
                inplace=True,
                subset=[column_name, datetime_column_name],
            )
            return result.sort_values(datetime_column_name)
        result.dropna(axis=0, how="any", inplace=True, subset=[column_name])
        return result.sort_index()


@default_renderer(wrap_type=ColumnValuePlot)
class ColumnValuePlotRenderer(MetricRenderer):
    def render_html(self, obj: ColumnValuePlot) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current_scatter = result.current
        reference_scatter = result.reference
        column_name = result.column_name

        # todo: better typing
        column = reference_scatter[column_name]
        assert isinstance(column, pd.Series)
        mean_ref = column.mean()
        std_ref = column.std()
        y0 = mean_ref - std_ref
        y1 = mean_ref + std_ref

        if result.datetime_column_name is not None:
            curr_x = current_scatter[result.datetime_column_name]
            ref_x = reference_scatter[result.datetime_column_name]
            x_name = "Timestamp"

        else:
            curr_x = current_scatter["index"]
            ref_x = reference_scatter["index"]
            x_name = "Index"

        color_options = self.color_options

        fig = go.Figure()

        fig.add_trace(
            go.Scattergl(
                x=curr_x,
                y=current_scatter[column_name],
                mode="markers",
                name="Current",
                marker=dict(size=6, color=color_options.get_current_data_color()),
            )
        )
        fig.add_trace(
            go.Scattergl(
                x=ref_x,
                y=column,
                mode="markers",
                name="Reference",
                marker=dict(size=6, color=color_options.get_reference_data_color()),
            )
        )

        x0 = np.max(curr_x)

        fig.add_trace(
            go.Scattergl(
                x=[x0, x0],
                y=[y0, y1],
                mode="markers",
                name="Current",
                marker=dict(size=0.01, color=color_options.non_visible_color, opacity=0.005),
                showlegend=False,
            )
        )

        fig.update_layout(
            xaxis_title=x_name,
            yaxis_title=f"{column_name} value",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            shapes=[
                dict(
                    type="rect",
                    # x-reference is assigned to the x-values
                    xref="paper",
                    # y-reference is assigned to the plot paper [0,1]
                    yref="y",
                    x0=0,
                    y0=y0,
                    x1=1,
                    y1=y1,
                    fillcolor=color_options.fill_color,
                    opacity=0.5,
                    layer="below",
                    line_width=0,
                ),
                dict(
                    type="line",
                    name="Reference",
                    xref="paper",
                    yref="y",
                    x0=0,  # min(testset_agg_by_date.index),
                    y0=(y0 + y1) / 2,
                    x1=1,  # max(testset_agg_by_date.index),
                    y1=(y0 + y1) / 2,
                    line=dict(color=color_options.zero_line_color, width=3),
                ),
            ],
        )
        return [plotly_figure(title=f"Column '{column_name}' Values", figure=fig, size=WidgetSize.FULL)]
