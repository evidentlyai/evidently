import json
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently.calculations.classification_performance import PredictionData
from evidently.calculations.classification_performance import get_prediction_data
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class ClassificationQualityByFeatureTableResults:
    current_plot_data: pd.DataFrame
    reference_plot_data: Optional[pd.DataFrame]
    target_name: str
    curr_predictions: PredictionData
    ref_predictions: Optional[PredictionData]
    columns: List[str]


class ClassificationQualityByFeatureTable(Metric[ClassificationQualityByFeatureTableResults]):
    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def calculate(self, data: InputData) -> ClassificationQualityByFeatureTableResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        curr_df = data.current_data.copy()
        ref_df = None
        if data.reference_data is not None:
            ref_df = data.reference_data.copy()
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' should be present")
        curr_predictions = get_prediction_data(data.current_data, dataset_columns, data.column_mapping.pos_label)
        ref_predictions = None
        if ref_df is not None:
            ref_predictions = get_prediction_data(data.reference_data, dataset_columns, data.column_mapping.pos_label)
        if self.columns is None:
            columns = dataset_columns.num_feature_names + dataset_columns.cat_feature_names
        else:
            columns = list(
                np.intersect1d(self.columns, dataset_columns.num_feature_names + dataset_columns.cat_feature_names)
            )

        return ClassificationQualityByFeatureTableResults(
            current_plot_data=curr_df,
            reference_plot_data=ref_df,
            curr_predictions=curr_predictions,
            ref_predictions=ref_predictions,
            columns=columns,
            target_name=target_name,
        )


@default_renderer(wrap_type=ClassificationQualityByFeatureTable)
class ClassificationQualityByFeatureTableRenderer(MetricRenderer):
    def render_json(self, obj: ClassificationQualityByFeatureTable) -> dict:
        return {}

    def render_html(self, obj: ClassificationQualityByFeatureTable) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current_data = result.current_plot_data
        reference_data = result.reference_plot_data
        target_name = result.target_name
        curr_predictions = result.curr_predictions
        ref_predictions = result.ref_predictions
        columns = result.columns
        labels = curr_predictions.labels

        color_options = self.color_options

        current_data["prediction_labels"] = curr_predictions.predictions.values

        if reference_data is not None and ref_predictions is not None:
            reference_data["prediction_labels"] = ref_predictions.predictions.values

        additional_graphs_data = []
        params_data = []
        for feature_name in columns:
            # add data for table in params

            params_data.append(
                {
                    "details": {
                        "parts": [{"title": "All", "id": "All" + "_" + str(feature_name)}]
                        + [{"title": str(label), "id": feature_name + "_" + str(label)} for label in labels],
                        "insights": [],
                    },
                    "f1": feature_name,
                }
            )

            # create confusion based plots
            current_data["dataset"] = "Current"
            merged_data = current_data
            facet_col: Optional[str] = None
            category_orders: Optional[dict] = None
            if reference_data is not None:
                reference_data["dataset"] = "Reference"
                merged_data = pd.concat([reference_data, current_data])
                facet_col = "dataset"
                category_orders = {"dataset": ["Current", "Reference"]}

            fig = px.histogram(
                merged_data,
                x=feature_name,
                color=target_name,
                facet_col=facet_col,
                histnorm="",
                barmode="overlay",
                category_orders=category_orders,
            )

            fig_json = json.loads(fig.to_json())

            # write plot data in table as additional data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    "All" + "_" + str(feature_name),
                    {"data": fig_json["data"], "layout": fig_json["layout"]},
                )
            )

            # Probas plots
            if curr_predictions.prediction_probas is not None:
                ref_columns = columns + ["prediction_labels", target_name]
                current_data = pd.concat([current_data[ref_columns], curr_predictions.prediction_probas], axis=1)
                if (
                    reference_data is not None
                    and ref_predictions is not None
                    and ref_predictions.prediction_probas is not None
                ):
                    reference_data = pd.concat([reference_data[ref_columns], ref_predictions.prediction_probas], axis=1)

                if reference_data is not None:
                    cols = 2
                    subplot_titles = ["current", "reference"]
                else:
                    cols = 1
                    subplot_titles = [""]

                for label in labels:
                    fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles, shared_yaxes=True)

                    # current Prediction
                    fig.add_trace(
                        go.Scatter(
                            x=current_data[current_data[target_name] == label][feature_name],
                            y=current_data[current_data[target_name] == label][label],
                            mode="markers",
                            name=str(label),
                            legendgroup=str(label),
                            marker=dict(
                                size=6,
                                # set color equal to a variable
                                color=color_options.get_current_data_color(),
                            ),
                        ),
                        row=1,
                        col=1,
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=current_data[current_data[target_name] != label][feature_name],
                            y=current_data[current_data[target_name] != label][label],
                            mode="markers",
                            name="other",
                            legendgroup="other",
                            marker=dict(
                                size=6,
                                # set color equal to a variable
                                color=color_options.get_reference_data_color(),
                            ),
                        ),
                        row=1,
                        col=1,
                    )

                    fig.update_xaxes(title_text=feature_name, showgrid=True, row=1, col=1)

                    # REF
                    if reference_data is not None:
                        fig.add_trace(
                            go.Scatter(
                                x=reference_data[reference_data[target_name] == label][feature_name],
                                y=reference_data[reference_data[target_name] == label][label],
                                mode="markers",
                                name=str(label),
                                legendgroup=str(label),
                                showlegend=False,
                                marker=dict(size=6, color=color_options.get_current_data_color()),
                            ),
                            row=1,
                            col=2,
                        )

                        fig.add_trace(
                            go.Scatter(
                                x=reference_data[reference_data[target_name] != label][feature_name],
                                y=reference_data[reference_data[target_name] != label][label],
                                mode="markers",
                                name="other",
                                legendgroup="other",
                                showlegend=False,
                                marker=dict(size=6, color=color_options.get_reference_data_color()),
                            ),
                            row=1,
                            col=2,
                        )
                        fig.update_xaxes(title_text=feature_name, row=1, col=2)

                    fig.update_layout(
                        yaxis_title="Probability",
                        yaxis=dict(range=(-0.1, 1.1), showticklabels=True),
                    )

                    fig_json = json.loads(fig.to_json())

                    # write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            feature_name + "_" + str(label),
                            {"data": fig_json["data"], "layout": fig_json["layout"]},
                        )
                    )
            # labels plots
            else:
                for label in labels:

                    def confusion_func(row, label=label):
                        return self._confusion(row, target_name, "prediction_labels", label)

                    merged_data["Confusion"] = merged_data.apply(confusion_func, axis=1)

                    fig = px.histogram(
                        merged_data,
                        x=feature_name,
                        color="Confusion",
                        facet_col=facet_col,
                        histnorm="",
                        barmode="overlay",
                        category_orders=category_orders,
                    )
                    fig_json = json.loads(fig.to_json())

                    # write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            feature_name + "_" + str(label),
                            {"data": fig_json["data"], "layout": fig_json["layout"]},
                        )
                    )
        return [
            header_text(label="Classification Quality By Feature"),
            BaseWidgetInfo(
                title="",
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": min(len(columns), 10),
                    "columns": [{"title": "Feature", "field": "f1"}],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            ),
        ]

    def _confusion(self, row, target_column, prediction_column, label):
        if row[target_column] == label and row[prediction_column] == label:
            return "TP"
        if row[target_column] != label and row[prediction_column] == label:
            return "FP"
        if row[target_column] == label and row[prediction_column] != label:
            return "FN"
        return "TN"  # last option
