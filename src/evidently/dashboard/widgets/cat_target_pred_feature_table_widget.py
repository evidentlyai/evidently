#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.express as px

from evidently import ColumnMapping
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer
from evidently.dashboard.widgets.utils import CutQuantileTransformer
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.options import QualityMetricsOptions


class CatTargetPredFeatureTable(Widget):
    @staticmethod
    def _get_rows_per_page(columns) -> int:
        return min(len(columns.num_feature_names) + len(columns.cat_feature_names), 10)

    def analyzers(self):
        return [CatTargetDriftAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:

        results = CatTargetDriftAnalyzer.get_results(analyzers_results)
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        cut_quantile = quality_metrics_options.cut_quantile

        if current_data is None:
            raise ValueError("current_data should be present")

        target_name = results.columns.utility_columns.target
        prediction_name = None
        if results.prediction_metrics:
            prediction_name = results.prediction_metrics.column_name

        if prediction_name is not None and target_name is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in results.columns.get_all_features_list(
                cat_before_num=False
            ):
                # add data for table in params
                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Target",
                                    "id": feature_name + "_target_values",
                                },
                                {
                                    "title": "Prediction",
                                    "id": feature_name + "_prediction_values",
                                },
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                    }
                )

                # create target plot
                reference_data["dataset"] = "Reference"
                current_data["dataset"] = "Current"
                quantile = quality_metrics_options.get_cut_quantile(feature_name)
                if cut_quantile and quantile is not None:
                    side, q = quantile
                    cqt = CutQuantileTransformer(side=side, q=q)
                    cqt.fit(reference_data[feature_name])
                    reference_data_to_plot = cqt.transform_df(
                        reference_data, feature_name
                    )
                    current_data_to_plot = cqt.transform_df(current_data, feature_name)
                else:
                    reference_data_to_plot = reference_data
                    current_data_to_plot = current_data
                merged_data = pd.concat([reference_data_to_plot, current_data_to_plot])

                target_fig = px.histogram(
                    merged_data,
                    x=feature_name,
                    color=target_name,
                    facet_col="dataset",
                    barmode="overlay",
                    category_orders={"dataset": ["Reference", "Current"]},
                )

                target_fig_json = json.loads(target_fig.to_json())

                # create prediction plot
                pred_fig = px.histogram(
                    merged_data,
                    x=feature_name,
                    color=prediction_name,
                    facet_col="dataset",
                    barmode="overlay",
                    category_orders={"dataset": ["Reference", "Current"]},
                )

                pred_fig_json = json.loads(pred_fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_target_values",
                        {
                            "data": target_fig_json["data"],
                            "layout": target_fig_json["layout"],
                        },
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_prediction_values",
                        {
                            "data": pred_fig_json["data"],
                            "layout": pred_fig_json["layout"],
                        },
                    )
                )

            return BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": self._get_rows_per_page(results.columns),
                    "columns": [{"title": "Feature", "field": "f1"}],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            )

        if target_name is not None:
            additional_graphs_data = []
            params_data = []

            for feature_name in results.columns.get_all_features_list(
                cat_before_num=False
            ):
                # add data for table in params
                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Target",
                                    "id": feature_name + "_target_values",
                                }
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                    }
                )

                # create target plot
                # TO DO%: out pf the cycle
                reference_data["dataset"] = "Reference"
                current_data["dataset"] = "Current"
                quantile = quality_metrics_options.get_cut_quantile(feature_name)
                if cut_quantile and quantile is not None:
                    side, q = quantile
                    cqt = CutQuantileTransformer(side=side, q=q)
                    cqt.fit(reference_data[feature_name])
                    reference_data_to_plot = cqt.transform_df(
                        reference_data, feature_name
                    )
                    current_data_to_plot = cqt.transform_df(current_data, feature_name)
                else:
                    reference_data_to_plot = reference_data
                    current_data_to_plot = current_data
                merged_data = pd.concat([reference_data_to_plot, current_data_to_plot])

                target_fig = px.histogram(
                    merged_data,
                    x=feature_name,
                    color=target_name,
                    facet_col="dataset",
                    barmode="overlay",
                    category_orders={"dataset": ["Reference", "Current"]},
                )

                target_fig_json = json.loads(target_fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_target_values",
                        {
                            "data": target_fig_json["data"],
                            "layout": target_fig_json["layout"],
                        },
                    )
                )

            return BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": self._get_rows_per_page(results.columns),
                    "columns": [{"title": "Feature", "field": "f1"}],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            )
        if results.columns.utility_columns.prediction is not None:
            additional_graphs_data = []
            params_data = []
            for feature_name in (
                results.columns.num_feature_names + results.columns.cat_feature_names
            ):
                # add data for table in params
                params_data.append(
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Prediction",
                                    "id": feature_name + "_prediction_values",
                                }
                            ],
                            "insights": [],
                        },
                        "f1": feature_name,
                    }
                )

                # create target plot
                reference_data["dataset"] = "Reference"
                current_data["dataset"] = "Current"
                quantile = quality_metrics_options.get_cut_quantile(feature_name)
                if cut_quantile and quantile is not None:
                    side, q = quantile
                    cqt = CutQuantileTransformer(side=side, q=q)
                    cqt.fit(reference_data[feature_name])
                    reference_data_to_plot = cqt.transform_df(
                        reference_data, feature_name
                    )
                    current_data_to_plot = cqt.transform_df(current_data, feature_name)
                else:
                    reference_data_to_plot = reference_data
                    current_data_to_plot = current_data
                merged_data = pd.concat([reference_data_to_plot, current_data_to_plot])

                prediction_fig = px.histogram(
                    merged_data,
                    x=feature_name,
                    barmode="overlay",
                    color=results.columns.utility_columns.prediction,
                    facet_col="dataset",
                    category_orders={"dataset": ["Reference", "Current"]},
                )

                prediction_fig_json = json.loads(prediction_fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_prediction_values",
                        {
                            "data": prediction_fig_json["data"],
                            "layout": prediction_fig_json["layout"],
                        },
                    )
                )

            return BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": self._get_rows_per_page(results.columns),
                    "columns": [{"title": "Feature", "field": "f1"}],
                    "data": params_data,
                },
                additionalGraphs=additional_graphs_data,
            )
        raise ValueError(
            f"Widget {self.title} require 'prediction' or 'target' columns not to be None"
        )
