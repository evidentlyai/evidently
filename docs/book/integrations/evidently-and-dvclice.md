---
description: Log Evidently metrics with DVC via DVCLive.
---

*This is a community-contributed integration. Author: [Francesco Calcavecchia](https://github.com/francesco086).*

**TL;DR:** You can use Evidently to calculate metrics, and DVCLive to log and view the results.

Jupyter notebook with en example:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/integrations/dvclive_logging/dvclive_integration.ipynb" %}

# **Overview**

[DVCLive](/doc/dvclive) can be used to track the results of
[Evidently](https://www.evidentlyai.com/). In the following we demonstrate it
through an example.

# **How it works**

```cli
$ pip install dvc dvclive evidently pandas
```

## **Step 1. Load the data**

Load the
[data from UCI repository](https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip)
and save it locally. For demonstration purposes, we treat this data as the input
data for a live model. To use with production models, you should make your
prediction logs available.

```cli
$ wget https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip
$ unzip bike+sharing+dataset.zip
```

```python
import pandas as pd

df = pd.read_csv("raw_data/day.csv", header=0, sep=',', parse_dates=['dteday'])
df.head()
```

This is how it looks: ![](<../.gitbook/assets/integrations/dvc_data_preview-min.png>)

## **Step 2. Define column mapping**

You should specify the categorical and numerical features so that Evidently
performs the correct statistical test for each of them. While Evidently can
parse the data structure automatically, manually specifying the column type can
minimize errors.

```python
from evidently.pipeline.column_mapping import ColumnMapping

data_columns = ColumnMapping()
data_columns.numerical_features = ['weathersit', 'temp', 'atemp', 'hum', 'windspeed']
data_columns.categorical_features = ['holiday', 'workingday']
```

## **Step 3. Define what to log**

Specify which metrics you want to calculate. In this case, you can generate the
Data Drift report and log the drift score for each feature.

```python
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


def eval_drift(reference, production, column_mapping):
    data_drift_report = Report(metrics=[DataDriftPreset()])
    data_drift_report.run(
        reference_data=reference, current_data=production, column_mapping=column_mapping
    )
    report = data_drift_report.as_dict()

    drifts = []

    for feature in (
        column_mapping.numerical_features + column_mapping.categorical_features
    ):
        drifts.append(
            (
                feature,
                report["metrics"][1]["result"]["drift_by_columns"][feature][
                    "drift_score"
                ],
            )
        )

    return drifts

```

You can adapt what you want to calculate by selecting a different Preset or
Metric from those available in Evidently.

## **Step 4. Define the comparison windows**

Specify the period that is considered reference: Evidently will use it as the
base for the comparison. Then, you should choose the periods to treat as
experiments. This emulates the production model runs.

```python
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

## **Step 5. Run and log experiments in DVC**

There are two ways to track the results of Evidently with DVCLive:

1. you can save the results of each item in the batch in one single experiment
   (each experiment corresponds to a git commit), in separate steps
2. or you can save the result of each item in the batch as a separate experiment

We will demonstrate both, and show you how to inspect the results regardless of
your IDE. However, if you are using VSCode, we recommend using the
[DVC extension for VS Code](https://marketplace.visualstudio.com/items?itemName=Iterative.dvc)
to inspect the results.

## **Step 6**

### **Option 1. One single experiment**

```python
from dvclive import Live

with Live() as live:
    for date in experiment_batches:
        live.log_param("begin", date[0])
        live.log_param("end", date[1])

        metrics = eval_drift(
            df.loc[df.dteday.between(reference_dates[0], reference_dates[1])],
            df.loc[df.dteday.between(date[0], date[1])],
            column_mapping=data_columns,
        )

        for feature in metrics:
            live.log_metric(feature[0], round(feature[1], 3))

        live.next_step()
```

You can then inspect the results using

```cli
$ dvc plots show
```

and inspecting the resulting `dvc_plots/index.html`, which should look like
this: ![](<../.gitbook/assets/integrations/dvc_plot_show.png>)

<!-- <admon icon="book"> -->

In a Jupyter notebook environment, you can show the plots as a cell output
simply by using `Live(report="notebook")`.

<!-- </admon> -->

### **Option 2. Multiple experiments**

```python
from dvclive import Live

for step, date in enumerate(experiment_batches):
    with Live() as live:
        live.log_param("begin", date[0])
        live.log_param("end", date[1])
        live.log_param("step", step)

        metrics = eval_drift(
            df.loc[df.dteday.between(reference_dates[0], reference_dates[1])],
            df.loc[df.dteday.between(date[0], date[1])],
            column_mapping=data_columns,
        )

        for feature in metrics:
            live.log_metric(feature[0], round(feature[1], 3))

```

You can the inspect the results using

```cli
$ dvc exp show
```

```
────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  Experiment                 Created    weathersit    temp   atemp     hum   windspeed   holiday   workingday   step   begin                 end
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
  workspace                  -               0.231       0       0   0.062       0.012     0.275        0.593   3      2011-02-15 00:00:00   2011-02-21 23:00:00
  master                     10:02 AM            -       -       -       -           -         -            -   -      -                     -
  ├── a96b45c [muggy-rand]   10:02 AM        0.231       0       0   0.062       0.012     0.275        0.593   3      2011-02-15 00:00:00   2011-02-21 23:00:00
  ├── 78c6668 [pawky-arcs]   10:02 AM        0.155   0.399   0.537   0.684       0.611     0.588        0.699   2      2011-02-07 00:00:00   2011-02-14 23:00:00
  ├── c1dd720 [joint-wont]   10:02 AM        0.779   0.098   0.107    0.03       0.171     0.545        0.653   1      2011-01-29 00:00:00   2011-02-07 23:00:00
  └── d0ddb8d [osmic-impi]   10:02 AM        0.985       1       1       1           1      0.98        0.851   0      2011-01-01 00:00:00   2011-01-29 23:00:00
 ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

<!-- <admon icon="book"> -->

In a Jupyter notebook environment, you can access the experiments results using
the [Python DVC api](/doc/api-reference):

```python
import dvc.api

dvc.api.exp_show()
```

<!-- </admon> -->
