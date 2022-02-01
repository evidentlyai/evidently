# Numerical Target Drift

**TL;DR:**  The report explores the changes in the numerical target function (prediction).

* Performs a suitable **statistical test** to compare target (prediction) **distribution**
* Calculates the **correlations** between the feature and the target (prediction)
* **Plots the relations** between each individual feature and the target (prediction)

## Summary

The **Target Drift** report helps detect and explore changes in the target function and/or model predictions.

The **Numerical Target Drift** report is suitable for problem statements with the numerical target function: regression, probabilistic classification, ranking, etc.

## Requirements

To run this report, you need to have input features, and **target and/or prediction** columns available.

You will need **two** datasets. The **reference** dataset serves as a benchmark. We analyze the change by comparing the **current** production data to the **reference** data.

You can potentially choose any two datasets for comparison. But keep in mind that only the **reference** dataset will be used as a basis for comparison.

## How it works

We estimate the drift for the **target** (actual values) and **predictions** in the same manner. If both columns are passed to the dashboard, we build two sets of plots.

If only one of them (either target or predictions) is provided, we build one set of plots. If neither target nor predictions column is available, you will get an error.

To **estimate the numerical target (prediction) drift**, we compare the distribution of the target (prediction) in the two datasets. We use the [two-sample Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov\_test) at a 0.95 confidence level to detect if the distribution has changed significantly.

We also calculate the [Pearson correlation](https://en.wikipedia.org/wiki/Pearson\_correlation\_coefficient) between the target (prediction) and each individual feature in the two datasets to detect a **change in the relationship.**

{% hint style="info" %}
To set a different confidence level or tests you use, you can define [custom options](../customization/options-for-data-target-drift.md).
{% endhint %}

## How it looks

The report includes 4 components. All plots are interactive.

### 1. Target (Prediction) Drift

The report first shows the **comparison of target (prediction) distributions** in the current and reference dataset. The result of the statistical test and P-value are displayed in the title.

![](../.gitbook/assets/num_targ_drift.png)

### 2. Target (Prediction) Correlations

The report shows the **correlations between individual features and the target (prediction)** in the current and reference dataset. It helps detects shifts in the relationship.

![](../.gitbook/assets/num_targ_drift_target_correlations.png)

### 3. Target (Prediction) Values&#x20;

The report visualizes the **target (prediction) values by index or time** (if the`datetime` column is available or defined in the `column_mapping` dictionary). This plot helps explore the target behavior and compare it between the datasets.

![](../.gitbook/assets/num_targ_drift_target_values.png)

### 4. Target (Prediction) Behavior By Feature

Finally, we generate an interactive table with the **visualizations of dependencies between the target and each feature**.&#x20;

![](../.gitbook/assets/num_targ_drift_behavior_by_feature.png)

If you click on any feature in the table, you get an overview of its behavior.

The plot shows how **feature values relate to the target (prediction) values** and if there are differences between the datasets. It helps explore if they can explain the target (prediction) shift.

![](../.gitbook/assets/num_targ_drift_behavior_by_feature_example_tax.png)

We recommend paying attention to the behavior of the **most important features** since significant changes might confuse the model and cause higher errors.

For example, in a Boston house pricing dataset, we can see a new segment with values of TAX above 600 but the low value of the target (house price).


## Report customization

You can set different [options-for-data-target-drift.md](../customization/options-for-data-target-drift.md "mention") to modify the report components.&#x20;

You can also select which components of the reports to display or choose to show the short version of the report: [select-widgets-to-display.md](../customization/select-widgets-to-display.md "mention").

If you want to create a new plot or metric, you can [add-a-custom-widget-or-tab.md](../customization/add-a-custom-widget-or-tab.md "mention").

## When to use the report

Here are our suggestions on when to use it—best combined with the [Data Drift report.](data-drift.md)

**1. Before model retraining.** Before feeding fresh data into the model, you might want to verify whether it even makes sense.

**2. When you are debugging the model decay.** If you observe a drop in performance, this report can help see what has changed.

**3. When you are flying blind, and no ground truth is available.** If you do not have immediate feedback, you can use this report to explore the changes in the model output and the relationship between the features and prediction. This can help anticipate [data and concept drift](https://evidentlyai.com/blog/machine-learning-monitoring-data-and-concept-drift).

## JSON Profile

If you choose to generate a JSON profile, it will contain the following information:&#x20;

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

## Examples

* Browse our [examples](../get-started/examples.md) for sample Jupyter notebooks.

You can also read the initial [release blog](https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift).
