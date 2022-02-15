#!/usr/bin/env python
# coding: utf-8
from typing import Dict, List
from typing import Optional
from typing import Union

from dataclasses import dataclass
import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.base_analyzer import Analyzer
from evidently.analyzers.utils import process_columns, DatasetUtilityColumns
# from evidently.options import QualityMetricsOptions
# from evidently.analyzers.utils import process_columns
# from evidently.analyzers.utils import DatasetColumns


@dataclass
class DataProfileAnalyzerResults:
    utility_columns: DatasetUtilityColumns
    cat_feature_names: List[str]
    num_feature_names: List[str]
    datetime_feature_names: List[str]
    ref_features_stats: Dict[str, Dict]
    curr_features_stats: Optional[Dict[str, Dict]]

class DataProfileAnalyzer(Analyzer):
    @staticmethod
    def get_results(analyzer_results) -> DataProfileAnalyzerResults:
        return analyzer_results[DataProfileAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping) -> DataProfileAnalyzerResults:
        columns = process_columns(reference_data, column_mapping)
        target_name = columns.utility_columns.target
        ref_features_stats = {}
        curr_features_stats = {}
        for feature_name in columns.num_feature_names:
            ref_features_stats[feature_name] = self._get_num_columns_stats(reference_data[feature_name])
            if current_data is not None:
                curr_features_stats[feature_name] = self._get_num_columns_stats(current_data[feature_name])

        for feature_name in columns.cat_feature_names:
            ref_features_stats[feature_name] = self._get_cat_columns_stats(reference_data[feature_name])
            if current_data is not None:
                curr_features_stats[feature_name] = self._get_cat_columns_stats(current_data[feature_name])
        
        if columns.utility_columns.date:
            date_list = columns.datetime_feature_names + [columns.utility_columns.date]
        else:
            date_list = columns.datetime_feature_names
        for feature_name in date_list:
            ref_features_stats[feature_name] = self._get_dt_columns_stats(reference_data[feature_name])
            if current_data is not None:
                curr_features_stats[feature_name] = self._get_dt_columns_stats(current_data[feature_name])
        
        if target_name:
            if column_mapping.task == 'classification':
                ref_features_stats[target_name] = self._get_cat_columns_stats(reference_data[target_name])
                if current_data is not None:
                    curr_features_stats[target_name] = self._get_cat_columns_stats(current_data[target_name])
            else:
                ref_features_stats[target_name] = self._get_num_columns_stats(reference_data[target_name])
                if current_data is not None:
                    curr_features_stats[target_name] = self._get_num_columns_stats(current_data[target_name])
            
        results = DataProfileAnalyzerResults(
                                             utility_columns=columns.utility_columns,
                                             cat_feature_names=columns.cat_feature_names,
                                             num_feature_names=columns.num_feature_names,
                                             datetime_feature_names=columns.datetime_feature_names,
                                             ref_features_stats=ref_features_stats,
                                             curr_features_stats=curr_features_stats)
        return results

    def _get_num_columns_stats(self, feature: pd.Series) -> Dict:
        res = dict(feature.describe().apply(lambda x: np.round(x, 2)))
        res['unique'] = feature.nunique()
        res['unique (%)'] = np.round(res['unique']/feature.shape[0], 2)
        value_counts = feature.value_counts(dropna=False)
        res['most common value'] = value_counts.index[0]
        res['most common value (%)'] = np.round(value_counts.iloc[0]/feature.shape[0], 2)
        if pd.isnull(res['most common value']) and res['count'] > 0:
            res['most common not null value'] = value_counts.index[1]
            res['most common not null value (%)'] = np.round(value_counts.iloc[1]/feature.shape[0], 2)
        res['missing'] = feature.isnull().sum()
        res['missing (%)'] = np.round(res['missing']/feature.shape[0], 2)
        res['infinite'] = np.sum(np.isinf(feature))
        res['infinite (%)'] = np.round(res['infinite']/feature.shape[0], 2)
        res['feature_type'] = 'num'
        return res

    def _get_cat_columns_stats(self, feature: pd.Series) -> Dict:
        res = {}
        res['count'] = feature.count()
        res['unique'] = feature.nunique()
        res['unique (%)'] = np.round(res['unique']/feature.shape[0], 2)
        value_counts = feature.value_counts(dropna=False)
        res['most common value'] = value_counts.index[0]
        res['most common value (%)'] = np.round(value_counts.iloc[0]/feature.shape[0], 2)
        if pd.isnull(res['most common value']) and res['count'] > 0:
            res['most common not null value'] = value_counts.index[1]
            res['most common not null value (%)'] = np.round(value_counts.iloc[1]/feature.shape[0], 2)
        res['missing'] = feature.isnull().sum()
        res['missing (%)'] = np.round(res['missing']/feature.shape[0], 2)
        res['feature_type'] = 'cat'
        return res

    def _get_dt_columns_stats(self, feature: pd.Series) -> Dict:
        res = {}
        res['count'] = feature.count()
        res['unique'] = feature.nunique()
        res['unique (%)'] = np.round(res['unique']/feature.shape[0], 2)
        value_counts = feature.value_counts(dropna=False)
        res['most common value'] = value_counts.index[0]
        res['most common value (%)'] = np.round(value_counts.iloc[0]/feature.shape[0], 2)
        if pd.isnull(res['most common value']) and res['count'] > 0:
            res['most common not null value'] = value_counts.index[1]
            res['most common not null value (%)'] = np.round(value_counts.iloc[1]/feature.shape[0], 2)
        res['missing'] = feature.isnull().sum()
        res['missing (%)'] = np.round(res['missing']/feature.shape[0], 2)
        res['first'] = feature.min()
        res['last'] = feature.max()
        res['feature_type'] = 'date'
        return res
    


