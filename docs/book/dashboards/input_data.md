---
description: How to prepare the data.
---

# Input Data 

This section applies both to Dashboards and Profiles.

## Data preparation

If you work in the notebook, you should prepare the data as a `pandas.DataFrame`. If you use command-line interface, you need the `csv` files. 

To generate the dashboards and profiles, Evidently usually performs comparison between two datasets. 

* The first dataset is the **reference**. This can be training or earlier production data that serves as a baseline for comparison.
* The second dataset is **current**. It can include the recent production data. 

![](<../.gitbook/assets/two\_datasets\_classification (1).png>)

You can prepare two separate datasets. You can also prepare only one dataset and identify the rows that refer to reference and current data accordingly.

For some reports (e.g. model performance), the second dataset is optional. You can generate a dashboard with no comparison performed. In this case, simply pass a single dataset.

{% hint style="info" %}
If your dataset is large, we suggest taking a sample. If you work in the notebook, you can do that with pandas before generating the dashboard. If you work using CLI, you can specify that in the configuration.
{% endhint %}

## Reference and current datasets 

We call the datasets "reference" and "current". This corresponds to the production model evaluation scenario. 

In practice, you can use Evidently to compare two datasets in different scenarios, for example: 

* **Training vs Test**
  * To compare the model performance on a hold-out **Test** to the **Training**.
  * Pass the training data as "Reference", and test data as "Current".
* **Production vs Training**
  * To compare the **Production** model performance to the **Training** period.
  * Pass the training data as "Reference", and production data as "Current".
* **Current performance vs Past**
  * To compare the **Current** production performance to an **Earlier** period.
  * For example, to compare the last week to the previous week or month.
  * Pass the earlier data as "Reference", and newer data as "Current".
* **Compare any two models or datasets**
  * For example, to estimate the historical drift for different windows in your training data or to compare how two models perform in the test.
  * Pass the first dataset as "Reference", and the second as "Current".

If you are generating the performance report for a single dataset, pass it as "Reference". 

## Dataset structure

The expected data schema is different depending on the report type.

* For the **Data Drift** report, include the input features only.
* For the **Target Drift** reports, include the input features and Target and/or the Prediction column.
* For the **Model Performance** reports, include the input features, Target, and Prediction.

If you include more columns than needed for a given report, they will be ignored. 

If you pass two datasets, the structure of both datasets should be identical. 

Below is a summary of the data requirements:

| Report Type                                                                                                    | Feature columns  | Target column                     | Prediction column                 | Works with a single dataset |
| -------------------------------------------------------------------------------------------------------------- | ---------------- | --------------------------------- | --------------------------------- | --------------------------- |
| ****[**Data Drift**](../reports/data-drift.md)****                                                             | Required         | No                                | No                                | No                          |
| ****[**Numerical Target Drift**](../reports/num-target-drift.md)****                                           | Required         | Target and/or Prediction required | Target and/or Prediction required | No                          |
| ****[**Categorical Target Drift** ](../reports/categorical-target-drift.md)****                                | Required         | Target and/or Prediction required | Target and/or Prediction required | No                          |
| ****[**Regression Performance**](../reports/reg-performance.md)****                                            | Required         | Required                          | Required                          | Yes                         |
| ****[**Classification Performance**](../reports/classification-performance.md)****                             | Required         | Required                          | Required                          | Yes                         |
| ****[**Probabilistic Classification Performance**](../reports/probabilistic-classification-performance.md)**** | Required         | Required                          | Required                          | Yes                         |
| ****[**Data Quality**](../reports/data-quality.md)**** | Required         | Optional                          | No                          | Yes                         |

## `DataFrame` requirements

Make sure the data complies with the following expectations.

1\) All column names are `string`

2\) All feature columns that are analyzed for drift have the numerical type `(np.number)`

* **All non-numerical columns will be ignored**. Categorical data can be encoded as numerical labels and specified in the column mapping. 
* **The datetime column is the only exception.** If available, it will be used as the x-axis in the data plots.
