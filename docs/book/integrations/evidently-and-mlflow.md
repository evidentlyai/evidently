---
description: Log Evidently metrics in the MLflow UI.
---

# Evidently and MLflow

**TL;DR:** You can use Evidently to calculate metrics, and MLflow Tracking to log and view the results. Here is a [sample Jupyter notebook](../../../../examples/integrations/mlflow_logging/mlflow_integration.ipynb).&#x20;

### **Overview**

Many machine learning teams use [MLflow](https://www.mlflow.org) for experiment management, deployment, and as a model registry.  If you are already familiar with MLflow, you can integrate it with Evidently to **track the performance of your models**.&#x20;

In this case, you use **Evidently to calculate the metrics** and **MLflow to log the results**. You can then access the metrics in the MLflow interface.&#x20;

### **How it works**

Evidently calculates a rich set of metrics and statistical tests. You can choose any of the pre-built [reports](../../reports/) to define the metrics you’d want to get.&#x20;

You can then generate **a JSON profile** that will contain the defined metrics output. You can combine several profile sections (e.g., Data and Prediction Drift together).&#x20;

You might not always need all metrics from the profile. You should explicitly define which parts of the output to send to **MLflow Tracking**.  &#x20;

## Tutorial 1: Evaluating Data Drift with **MLFlow and Evidently**&#x20;

In this example, we will use Evidently to check input features for [Data Drift](../../reports/data-drift.md) and log and visualize the results with MLflow.

Here is a Jupyter notebook with the example:&#x20;

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/mlflow_logging/mlflow_integration.ipynb" %}

### **Step 1. Install MLflow and Evidently**

Evidently is available as a PyPI package:

```
$ pip install evidently
```

For more details, refer to the Evidently [installation guide](../../get-started/install-evidently.md).&#x20;

To install MLflow, run:&#x20;

```
$ pip install mlflow
```

Or install MLflow with scikit-learn via&#x20;

```
$pip install mlflow[extras] 
```

For more details, refer to MLflow [documentation](https://mlflow.org/docs/latest/tutorials-and-examples/tutorial.html#id5).

### Step 2. Load the data

Load the data from UCI repository ([link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)) and save it locally.&#x20;

For demonstration purposes, we treat this data as the input data for a live model. To use with production models, you should make your prediction logs available.

This is how it looks:

![](<../.gitbook/assets/Screenshot 2021-07-19 at 18.56.18.png>)

### **Step 3. Define column mapping**&#x20;

We specify the categorical and numerical features so that Evidently performs the correct statistical test for each of them.

```
data_columns = {}
data_columns['numerical_features'] = ['weather', 'temp', 'atemp', 'humidity', 'windspeed']
data_columns['categorical_features'] = ['holiday', 'workingday']
```

### Step 4. Define what to log

We specify which metrics we want to see. In this case, we want to get the p-value of the statistical test performed to evaluate the drift for each feature.&#x20;

```
def eval_drift(reference, production, column_mapping):
    data_drift_profile = Profile(sections=[DataDriftProfileSection])
    data_drift_profile.calculate(reference, production, column_mapping=column_mapping)
    report = data_drift_profile.json()
    json_report = json.loads(report)

    drifts = []
    for feature in column_mapping['numerical_features'] + column_mapping['categorical_features']:
        drifts.append((feature, json_report['data_drift']['data']['metrics'][feature]['p_value'])) 
    return drifts
```

### Step 5. Define the comparison windows

We specify the period that is considered **reference**: we will use it as the base for the comparison. Then, we choose the periods that we treat as experiments that emulate production model runs.&#x20;

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

### Step 6. Run and log experiments in MLflow

We initiate the experiments and log the metrics calculated with Evidently on each run.&#x20;

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

### Step 7. View the results in MLflow web UI &#x20;

You can then use the MLflow UI to see the results of the runs.&#x20;

![](../.gitbook/assets/mlflow\_1.png)

With a large number of metrics, you can use the expanded view.

![](../.gitbook/assets/mlflow\_3.png)

## Tutorial 2: Evaluating Historical Data Drift with Evidently, Plotly and **MLflow** &#x20;

See a tutorial [here](https://evidentlyai.com/blog/tutorial-3-historical-data-drift).
