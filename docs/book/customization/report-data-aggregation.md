Data Aggregation in Reports

---
description: How to change data aggregation in plots.
---

**Pre-requisites**:
* You know how to generate Reports with default parameters.
* You know how to pass custom parameters for Reports or Metrics

# Code example

You can refer to an example How-to-notebook showing how to use `agg_data` parameter:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_agg_data_param.ipynb" %}

# Default

Starting from version 0.3.2, all visualization in Reports are aggregated by default. This helps reduce the size of the resulting HTML.

For example, you can create a custom Report:

```python
report = Report(metrics=[
    RegressionPredictedVsActualScatter(),
    RegressionPredictedVsActualPlot()
])
report.run(reference_data=housing_ref, current_data=housing_cur)
report
```

Here is how the Scatter Plot will look:

![RegressionPredictedVsActualScatter()](../.gitbook/assets/reports/metric_regression_predvsactual_scatter_agg-min.png)

{% hint style="info" %}
**This does not affect Test Suites.** All visualizations in Test Suites are already aggregated.
{% endhint %}

# Embedding parameters - Metrics and Tests 
