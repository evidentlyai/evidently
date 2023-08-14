from sre_constants import SUCCESS
from typing import Text, Any, Dict

from evidently import ColumnMapping
from evidently.metrics import (
    RegressionQualityMetric,
    RegressionPredictedVsActualScatter,
    RegressionPredictedVsActualPlot,
    RegressionErrorPlot,
    RegressionAbsPercentageErrorPlot,
    RegressionErrorDistribution,
    RegressionErrorNormality,
    
)
from evidently.metric_preset import TargetDriftPreset, DataDriftPreset
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.tests import TestValueMeanError, TestValueMAE
import pandas as pd


def build_regression_quality_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping
) -> Any:

    model_report = Report(metrics=[
        RegressionQualityMetric(),
    ])
    model_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    
    return model_report

def get_regression_quality_metrics(
    regression_quality_report: Report
) -> Dict:

    metrics = {} 
    report_dict = regression_quality_report.as_dict()
    
    metrics['me'] = report_dict['metrics'][0]['result']['current']['mean_error']
    metrics['mae'] = report_dict['metrics'][0]['result']['current']["mean_abs_error"]
    
    return metrics

def build_data_drift_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping, 
    drift_share=0.4) -> Report:
    """
    Returns a list with pairs (feature_name, drift_score)
    Drift Score depends on the selected statistical test or distance and the threshold
    """    
    data_drift_report = Report(metrics=[
        DataDriftPreset(drift_share=drift_share)
        ])
    data_drift_report.run(reference_data=reference_data, current_data=current_data, column_mapping=column_mapping)

    return data_drift_report

def get_data_drift_metrics(report: Dict) -> Dict:
    """
    Returns a list with pairs (feature_name, drift_score)
    Drift Score depends on the selected statistical test or distance and the threshold
    """ 
    metrics = {}   
    report_dict = report.as_dict()
    
    for metric in ['dataset_drift', 
                   'number_of_drifted_columns', 
                   'share_of_drifted_columns']: 
        metrics.update({metric: report_dict["metrics"][0]["result"][metric]})

    return metrics



def build_model_performance_test_report(
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping
    ) -> Report:
    """
    Returns a list with pairs (feature_name, drift_score)
    Drift Score depends on the selected statistical test or distance and the threshold
    """    
    regression_performance_test = TestSuite(tests=[
        TestValueMeanError(lte=10, gte=-10),
        TestValueMAE(lte=15),
    ])

    regression_performance_test.run(
        reference_data=None, 
        current_data=current_data,
        column_mapping=column_mapping,
    )

    return regression_performance_test

def get_test_status(report) -> Dict:
    """
    Returns a list with pairs (feature_name, drift_score)
    Drift Score depends on the selected statistical test or distance and the threshold
    """ 
    FAIL = 0
    SUCCESS = 1
    
    for test in report.as_dict()['tests']:
        if test['status'] is 'FAIL':
            return FAIL

    return SUCCESS


def build_model_monitoring_report(
    reference_data: pd.DataFrame,
    current_data: pd.DataFrame,
    column_mapping: ColumnMapping
) -> Any:

    model_report = Report(metrics=[
        RegressionQualityMetric(),
        RegressionErrorPlot(),
        RegressionErrorDistribution()
    ])
    model_report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    
    return model_report

def get_model_monitoring_metrics(
    regression_quality_report: Report
) -> Dict:

    metrics = {} 
    report_dict = regression_quality_report.as_dict()
    
    metrics['me'] = report_dict['metrics'][0]['result']['current']['mean_error']
    metrics['mae'] = report_dict['metrics'][0]['result']['current']["mean_abs_error"]
    metrics['rmse'] = report_dict['metrics'][0]['result']['current']["rmse"]
    metrics['mape'] = report_dict['metrics'][0]['result']['current']["mean_abs_perc_error"]
    
    return metrics