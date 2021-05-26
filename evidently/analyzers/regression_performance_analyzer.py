#!/usr/bin/env python
# coding: utf-8

from evidently.analyzers.base_analyzer import Analyzer
import pandas as pd
from pandas.api.types import is_numeric_dtype
import numpy as np

from scipy.stats import ks_2samp, chisquare, probplot
from sklearn import metrics

class RegressionPerformanceAnalyzer(Analyzer):
    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping):
        result = dict()
        if column_mapping:
            date_column = column_mapping.get('datetime')
            id_column = column_mapping.get('id')
            target_column = column_mapping.get('target')
            prediction_column = column_mapping.get('prediction')
            num_feature_names = column_mapping.get('numerical_features')
            target_names = column_mapping.get('target_names')
            if num_feature_names is None:
                num_feature_names = []
            else:
                num_feature_names = [name for name in num_feature_names if is_numeric_dtype(reference_data[name])] 

            cat_feature_names = column_mapping.get('categorical_features')
            if cat_feature_names is None:
                cat_feature_names = []
            else:
                cat_feature_names = [name for name in cat_feature_names if is_numeric_dtype(reference_data[name])] 
        
        else:
            date_column = 'datetime' if 'datetime' in reference_data.columns else None
            id_column = None
            target_column = 'target' if 'target' in reference_data.columns else None
            prediction_column = 'prediction' if 'prediction' in reference_data.columns else None

            utility_columns = [date_column, id_column, target_column, prediction_column]

            num_feature_names = list(set(reference_data.select_dtypes([np.number]).columns) - set(utility_columns))
            cat_feature_names = list(set(reference_data.select_dtypes([np.object]).columns) - set(utility_columns))

            target_names = None

        result["utility_columns"] = {'date':date_column, 'id':id_column, 'target':target_column, 'prediction':prediction_column}
        result["cat_feature_names"] = cat_feature_names
        result["num_feature_names"] = num_feature_names

        result['metrics'] = {}
        if target_column is not None and prediction_column is not None:
            reference_data.replace([np.inf, -np.inf], np.nan, inplace=True)
            reference_data.dropna(axis=0, how='any', inplace=True)
            
            #calculate quality metrics
            me = np.mean(reference_data[prediction_column] - reference_data[target_column])
            sde = np.std(reference_data[prediction_column] - reference_data[target_column], ddof = 1)

            abs_err = np.abs(reference_data[prediction_column] - reference_data[target_column])
            mae = np.mean(abs_err)
            sdae = np.std(abs_err, ddof = 1)

            abs_perc_err = 100.*np.abs(reference_data[prediction_column] - reference_data[target_column])/reference_data[target_column]
            mape = np.mean(abs_perc_err)
            sdape = np.std(abs_perc_err, ddof = 1)

            result['metrics']['reference'] = {'mean_error':float(me), 'mean_abs_error':float(mae), 'mean_abs_perc_error':float(mape),
                'error_std':float(sde), 'abs_error_std':float(sdae), 'abs_perc_error_std':float(sdape)}

            #error normality
            error = reference_data[prediction_column] - reference_data[target_column] 
            qq_lines = probplot(error, dist="norm", plot=None)
            theoretical_q_x = np.linspace(qq_lines[0][0][0], qq_lines[0][0][-1], 100)

            qq_dots = [t.tolist() for t in qq_lines[0]]
            qq_line = list(qq_lines[1])

            result['metrics']['reference']['error_normality'] = {'order_statistic_medians':[float(x) for x in qq_dots[0]], 
                'order_statistic_medians':[float(x) for x in qq_dots[1]], 'slope':float(qq_line[0]), 'intercept':float(qq_line[1]), 'r':float(qq_line[2])}

            #underperformance metrics
            quantile_5 = np.quantile(error, .05)
            quantile_95 = np.quantile(error, .95)

            mae = np.mean(error)
            mae_under = np.mean(error[error <= quantile_5])
            mae_exp = np.mean(error[(error > quantile_5) & (error < quantile_95)])
            mae_over = np.mean(error[error >= quantile_95])

            sd = np.std(error, ddof = 1)
            sd_under = np.std(error[error <= quantile_5], ddof = 1)
            sd_exp = np.std(error[(error > quantile_5) & (error < quantile_95)], ddof = 1)
            sd_over = np.std(error[error >= quantile_95], ddof = 1)

            result['metrics']['reference']['underperformance'] = {}
            result['metrics']['reference']['underperformance']['majority'] = {'mean_error':float(mae_exp), 'std_error':float(sd_exp)}
            result['metrics']['reference']['underperformance']['underestimation'] = {'mean_error':float(mae_under), 'std_error':float(sd_under)}
            result['metrics']['reference']['underperformance']['overestimation'] = {'mean_error':float(mae_over), 'std_error':float(sd_over)}
            
            if production_data is not None:
                production_data.replace([np.inf, -np.inf], np.nan, inplace=True)
                production_data.dropna(axis=0, how='any', inplace=True)
            
                #calculate quality metrics
                me = np.mean(production_data[prediction_column] - production_data[target_column])
                sde = np.std(production_data[prediction_column] - production_data[target_column], ddof = 1)

                abs_err = np.abs(production_data[prediction_column] - production_data[target_column])
                mae = np.mean(abs_err)
                sdae = np.std(abs_err, ddof = 1)

                abs_perc_err = 100.*np.abs(production_data[prediction_column] - production_data[target_column])/production_data[target_column]
                mape = np.mean(abs_perc_err)
                sdape = np.std(abs_perc_err, ddof = 1)

                result['metrics']['current'] = {'mean_error':float(me), 'mean_abs_error':float(mae), 'mean_abs_perc_error':float(mape),
                'error_std':float(sde), 'abs_error_std':float(sdae), 'abs_perc_error_std':float(sdape)}

                #error normality
                prod_error = production_data[prediction_column] - production_data[target_column] 
                qq_lines = probplot(prod_error, dist="norm", plot=None)
                theoretical_q_x = np.linspace(qq_lines[0][0][0], qq_lines[0][0][-1], 100)

                qq_dots = [t.tolist() for t in qq_lines[0]]
                qq_line = list(qq_lines[1])

                result['metrics']['current']['error_normality'] = {'order_statistic_medians':[float(x) for x in qq_dots[0]], 
                'order_statistic_medians':[float(x) for x in qq_dots[1]], 'slope':float(qq_line[0]), 'intercept':float(qq_line[1]), 'r':float(qq_line[2])}

                #underperformance metrics
                prod_quantile_5 = np.quantile(prod_error, .05)
                prod_quantile_95 = np.quantile(prod_error, .95)

                prod_mae = np.mean(prod_error)
                prod_mae_under = np.mean(prod_error[prod_error <= prod_quantile_5])
                prod_mae_exp = np.mean(prod_error[(prod_error > prod_quantile_5) & (prod_error < prod_quantile_95)])
                prod_mae_over = np.mean(prod_error[prod_error >= prod_quantile_95])

                prod_sd = np.std(prod_error, ddof = 1)
                prod_sd_under = np.std(prod_error[prod_error <= prod_quantile_5], ddof = 1)
                prod_sd_exp = np.std(prod_error[(prod_error > prod_quantile_5) & (prod_error < prod_quantile_95)], ddof = 1)
                prod_sd_over = np.std(prod_error[prod_error >= prod_quantile_95], ddof = 1)

                result['metrics']['current']['underperformance'] = {}
                result['metrics']['current']['underperformance']['majority'] = {'mean_error':float(prod_mae_exp), 'std_error':float(prod_sd_exp)}
                result['metrics']['current']['underperformance']['underestimation'] = {'mean_error':float(prod_mae_under), 'std_error':float(prod_sd_under)}
                result['metrics']['current']['underperformance']['overestimation'] = {'mean_error':float(prod_mae_over), 'std_error':float(prod_sd_over)}

                #error bias table
                error_bias = {}
                for feature_name in num_feature_names:
                    feature_type = 'num'

                    ref_overal_value = np.mean(reference_data[feature_name])
                    ref_under_value = np.mean(reference_data[error <= quantile_5][feature_name])
                    ref_expected_value = np.mean(reference_data[(error > quantile_5) & (error < quantile_95)][feature_name])
                    ref_over_value = np.mean(reference_data[error >= quantile_95][feature_name])
                    ref_range_value = 0 if ref_over_value == ref_under_value else 100*abs(ref_over_value - ref_under_value)/(np.max(reference_data[feature_name]) - np.min(reference_data[feature_name]))

                    prod_overal_value = np.mean(production_data[feature_name])
                    prod_under_value = np.mean(production_data[prod_error <= prod_quantile_5][feature_name])
                    prod_expected_value = np.mean(production_data[(prod_error > prod_quantile_5) & (prod_error < prod_quantile_95)][feature_name])
                    prod_over_value = np.mean(production_data[prod_error >= prod_quantile_95][feature_name])
                    prod_range_value = 0 if prod_over_value == prod_under_value else 100*abs(prod_over_value - prod_under_value)/(np.max(production_data[feature_name]) - np.min(production_data[feature_name]))

                    error_bias[feature_name] = {'feature_type':feature_type, 'ref_majority':float(ref_expected_value), 'ref_under':float(ref_under_value), 
                        'ref_over':float(ref_over_value), 'ref_range':float(ref_range_value),'prod_majority':float(prod_expected_value), 'prod_under':float(prod_under_value), 
                        'prod_over':float(prod_over_value), 'prod_range':float(prod_range_value)}

                for feature_name in cat_feature_names:
                    feature_type = 'cat'

                    ref_overal_value = reference_data[feature_name].value_counts().idxmax()
                    ref_under_value = reference_data[error <= quantile_5][feature_name].value_counts().idxmax()
                    ref_over_value = reference_data[error >= quantile_95][feature_name].value_counts().idxmax()
                    ref_range_value = 1 if (ref_overal_value != ref_under_value) or (ref_over_value != ref_overal_value) \
                       or (ref_under_value != ref_overal_value) else 0

                    prod_overal_value = production_data[feature_name].value_counts().idxmax()
                    prod_under_value = production_data[prod_error <= prod_quantile_5][feature_name].value_counts().idxmax()
                    prod_over_value = production_data[prod_error >= prod_quantile_95][feature_name].value_counts().idxmax()
                    prod_range_value = 1 if (prod_overal_value != prod_under_value) or (prod_over_value != prod_overal_value) \
                       or (prod_under_value != prod_overal_value) else 0

                    error_bias[feature_name] = {'feature_type':feature_type, 'ref_majority':float(ref_overal_value), 'ref_under':float(ref_under_value), 
                        'ref_over':float(ref_over_value), 'ref_range':float(ref_range_value),'prod_majority':float(prod_overal_value), 'prod_under':float(prod_under_value), 
                        'prod_over':float(prod_over_value), 'prod_range':float(prod_range_value)}

                result['metrics']['error_bias'] = error_bias

        return result
