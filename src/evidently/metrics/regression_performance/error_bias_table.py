import copy
import json
from typing import List
from typing import Optional

import dataclasses
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from evidently.calculations.regression_performance import error_bias_table
from evidently.calculations.regression_performance import error_with_quantiles
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.renderers.html_widgets import header_text
from evidently.utils.data_operations import process_columns


@dataclasses.dataclass
class RegressionErrorBiasTableResults:
    current_plot_data: pd.DataFrame
    reference_plot_data: Optional[pd.DataFrame]
    target_name: str
    prediction_name: str
    num_feature_names: List[str]
    cat_feature_names: List[str]
    error_bias: Optional[dict] = None
    columns: Optional[List[str]] = None


class RegressionErrorBiasTable(Metric[RegressionErrorBiasTableResults]):
    columns: Optional[List[str]]

    def __init__(self, columns: Optional[List[str]] = None):
        self.columns = columns

    def calculate(self, data: InputData) -> RegressionErrorBiasTableResults:
        dataset_columns = process_columns(data.current_data, data.column_mapping)
        target_name = dataset_columns.utility_columns.target
        prediction_name = dataset_columns.utility_columns.prediction
        curr_df = data.current_data
        ref_df = data.reference_data
        if self.columns is None:
            columns = list(curr_df.columns)
        else:
            columns = self.columns
        if target_name is None or prediction_name is None:
            raise ValueError("The columns 'target' and 'prediction' columns should be present")
        if not isinstance(prediction_name, str):
            raise ValueError("Expect one column for prediction. List of columns was provided.")
        num_feature_names = list(np.intersect1d(dataset_columns.num_feature_names, columns))
        cat_feature_names = list(np.intersect1d(dataset_columns.cat_feature_names, columns))
        columns_ext = np.union1d(columns, [target_name, prediction_name])
        curr_df = self._make_df_for_plot(curr_df[columns_ext], target_name, prediction_name, None)
        if ref_df is not None:
            ref_df = self._make_df_for_plot(ref_df[columns_ext], target_name, prediction_name, None)

        err_quantiles = error_with_quantiles(curr_df, prediction_name, target_name)
        feature_bias = error_bias_table(curr_df, err_quantiles, num_feature_names, cat_feature_names)
        error_bias = {
            feature: dict(feature_type=bias.feature_type, **bias.as_dict("current_"))
            for feature, bias in feature_bias.items()
        }

        if error_bias is not None:
            error_bias = copy.deepcopy(error_bias)

        else:
            error_bias = None

        if ref_df is not None:
            ref_err_quantiles = error_with_quantiles(ref_df, prediction_name, target_name)
            ref_feature_bias = error_bias_table(ref_df, ref_err_quantiles, num_feature_names, cat_feature_names)
            ref_error_bias = {
                feature: dict(feature_type=bias.feature_type, **bias.as_dict("ref_"))
                for feature, bias in ref_feature_bias.items()
            }
            if ref_error_bias is not None:
                if error_bias is not None:
                    for feature_name, reference_bias in ref_error_bias.items():
                        error_bias[feature_name].update(reference_bias)

                else:
                    error_bias = copy.deepcopy(ref_error_bias)

        if error_bias:
            error_bias_res = error_bias
        else:
            error_bias_res = {}

        columns = list(np.intersect1d(curr_df.columns, columns))

        return RegressionErrorBiasTableResults(
            current_plot_data=curr_df,
            reference_plot_data=ref_df,
            target_name=target_name,
            prediction_name=prediction_name,
            num_feature_names=[str(v) for v in num_feature_names],
            cat_feature_names=[str(v) for v in cat_feature_names],
            error_bias=error_bias_res,
            columns=[str(v) for v in columns],
        )

    @staticmethod
    def _make_df_for_plot(
        df: pd.DataFrame, target_name: str, prediction_name: str, datetime_column_name: Optional[str]
    ):
        result = df.replace([np.inf, -np.inf], np.nan)
        if datetime_column_name is not None:
            result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name, datetime_column_name])
            return result.sort_values(datetime_column_name)
        result.dropna(axis=0, how="any", inplace=True, subset=[target_name, prediction_name])
        return result.sort_index()


@default_renderer(wrap_type=RegressionErrorBiasTable)
class RegressionErrorBiasTableRenderer(MetricRenderer):
    def render_json(self, obj: RegressionErrorBiasTable) -> dict:
        result = dataclasses.asdict(obj.get_result())
        result.pop("current_plot_data", None)
        result.pop("reference_plot_data", None)
        return result

    def render_html(self, obj: RegressionErrorBiasTable) -> List[BaseWidgetInfo]:
        result = obj.get_result()
        current_data = result.current_plot_data
        reference_data = result.reference_plot_data
        target_name = result.target_name
        prediction_name = result.prediction_name

        if reference_data is not None:
            ref_error = reference_data[prediction_name] - reference_data[target_name]
            current_error = current_data[prediction_name] - current_data[target_name]

            ref_quntile_5 = np.quantile(ref_error, 0.05)
            ref_quntile_95 = np.quantile(ref_error, 0.95)

            current_quntile_5 = np.quantile(current_error, 0.05)
            current_quntile_95 = np.quantile(current_error, 0.95)

            # create subplots
            reference_data["dataset"] = "Reference"
            reference_data["Error bias"] = list(map(self._error_bias_string(ref_quntile_5, ref_quntile_95), ref_error))

            current_data["dataset"] = "Current"
            current_data["Error bias"] = list(
                map(self._error_bias_string(current_quntile_5, current_quntile_95), current_error)
            )
            merged_data = pd.concat([reference_data, current_data])

            reference_data.drop(["dataset", "Error bias"], axis=1, inplace=True)
            current_data.drop(["dataset", "Error bias"], axis=1, inplace=True)

            params_data = []
            additional_graphs_data = []

            for feature_name in result.num_feature_names:
                feature_type = "num"

                feature_hist = px.histogram(
                    merged_data,
                    x=feature_name,
                    color="Error bias",
                    facet_col="dataset",
                    histnorm="percent",
                    barmode="overlay",
                    category_orders={
                        "dataset": ["Reference", "Current"],
                        "Error bias": ["Underestimation", "Overestimation", "Majority"],
                    },
                )

                feature_hist_json = json.loads(feature_hist.to_json())

                segment_fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

                segment_fig.add_trace(
                    go.Scatter(
                        x=reference_data[target_name],
                        y=reference_data[prediction_name],
                        mode="markers",
                        marker=dict(
                            size=6,
                            cmax=max(max(reference_data[feature_name]), max(current_data[feature_name])),
                            cmin=min(min(reference_data[feature_name]), min(current_data[feature_name])),
                            color=reference_data[feature_name],
                        ),
                        showlegend=False,
                    ),
                    row=1,
                    col=1,
                )

                segment_fig.add_trace(
                    go.Scatter(
                        x=current_data[target_name],
                        y=current_data[prediction_name],
                        mode="markers",
                        marker=dict(
                            size=6,
                            cmax=max(max(reference_data[feature_name]), max(current_data[feature_name])),
                            cmin=min(min(reference_data[feature_name]), min(current_data[feature_name])),
                            color=current_data[feature_name],
                            colorbar=dict(title=feature_name),
                        ),
                        showlegend=False,
                    ),
                    row=1,
                    col=2,
                )

                # Update xaxis properties
                segment_fig.update_xaxes(title_text="Actual Value", showgrid=True, row=1, col=1)
                segment_fig.update_xaxes(title_text="Actual Value", showgrid=True, row=1, col=2)

                # Update yaxis properties
                segment_fig.update_yaxes(title_text="Predicted Value", showgrid=True, row=1, col=1)
                segment_fig.update_yaxes(title_text="Predicted Value", showgrid=True, row=1, col=2)

                segment_json = json.loads(segment_fig.to_json())

                if result.error_bias is None:
                    raise ValueError("RegressionErrorBiasTableRenderer got no error_bias value")

                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {"title": "Error bias", "id": feature_name + "_hist"},
                                {"title": "Predicted vs Actual", "id": feature_name + "_segm"},
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": round(result.error_bias[feature_name]["ref_majority"], 2),
                        "f4": round(result.error_bias[feature_name]["ref_under"], 2),
                        "f5": round(result.error_bias[feature_name]["ref_over"], 2),
                        "f6": round(result.error_bias[feature_name]["ref_range"], 2),
                        "f7": round(result.error_bias[feature_name]["current_majority"], 2),
                        "f8": round(result.error_bias[feature_name]["current_under"], 2),
                        "f9": round(result.error_bias[feature_name]["current_over"], 2),
                        "f10": round(result.error_bias[feature_name]["current_range"], 2),
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_hist",
                        {"data": feature_hist_json["data"], "layout": feature_hist_json["layout"]},
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_segm", {"data": segment_json["data"], "layout": segment_json["layout"]}
                    )
                )

            for feature_name in result.cat_feature_names:
                feature_type = "cat"

                feature_hist = px.histogram(
                    merged_data,
                    x=feature_name,
                    color="Error bias",
                    facet_col="dataset",
                    histnorm="percent",
                    barmode="overlay",
                    category_orders={
                        "dataset": ["Reference", "Current"],
                        "Error bias": ["Underestimation", "Overestimation", "Majority"],
                    },
                )

                feature_hist_json = json.loads(feature_hist.to_json())

                segment_fig = px.scatter(
                    merged_data, x=target_name, y=prediction_name, color=feature_name, facet_col="dataset"
                )

                segment_json = json.loads(segment_fig.to_json())

                if result.error_bias is None:
                    raise ValueError("RegressionErrorBiasTableRenderer got no error_bias value")

                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {"title": "Error bias", "id": feature_name + "_hist"},
                                {"title": "Predicted vs Actual", "id": feature_name + "_segm"},
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": str(result.error_bias[feature_name]["ref_majority"]),
                        "f4": str(result.error_bias[feature_name]["ref_under"]),
                        "f5": str(result.error_bias[feature_name]["ref_over"]),
                        "f6": str(result.error_bias[feature_name]["ref_range"]),
                        "f7": str(result.error_bias[feature_name]["current_majority"]),
                        "f8": str(result.error_bias[feature_name]["current_under"]),
                        "f9": str(result.error_bias[feature_name]["current_over"]),
                        "f10": int(result.error_bias[feature_name]["current_range"]),
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_hist",
                        {"data": feature_hist_json["data"], "layout": feature_hist_json["layout"]},
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_segm", {"data": segment_json["data"], "layout": segment_json["layout"]}
                    )
                )
            if result.columns is None:
                size = 0
            else:
                size = len(result.columns)
            widget_info = BaseWidgetInfo(
                title="",
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": min(size, 10),
                    "columns": [
                        {"title": "Feature", "field": "f1"},
                        {"title": "Type", "field": "f2"},
                        {"title": "REF: Majority", "field": "f3"},
                        {"title": "REF: Under", "field": "f4"},
                        {"title": "REF: Over", "field": "f5"},
                        {"title": "REF: Range(%)", "field": "f6"},
                        {"title": "CURR: Majority", "field": "f7"},
                        {"title": "CURR: Under", "field": "f8"},
                        {"title": "CURR: Over", "field": "f9"},
                        {"title": "CURR: Range(%)", "field": "f10", "sort": "desc"},
                    ],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            )

        else:
            error = current_data[prediction_name] - current_data[target_name]

            quntile_5 = np.quantile(error, 0.05)
            quntile_95 = np.quantile(error, 0.95)

            current_data["Error bias"] = list(
                map(
                    lambda x: "Underestimation"
                    if x <= quntile_5
                    else "Majority"
                    if x < quntile_95
                    else "Overestimation",
                    error,
                )
            )

            params_data = []
            additional_graphs_data = []

            for feature_name in result.num_feature_names:  # + cat_feature_names: #feature_names:

                feature_type = "num"

                hist = px.histogram(
                    current_data,
                    x=feature_name,
                    color="Error bias",
                    histnorm="percent",
                    barmode="overlay",
                    category_orders={"Error bias": ["Underestimation", "Overestimation", "Majority"]},
                )

                hist_figure = json.loads(hist.to_json())

                segm = px.scatter(current_data, x=target_name, y=prediction_name, color=feature_name)
                segm_figure = json.loads(segm.to_json())

                if result.error_bias is None:
                    raise ValueError("Widget RegressionErrorBiasTableRenderer got no error_bias value")

                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {"title": "Error bias", "id": feature_name + "_hist"},
                                {"title": "Predicted vs Actual", "id": feature_name + "_segm"},
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": round(result.error_bias[feature_name]["current_majority"], 2),
                        "f4": round(result.error_bias[feature_name]["current_under"], 2),
                        "f5": round(result.error_bias[feature_name]["current_over"], 2),
                        "f6": round(result.error_bias[feature_name]["current_range"], 2),
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_hist", {"data": hist_figure["data"], "layout": hist_figure["layout"]}
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_segm", {"data": segm_figure["data"], "layout": segm_figure["layout"]}
                    )
                )

            for feature_name in result.cat_feature_names:  # feature_names:

                feature_type = "cat"

                hist = px.histogram(
                    current_data,
                    x=feature_name,
                    color="Error bias",
                    histnorm="percent",
                    barmode="overlay",
                    category_orders={"Error bias": ["Underestimation", "Overestimation", "Majority"]},
                )

                hist_figure = json.loads(hist.to_json())

                initial_type = current_data[feature_name].dtype
                current_data[feature_name] = current_data[feature_name].astype(str)
                segm = px.scatter(current_data, x=target_name, y=prediction_name, color=feature_name)
                current_data[feature_name] = current_data[feature_name].astype(initial_type)

                segm_figure = json.loads(segm.to_json())

                if result.error_bias is None:
                    raise ValueError("RegressionErrorBiasTableRenderer got no error_bias value")

                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {"title": "Error bias", "id": feature_name + "_hist"},
                                {"title": "Predicted vs Actual", "id": feature_name + "_segm"},
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": str(result.error_bias[feature_name]["current_majority"]),
                        "f4": str(result.error_bias[feature_name]["current_under"]),
                        "f5": str(result.error_bias[feature_name]["current_over"]),
                        "f6": str(result.error_bias[feature_name]["current_range"]),
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_hist", {"data": hist_figure["data"], "layout": hist_figure["layout"]}
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_segm", {"data": segm_figure["data"], "layout": segm_figure["layout"]}
                    )
                )

            current_data.drop("Error bias", axis=1, inplace=True)

            if result.columns is None:
                size = 0
            else:
                size = len(result.columns)

            widget_info = BaseWidgetInfo(
                title="",
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": min(size, 10),
                    "columns": [
                        {"title": "Feature", "field": "f1"},
                        {"title": "Type", "field": "f2"},
                        {"title": "Majority", "field": "f3"},
                        {"title": "Underestimation", "field": "f4"},
                        {"title": "Overestimation", "field": "f5"},
                        {"title": "Range(%)", "field": "f6", "sort": "desc"},
                    ],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            )
        return [header_text(label="Error Bias: Mean/Most Common Feature Value per Group"), widget_info]

    @staticmethod
    def _error_bias_string(quantile_5, quantile_95):
        def __error_bias_string(error):
            if error <= quantile_5:
                return "Underestimation"
            if error < quantile_95:
                return "Majority"
            return "Overestimation"

        return __error_bias_string
