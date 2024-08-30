---
description: How to prepare the data to run Evidently Reports or Test Suites.
---

To run evaluations on your datasets with the Evidently Python library, you should prepare your data in a certain way. This section covers how to do that. 

{% hint style="info" %}
**Looking for something else?**. Check [Tracing](../tracing/tracing_overview.md) to understand how to instrument your application. Check [Datasets](../datasets/datasets_overview.md) to learn how to upload and work with datasets in the user interface. For more details on running evaluations after you prepare the data, see [Reports and Test Suites](../tests-and-reports/introduction.md).
{% endhint %}

# Input data format

Evidently works with Pandas DataFrames, with some metrics also supported on [Spark](../tests-and-reports/spark.md).

Your input data should be in **tabular** format. All column names must be strings. The data can include any numerical, categorical, text, DateTime, and ID columns. You can also pass embeddings as numerical features. 

The structure is flexible. For example, you can pass:
* **Any tabular dataset**. You can run checks for data quality and drift for any dataset.
* **Logs of generative LLM application**. Include text inputs, outputs, and metadata.
* **ML model inferences**. You can analyze prediction logs that include model features (numerical, categorical, embeddings), predictions, and optional target values. 

To run certain evaluations, you must include specific columns. For instance, to evaluate classification quality, you need columns with predicted and actual labels. These should be named "prediction" and "target", or you’ll need to point to the columns that contain them. This process is called **Column Mapping**. You can learn more in the next section.

{% content-ref url="column-mapping.md" %}
[Column Mapping](column-mapping.md)
{% endcontent-ref %}

# Reference and current data

Usually, you evaluate a single dataset, which we call the **current** dataset. But in some cases, you might also use a second dataset, known as the **reference** dataset. You pass them simultaneously when running an evaluation.

![](<../.gitbook/assets/two\_datasets\_classification.png>)

When you may need two datasets:
* **Side-by-side comparison**. If you want to compare model performance or data quality over two different periods or between model versions, you can do this inside one Report. Pass one dataset as `current`, and another as `reference`.
* **Data drift detection**. To detect distribution shifts, you compare two datasets using methods like distance metrics. You always need two datasets. Use your latest production batch as `current`, and choose a `reference` dataset to compare against, such as your validation data or an earlier production batch.
* **Automatic Test generation**. If you provide a `reference` dataset, Evidently can automatically set up Test conditions, like expected min-max values for specific columns. This way, you don’t have to write each test condition manually.

If you pass two datasets, the structure of both datasets should be identical. 

# Data volume

Running computationally intensive evaluations on large datasets can take time. This depends on the specific analysis as well as your infrastructure. In many cases, such as for probabilistic data drift detection, it’s more efficient to work with **samples** of your data. For instance, instead of running drift detection on millions of rows, you can apply random or stratified sampling and then compare samples of your data.  

For datasets that don’t fit in memory, you can run calculations using [Spark](../tests-and-reports/spark.md).
