---
description: How to change data aggregation in plots.
---

**Pre-requisites**:
* You know how to generate Reports with default parameters.
* You know how to pass custom parameters for Reports or Metrics.

# Code example

You can refer to an example How-to-notebook on using `agg_data` parameter:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_agg_data_param.ipynb" %}

# Default

Starting from version 0.3.2, all visualizations in Reports are aggregated by default. This helps reduce the size of the resulting HTML.

For example, you can create a custom Report:

```python
report = Report(metrics=[
    RegressionPredictedVsActualScatter(),
    RegressionPredictedVsActualPlot()
])
report.run(reference_data=housing_ref, current_data=housing_cur)
report
```

Here is how the Scatter Plot in this Report will look:

![RegressionPredictedVsActualScatter()](../.gitbook/assets/reports/metric_regression_predvsactual_scatter_agg-min.png)

{% hint style="info" %}
**This does not affect Test Suites.** All visualizations in Test Suites are already aggregated.
{% endhint %}

# Non-aggregated plots in Reports 

If you want to see non-aggregated plots, you can set the `agg_data` parameter as `false`.

You can set it on the Report level by passing the corresponding option. 

```python
report = Report(
    metrics=[
      RegressionPredictedVsActualScatter(),
      RegressionPredictedVsActualPlot()
    ],
    options={"agg_data": False}
  )
report.run(reference_data=housing_ref, current_data=housing_cur)
report
```

All plots in the Report will be non-aggregated. Here is how the Scatter Plot in this Report will look:

![RegressionPredictedVsActualScatter()](../.gitbook/assets/reports/metric_regression_predvsactual_scatter_non_agg-min.png)

{% hint style="info" %}
**Consider the data size.** We recommend setting this option for smaller datasets or when you apply sampling. With non-aggregated plots, the HTML will contain all the data on individual data points. They may take significant time to load and be large in size. 
{% endhint %}

# Non-aggregated plots for Metrics

If you want to generate non-aggregated plots only for some visualizations. you can pass the `agg_data` option to the chosen Metrics:

```python
report = Report(
    metrics=[
      RegressionQualityMetric(),
      RegressionPredictedVsActualScatter(options={"agg_data": False}),
      RegressionPredictedVsActualPlot()
    ],
  )
report.run(reference_data=housing_ref, current_data=housing_cur)
report
```
