import json
import pandas as pd
import plotly.graph_objects as go
import requests
import zipfile
import io

from datetime import datetime
from typing import List, Dict, Tuple, Union, Optional

from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient


def detect_dataset_drift(reference, production, column_mapping, get_ratio=False):
    """
    Returns True if Data Drift is detected, else returns False.
    If get_ratio is True, returns the share of drifted features.
    The Data Drift detection depends on the confidence level and the threshold.
    For each individual feature Data Drift is detected with the selected confidence (default value is 0.95).
    Data Drift for the dataset is detected if share of the drifted features is above the selected threshold (default value is 0.5).
    """
    
    data_drift_report = Report(metrics=[
        DataDriftPreset(drift_share=0.4)
        ])
    data_drift_report.run(reference_data=reference, current_data=production, column_mapping=column_mapping)
    report = data_drift_report.as_dict()
    
    if get_ratio:
        return report["metrics"][0]["result"]["drift_share"]
    else:
        return report["metrics"][0]["result"]["dataset_drift"]
    
    
#evaluate data drift with Evidently Profile
def detect_features_drift(data_drift_report, column_mapping, get_scores=False):
    """
    Returns True if Data Drift is detected, else returns False. 
    If get_scores is True, returns scores value (like p-value) for each feature.
    The Data Drift detection depends on the confidence level and the threshold.
    For each individual feature Data Drift is detected with the selected confidence (default value is 0.95).
    """
    
    # data_drift_report = Report(metrics=[DataDriftPreset()])
    # data_drift_report.run(reference_data=reference, current_data=production, column_mapping=column_mapping)
    report = data_drift_report.as_dict()
    
    drifts = []
    num_features = column_mapping.numerical_features if column_mapping.numerical_features else []
    cat_features = column_mapping.categorical_features if column_mapping.categorical_features else []
    for feature in num_features + cat_features:
        drift_score = report["metrics"][1]["result"]["drift_by_columns"][feature]["drift_score"]
        if get_scores:
            drifts.append((feature, drift_score))
        else:
            drifts.append((feature, report["metrics"][1]["result"]["drift_by_columns"][feature]["drift_detected"]))
             
    return drifts
