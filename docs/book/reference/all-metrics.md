---
description: List of Metrics, Descriptors and Metric Presets available in Evidently.
---

<details>

<summary>How to use this page</summary>

This is a reference page. It shows all the available Metrics, Descriptors and Presets. 
  
You can use the menu on the right to navigate the sections. We organize the Metrics by logical groups. Note that these groups do **not** match the Presets with a similar name. For example, there are more Data Quality Metrics than included in the `DataQualityPreset`. 

# How to read the tables

* **Name**: the name of the Metric.  
* **Description**: plain text explanation. For Metrics, we also specify whether it applies to the whole dataset or individual columns.
* **Parameters**: required and optional parameters for the Metric or Preset. We also specify the defaults that apply if you do not pass a custom parameter.

**Metric visualizations**. Each Metric includes a default render. To see the visualization, navigate to the [example notebooks](../get-started/examples.md) and run the notebook with all Metrics or Metric Presets.

</details>

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, check the "All metrics" notebook in [examples](../examples/examples.md). If you notice an error, please send us a pull request with an update! 
{% endhint %}

# Metric Presets

**Defaults**: Presets use the default parameters for each Metric. You can see them in the tables below. 

<details>

<summary>Data Quality Preset</summary>

`DataQualityPreset` captures column and dataset summaries. Input columns are required. Prediction and target are optional.

**Composition**:
* `DatasetSummaryMetric()`
* `ColumnSummaryMetric()` for `all` or specified `сolumns`
* `DatasetMissingValuesMetric()`

**Optional parameters**:
* `columns`

</details>

<details>

<summary>Data Drift Preset</summary>

`DataDriftPreset` evaluates the data distribution drift in all individual columns, and share of drifting columns in the dataset. Input columns are required. 

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

`TextOverviewPreset()` provides a summary for a single or multiple text columns. Text columns are required.

**Comoposition**:
* `ColumnSummaryMetric()` for text descriptors for all columns. Descriptors included:
  * `Sentiment()`
  * `SentenceCount()`
  * `OOV()`
  * `TextLength()`
  * `NonLetterCharacterPercentage()` 
* `SemanticSimilarity()` between each pair of text columns, if there more than one. 

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

| Metric | Parameters |
| - | - |
| **DatasetSummaryMetric()** <br><br> Dataset-level.<br><br>Calculates descriptive dataset statistics, including:<ul><li>Number of columns by type</li><li>Number of rows</li><li>Missing values</li><li>Empty columns</li><li>Constant and almost constant columns</li><li>Duplicated and almost duplicated columns</li></ul>| **Required**:<br>n/a<br><br>**Optional:**<ul><li>`missing_values = [], replace = True/False` (see default types below)</li><li>`almost_constant_threshold` (default = 0.95)</li><li>`almost_duplicated_threshold` (default = 0.95)</li></ul> |
| **DatasetMissingValuesMetric()** <br><br> Dataset-level.<br><br>Calculates the number and share of missing values in the dataset. <br><br> Displays the number of missing values per column. | **Required**:<br>n/a<br><br>**Optional:**<ul><li>`missing_values = [], replace = True/False` (default = four types of missing values, see above)</li></ul>|
| **DatasetCorrelationsMetric()** <br><br>Dataset-level.<br><br>Calculates the correlations between all columns in the dataset. Uses: Pearson, Spearman, Kendall, Cramer_V. <br><br> Visualizes the heatmap. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ColumnSummaryMetric()** <br><br> Column-level.<br><br>Calculates various descriptive statistics for numerical, categorical, text or DateTime columns, including: <ul><li>Count</li><li>Min, max, mean (for numerical)</li><li>Standard deviation (for numerical)</li><li>Quantiles - 25%, 50%, 75% (for numerical)</li><li>Unique value share</li><li>Most common value share</li><li>Missing value share</li><li>New and missing categories (for categorical)</li><li>Last and first date (for DateTime)</li><li>Length, OOV% and Non-letter % (for text)</li></ul><br>Plots the distribution histogram. If DateTime is provided, also plots the distribution over time. If Target is provided, also plots the relation with Target. | **Required**:<br>`column_name`<br><br>**Optional:**<br>n/a|
| **ColumnMissingValuesMetric()** <br><br> Column-level.<br><br>Calculates the number and share of missing values in the column. |  **Required**:<br>n/a<br><br>**Optional:**<ul><li>`missing_values = [], replace = True/False` (default = four types of missing values, see below)</li></ul>|
| **ColumnRegExpMetric()** <br><br> Column-level.<br><br>Calculates the number and share of the values that do not match a defined regular expression. <br><br> Example use: `ColumnRegExpMetric(column_name="status", reg_exp=r".*child.*")`  | **Required:**<ul><li>`column_name`</li><li>`reg_exp`</li></ul>**Optional:**<ul><li>`top` (the number of the most mismatched columns to return, default = 10)</li></ul>|
| **ColumnDistributionMetric()** <br><br> Column-level.<br><br>Plots the distribution histogram and returns bin positions and values for the given column.  | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnValuePlot()** <br><br> Column-level.<br><br>Plots the values in time. | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnQuantileMetric()** <br><br> Column-level.<br><br>Calculates the defined quantile value and plots the distribution for the given numerical column.  <br><br> Example use: `ColumnQuantileMetric(column_name="name", quantile=0.75)` | **Required:**<ul><li>`column_name`</li><li>`quantile`</li></ul>**Optional:**<br>n/a |
| **ColumnCorrelationsMetric()** <br><br>Column-level.<br><br>Calculates the correlations between the defined column and all the other columns in the dataset. | **Required:**<br>`column_name`<br><br>**Optional:**<br>n/a |
| **ColumnValueListMetric()** <br><br> Column-level.<br><br>Calculates the number of values in the list / out of the list / not found in a given column. The value list should be specified.<br><br> Example use: `ColumnValueListMetric(column_name="city", values=["London", "Paris"])` | **Required:**<ul><li>`column_name`</li><li>`values`</li></ul>**Optional:**<br>n/a |
| **ColumnValueRangeMetric()** <br><br> Column-level.<br><br>Calculates the number and share of values in the specified range / out of range in a given column. Plots the distributions. <br><br> Example use: `ColumnValueRangeMetric(column_name="age", left=10, right=20)`  | **Required:**<ul><li>`column_name` </li><li>`left`</li><li>`right`</li></ul> |
| **ConflictPredictionMetric()** <br><br> Dataset-level.<br><br>Calculates the number of instances where the model returns a different output for an identical input. Can be a signal of low-quality model or data errors.| **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ConflictTargetMetric()** <br><br> Dataset-level.<br><br>Calculates the number of instances where there is a different target value or label for an identical input. Can be a signal of a labeling or data error.| **Required:**<br>n/a<br><br>**Optional:**<br>n/a |

**Defaults for Missing Values**. The metrics that calculate the number or share of missing values detect four types of missing values by default: Pandas nulls (None, NAN, etc.), "" (empty string), Numpy "-inf" value, Numpy "inf" value. You can also pass custom missing values as a parameter and specify if you want to replace the default list. Example:

```python
DatasetMissingValuesMetric(missing_values=["", 0, "n/a", -9999, None], replace=True)
```

# Text Evals 

Text Evals only apply to text columns. To compute a Descriptor for a single text column, use a `TextEvals` Preset. 

You can also explicitly specify the Evidently Metric (e.g., `ColumnSummaryMetric`) to visualize the descriptor, or pick a [Test](all-tests.md) (e.g., `TestColumnValueMin`) to run validations. 

## Descriptors: Patterns

| Descriptor | Parameters |
| - | - |
| **RegExp()** <ul><li> Matches text against any specified regular expression. </li><li> Returns True/False for every input.</li></ul> Example use:<br> `RegExp(reg_exp=r"^I")` | **Required:**<br>`reg_exp`<br><br>**Optional:**<ul><li>`display_name`</li></ul> |
| **BeginsWith()** <ul><li> Checks if the text begins with a specified combination. </li><li> Returns True/False for every input.</li></ul> Example use:<br> `BeginsWith(prefix="How")`| **Required:**<br>`prefix`<br><br>**Optional:**<ul><li>`display_name`</li><li>`case_sensitive = True` or `False`</li></ul> |
| **EndsWith()** <ul><li> Checks if the text ends with a specified combination. </li><li> Returns True/False for every input. </li></ul> Example use:<br> `EndsWith(suffix="Thank you.")`| **Required:**<br>`suffix`<br><br>**Optional:**<ul><li>`display_name`</li><li>`case_sensitive = True` or `False`</li></ul> |
| **Contains()** <ul><li> Checks if the text contains any or all specified items (e.g. competitor names, etc.) </li><li> Returns True/False for every input. </li></ul> Example use:<br> `Contains(items=["medical leave"])`| **Required:** <br> `items: List[str]` <br><br>**Optional:**<ul><li>`display_name`</li><li>`mode = 'any'` or `'all'`</li><li>`case_sensitive = True` or `False`</li></ul> |
| **DoesNotContain()** <ul><li>Checks if the text does not contain any or all specified items. </li><li> Returns True/False for every input. </li></ul> Example use:<br> `DoesNotContain(items=["as a large language model"]` | **Required:** <br> `items: List[str]` <br><br>**Optional:**<ul><li>`display_name`</li><li>`mode = 'all'` or `'any'`</li><li>`case_sensitive = True` or `False`</li></ul> |
| **IncludesWords()** <ul><li> Checks if the text includes **any** (default) or **all** specified words. </li><li> Considers only vocabulary words (from NLTK vocabulary). </li><li> By default, considers inflected and variant forms of the same word. </li><li> Returns True/False for every input. </li></ul> Example use:<br> `IncludesWords(words_list=['booking', 'hotel', 'flight']` | **Required:** <br> `words_list: List[str]` <br><br>**Optional:**<ul><li>`display_name`</li><li>`mode = 'any'` or `'all'`</li><li>`lemmatize = True` or `False`</li></ul> |
| **ExcludesWords()** <ul><li>Checks if the text excludes all specified words.</li><li> Considers only vocabulary words (from NLTK vocabulary). </li><li>By default, considers inflected and variant forms of the same word. </li><li>Returns True/False for every input. </li></ul> Example use:<br> `ExcludesWords(words_list=['buy', 'sell', 'bet']`| **Required:** <br>`words_list: List[str]` <br><br>**Optional:**<ul><li>`display_name`</li><li>`mode = 'all'` or `'any'`</li><li>`lemmatize = True` or `False`</li></ul> |

## Descriptors: Text stats

| Descriptor | Parameters |
| - | - |
| **TextLength()** <ul><li> Measures the length of the text.</li><li> Returns an absolute number.</li></ul> | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`display_name`</li></ul> |
| **OOV()** <ul><li>Calculates the percentage of out-of-vocabulary words based on imported NLTK vocabulary.</li><li> Return a score on a scale: 0 to 100. </li></ul> | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`display_name`</li><li>`ignore_words: Tuple = ()`</li></ul> |
| **NonLetterCharacterPercentage()** <ul><li>Calculates the percentage of non-letter characters. </li><li> Return a score on a scale: 0 to 100. </li></ul> | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`display_name`</li></ul>|
| **SentenceCount()** <ul><li> Counts the number of sentences in the text. </li><li> Returns an absolute number.</li></ul> | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`display_name`</li></ul> |
| **WordCount()** <ul><li> Counts the number of words in the text.</li><li> Returns an absolute number.</li></ul> | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`display_name`</li></ul> |

## Descriptors: Model-based

| Descriptor | Parameters |
| - | - |
| **Sentiment()** <ul><li>Analyzes the sentiment of the text. </li><li> Return a score on a scale: -1 (negative) to 1 positive). </li></ul>| **Required:**<br>n/a<br><br>**Optional:**<ul><li>`display_name`</li></ul> |
| **HuggingFaceToxicityModel()** <ul><li> Detects hate speech using [HuggingFace Model](https://huggingface.co/facebook/roberta-hate-speech-dynabench-r4-target). </li><li> Returns predicted probability for the “hate” label. </li><li> Scale: 0 to 1. </li></ul> | **Optional**: <ul><li>`toxic_label="hate"` (default)</li><li> `display_name`</li></ul> |
| **HuggingFaceModel()** <br><br> Scores the text using the selected HuggingFace model.| See [docs](../customization/huggingface_descriptor.md) with some example models (classification by topic, emotion, etc.)|
| **OpenAIPrompting()** <br><br> Scores the text using the defined prompt and OpenAI model as LLM-as-a-judge.| See [docs](../customization/llm_as_a_judge.md) for examples.|
| **Semantic Similarity()** <ul><li>Calculates pairwise semantic similarity between columns.</li><li>Generates text embeddings using a [transformer model](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2). </li><li>Calculates Cosine Similarity between each pair of texts. </li><li> Return a score on a scale: 0 to 1. (0: different, 0.5: unrelated, 1: identical). </li></ul> Example use:<br>`ColumnSummaryMetric(column_name=SemanticSimilarity().on(["response", "new_response"]))`. | **Required:** <ul><li>two column names</li></ul> **Optional:**<ul><li>`display_name`</li></ul> |

## Text-Specific Metrics

The following metrics only apply to text columns. 

| Metric | Parameters |
|---|---|
| **TextDescriptorsDistribution()** <ul><li> Column-level.</li><li>Visualizes distributions for auto-generated text descriptors (`TextLength()`, `OOV()` etc.)</li></ul>  | **Required:**<ul><li>`column_name` </li></ul> |
| **TextDescriptorsCorrelationMetric()** <ul><li> Column-level.</li><li>Calculates and visualizes correlations between auto-generated text descriptors and other columns in the dataset.</li></ul> | **Required:**<ul><li>`column_name` </li></ul> |
| **TextDescriptorsDriftMetric()** <ul><li>  Column-level. </li><li>Calculates data drift for auto-generated text descriptors and visualizes the distributions of text characteristics. </li></ul> | **Required:**<ul><li>`column_name`</li></ul><br> **Optional:**<ul><li>`stattest`</li><li>`stattest_threshold`</li> </li></ul>|

# Data Drift

**Defaults for Data Drift**. By default, all data drift metrics use the Evidently [drift detection logic](data-drift-algorithm.md) that selects a drift detection method based on feature type and volume. You always need a reference dataset.

To modify the logic or select a different test, you should set [data drift parameters](../customization/options-for-statistical-tests.md) or [embeddings drift parameters](../customization/embeddings-drift-parameters.md). You can choose from 20+ drift detection methods and optionally pass [feature importances](../customization/feature-importance.md).

| Metric | Parameters |
| - | - |
| **DatasetDriftMetric()** <ul><li> Dataset-level.</li><li>Calculates the number and share of drifted features in the dataset. </li><li>Each feature is tested for drift individually using the default algorithm, unless a custom approach is specified.</li></ul>| **Required:**<br>n/a<br><br>**Optional:**<ul><li>`сolumns` (default=all)</li><li>`drift_share`(default for dataset drift = 0.5)</li> <li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul>[How to set data drift parameters](../customization/options-for-statistical-tests.md).|
| **DataDriftTable()** <ul><li>Dataset-level.</li><li>Calculates data drift for all or selected columns. </li><li> Returns drift detection results for each column. </li><li>Visualizes distributions for all columns in a table.</li></ul>| **Required:**<br>n/a<br><br>**Optional:** <ul><li>`сolumns`</li><li>`stattest`</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).|
| **ColumnDriftMetric()** <ul><li> Column-level. </li><li> Calculates data drift for a defined column (tabular or text). </li><li>Visualizes distributions.</li></ul>| **Required:**<ul><li>`column_name`</li></ul><br>**Optional:**<ul><li>`stattest`</li><li>`stattest_threshold`</li> </li></ul> [How to set data drift parameters](../customization/options-for-statistical-tests.md)||
| **EmbeddingsDriftMetric()** <ul><li>Column-level.</li><li> Calculates data drift for embeddings. </li><li> Requires embedding column mapping. </li></ul>| **Required:**<ul><li>`embeddings_name`</li></ul><br>**Optional:**<ul><li>`drift_method`</li></ul>[How to set embeddings drift parameters](../customization/embeddings-drift-parameters.md).|

# Classification

The metrics work both for probabilistic and non-probabilistic classification. All metrics are dataset-level. All metrics require column mapping of target and prediction.

| Metric | Parameters |
|---|---|
| **ClassificationDummyMetric()** <br><br> Calculates the quality of the dummy model built on the same data. This can serve as a baseline. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationQualityMetric()** <br><br> Calculates various classification performance metrics, including:<ul><li>Accuracy</li><li>Precision</li><li>Recall</li><li>F-1 score</li><li>TPR (True Positive Rate)</li><li>TNR (True Negative Rate)</li><li>FPR (False Positive Rate)</li><li>FNR (False Negative Rate)</li><li>ROC AUC Score (for probabilistic classification)</li><li>LogLoss (for probabilistic classification) </li></ul> | **Required:**:<br>n/a<br><br>**Optional:**<ul><li>`probas_threshold` (default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul> |
| **ClassificationClassBalance()** <br><br> Calculates the number of objects for each label. Plots the histogram. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationConfusionMatrix()** <br><br> Calculates the TPR, TNR, FPR, FNR, and plots the confusion matrix.  | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul> |
| **ClassificationQualityByClass()** <br><br> Calculates the classification quality metrics for each class. Plots the matrix. | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>|
| **ClassificationClassSeparationPlot()** <br><br> Visualization of the predicted probabilities by class. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationProbDistribution()** <br><br> Visualization of the probability distribution by class. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationRocCurve()** <br><br> Plots ROC Curve. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationPRCurve()** <br><br> Plots Precision-Recall Curve. Applicable for probabilistic classification only. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationPRTable()** <br><br> Calculates the Precision-Recall table that shows model quality at a different decision threshold.  | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **ClassificationQualityByFeatureTable()** <br><br> Plots the relationship between feature values and model quality. | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`columns`(default = all categorical and numerical columns)</li></ul> |

# Regression

All metrics are dataset-level. All metrics require column mapping of target and prediction.

| Metric | Parameters |
|---|---|
| **RegressionDummyMetric()** <br><br> Calculates the quality of the dummy model built on the same data. This can serve as a baseline. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionQualityMetric()** <br><br> Calculates various regression performance metrics, including:<ul><li>RMSE</li><li>Mean error (+ standard deviation)</li><li>MAE(+ standard deviation)</li><li>MAPE (+ standard deviation)</li><li>Max absolute error</li></ul> | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionPredictedVsActualScatter()** <br><br> Visualizes predicted vs actual values in a scatter plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionPredictedVsActualPlot()** <br><br> Visualizes predicted vs. actual values in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionErrorPlot()** <br><br> Visualizes the model error (predicted - actual) in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionAbsPercentageErrorPlot()** <br><br> Visualizes the absolute percentage error in a line plot. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionErrorDistribution()** <br><br> Visualizes the distribution of the model error in a histogram. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionErrorNormality()** <br><br> Visualizes the quantile-quantile plot (Q-Q plot) to estimate value normality. | **Required:**<br>n/a<br><br>**Optional:**<br>n/a |
| **RegressionTopErrorMetric()** <br><br> Calculates the regression performance metrics for different groups: <ul><li>top-X% of predictions with overestimation </li><li> top-X% of predictions with underestimation </li><li>Majority(the rest)</li></ul><br>Visualizes the group division on a scatter plot with predicted vs. actual values. | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`top_error` (default=0.05; the metrics are calculated for top-5% predictions with overestimation and underestimation).</li></ul> |
| **RegressionErrorBiasTable()** <br><br> Plots the relationship between feature values and model quality per group (for top-X% error groups, as above). | **Required:**<br>n/a<br><br>**Optional:**<ul><li>`columns`(default = all categorical and numerical columns)</li><li>`top_error` (default=0.05; the metrics are calculated for top-5% predictions with overestimation and underestimation).</li></ul>|

# Ranking and Recommendations 

All metrics are dataset-level. Check individual metric descriptions [here](ranking-metrics.md). All metrics require recommendations column mapping.

Optional shared parameters for multiple metrics:
* `no_feedback_users: bool = False`. Specifies whether to include the users who did not select any of the items, when computing the quality metric. Default: False.
* `min_rel_score: Optional[int] = None`. Specifies the minimum relevance score to consider relevant when calculating the quality metrics for non-binary targets (e.g., if a target is a rating or a custom score).

| Metric | Parameters |
|---|---|
| **RecallTopKMetric()** <br><br> Calculates the recall at `k`. | **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **PrecisionTopKMetric()** <br><br> Calculates the precision at `k`.| **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **FBetaTopKMetric()** <br><br> Calculates the F-measure at `k`.| **Required**:<ul><li>`beta`(default = 1)</li><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **MAPKMetric()** <br><br> Calculates the Mean Average Precision (MAP) at `k`.| **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **MARKMetric()** <br><br> Calculates the Mean Average Recall (MAR) at `k`.| **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **NDCGKMetric()** <br><br> Calculates the Normalized Discounted Cumulative Gain at `k`. | **Required**:<ul><li>`k`</li></ul>**Optional:**<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul>|
| **MRRKMetric()** <br><br> Calculates the Mean Reciprocal Rank (MRR) at `k`. | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>`min_rel_score`</li><li>`no_feedback_users`</li></ul> |
| **HitRateKMetric()** <br><br> Calculates the hit rate at `k`: a share of users for which at least one relevant item is included in the K. | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>`min_rel_score`</li><li>`no_feedback_users`</li></ul> |
| **DiversityMetric()** <br><br> Calculates intra-list Diversity at `k`: diversity of recommendations shown to each user in top-K recommendations, averaged by all users.  | **Required**:<ul><li>`k`</li><li>`item_features: List`</li></ul>**Optional:**<ul><li>-</li></ul> |
| **NoveltyMetric()** <br><br> Calculates novelty at `k`: novelty of recommendations shown to each user in top-K recommendations, averaged by all users.<br><br>Requires a training dataset.| **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **SerendipityMetric()** <br><br> Calculates serendipity at `k`: how unusual the relevant recommendations are in top-K, averaged by all users.<br><br>Requires a training dataset.| **Required**:<ul><li>`k`</li><li>`item_features: List`</li></ul>**Optional**:<ul><li>`min_rel_score`</li></ul> |
| **PersonalizationMetric()** <br><br> Measures the average uniqueness of each user's top-K recommendations.<br><br> | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **PopularityBias()** <br><br> Evaluates the popularity bias in recommendations by computing ARP (average recommendation popularity), Gini index, and coverage. <br><br>Requires a training dataset. | **Required**:<ul><li>`K`</li><li>`normalize_arp (default: False)` - whether to normalize ARP calculation by the most popular item in training</li></ul>**Optional**:<ul><li>-</li></ul> |
| **ItemBiasMetric()** <br><br> Visualizes the distribution of recommendations by a chosen dimension (column), сomparative to its distribution in the training set.<br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li><li>`column_name`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **UserBiasMetric()** <br><br> Visualizes the distribution of the chosen category (e.g. user characteristic), comparative to its distribution in the training dataset.<br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li><li>`column_name`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **ScoreDistribution()** <br><br> Computes the predicted score entropy. Visualizes the distribution of the scores at `k` (and all scores, if available).<br><br>Applies only when the `recommendations_type` is a `score`. | **Required**:<ul><li>`k`</li></ul>**Optional**:<ul><li>-</li></ul> |
| **RecCasesTable()** <br><br> Shows the list of recommendations for specific user IDs (or 5 random if not specified).  | **Required**:<ul><li>-</li></ul>**Optional**:<ul><li>`display_features: List`</li><li>`user_ids: List`</li><li>`train_item_num: int`</li></ul> |
