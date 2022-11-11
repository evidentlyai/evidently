---
description: List of all metrics available in Evidently.
---

How to read the tables:

* **Metrics**: the name of the metric.  
* **Description**: plain text explanation of the metric. If relevant, we also specify whether the metric applies to the whole dataset or individual columns.
* **Parameters**: description of the parameters you can change, and defaults. 

We organize the metrics into logical groups. Note that the groups do not match the presets with the same name, e.g., there are more Data Quality metrics below than in the `DataQualityPreset`.

**Metric visualizations**. Each metric also includes a default render. To see the visualization, navigate to the [example notebooks](../get-started/examples.md).

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All metrics" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}

## Data Integrity

**Note on Missing values related metrics**. The metrics that calculate the number or share of missing values detect four types of the values by default: Pandas nulls (None, NAN, etc.), "" (empty string), Numpy "-inf" value, Numpy "inf" value. You can also pass a custom missing values as a parameter and specify if you want to replace the default list. Example:

```python
DatasetMissingValuesMetric(missing_values=["", 0, "n/a", -9999, None], replace=True)
```
| Metric | Description | Parameters                                                                                                                                                                                                                       |
|---|---|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DatasetSummaryMetric() | Dataset-level.<br><br>Calculates various descriptive statistics for the dataset, incl. the number of columns, rows, cat/num features, missing values, empty values, and duplicate values.  | **Required:**<br>n/a<br><br>**Optional:**<br>missing_values = [], replace = True/False (default = four types of missing values, see above) <br><br>almost_constant_threshold (default = 0.95)<br><br>almost_duplicated_threshold (default = 0.95) |
| DatasetMissingValuesMetric() | Dataset-level.<br><br>Calculates the number and share of missing values in the dataset. Displays the number of missing values per column. | **Required:**:<br>n/a<br><br>**Optional:**<br>missing_values = [], replace = True/False (default = four types of missing values, see above)                                                                                               |
| ColumnSummaryMetric(column_name="age") | Column-level.<br><br>Calculates various descriptive statistics for the column, incl. the number of missing, empty, duplicate values, etc. <br><br>The stats depend on the column type: numerical, categorical, or DateTime. | **Required:**<br>column_name<br><br>**Optional:**<br>n/a                                                                                                                                                                         |
| ColumnMissingValuesMetric(column_name="education")<br>  | Column-level.<br><br>Calculates the number and share of missing values in the column. | **Required:**<br>column_name<br><br>**Optional:**<br>missing_values = [], replace = True/False (default = four types of missing values by default, see above)                                                                                     |
| ColumnRegExpMetric(column_name="relationship", reg_exp=r".*child.*") | Column-level.<br><br>Calculates the number and share of the values that do not match a defined regular expression.  | **Required:**<br>column_name<br>reg_exp<br><br>**Optional:**<br>top (the number of the most mismatched columns to return, default = 10)                                                                                          |

## Data Quality

| Metric | Description | Parameters |
|---|---|---|
| DatasetCorrelationsMetric() | Dataset-level.<br><br>Calculates the correlations between the columns in the dataset. Visualizes the heatmap. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ColumnDistributionMetric(column_name="education") | Column-level.<br><br>Plots the distribution histogram and returns bin positions and values for the given column.  | **Required:**<br>column_name<br><br>**Optional:**<br>n/a |
| ColumnQuantileMetric(column_name="education-num", quantile=0.75)<br> <br>  | Column-level.<br><br>Calculates the defined quantile value and plots the distribution for the given column.  | **Required:**<br>column_name<br>quantile<br><br>**Optional:**<br>n/a |
| ColumnCorrelationsMetric(column_name="education") | Column-level.<br><br>Calculates the correlations between the defined column and all the other columns in the dataset. | **Required:**<br>column_name<br><br>**Optional:**<br>n/a |
| ColumnValueListMetric(column_name="relationship", values=["Husband", "Unmarried"]) | Column-level.<br><br>Calculates the number of values in the list / out of the list / not found in a given column. The value list should be specified. | **Required:**<br>column_name <br>Values<br><br>**Optional:**<br>n/a |
| ColumnValueRangeMetric(column_name="age", left=10, right=20) | Column-level.<br><br>Calculates the number and share of values in the specified range / out of range in a given column. Plots the distributions. | **Required:**<br>column_name <br>left <br>right |

## Data Drift

By default, all data drift tests use the Evidently [drift detection logic](data-drift-algorithm.md) that selects a different statistical test or metric based on feature type and volume. You always need a reference dataset.

To modify the logic or select a different test, you should pass a [DataDriftOptions](../customization/options-for-statistical-tests.md) object. 

| Metric | Description | Parameters |
|---|---|---|
| DatasetDriftMetric()<br>  | Dataset-level.<br><br>Calculates the number and share of drifted features. Returns true/false for the dataset drift at a given threshold (defined by the share of drifting features). | **Required:**<br>n/a<br><br>**Optional:**<br>threshold (default for dataset drift = 0.5)<br><br>columns (default = all)<br><br>DataDriftOptions (default =  Evidently [data drift algorithm](data-drift-algorithm.md)) |
| DataDriftTable() | Dataset-level.<br><br>Calculates data drift for all columns in the dataset. Visualizes distributions.  | **Required:**<br>n/a<br><br>**Optional:** <br>columns (default = all)<br><br>DataDriftOptions (default =  [data drift algorithm](data-drift-algorithm.md))  |
| ColumnDriftMetric('age') | Column-level. <br><br>Calculates data drift for the defined column. Visualizes distributions.  | **Required:**<br>column_name<br><br>**Optional:**<br>DataDriftOptions (default =  [data drift algorithm](data-drift-algorithm.md)) |

## Classification

The metrics work both for probabilistic and non-probabilistic classification. All metrics are dataset-level.

| Metric | Description | Parameters |
|---|---|---|
| ClassificationQualityMetric() | Calculates various classification performance metrics, incl. precision, accuracy, recall, F1-score, TPR, TNR, FPR, and FNR. For probabilistic classification, also: ROC AUC score, LogLoss. | **Required:**:<br>n/a<br><br>**Optional:**<br>threshold (default for classification = None; default for probabilistic classification = 0.5)<br><br>k (default = None) |
| ClassificationClassBalance() | Calculates the number of objects for each label. Plots the histogram. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ClassificationConfusionMatrix() | Calculates the TPR, TNR, FPR, FNR, and plots the confusion matrix.  | **Required:**<br>n/a<br><br>**Optional:**<br>threshold (default for classification = None; default for probabilistic classification = 0.5)<br><br>k (default = None) |
| ClassificationQualityByClass() | Calculates the classification quality metrics for each class. Plots the matrix. | **Required:**:<br>n/a<br><br>**Optional:**<br>threshold (default for classification = None; default for probabilistic classification = 0.5)<br><br>k (default = None) |
| ClassificationClassSeparationPlot() | Visualization of the predicted probabilities by class. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ClassificationProbDistribution() | Visualization of the probability distribution by class. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ClassificationRocCurve() | Plots ROC Curve. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ClassificationPRCurve() | Plots Precision-Recall Curve. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ClassificationPRTable() | Calculates the Precision-Recall table that shows model quality at a different decision threshold.  | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| ClassificationQualityByFeatureTable() | Plots the relationship between feature values and model quality. | **Required:**<br>n/a<br><br>**Optional:**<br>columns (default = all numerical and categorical)<br><br>threshold (default for classification = None; default for probabilistic classification = 0.5)<br><br>k (default = None) |

## Regression

All metrics are dataset-level.

| Metric | Description | Parameters |
|---|---|---|
| RegressionQualityMetric() | Calculates various regression performance metrics, incl. Mean Error, MAE, MAPE, etc.  | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionPredictedVsActualScatter() | Visualizes predicted vs actual values in a scatter plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionPredictedVsActualPlot() | Visualizes predicted vs. actual values in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionErrorPlot() | Visualizes the model error (predicted - actual) in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionAbsPercentageErrorPlot() | Visualizes the absolute percentage error in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionErrorDistribution() | Visualizes the distribution of the model error in a histogram. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionErrorNormality() | Visualizes the quantile-quantile plot (Q-Q plot) to estimate value normality. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| RegressionTopErrorMetric() | Calculates the regression performance metrics for different groups: top-X% of predictions with overestimation, top-X% of predictions with underestimation, and the rest.<br>Visualizes the group division on a scatter plot with predicted vs. actual values. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a<br><br>**Default:**<br>By default, the metrics are calculated for top-5% predictions with overestimation and underestimation. |
| RegressionErrorBiasTable(columns=['col_1', 'col_2']), | Plots the relationship between feature values and model quality per group (for top-X% error groups, as above). | **Required:**<br>n/a<br><br>**Optional:**<br>columns (default = all categorical and numerical columns)<br><br>**Default:**<br>By default, the metrics are calculated for top-5% predictions with overestimation and underestimation. |
