#!/usr/bin/env python
# coding: utf-8

import json
from typing import Optional

import pandas as pd
import plotly.express as px

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.widgets.widget import Widget


class ClassConfusionBasedFeatureDistrTable(Widget):
    def analyzers(self):
        return [ClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[ClassificationPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            raise ValueError(f"Widget {self.title} requires 'target' and 'prediction' columns.")
        if current_data is not None:

            additional_graphs_data = []
            params_data = []

            for feature_name in results['num_feature_names'] + results['cat_feature_names']:
                # add data for table in params
                labels = sorted(set(reference_data[results['utility_columns']['target']]))

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
                merged_data = pd.concat([reference_data, current_data])

                fig = px.histogram(merged_data, x=feature_name, color=results['utility_columns']['target'],
                                   facet_col="dataset", histnorm='',
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
                        return _confusion(row, results['utility_columns']['target'],
                                          results['utility_columns']['prediction'], label)

                    merged_data['Confusion'] = merged_data.apply(confusion_func, axis=1)

                    fig = px.histogram(merged_data, x=feature_name, color='Confusion', facet_col="dataset",
                                       histnorm='',
                                       category_orders={"dataset": ["Reference", "Current"],
                                                        "Confusion": ["TP", "TN", "FP", "FN"]})
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
                    "rowsPerPage": min(len(results['num_feature_names']) + len(results['cat_feature_names']), 10),
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

        for feature_name in results['num_feature_names'] + results['cat_feature_names']:
            # add data for table in params
            labels = sorted(set(reference_data[results['utility_columns']['target']]))

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
            fig = px.histogram(reference_data, x=feature_name, color=results['utility_columns']['target'],
                               histnorm='')

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
                    return _confusion(row, results['utility_columns']['target'],
                                      results['utility_columns']['prediction'], label)

                reference_data['Confusion'] = reference_data.apply(_confusion_func, axis=1)

                fig = px.histogram(reference_data, x=feature_name, color='Confusion', histnorm='',
                                   category_orders={"Confusion": ["TP", "TN", "FP", "FN"]})

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
                "rowsPerPage": min(len(results['num_feature_names']) + len(results['cat_feature_names']), 10),
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
