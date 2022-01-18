#!/usr/bin/env python
# coding: utf-8
import json
from typing import Optional

import pandas as pd
import numpy as np

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.regression_performance_analyzer import RegressionPerformanceAnalyzer
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget


def _error_bias_string(quantile_5, quantile_95):
    def __error_bias_string(error):
        if error <= quantile_5:
            return 'Underestimation'
        if error < quantile_95:
            return 'Majority'
        return 'Overestimation'
    return __error_bias_string


class UnderperformSegmTableWidget(Widget):
    def analyzers(self):
        return [RegressionPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:

        results = analyzers_results[RegressionPerformanceAnalyzer]

        if results['utility_columns']['target'] is None or results['utility_columns']['prediction'] is None:
            raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns.")

        widget_info = None
        if current_data is not None:
            current_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            current_data.dropna(axis=0, how='any', inplace=True)

            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            ref_error = reference_data[results['utility_columns']['prediction']] - reference_data[
                results['utility_columns']['target']]
            current_error = current_data[results['utility_columns']['prediction']] - current_data[
                results['utility_columns']['target']]

            ref_quntile_5 = np.quantile(ref_error, .05)
            ref_quntile_95 = np.quantile(ref_error, .95)

            current_quntile_5 = np.quantile(current_error, .05)
            current_quntile_95 = np.quantile(current_error, .95)

            # create subplots
            reference_data['dataset'] = 'Reference'
            reference_data['Error bias'] = list(map(_error_bias_string(ref_quntile_5, ref_quntile_95), ref_error))

            current_data['dataset'] = 'Current'
            current_data['Error bias'] = list(map(_error_bias_string(current_quntile_5, current_quntile_95),
                                                  current_error))
            merged_data = pd.concat([reference_data, current_data])

            reference_data.drop(['dataset', 'Error bias'], axis=1, inplace=True)
            current_data.drop(['dataset', 'Error bias'], axis=1, inplace=True)

            params_data = []
            additional_graphs_data = []

            for feature_name in results["num_feature_names"]:
                feature_type = 'num'

                feature_hist = px.histogram(merged_data, x=feature_name, color='Error bias', facet_col="dataset",
                                            histnorm='percent', barmode='overlay',
                                            category_orders={"dataset": ["Reference", "Current"],
                                                             "Error bias": ["Underestimation", "Overestimation",
                                                                            "Majority"]})

                feature_hist_json = json.loads(feature_hist.to_json())

                segment_fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

                segment_fig.add_trace(
                    go.Scatter(
                        x=reference_data[results['utility_columns']['target']],
                        y=reference_data[results['utility_columns']['prediction']],
                        mode='markers',
                        marker=dict(
                            size=6,
                            cmax=max(max(reference_data[feature_name]), max(current_data[feature_name])),
                            cmin=min(min(reference_data[feature_name]), min(current_data[feature_name])),
                            color=reference_data[feature_name],
                        ),
                        showlegend=False,
                    ),
                    row=1, col=1
                )

                segment_fig.add_trace(
                    go.Scatter(
                        x=current_data[results['utility_columns']['target']],
                        y=current_data[results['utility_columns']['prediction']],
                        mode='markers',
                        marker=dict(
                            size=6,
                            cmax=max(max(reference_data[feature_name]), max(current_data[feature_name])),
                            cmin=min(min(reference_data[feature_name]), min(current_data[feature_name])),
                            color=current_data[feature_name],
                            colorbar=dict(
                                title=feature_name
                            ),
                        ),
                        showlegend=False,
                    ),
                    row=1, col=2
                )

                # Update xaxis properties
                segment_fig.update_xaxes(title_text="Actual Value", showgrid=True, row=1, col=1)
                segment_fig.update_xaxes(title_text="Actual Value", showgrid=True, row=1, col=2)

                # Update yaxis properties
                segment_fig.update_yaxes(title_text="Predicted Value", showgrid=True, row=1, col=1)
                segment_fig.update_yaxes(title_text="Predicted Value", showgrid=True, row=1, col=2)

                segment_json = json.loads(segment_fig.to_json())

                params_data.append(
                    {
                        "details":
                            {
                                "parts": [
                                    {
                                        "title": "Error bias",
                                        "id": feature_name + "_hist"
                                    },
                                    {
                                        "title": "Predicted vs Actual",
                                        "id": feature_name + "_segm"
                                    }

                                ],
                                "insights": []
                            },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": round(results['metrics']['error_bias'][feature_name]['ref_majority'], 2),
                        "f4": round(results['metrics']['error_bias'][feature_name]['ref_under'], 2),
                        "f5": round(results['metrics']['error_bias'][feature_name]['ref_over'], 2),
                        "f6": round(results['metrics']['error_bias'][feature_name]['ref_range'], 2),
                        "f7": round(results['metrics']['error_bias'][feature_name]['current_majority'], 2),
                        "f8": round(results['metrics']['error_bias'][feature_name]['current_under'], 2),
                        "f9": round(results['metrics']['error_bias'][feature_name]['current_over'], 2),
                        "f10": round(results['metrics']['error_bias'][feature_name]['current_range'], 2)
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_hist',
                        {
                            "data": feature_hist_json['data'],
                            "layout": feature_hist_json['layout']
                        }
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_segm',
                        {
                            "data": segment_json['data'],
                            "layout": segment_json['layout']
                        }
                    )
                )

            for feature_name in results["cat_feature_names"]:
                feature_type = 'cat'

                feature_hist = px.histogram(merged_data, x=feature_name, color='Error bias', facet_col="dataset",
                                            histnorm='percent', barmode='overlay',
                                            category_orders={"dataset": ["Reference", "Current"],
                                                             "Error bias": ["Underestimation", "Overestimation",
                                                                            "Majority"]})

                feature_hist_json = json.loads(feature_hist.to_json())

                segment_fig = make_subplots(rows=1, cols=2, subplot_titles=("Reference", "Current"))

                segment_fig.add_trace(
                    go.Scatter(
                        x=reference_data[results['utility_columns']['target']],
                        y=reference_data[results['utility_columns']['prediction']],
                        mode='markers',
                        marker=dict(
                            size=6,
                            cmax=max(max(reference_data[feature_name]), max(current_data[feature_name])),
                            cmin=min(min(reference_data[feature_name]), min(current_data[feature_name])),
                            color=reference_data[feature_name],
                        ),
                        showlegend=False,
                    ),
                    row=1, col=1
                )

                segment_fig.add_trace(
                    go.Scatter(
                        x=current_data[results['utility_columns']['target']],
                        y=current_data[results['utility_columns']['prediction']],
                        mode='markers',
                        marker=dict(
                            size=6,
                            cmax=max(max(reference_data[feature_name]), max(current_data[feature_name])),
                            cmin=min(min(reference_data[feature_name]), min(current_data[feature_name])),
                            color=current_data[feature_name],
                            colorbar=dict(
                                title=feature_name
                            ),
                        ),
                        showlegend=False,
                    ),
                    row=1, col=2
                )

                # Update xaxis properties
                segment_fig.update_xaxes(title_text="Actual Value", showgrid=True, row=1, col=1)
                segment_fig.update_xaxes(title_text="Actual Value", showgrid=True, row=1, col=2)

                # Update yaxis properties
                segment_fig.update_yaxes(title_text="Predicted Value", showgrid=True, row=1, col=1)
                segment_fig.update_yaxes(title_text="Predicted Value", showgrid=True, row=1, col=2)

                segment_json = json.loads(segment_fig.to_json())

                params_data.append(
                    {
                        "details":
                            {
                                "parts": [
                                    {
                                        "title": "Error bias",
                                        "id": feature_name + "_hist"
                                    },
                                    {
                                        "title": "Predicted vs Actual",
                                        "id": feature_name + "_segm"
                                    }
                                ],
                                "insights": []
                            },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": str(results['metrics']['error_bias'][feature_name]['ref_majority']),
                        "f4": str(results['metrics']['error_bias'][feature_name]['ref_under']),
                        "f5": str(results['metrics']['error_bias'][feature_name]['ref_over']),
                        "f6": str(results['metrics']['error_bias'][feature_name]['ref_range']),
                        "f7": str(results['metrics']['error_bias'][feature_name]['current_majority']),
                        "f8": str(results['metrics']['error_bias'][feature_name]['current_under']),
                        "f9": str(results['metrics']['error_bias'][feature_name]['current_over']),
                        "f10": int(results['metrics']['error_bias'][feature_name]['current_range'])
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_hist',
                        {
                            "data": feature_hist_json['data'],
                            "layout": feature_hist_json['layout']
                        }
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_segm',
                        {
                            "data": segment_json['data'],
                            "layout": segment_json['layout']
                        }
                    )
                )

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": min(len(results["num_feature_names"]) + len(results["cat_feature_names"]), 10),
                    "columns": [
                        {
                            "title": "Feature",
                            "field": "f1"
                        },
                        {
                            "title": "Type",
                            "field": "f2"
                        },
                        {
                            "title": "REF: Majority",
                            "field": "f3"
                        },
                        {
                            "title": "REF: Under",
                            "field": "f4"
                        },
                        {
                            "title": "REF: Over",
                            "field": "f5"
                        },
                        {
                            "title": "REF: Range(%)",
                            "field": "f6"
                        },
                        {
                            "title": "CURR: Majority",
                            "field": "f7"
                        },
                        {
                            "title": "CURR: Under",
                            "field": "f8"
                        },
                        {
                            "title": "CURR: Over",
                            "field": "f9"
                        },
                        {
                            "title": "CURR: Range(%)",
                            "field": "f10",
                            "sort": "desc"
                        }

                    ],
                    "data": params_data
                },
                additionalGraphs=additional_graphs_data
            )

        else:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)

            error = reference_data[results['utility_columns']['prediction']] - reference_data[
                results['utility_columns']['target']]

            quntile_5 = np.quantile(error, .05)
            quntile_95 = np.quantile(error, .95)

            reference_data['Error bias'] = reference_data['Error bias'] = list(
                map(lambda x: 'Underestimation'
                              if x <= quntile_5 else 'Majority'
                              if x < quntile_95 else 'Overestimation', error))

            params_data = []
            additional_graphs_data = []

            for feature_name in results["num_feature_names"]:  # + cat_feature_names: #feature_names:

                feature_type = 'num'

                hist = px.histogram(reference_data, x=feature_name, color='Error bias', histnorm='percent',
                                    barmode='overlay',
                                    category_orders={"Error bias": ["Underestimation", "Overestimation", "Majority"]})

                hist_figure = json.loads(hist.to_json())

                segm = px.scatter(reference_data, x=results['utility_columns']['target'],
                                  y=results['utility_columns']['prediction'], color=feature_name)
                segm_figure = json.loads(segm.to_json())

                params_data.append(
                    {
                        "details":
                            {
                                "parts": [
                                    {
                                        "title": "Error bias",
                                        "id": feature_name + "_hist"
                                    },
                                    {
                                        "title": "Predicted vs Actual",
                                        "id": feature_name + "_segm"
                                    }

                                ],
                                "insights": []
                            },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": round(results['metrics']['error_bias'][feature_name]['ref_majority'], 2),
                        "f4": round(results['metrics']['error_bias'][feature_name]['ref_under'], 2),
                        "f5": round(results['metrics']['error_bias'][feature_name]['ref_over'], 2),
                        "f6": round(results['metrics']['error_bias'][feature_name]['ref_range'], 2)
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_hist',
                        {
                            "data": hist_figure['data'],
                            "layout": hist_figure['layout']
                        }
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_segm',
                        {
                            "data": segm_figure['data'],
                            "layout": segm_figure['layout']
                        }
                    )
                )

            for feature_name in results["cat_feature_names"]:  # feature_names:

                feature_type = 'cat'

                hist = px.histogram(reference_data, x=feature_name, color='Error bias', histnorm='percent',
                                    barmode='overlay',
                                    category_orders={"Error bias": ["Underestimation", "Overestimation", "Majority"]})

                hist_figure = json.loads(hist.to_json())

                initial_type = reference_data[feature_name].dtype
                reference_data[feature_name] = reference_data[feature_name].astype(str)
                segm = px.scatter(reference_data, x=results['utility_columns']['target'],
                                  y=results['utility_columns']['prediction'], color=feature_name)
                reference_data[feature_name] = reference_data[feature_name].astype(initial_type)

                segm_figure = json.loads(segm.to_json())

                params_data.append(
                    {
                        "details":
                            {
                                "parts": [
                                    {
                                        "title": "Error bias",
                                        "id": feature_name + "_hist"
                                    },
                                    {
                                        "title": "Predicted vs Actual",
                                        "id": feature_name + "_segm"
                                    }
                                ],
                                "insights": []
                            },
                        "f1": feature_name,
                        "f2": feature_type,
                        "f3": str(results['metrics']['error_bias'][feature_name]['ref_majority']),
                        "f4": str(results['metrics']['error_bias'][feature_name]['ref_under']),
                        "f5": str(results['metrics']['error_bias'][feature_name]['ref_over']),
                        "f6": str(results['metrics']['error_bias'][feature_name]['ref_range'])
                    }
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_hist',
                        {
                            "data": hist_figure['data'],
                            "layout": hist_figure['layout']
                        }
                    )
                )

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name + '_segm',
                        {
                            "data": segm_figure['data'],
                            "layout": segm_figure['layout']
                        }
                    )
                )

            reference_data.drop('Error bias', axis=1, inplace=True)

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=2,
                params={
                    "rowsPerPage": min(len(results["num_feature_names"]) + len(results["cat_feature_names"]), 10),
                    "columns": [
                        {
                            "title": "Feature",
                            "field": "f1"
                        },
                        {
                            "title": "Type",
                            "field": "f2"
                        },
                        {
                            "title": "Majority",
                            "field": "f3"
                        },
                        {
                            "title": "Underestimation",
                            "field": "f4"
                        },
                        {
                            "title": "Overestimation",
                            "field": "f5"
                        },
                        {
                            "title": "Range(%)",
                            "field": "f6",
                            "sort": "desc"
                        }
                    ],
                    "data": params_data
                },
                additionalGraphs=additional_graphs_data
            )
        return widget_info
