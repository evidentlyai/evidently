---
description: How to prepare the data to run Evidently reports or tests.
---

# Input data

**TL;DR:** Pass two datasets: reference and current. Use `pandas.DataFrame`. Keep the schema identical. Downsample if too large. As an option, pass only the current data.

## Data Preparation

Prepare the input data as a `pandas.DataFrame`.

You typically need **two datasets**. In Evidently, we call them `reference` and `current` datasets.

* **Reference** dataset is a baseline for comparison. This can be training data or earlier production data.
* **Current** dataset is the second dataset compared to the baseline. It can include the most recent production data.

![](<../.gitbook/assets/two\_datasets\_classification (1) (2).png>)

## Single dataset

If you want to use a **single** dataset without reference, pass it as the **current** dataset.

It will work in most cases. One exception is calculating data or prediction drift which always requires two datasets to compare the distributions.

If you pass a single dataset to generate a **report**, there will be no side-by-side comparison. The report will show metrics (e.g., Data Quality or Regression Performance metrics) for a single dataset.

If you pass a single dataset to run **tests**, Evidently will use the default test parameters. For example, it will compare the model performance with a dummy model. You can also manually set the test conditions (e.g., expected min-max value ranges) without the reference dataset.

{% hint style="info" %}
The default parameters for each test are listed in the [All tests](../reference/all-tests.md) table.
{% endhint %}

## Dataset structure

To use Evidently, you need a dataset that contains model prediction logs. It might contain:

* Input feature columns
* Prediction column
* Target column
* Additional columns such as DateTime and ID

The exact schema requirements differ based on the contents of the report or test suite. For example, to evaluate Data Drift or Data Quality, you can pass only the feature columns. To evaluate Model Performance, you also need model prediction and target (true labels or actuals).

If you pass two datasets, the structure of both datasets should be identical. All column names should be `string`.

{% hint style="info" %}
You can read more about the data schema requirements in the [column mapping section](column-mapping.md).
{% endhint %}

## Data volume and sampling

HTML **reports** may take time to load. This is because they store some of the data inside the HTML to generate the interactive plots. The exact limitation depends on your infrastructure (e.g., memory).

If the dataset is too large, you might need to downsample it before passing the data to Evidently. For instance, you can apply random sampling or stratified sampling. You can also limit the number of columns (e.g., generate the report only for the most important features).

**Test suites** contain different visualizations and can handle larger input data volumes.

## Supported data types

Right now, Evidently works only with tabular data. We are working to cover other data types.
