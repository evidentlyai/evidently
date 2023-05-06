---
description: List of all the metrics and metric presets available in Evidently.
---

<details>

<summary>How to use this page</summary>

This is a reference page. It shows all the metrics and metric presets available in the library, and their parameters. 
  
You can use the menu on the right to navigate the sections. We organize the metrics by logical groups. Note that these groups do **not** match the presets with a similar name. For example, there are more Data Quality metrics below than in the `DataQualityPreset`. 
  
You can use this reference page to discover additional metrics to include in your custom report.

# How to read the tables

* **Name**: the name of the metric of a preset.  
* **Description**: plain text explanation of the metric, or the contents of the preset. For metrics, we also specify whether the metric applies to the whole dataset or individual columns.
* **Parameters**: description of the required parameters and optional parameters you can pass to the corresponding metric or preset. For metrics, we also specify the default conditions. They apply if you do not pass a custom parameter.

**Metric visualizations**. Each metric also includes a default render. If you want to see the visualization, navigate to the [example notebooks](../get-started/examples.md) and run the notebook with all metrics or with all metric presets.

</details>

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the [API reference](https://docs.evidentlyai.com/reference/api-reference) or the current version of the "All metrics" example notebook in the [Examples](../examples/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}

# Metric Presets

**Defaults**: each Metric in a Preset uses the default parameters for this Metric. You can see them in the tables below. 

| Preset name and Description | Parameters |
|---|---|
| **`DataQualityPreset`**<br><br>Evaluates the data quality and provides descriptive stats. <br><br>Input features are required. Prediction and target are optional. <br><br>**Contents**:<br>`DatasetSummaryMetric()`<br>`ColumnSummaryMetric(column_name=column_name)` for `all` or `сolumns` if provided <br>`DatasetMissingValuesMetric()`<br>`DatasetCorrelationsMetric()` | **Optional**:<br>`columns`<br> |
| **`DataDriftPreset`**<br> Evaluates the data drift in the individual columns and the dataset. <br><br> Input features are required. <br><br>**Contents**:<br>`DataDriftTable(сolumns=сolumns)` or `all` if not listed<br>`DatasetDriftMetric(сolumns=сolumns)` or `all` if not listed  | **Optional**:<ul><li>`columns`</li><li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`text_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li><li>`text_stattest_threshold`</li><li>`embeddings`</li><li>`embeddings_drift_method`</li><li>`drift_share`</li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).|
| **`TargetDriftPreset`** <br><br>Evaluates the prediction or target drift. <br><br>Target or prediction is required. Input features are optional.<br><br>**Contents**:<br>`ColumnDriftMetric(column_name=target, prediction)`<br>`ColumnCorrelationsMetric(column_name=target, prediction)`<br>`TargetByFeaturesTable(columns=columns)` or `all` if not listed <br><br>If regression:<br>`ColumnValuePlot(column_name=target, prediction)` | **Optional**:<ul><li>`columns`</li><li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold` </li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md). |
| **`RegressionPreset`**<br> Evaluates the quality of a regression model. <br><br>Prediction and target are required. Input features are optional.<br><br>**Contents**:<br>`RegressionQualityMetric()`<br>`RegressionPredictedVsActualScatter()`<br>`RegressionPredictedVsActualPlot()`<br>`RegressionErrorPlot()`<br>`RegressionAbsPercentageErrorPlot()`<br>`RegressionErrorDistribution()`<br>`RegressionErrorNormality()`<br>`RegressionTopErrorMetric()`<br>`RegressionErrorBiasTable(columns=columns)`or `all` if not listed  | **Optional**:<br>`columns` |
| **`ClassificationPreset`** <br>Evaluates the quality of a classification model. <br><br>Prediction and target are required. Input features are optional.<br><br>**Contents**:<br>`ClassificationQualityMetric()`<br>`ClassificationClassBalance()`<br>`ClassificationConfusionMatrix()`<br>`ClassificationQualityByClass()`<br><br>If probabilistic classification, also:<br>`ClassificationClassSeparationPlot()`<br>`ClassificationProbDistribution()`<br>`ClassificationRocCurve()`<br>`ClassificationPRCurve()`<br>`ClassificationPRTable()`<br>`ClassificationQualityByFeatureTable(columns=columns)` or `all` if not listed  | **Optional**:<ul><li>`columns`</li><li>`probas_threshold`</li><li>`k`</li></ul> |
|**`TextOverviewPreset(column_name=”text”)`** <br>Evaluates data drift and descriptive statistics for text data. <br><br>Input features (text) are required.<br><br>**Contents**:<br>`ColumnSummaryMetric()`<br>`TextDescriptorsDistribution()`<br>`TextDescriptorsCorrelation()`<br><br>If reference data is provided, also:<br> `ColumnDriftMetric()`<br>`TextDescriptorsDriftMetric()`| **Required**:<br>`column_name` |

# Data Integrity

**Defaults for Missing Values**. The metrics that calculate the number or share of missing values detect four types of the values by default: Pandas nulls (None, NAN, etc.), "" (empty string), Numpy "-inf" value, Numpy "inf" value. You can also pass a custom missing values as a parameter and specify if you want to replace the default list. Example:

```python
DatasetMissingValuesMetric(missing_values=["", 0, "n/a", -9999, None], replace=True)
```
| Metric name | Description | Parameters                                                                                                                                                                                                                       |
|---|---|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **DatasetSummaryMetric()** | Dataset-level.<br><br>Calculates various descriptive statistics for the dataset, incl. the number of columns, rows, cat/num features, missing values, empty values, and duplicate values.  | **Required**:<br>n/a<br><br>**Optional:**<ul><li>`missing_values = [], replace = True/False` (default = four types of missing values, see above)</li><li>`almost_constant_threshold` (default = 0.95)</li><li>`almost_duplicated_threshold` (default = 0.95)</li></ul> |
| **DatasetMissingValuesMetric()** | Dataset-level.<br><br>Calculates the number and share of missing values in the dataset. Displays the number of missing values per column. | **Required**:<br>n/a<br><br>**Optional:**<ul><li>`missing_values = [], replace = True/False` (default = four types of missing values, see above)</li></ul>|
| **ColumnSummaryMetric**(column_name="age") | Column-level.<br><br>Calculates various descriptive statistics for the column, incl. the number of missing, empty, duplicate values, etc. <br><br>The stats depend on the column type: numerical, categorical, text or DateTime. | **Required**:<br>`column_name`<br><br>**Optional:**<br>n/a|
| **ColumnMissingValuesMetric**(column_name="education")<br>  | Column-level.<br><br>Calculates the number and share of missing values in the column. |  **Required**:<br>n/a<br><br>**Optional:**<ul><li>`missing_values = [], replace = True/False` (default = four types of missing values, see above)</li></ul>|
| **ColumnRegExpMetric**(column_name="relationship", reg_exp=r".*child.*") | Column-level.<br><br>Calculates the number and share of the values that do not match a defined regular expression.  | **Required:**<ul><li>`column_name`</li><li>`reg_exp`</li></ul>**Optional:**<ul><li>`top` (the number of the most mismatched columns to return, default = 10)</li></ul>|

# Data Quality

| Metric name | Description | Parameters |
|---|---|---|
| **ConflictPredictionMetric()** | Dataset-level.<br><br>Calculates the number of instances where the model returns a different output for an identical input. Can be a signal of low-quality model or data errors.| **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ConflictTargetMetric()** | Dataset-level.<br><br>Calculates the number of instances where there is a different target value or label for an identical input. Can be a signal of a labeling or data error.| **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **DatasetCorrelationsMetric()**| Dataset-level.<br><br>Calculates the correlations between the columns in the dataset. Visualizes the heatmap. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ColumnDistributionMetric**(column_name="education") | Column-level.<br><br>Plots the distribution histogram and returns bin positions and values for the given column.  | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnQuantileMetric**(column_name="education-num", quantile=0.75)<br> <br>  | Column-level.<br><br>Calculates the defined quantile value and plots the distribution for the given column.  | **Required:**<ul><li>`column_name`</li><li>`quantile`</li></ul>**Optional:**<br>n/a |
| **ColumnCorrelationsMetric**(column_name="education") | Column-level.<br><br>Calculates the correlations between the defined column and all the other columns in the dataset. | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnValueListMetric**(column_name="relationship", values=["Husband", "Unmarried"]) | Column-level.<br><br>Calculates the number of values in the list / out of the list / not found in a given column. The value list should be specified. | **Required:**<ul><li>`column_name`</li><li>`values`</li></ul>**Optional:**<br>n/a |
| **ColumnValueRangeMetric**(column_name="age", left=10, right=20) | Column-level.<br><br>Calculates the number and share of values in the specified range / out of range in a given column. Plots the distributions. | **Required:**<ul><li>`column_name` </li><li>`left`</li><li>`right`</li></ul> |
| **TextDescriptorsDistribution**(column_name=”text”)| Column-level.<br><br>Calculates and visualizes distributions for auto-generated text descriptors (text length, the share of out-of-vocabulary words, etc.) | **Required:**<ul><li>`column_name` </li></ul> |
| **TextDescriptorsCorrelationMetric**(column_name=”text”) | Column-level.<br><br>Calculates and visualizes correlations between auto-generated text descriptors and other columns in the dataset.| **Required:**<ul><li>`column_name` </li></ul> |

# Data Drift

**Defaults for Data Drift**. By default, all data drift tests use the Evidently [drift detection logic](data-drift-algorithm.md) that selects a different statistical test or metric based on feature type and volume. You always need a reference dataset.

To modify the logic or select a different test, you should set [data drift parameters](../customization/options-for-statistical-tests.md) or [embeddings drift parameters](../customization/embeddings-drift-parameters.md).

| Metric name | Description | Parameters |
|---|---|---|
| **DatasetDriftMetric()** <br>  | Dataset-level.<br><br>Calculates the number and share of drifted features. Returns true/false for the dataset drift at a given threshold (defined by the share of drifting features). Each feature is tested for drift individually using the default algorithm, unless a custom approach is specified.| **Required:**<br>n/a<br><br>**Optional:**<ul><li>`сolumns` (default=all)</li><li>`drift_share`(default for dataset drift = 0.5)</li> <li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul>[How to set data drift parameters](../customization/options-for-statistical-tests.md).|
| **DataDriftTable()** | Dataset-level.<br><br>Calculates data drift for all columns in the dataset, or for a defined list of columns. Returns drift detection results for each column and visualizes distributions in a table. Uses the default drift algorithm of test selection, unless a custom approach is specified.| **Required:**<br>n/a<br><br>**Optional:** <ul><li>`сolumns`</li><li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).|
| **ColumnDriftMetric('age')** | Column-level. <br><br>Calculates data drift for a defined column (tabular or text). Visualizes distributions. Uses the default-selected test unless a custom is specified. | **Required:**<ul><li>`column_name`</li></ul><br>**Optional:**<ul><li>`stattest`</li><li>`stattest_threshold`</li> </li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md)||
| **TextDescriptorsDriftMetric**(column_name=”text”) | Column-level. <br><br>Calculates data drift for auto-generated text descriptors and visualizes the distributions of text characteristics. | **Required:**<ul><li>`column_name`</li></ul><br>**Optional:**<ul><li>`stattest`</li><li>`stattest_threshold`</li> </li></ul>|
| **EmbeddingsDriftMetric**('small_subset')| Column-level. <br><br>Calculates data drift for embeddings. | **Required:**<ul><li>`embeddings_name`</li></ul><br>**Optional:**<ul><li>`drift_method`</li></ul>[How to set embeddings drift parameters](../customization/embeddings-drift-parameters.md).|


# Classification

The metrics work both for probabilistic and non-probabilistic classification. All metrics are dataset-level.

| Metric name | Description | Parameters |
|---|---|---|
| **ClassificationDummyMetric()** | Calculates the quality of the dummy model built on the same data. This can serve as a baseline. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationQualityMetric()** | Calculates various classification performance metrics, incl. precision, accuracy, recall, F1-score, TPR, TNR, FPR, and FNR. For probabilistic classification, also: ROC AUC score, LogLoss. | **Required:**:<br>n/a<br><br>**Optional:**<ul><li>`probas_threshold` (default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul> |
| **ClassificationClassBalance()** | Calculates the number of objects for each label. Plots the histogram. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationConfusionMatrix()** | Calculates the TPR, TNR, FPR, FNR, and plots the confusion matrix.  | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul> |
| **ClassificationQualityByClass()** | Calculates the classification quality metrics for each class. Plots the matrix. | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>|
| **ClassificationClassSeparationPlot()** | Visualization of the predicted probabilities by class. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationProbDistribution()** | Visualization of the probability distribution by class. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationRocCurve()** | Plots ROC Curve. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationPRCurve()** | Plots Precision-Recall Curve. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationPRTable()** | Calculates the Precision-Recall table that shows model quality at a different decision threshold.  | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationQualityByFeatureTable()** | Plots the relationship between feature values and model quality. | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`columns`(default = all categorical and numerical columns)</li></ul> |

# Regression

All metrics are dataset-level.

| Metric name | Description | Parameters |
|---|---|---|
| **RegressionDummyMetric()** | Calculates the quality of the dummy model built on the same data. This can serve as a baseline. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionQualityMetric()** | Calculates various regression performance metrics, incl. Mean Error, MAE, MAPE, etc.  | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionPredictedVsActualScatter()** | Visualizes predicted vs actual values in a scatter plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionPredictedVsActualPlot()** | Visualizes predicted vs. actual values in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionErrorPlot()** | Visualizes the model error (predicted - actual) in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionAbsPercentageErrorPlot()**  | Visualizes the absolute percentage error in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionErrorDistribution()**  | Visualizes the distribution of the model error in a histogram. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionErrorNormality()**  | Visualizes the quantile-quantile plot (Q-Q plot) to estimate value normality. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionTopErrorMetric()**  | Calculates the regression performance metrics for different groups: top-X% of predictions with overestimation, top-X% of predictions with underestimation, and the rest.<br>Visualizes the group division on a scatter plot with predicted vs. actual values. | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`top_error` (default=0.05; the metrics are calculated for top-5% predictions with overestimation and underestimation).</li></ul> |
| **RegressionErrorBiasTable()** | Plots the relationship between feature values and model quality per group (for top-X% error groups, as above). | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`columns`(default = all categorical and numerical columns)</li><li>`top_error` (default=0.05; the metrics are calculated for top-5% predictions with overestimation and underestimation).</li></ul>|
