#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.express as px

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget
from evidently.dashboard.widgets.utils import CutQuantileTransformer
from evidently.options import QualityMetricsOptions


class ClassConfusionBasedFeatureDistrTable(Widget):
    def analyzers(self):
        return [ClassificationPerformanceAnalyzer]

    @staticmethod
    def _get_rows_per_page(features_count: int) -> int:
        """How mane rows of features we want to show on one page. If we have many features - show 10 on one page"""
        return min(features_count, 10)

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = ClassificationPerformanceAnalyzer.get_results(analyzers_results)
        quality_metrics_options = self.options_provider.get(QualityMetricsOptions)
        cut_quantile = quality_metrics_options.cut_quantile
        target_name = results.columns.utility_columns.target
        prediction_name = results.columns.utility_columns.prediction
        rows_per_page = self._get_rows_per_page(results.columns.get_features_len())

        if target_name is None or results.columns.utility_columns.prediction is None:
            raise ValueError(f"Widget {self.title} requires 'target' and 'prediction' columns.")

        if current_data is not None:
            additional_graphs_data = []
            params_data = []

            for feature_name in results.columns.get_all_features_list(cat_before_num=False):
                # add data for table in params
                labels = sorted(set(reference_data[target_name]))

                params_data.append(
                    {
                        "details": {
                            "parts": [{"title": "All", "id": "All" + "_" + str(feature_name)}] + [
                                {"title": str(label), "id": feature_name + "_" + str(label)} for label in labels],
                            "insights": []
                        },
                        "f1": feature_name
                    }
                )

                # create confusion based plots
                reference_data['dataset'] = 'Reference'
                current_data['dataset'] = 'Current'
                if cut_quantile and quality_metrics_options.get_cut_quantile(feature_name):
                    side, q = quality_metrics_options.get_cut_quantile(feature_name)
                    cqt = CutQuantileTransformer(side=side, q=q)
                    cqt.fit(reference_data[feature_name])
                    reference_data_to_plot = cqt.transform_df(reference_data, feature_name)
                    current_data_to_plot = cqt.transform_df(current_data, feature_name)
                else:
                    reference_data_to_plot = reference_data
                    current_data_to_plot = current_data
                merged_data = pd.concat([reference_data_to_plot, current_data_to_plot])

                fig = px.histogram(merged_data, x=feature_name, color=target_name,
                                   facet_col="dataset", histnorm='', barmode='overlay',
                                   category_orders={"dataset": ["Reference", "Current"]})

                fig_json = json.loads(fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        "All" + "_" + str(feature_name),
                        {
                            "data": fig_json['data'],
                            "layout": fig_json['layout']
                        },
                    )
                )

                for label in labels:
                    def confusion_func(row, label=label):
                        return _confusion(row, target_name, prediction_name, label)

                    merged_data['Confusion'] = merged_data.apply(confusion_func, axis=1)

                    fig = px.histogram(
                        merged_data, x=feature_name, color='Confusion', facet_col="dataset",
                        histnorm='', barmode='overlay',
                        category_orders={
                            "dataset": ["Reference", "Current"],
                            "Confusion": ["TP", "TN", "FP", "FN"]
                        }
                    )
                    fig_json = json.loads(fig.to_json())

                    # write plot data in table as additional data
                    additional_graphs_data.append(
                        AdditionalGraphInfo(
                            feature_name + "_" + str(label),
                            {
                                "data": fig_json['data'],
                                "layout": fig_json['layout']
                            },
                        )
                    )

            return BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": rows_per_page,
                    "columns": [
                        {
                            "title": "Feature",
                            "field": "f1"
                        }
                    ],
                    "data": params_data
                },
                additionalGraphs=additional_graphs_data
            )
        # if no current data is set.
        additional_graphs_data = []
        params_data = []

        for feature_name in results.columns.get_all_features_list(cat_before_num=False):
            # add data for table in params
            labels = sorted(set(reference_data[target_name]))

            params_data.append(
                {
                    "details": {
                        "parts": [{"title": "All", "id": "All" + "_" + str(feature_name)}] + [
                            {"title": str(label), "id": feature_name + "_" + str(label)} for label in labels],
                        "insights": []
                    },
                    "f1": feature_name
                }
            )

            # create confusion based plots
            if cut_quantile and quality_metrics_options.get_cut_quantile(feature_name):
                side, q = quality_metrics_options.get_cut_quantile(feature_name)
                cqt = CutQuantileTransformer(side=side, q=q)
                cqt.fit(reference_data[feature_name])
                reference_data_to_plot = cqt.transform_df(reference_data, feature_name)
            else:
                reference_data_to_plot = reference_data

            fig = px.histogram(
                reference_data_to_plot, x=feature_name, color=target_name, histnorm='', barmode='overlay'
            )

            fig_json = json.loads(fig.to_json())

            # write plot data in table as additional data
            additional_graphs_data.append(
                AdditionalGraphInfo(
                    "All" + "_" + str(feature_name),
                    {
                        "data": fig_json['data'],
                        "layout": fig_json['layout']
                    },
                )
            )

            for label in labels:
                def _confusion_func(row, label=label):
                    return _confusion(row, target_name, prediction_name, label)

                reference_data['Confusion'] = reference_data.apply(_confusion_func, axis=1)

                fig = px.histogram(
                    reference_data_to_plot, x=feature_name, color='Confusion', histnorm='', barmode='overlay',
                    category_orders={"Confusion": ["TP", "TN", "FP", "FN"]}
                )

                fig_json = json.loads(fig.to_json())

                # write plot data in table as additional data
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + "_" + str(label),
                        {
                            "data": fig_json['data'],
                            "layout": fig_json['layout']
                        },
                    )
                )

        return BaseWidgetInfo(
            title=self.title,
            type="big_table",
            size=2,
            params={
                "rowsPerPage": rows_per_page,
                "columns": [
                    {
                        "title": "Feature",
                        "field": "f1"
                    }
                ],
                "data": params_data
            },
            additionalGraphs=additional_graphs_data
        )


def _confusion(row, target_column, prediction_column, label):
    if row[target_column] == label and row[prediction_column] == label:
        return 'TP'
    if row[target_column] != label and row[prediction_column] == label:
        return 'FP'
    if row[target_column] == label and row[prediction_column] != label:
        return 'FN'
    return 'TN'  # last option
