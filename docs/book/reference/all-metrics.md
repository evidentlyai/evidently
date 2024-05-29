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

<details>

<summary>Data Quality Preset</summary>

`DataQualityPreset` captures column and dataset summaries. Input features are required. Prediction and target are optional.

**Composition**:
* `DatasetSummaryMetric()`
* `ColumnSummaryMetric()` for `all` or specified `сolumns`
* `DatasetMissingValuesMetric()`
* `DatasetCorrelationsMetric()`

**Optional parameters**:
* `columns`

</details>

<details>

<summary>Data Drift Preset</summary>

`DataDriftPreset` evaluates the data distribution drift in all individual columns, and share of drifting columns in the dataset. Input features are required. 

**Composition**:
* `DataDriftTable()` for all or specified `columns`
* `DatasetDriftMetric()` for all or specified `columns`

**Optional parameters**:
* `columns`
* `stattest`
* `cat_stattest`
* `num_stattest`
* `per_column_stattest`
* `text_stattest`
* `stattest_threshold`
* `cat_stattest_threshold`
* `num_stattest_threshold`
* `per_column_stattest_threshold`
* `text_stattest_threshold`
* `embeddings`
* `embeddings_drift_method`
* `drift_share`

How to set [data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).

</details>

<details>

<summary>Target Drift Preset</summary>

`TargetDriftPreset` evaluates the prediction or target drift. Target and/or prediction is required. Input features are optional.

**Composition**:
* `ColumnDriftMetric()` for `target` and/or `prediction` columns
* `ColumnCorrelationsMetric()`  for `target` and/or `prediction` columns
* `TargetByFeaturesTable()` for all or specified `columns`
* `ColumnValuePlot()` for `target` and/or `prediction` columns - if the task is `regression`

**Optional parameters**:
* `columns`
* `stattest`
* `cat_stattest`
* `num_stattest`
* `per_column_stattest`
* `stattest_threshold`
* `cat_stattest_threshold`
* `num_stattest_threshold`
* `per_column_stattest_threshold`

How to set [data drift parameters](../customization/options-for-statistical-tests.md). 

</details>

<details>

<summary>Regression Preset</summary>

`RegressionPreset` evaluates the quality of a regression model. Prediction and target are required. Input features are optional.

**Composition**:
* `RegressionQualityMetric()`
* `RegressionPredictedVsActualScatter()`
* `RegressionPredictedVsActualPlot()`
* `RegressionErrorPlot()`
* `RegressionAbsPercentageErrorPlot()`
* `RegressionErrorDistribution()`
* `RegressionErrorNormality()`
* `RegressionTopErrorMetric()`
* `RegressionErrorBiasTable()` for all or specified `columns`

**Optional parameters**:
* `columns`

</details>

<details>
  
<summary>Classification Preset</summary>

`ClassificationPreset` evaluates the quality of a classification model. Prediction and target are required. Input features are optional.

**Composition**:
* `ClassificationQualityMetric()`
* `ClassificationClassBalance()`
* `ClassificationConfusionMatrix()`
* `ClassificationQualityByClass()`
* `ClassificationClassSeparationPlot()` - if probabilistic classification
* `ClassificationProbDistribution()`- if probabilistic classification
* `ClassificationRocCurve()` - if probabilistic classification
* `ClassificationPRCurve()` - if probabilistic classification
* `ClassificationPRTable()` - if probabilistic classification
* `ClassificationQualityByFeatureTable()` for all or specified `columns`</li></ul>

**Optional parameters**:
* `columns`
* `probas_threshold`

</details>

<details>
  
<summary>Text Overview Preset</summary>

`TextOverviewPreset()` provides a summary for a single or multiple text columns. Text columns (inputs and/or outputs) are required.

**Comoposition**:
* `ColumnSummaryMetric()` for text descriptors for all columns. Descriptors included:
  * `Sentiment()`
  * `SentenceCount()`
  * `OOV()`
  * `TextLength()`
  * `NonLetterCharacterPercentage()` 
* `SemanticSimilarity()` between each pair of text columns - if more than one text column is provided.

**Required parameters**:
* `column_name` or `columns` list

**Optional parameters**:
* `descriptors` list

</details>

<details>
  
<summary>Text Evals</summary>

`TextEvals()` provides a simplified interface to list `Descriptors` for a given text column. It it returns a summary of evaluation results.

**Composition**:
* `ColumnSummaryMetric()` for text descriptors for the specified text column:
  * `Sentiment()`
  * `SentenceCount()`
  * `OOV()`
  * `TextLength()`
  * `NonLetterCharacterPercentage()`
  
**Required parameters**:
* `column_name`

</details>

<details>
  
<summary>RecSys (Recommender System) Preset</summary>

`RecsysPreset` evaluates the quality of the recommender system. Recommendations and true relevance scores are required. For some metrics, training data and item features are required. 

**Composition**:
* `PrecisionTopKMetric()`
* `RecallTopKMetric()`
* `FBetaTopKMetric()`
* `MAPKMetric()`
* `NDCGKMetric()`
* `MRRKMetric()`
* `HitRateKMetric()`
* `PersonalizationMetric()`
* `PopularityBias()`
* `RecCasesTable()`
* `ScoreDistribution()`
* `DiversityMetric()`
* `SerendipityMetric()`
* `NoveltyMetric()`
* `ItemBiasMetric()` (pass column as a parameter)
* `UserBiasMetric()`(pass column as a parameter)

**Required parameter**:
* `k`

**Optional parameters**:
* `min_rel_score: Optional[int]`
* `no_feedback_users: bool`
* `normalize_arp: bool`
* `user_ids: Optional[List[Union[int, str]]]`
* `display_features: Optional[List[str]]`
* `item_features: Optional[List[str]]`
* `user_bias_columns: Optional[List[str]]`
* `item_bias_columns: Optional[List[str]]`

</details>

# Data Quality

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
| **ConflictPredictionMetric()** | Dataset-level.<br><br>Calculates the number of instances where the model returns a different output for an identical input. Can be a signal of low-quality model or data errors.| **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ConflictTargetMetric()** | Dataset-level.<br><br>Calculates the number of instances where there is a different target value or label for an identical input. Can be a signal of a labeling or data error.| **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **DatasetCorrelationsMetric()**| Dataset-level.<br><br>Calculates the correlations between the columns in the dataset. Visualizes the heatmap. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ColumnDistributionMetric**(column_name="education") | Column-level.<br><br>Plots the distribution histogram and returns bin positions and values for the given column.  | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnValuePlot**(column_name="education") | Column-level.<br><br>Plots the values in time. | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnQuantileMetric**(column_name="education-num", quantile=0.75)<br> <br>  | Column-level.<br><br>Calculates the defined quantile value and plots the distribution for the given column.  | **Required:**<ul><li>`column_name`</li><li>`quantile`</li></ul>**Optional:**<br>n/a |
| **ColumnCorrelationsMetric**(column_name="education") | Column-level.<br><br>Calculates the correlations between the defined column and all the other columns in the dataset. | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnValueListMetric**(column_name="relationship", values=["Husband", "Unmarried"]) | Column-level.<br><br>Calculates the number of values in the list / out of the list / not found in a given column. The value list should be specified. | **Required:**<ul><li>`column_name`</li><li>`values`</li></ul>**Optional:**<br>n/a |
| **ColumnValueRangeMetric**(column_name="age", left=10, right=20) | Column-level.<br><br>Calculates the number and share of values in the specified range / out of range in a given column. Plots the distributions. | **Required:**<ul><li>`column_name` </li><li>`left`</li><li>`right`</li></ul> |

# Text Metrics

| Metric name | Description | Parameters |
|---|---|---|
| **TextDescriptorsDistribution**(column_name=”text”)| Column-level.<br><br>Calculates and visualizes distributions for auto-generated text descriptors (text length, the share of out-of-vocabulary words, etc.) | **Required:**<ul><li>`column_name` </li></ul> |
| **TextDescriptorsCorrelationMetric**(column_name=”text”) | Column-level.<br><br>Calculates and visualizes correlations between auto-generated text descriptors and other columns in the dataset.| **Required:**<ul><li>`column_name` </li></ul> |
| **TextDescriptorsDriftMetric**(column_name=”text”) | Column-level. <br><br>Calculates data drift for auto-generated text descriptors and visualizes the distributions of text characteristics. | **Required:**<ul><li>`column_name`</li></ul><br>**Optional:**<ul><li>`stattest`</li><li>`stattest_threshold`</li> </li></ul>|

# Data Drift

**Defaults for Data Drift**. By default, all data drift tests use the Evidently [drift detection logic](data-drift-algorithm.md) that selects a different statistical test or metric based on feature type and volume. You always need a reference dataset.

To modify the logic or select a different test, you should set [data drift parameters](../customization/options-for-statistical-tests.md) or [embeddings drift parameters](../customization/embeddings-drift-parameters.md).

| Metric name | Description | Parameters |
|---|---|---|
| **DatasetDriftMetric()** <br>  | Dataset-level.<br><br>Calculates the number and share of drifted features. Returns true/false for the dataset drift at a given threshold (defined by the share of drifting features). Each feature is tested for drift individually using the default algorithm, unless a custom approach is specified.| **Required:**<br>n/a<br><br>**Optional:**<ul><li>`сolumns` (default=all)</li><li>`drift_share`(default for dataset drift = 0.5)</li> <li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul>[How to set data drift parameters](../customization/options-for-statistical-tests.md).|
| **DataDriftTable()** | Dataset-level.<br><br>Calculates data drift for all columns in the dataset, or for a defined list of columns. Returns drift detection results for each column and visualizes distributions in a table. Uses the default drift algorithm of test selection, unless a custom approach is specified.| **Required:**<br>n/a<br><br>**Optional:** <ul><li>`сolumns`</li><li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).|
| **ColumnDriftMetric('age')** | Column-level. <br><br>Calculates data drift for a defined column (tabular or text). Visualizes distributions. Uses the default-selected test unless a custom is specified. | **Required:**<ul><li>`column_name`</li></ul><br>**Optional:**<ul><li>`stattest`</li><li>`stattest_threshold`</li> </li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md)||
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


# Ranking and Recommendations 

All metrics are dataset-level. Check individual metric descriptions [here](ranking-metrics.md).

Optional shared parameters for multiple metrics:
* `no_feedback_users: bool = False`. Specifies whether to include the users who did not select any of the items, when computing the quality metric. Default: False.
* `min_rel_score: Optional[int] = None`. Specifies the minimum relevance score to consider relevant when calculating the quality metrics for non-binary targets (e.g., if a target is a rating or a custom score).

| Metric name | Description | Parameters |
|---|---|---|
| **RecallTopKMetric()** | Calculates the recall at `k`. | **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **PrecisionTopKMetric()** | Calculates the precision at `k`.| **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **FBetaTopKMetric()** | Calculates the F-measure at `k`.| **Required**:<ul><li>`beta`(default = 1)</li><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **MAPKMetric()** | Calculates the Mean Average Precision (MAP) at `k`.| **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **MARKMetric()** | Calculates the Mean Average Recall (MAR) at `k`.| **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **NDCGKMetric()** | Calculates the Normalized Discounted Cumulative Gain at `k`. | **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **MRRKMetric()** | Calculates the Mean Reciprocal Rank (MRR) at `k`. | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>`min_rel_score`</li><li>`no_feedback_users`</li></ul> |
| **HitRateKMetric()** | Calculates the hit rate at `k`: a share of users for which at least one relevant item is included in the K. | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>`min_rel_score`</li><li>`no_feedback_users`</li></ul> |
| **DiversityMetric()** | Calculates intra-list Diversity at `k`: diversity of recommendations shown to each user in top-K recommendations, averaged by all users.  | **Required**:<ul><li>`k`</li><li>`item_features: List`</li></ul>**Optional:**<ul><li>-</li></ul> |
| **NoveltyMetric()** | Calculates novelty at `k`: novelty of recommendations shown to each user in top-K recommendations, averaged by all users.<br><br>Requires a training dataset.| **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **SerendipityMetric()** | Calculates serendipity at `k`: how unusual the relevant recommendations are in top-K, averaged by all users.<br><br>Requires a training dataset.| **Required**:<ul><li>`k`</li><li>`item_features: List`</li></ul>**Optional**:<ul><li>`min_rel_score`</li></ul> |
| **PersonalizationMetric()** | Measures the average uniqueness of each user's top-K recommendations.<br><br> | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **PopularityBias()** | Evaluates the popularity bias in recommendations by computing ARP (average recommendation popularity), Gini index, and coverage. <br><br>Requires a training dataset | **Required**:<ul><li>`K`</li><li>`normalize_arp (default: False)` - whether to normalize ARP calculation by the most popular item in training</li></ul>**Optional**:<ul><li>-</li></ul> |
| **ItemBiasMetric()** | Visualizes the distribution of recommendations by a chosen dimension (column), сomparative to its distribution in the training set.<br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li><li>`column_name`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **UserBiasMetric()** | Visualizes the distribution of the chosen category (e.g. user characteristic), comparative to its distribution in the training dataset.<br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li><li>`column_name`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **ScoreDistribution()** | Computes the predicted score entropy. Visualizes the distribution of the scores at `k` (and all scores, if available).<br><br>Applies only when the `recommendations_type` is a `score`. | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **RecCasesTable()** | Shows the list of recommendations for specific user IDs (or 5 random if not specified).  | **Required**:<ul><li>-</li></ul>**Optional**:<ul><li>`display_features: List`</li><li>`user_ids: List`</li><li>`train_item_num: int`</li></ul> |

