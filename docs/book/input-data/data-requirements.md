---
description: How to prepare the data to run Evidently reports or tests.
---

# Input data

**TL;DR:** Pass two datasets: reference and current. Use `pandas.DataFrame`. Keep the schema identical. Downsample if too large. As an option, pass only the current data.

## Data Preparation

Prepare the input data as a `pandas.DataFrame`. You can also compute some of the metrics on [Spark](../tests-and-reports/spark.md).

You typically need **two datasets**. In Evidently, we call them `reference` and `current` datasets.

* **Reference** dataset is a baseline for comparison, or an exemplary dataset that helps generate test conditions. This can be training data or earlier production data.
* **Current** dataset is the dataset you want to evaluate. It can include the most recent production data.

![](<../.gitbook/assets/two\_datasets\_classification.png>)

## Single dataset

If you want to use a **single** dataset without reference, pass it as the **current** dataset.

It will work for most of the Metrics and Tests. One notable exception is calculating data or prediction drift which always requires two datasets to compare the distributions.

If you pass a single dataset to generate a **Report**, there will be no side-by-side comparison. The Report will show Metrics (e.g., Data Quality or Regression Performance metrics) for a single dataset.

If you pass a single dataset to run **Tests** with no other parameters, Evidently will use the default Test parameters. For example, it will compare the model performance with a dummy model. You can also manually set the Test conditions (e.g., expected min-max value ranges). In this case, the reference dataset is not required.

{% hint style="info" %}
The default parameters for each test are listed in the [All tests](../reference/all-tests.md) table.
{% endhint %}

## Dataset structure

To use Evidently, you need a dataset that contains model prediction logs. It might contain:

* Input feature columns
* Prediction column
* Target column (if known)
* Additional columns such as DateTime and ID

The exact schema requirements differ based on the contents of the Report or Test suite. For example, to evaluate Data Drift or Data Quality, you can pass only the feature columns. To evaluate Model Performance, you also need model prediction and target (true labels or actuals).

If you pass two datasets, the structure of both datasets should be identical. All column names should be `string`.

{% hint style="info" %}
You can read more about the data schema requirements in the [column mapping section](column-mapping.md).
{% endhint %}

## Data volume and sampling

To minimize the size of **HTML Reports**, the visualizations are aggregated by default. If you want to see plots with raw data (individual prediction points), you should pass the [corresponding option](../customization/report-data-aggregation.md). Note that when you generate Reports with raw data, they may take time to load. The exact limitation depends on your infrastructure (e.g., memory).

If the dataset is too large, and you want to get raw data plots, you might need to downsample the data before passing the data to Evidently. For instance, you can apply random sampling or stratified sampling. You can also limit the number of columns (e.g., generate the Report only for the most important features).

**Test suites** contain different visualizations and can handle larger input data volumes.

When you have a large volume of data, you can also run calculations in Spark [Spark](../tests-and-reports/spark.md).

## Supported data types

Right now, Evidently works with tabular, raw text data and embeddings. You can also pass a dataset that contains different data types: for example, some columns may contain numerical or categorical data, while others contain text.
