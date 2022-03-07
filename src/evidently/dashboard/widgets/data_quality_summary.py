#!/usr/bin/env python
# coding: utf-8
import json
from typing import List
from typing import Optional
from typing import Tuple, Union
import pandas as pd
import numpy as np

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzerResults
from evidently.analyzers.data_quality_analyzer import FeatureQualityStats
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget

class DataQualitySummaryWidget(Widget):

    def analyzers(self):
        return [DataQualityAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        data_quality_results = DataQualityAnalyzer.get_results(analyzers_results)
        reference_stats = self._get_df_stats(data_quality_results, reference_data, 
                                             data_quality_results.reference_features_stats)
        if current_data is not None:
            current_stats = self._get_df_stats(data_quality_results, current_data, 
                                             data_quality_results.current_features_stats)
        else:
            current_stats = None

        if current_data is not None:
            metrics_values_headers = ["reference", "current"]

        else:
            metrics_values_headers = [""]

        stats_list = ['number of variables', 'number of observations', 'missing cells', 'categorical features', 
                      'numeric features', 'datetime features', 'constant features', 'empty features', 
                      'almost constant features', 'almost empty features']
        metrics = self._get_stats_with_names(stats_list, reference_stats, current_stats)

        wi = BaseWidgetInfo(
                type="expandable_list",
                title="",
                size=2,
                params={
                    "header": "Summary",
                    "description": "",
                    "metricsValuesHeaders": metrics_values_headers,
                    "metrics": metrics,
                    "graph": {},
                    "details": {},
                },
                # additionalGraphs=additional_graphs
            )
        return wi

    @staticmethod
    def _dict_for_metrics(label, ref_value, curr_value):
        values = [ref_value]
        if curr_value is not None: 
            values.append(curr_value)
        res = {
            "label": label,
            "values": values,
        }
        return res

    def _get_df_stats(self, data_quality_results, df: pd.DataFrame, df_stats: FeatureQualityStats):
        result = {}
        all_features = data_quality_results.columns.get_all_features_list(
            cat_before_num=True, include_datetime_feature=True
        )
        if data_quality_results.columns.utility_columns.date:
            all_features = [data_quality_results.columns.utility_columns.date] + all_features
        if data_quality_results.columns.utility_columns.target:
            all_features = [data_quality_results.columns.utility_columns.target] + all_features
        result['number of variables'] = len(all_features)
        result['number of observations'] = df.shape[0]
        missing_cells = df[all_features].isnull().sum()
        missing_cells_percentage = np.round(missing_cells / (df.shape[0]*df.shape[1]), 2)
        result['missing cells'] = f'{missing_cells} ({missing_cells_percentage}%)'
        result['categorical features'] = len(data_quality_results.columns.cat_feature_names)
        result['numeric features'] = len(data_quality_results.columns.num_feature_names)
        result['datetime features'] = len(data_quality_results.columns.datetime_feature_names)
        constant_values = pd.Series([df_stats[x].most_common_value_percentage for x in all_features])
        empty_values = pd.Series([df_stats[x].missing_percentage for x in all_features])
        result['constant features'] = (constant_values==1).sum()
        result['empty features'] = (empty_values==1).sum()
        result['almost constant features'] = (constant_values>=0.95).sum()
        result['almost empty features'] = (empty_values>=0.95).sum()
        return result

    @staticmethod
    def _get_stats_with_names(
        stats_list: List[str],
        reference_stats: dict,
        current_stats: Optional[dict],
    ) -> List[dict]:

        result = []

        for val in stats_list:
            values = [reference_stats[val]]

            if current_stats is not None:
                values.append(current_stats[val])

            result.append(
                {
                    "label": val,
                    "values": values,
                }
            )
        return result