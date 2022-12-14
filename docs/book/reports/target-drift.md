**TL;DR:** You can detect and explore changes in the target function (prediction) and detect distribution drift.

For Reports, you can use the pre-built `TargetDriftPreset`.
For Test Suites, you can use a `TestColumnDrift` test and apply it to the prediction or target column.

# Use case 

You can analyze target or prediction drift: 

**1. To monitor the model performance without ground truth.** When you do not have true labels or actuals, you can monitor Prediction Drift to react to meaningful changes. For example, to detect when there is a distribution shift in predicted values, probabilities, or classes. You can often combine it with the [Data Drift analysis.](data-drift.md)

**2. When you are debugging the model decay.** If you observe a drop in performance, you can evaluate Target Drift to see how the behavior of the target changed and explore the shift in the relationship between the features and prediction. 

**3. Before model retraining.** Before feeding fresh data into the model, you might want to verify whether it even makes sense. If there is no target drift, the concept is stable, and retraining might not be necessary.

# Report: Target Drift Preset  

## How it works

The `TargetDriftPreset` helps detect and explore changes in the target function and/or model predictions:
* Performs a suitable **statistical test** to compare target (prediction) **distribution**.
* For numerical targets, calculates the **correlations** between the feature and the target (prediction)
* **Plots the relations** between each individual feature and the target (prediction)

You can generate this preset both for numerical targets (e.g. if you have a regression problem) or categorical targets (e.g. if you have a classification problem). You can explicitly specify the type of the target column in column mapping. If it is not specified, Evidently will define the column type automatically.

## Data Requirements

To run this preset, you need to have **target and/or prediction** columns available. Input features are optional. Pass them if you want to analyze the correlations between the features and target (prediction).   

Evidently estimates the drift for the **target** and **predictions** in the same manner. If you pass both columns, Evidently will generate two sets of plots. If you pass only one of them (either target or predictions), Evidently will build one set of plots. 

You will need **two** datasets. The **reference** dataset serves as a benchmark. Evidently analyzes the change by comparing the **current** production data to the **reference** data.

## How it looks

The report includes 4 components. All plots are interactive.

### 1. Target (Prediction) Drift

The report first shows the **comparison of target (prediction) distributions** in the current and reference datasets. You can see the result of the statistical test or the value of a distance metric.

Evidently uses the default [data drift detection algorithm](../reference/data-drift-algorithm.md) to select the drift detection method based on target type and the number of observations in the reference dataset.

{% hint style="info" %}
You can modify the drift detection logic by selecting a different method already available in the library, including PSI, K–L divergence, Jensen-Shannon distance, Wasserstein distance, and/or by setting a different threshold. See more details about [setting data drift options](../customization/options-for-statistical-tests.md). You can also implement a [custom drift detection method](../customization/add-custom-metric-or-test.md).
{% endhint %}

### 2. Target (Prediction) Correlations

For numerical targets, the report calculates the [Pearson correlation](https://en.wikipedia.org/wiki/Pearson\_correlation\_coefficient) between the target (prediction) and each individual feature in the two datasets to detect a **change in the relationship.**

![](<../.gitbook/assets/num\_targ\_drift (1).png>)

The report shows the **correlations between individual features and the target (prediction)** in the current and reference dataset. It helps detects shifts in the relationship.

![](<../.gitbook/assets/num\_targ\_drift\_target\_correlations (1).png>)

### 3. Target (Prediction) Values

For numerical targets, the report visualizes the **target (prediction) values by index or time** (if the`datetime` column is available or defined in the `column_mapping` dictionary). This plot helps explore the target behavior and compare it between the datasets.

![](<../.gitbook/assets/num\_targ\_drift\_target\_values (1).png>)

### 4. Target (Prediction) Behavior By Feature

Finally, it generates an interactive table with the **visualizations of dependencies between the target and each feature**.

![](<../.gitbook/assets/num\_targ\_drift\_behavior\_by\_feature (1).png>)

If you click on any feature in the table, you get an overview of its behavior. The plot shows how **feature values relate to the target (prediction) values** and if there are differences between the datasets. It helps explore if they can explain the target (prediction) shift.

For numerical targets:

![](../.gitbook/assets/num\_targ\_drift\_behavior\_by\_feature\_example\_tax.png)

We recommend paying attention to the behavior of the **most important features** since significant changes might confuse the model and cause higher errors. For example, in a Boston house pricing dataset, we can see a new segment with values of TAX above 600 but the low value of the target (house price).

For categorical targets:

![](../.gitbook/assets/cat\_target\_drift\_behavior\_by\_feature\_example.png)


## Metrics output

You can get the report output as a JSON or a Python dictionary:

```yaml
{
 "num_target_drift": {
    "name": "num_target_drift",
    "datetime": "datetime",
    "data": {
      "utility_columns": {
        "date": null,
        "id": null,
        "target": "target",
        "prediction": null
      },
      "cat_feature_names": [],
      "num_feature_names": [],
      "metrics": {
        "target_name": "target",
        "target_type": "num",
        "target_drift": p_value,
        "target_correlations": {
          "reference": {
            "feature_name": corr_coefficient
          },
          "current": {
            "feature_name": corr_coefficient
          }
        }
      }
    }
  },
  "timestamp": "timestamp"
}
```

## Report customization

* You can [specify the drift detection methods and thresholds](../customization/options-for-statistical-tests.md). 
* You can add a [custom drift detection method](../customization/add-custom-metric-or-test.md).
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* You can create a different report or test suite from scratch taking this one as an inspiration. 


# Examples

* Browse the [examples](../get-started/examples.md) for sample Jupyter notebooks and Colabs.
