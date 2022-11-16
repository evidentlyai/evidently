import json
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from pandas.api.types import is_string_dtype
from plotly.subplots import make_subplots

from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class TargetByFeaturesTableResults:
    current_plot_data: pd.DataFrame
    reference_plot_data: pd.DataFrame
    target_name: Optional[str]
    curr_predictions: Optional[PredictionData]
    ref_predictions: Optional[PredictionData]
    columns: List[str]
    task: str


class TargetByFeaturesTable(Metric[TargetByFeaturesTableResults]):
    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def calculate(self, data: InputData) -> TargetByFeaturesTableResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        if target_name is None and prediction_name is None:
            raise ValueError("The columns 'target' or 'prediction' should be present")
        if data.reference_data is None:
            raise ValueError("Reference data should be present")
        curr_df = data.current_data.copy()
        ref_df = data.reference_data.copy()
        curr_predictions = None
        ref_predictions = None
        if prediction_name is not None:
            curr_predictions = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
            ref_predictions = get_prediction_data(data.reference_data, dataset_columns, data.column_mapping.pos_label)

        if self.columns is None:
            columns = dataset_columns.num_feature_names + dataset_columns.cat_feature_names
        else:
            columns = list(
                np.intersect1d(self.columns, dataset_columns.num_feature_names + dataset_columns.cat_feature_names)
            )
        if data.column_mapping.task is not None:
            task = data.column_mapping.task
        else:
            if target_name is not None:
                if curr_df[target_name].nunique() < 5 or is_string_dtype(curr_df[target_name]):
                    task = "classification"
                else:
                    task = "regression"
            else:
                raise ValueError("Task parameter of column_mapping should be specified")

        return TargetByFeaturesTableResults(
            current_plot_data=curr_df,
            reference_plot_data=ref_df,
            curr_predictions=curr_predictions,
            ref_predictions=ref_predictions,
            columns=columns,
            target_name=target_name,
            task=task,
        )


@default_renderer(wrap_type=TargetByFeaturesTable)
class TargetByFeaturesTableRenderer(MetricRenderer):
    def render_json(self, obj: TargetByFeaturesTable) -> dict:
        return {}

    def render_html(self, obj: TargetByFeaturesTable) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current_data = result.current_plot_data
        reference_data = result.reference_plot_data
        target_name = result.target_name
        curr_predictions = result.curr_predictions
        ref_predictions = result.ref_predictions
        columns = result.columns
        task = result.task

        if curr_predictions is not None and ref_predictions is not None:
            current_data["prediction_labels"] = curr_predictions.predictions.values
            reference_data["prediction_labels"] = ref_predictions.predictions.values

        additional_graphs_data = []
        params_data = []

        for feature_name in columns:
            # add data for table in params
            parts = []

            if target_name is not None:
                parts.append({"title": "Target", "id": feature_name + "_target_values"})
                if task == "regression":
                    target_fig = self._get_regression_fig(feature_name, target_name, current_data, reference_data)
                else:
                    target_fig = self._get_classification_fig(feature_name, target_name, current_data, reference_data)

                target_fig_json = json.loads(target_fig.to_json())

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_target_values",
                        {"data": target_fig_json["data"], "layout": target_fig_json["layout"]},
                    )
                )

            if curr_predictions is not None:
                parts.append({"title": "Prediction", "id": feature_name + "_prediction_values"})
                if task == "regression":
                    preds_fig = self._get_regression_fig(
                        feature_name, "prediction_labels", current_data, reference_data
                    )
                else:
                    preds_fig = self._get_classification_fig(
                        feature_name, "prediction_labels", current_data, reference_data
                    )
                preds_fig_json = json.loads(preds_fig.to_json())

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_prediction_values",
                        {"data": preds_fig_json["data"], "layout": preds_fig_json["layout"]},
                    )
                )

            params_data.append(
                {
                    "details": {
                        "parts": parts,
                        "insights": [],
                    },
                    "f1": feature_name,
                }
            )
        return [
            BaseWidgetInfo(
                title="Target (Prediction) Behavior By Feature",
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": min(len(columns), 10),
                    "columns": [{"title": "Feature", "field": "f1"}],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            )
        ]

    def _get_regression_fig(self, feature_name: str, main_column: str, curr_data: pd.DataFrame, ref_data: pd.DataFrame):
        fig = make_subplots(rows=1, cols=2, subplot_titles=("Current", "Reference"), shared_yaxes=True)
        fig.add_trace(
            go.Scattergl(
                x=curr_data[feature_name],
                y=curr_data[main_column],
                mode="markers",
                name="current",
                marker=dict(size=6, color=self.color_options.primary_color),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(
                x=ref_data[feature_name],
                y=ref_data[main_column],
                mode="markers",
                name="reference",
                marker=dict(size=6, color=self.color_options.secondary_color),
            ),
            row=1,
            col=2,
        )
        fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=1)
        fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=2)
        fig.update_yaxes(title_text=main_column, showgrid=True, row=1, col=1)

        return fig

    def _get_classification_fig(
        self, feature_name: str, main_column: str, curr_data: pd.DataFrame, ref_data: pd.DataFrame
    ):
        curr = curr_data.copy()
        ref = ref_data.copy()
        ref["dataset"] = "Reference"
        curr["dataset"] = "Current"
        merged_data = pd.concat([ref, curr])
        fig = px.histogram(
            merged_data,
            x=feature_name,
            color=main_column,
            facet_col="dataset",
            barmode="overlay",
            category_orders={"dataset": ["Current", "Reference"]},
        )

        return fig
