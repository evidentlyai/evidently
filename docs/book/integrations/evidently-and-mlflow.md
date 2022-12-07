---
description: Log Evidently metrics in the MLflow UI.
---

# Evidently and MLflow

**TL;DR:** You can use Evidently to calculate metrics, and MLflow Tracking to log and view the results. 

Jupyter notebook with en example:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/mlflow_logging/mlflow_integration.ipynb" %}

# **Overview**

Many machine learning teams use [MLflow](https://www.mlflow.org) for experiment management, deployment, and as a model registry. If you are already familiar with MLflow, you can integrate it with Evidently to **track the performance of your models**.

In this case, you use **Evidently to calculate the metrics** and **MLflow to log the results**. You can then access the metrics in the MLflow interface.

# **How it works**

Evidently calculates a rich set of metrics and statistical tests. You can choose any of the [pre-built reports](../reports/) or combine [individual metrics](../reference/all-metrics.md) to define what you want to measure. For example, you can evaluate prediction drift and feature drift together.

You can then generate the calculation output **in a JSON format**. You should explicitly define which parts of the output to send to **MLflow Tracking**.

## Tutorial 1: Evaluating Data Drift with **MLFlow and Evidently**

In this tutorial, you will use Evidently to check input features for [Data Drift](../reports/data-drift.md) and log and visualize the results with MLflow.

Here is a Jupyter notebook with the example:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/mlflow_logging/mlflow_integration.ipynb" %}

In case of any discrepancies refer to the example notebook as a source of truth.

## **Step 1. Install MLflow and Evidently**

Evidently is available as a PyPI package:

```
$ pip install evidently
```

To install MLflow, run:

```
$ pip install mlflow
```

Or install MLflow with scikit-learn via

```
$pip install mlflow[extras] 
```

For more details, refer to MLflow [documentation](https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html#id5).

## Step 2. Load the data

Load the [data from UCI repository](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset) and save it locally.

For demonstration purposes, we treat this data as the input data for a live model. To use with production models, you should make your prediction logs available.

This is how it looks:

![](<../.gitbook/assets/Screenshot 2021-07-19 at 18.56.18 (1).png>)

## **Step 3. Define column mapping**

You should specify the categorical and numerical features so that Evidently performs the correct statistical test for each of them. While Evidently can parse the data structure automatically, manually specifying the column type can minimize errors.

```
data_columns = ColumnMapping()
data_columns.numerical_features = ['weathersit', 'temp', 'atemp', 'hum', 'windspeed']
data_columns.categorical_features = ['holiday', 'workingday']
```

## Step 4. Define what to log

Specify which metrics you want to calculate. In this case, you can generate the Data Drift report and log the drift score for each feature.

```
def eval_drift(reference, production, column_mapping):

    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(reference_data=reference, current_data=production, column_mapping=column_mapping)
    report = data_drift_report.as_dict()

    drifts = []

    for feature in column_mapping.numerical_features + column_mapping.categorical_features:
        drifts.append((feature, report["metrics"][1]["result"]["drift_by_columns"][feature]["drift_score"]))

    return drifts
```

## Step 5. Define the comparison windows

Specify the period that is considered **reference**: Evidently will use it as the base for the comparison. Then, you should choose the periods to treat as experiments. This emulates the production model runs.

```
#set reference dates
reference_dates = ('2011-01-01 00:00:00','2011-01-28 23:00:00')

#set experiment batches dates
experiment_batches = [
    ('2011-01-01 00:00:00','2011-01-29 23:00:00'),
    ('2011-01-29 00:00:00','2011-02-07 23:00:00'),
    ('2011-02-07 00:00:00','2011-02-14 23:00:00'),
    ('2011-02-15 00:00:00','2011-02-21 23:00:00'),  
]
```

## Step 6. Run and log experiments in MLflow

Initiate the experiments and log the metrics calculated with Evidently on each run.

```
#log into MLflow
client = MlflowClient()

#set experiment
mlflow.set_experiment('Data Drift Evaluation with Evidently')

#start new run
for date in experiment_batches:
    with mlflow.start_run() as run: #inside brackets run_name='test'
        
        # Log parameters
        mlflow.log_param("begin", date[0])
        mlflow.log_param("end", date[1])

        # Log metrics
        metrics = eval_drift(raw_data.loc[reference_dates[0]:reference_dates[1]], 
                             raw_data.loc[date[0]:date[1]], 
                             column_mapping=data_columns)
        for feature in metrics:
            mlflow.log_metric(feature[0], round(feature[1], 3))

        print(run.info)
```

## Step 7. View the results in MLflow web UI

You can then use the MLflow UI to see the results of the runs.

![](<../.gitbook/assets/mlflow\_1 (1).png>)

With a large number of metrics, you can use the expanded view.

![](<../.gitbook/assets/mlflow\_3 (2).png>)

# Tutorial 2: Evaluating Historical Data Drift with Evidently, Plotly and **MLflow**

This is an additional tutorial that demonstrates how you can evaluate historical drift in your data. It also shows how to log experiments with MLflow in a similar fashion.

Refer to the [blog with the tutorial](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) and [example notebook](https://github.com/evidentlyai/evidently/blob/main/examples/integrations/mlflow_logging/historical_drift_visualization.ipynb).
