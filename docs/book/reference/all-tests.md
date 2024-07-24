---
description: List of all Tests and Test Presets available in Evidently.
---

<details>

<summary>How to use this page</summary>
 
This is a reference page. You can return here:
* To discover **available Tests** and choose which to include in a custom Test suite.
* To understand which **parameters** you can change for a specific Test or Preset.
* To verify which tests are included in a **Test Preset**.

You can use the menu on the right to navigate the sections. 

# How to read the tables

* **Name**: the name of the Test or Test preset.  
* **Description**: plain text explanation. For Tests, we specify whether it applies to the whole dataset or individual columns.
* **Parameters**: available configurations. 
  * Required parameters are necessary for calculations, e.g. a column name for a column-level test.
  * Optional parameters modify how the underlying metric is calculated, e.g. which statistical test or correlation method is used.
  * [*Test condition parameters*](../tests-and-reports/custom-test-suite.md#custom-conditions) set the conditions (e.g. equal, not equal, greater than, etc.) that define the expectations from the Test output. If the condition is violated, the test returns a fail. They apply to most of the Tests, and are optional.
* **Default Test condition**: they apply if you do not set a custom сondition. 
  * With reference: the Test conditions that apply when you pass a reference dataset and Evidently can derive conditions from it. (E.g. expect +/- 10% from reference).
  * No reference: the Test conditions that apply if you do not provide the reference. They are based on heuristics.
 
**Test visualizations**. Each Test also includes a default render. If you want to see the visualization, navigate to the [example notebooks](../examples/examples.md).
</details>

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the [API reference](https://docs.evidentlyai.com/reference/api-reference) or the "All tests" notebook in the [Examples](../examples/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}

# Test Presets

Default conditions for each Test in the Preset match the Test's defaults. You can see them in the tables below. The listed Preset parameters apply to the relevant individual Tests inside the Preset.

<details>
 
<summary>NoTargetPerformance Test Preset</summary>

Preset name: `NoTargetPerformanceTestPreset()`

**Composition**: 
* `TestShareOfDriftedColumns()`
* `TestColumnDrift(column_name=prediction)`
* `TestColumnShareOfMissingValues()` for `all` or `сolumns` if provided
* `TestShareOfOutRangeValues()` for all numerical or specified `columns`
* `TestShareOfOutListValues()` for all categorical or specified `columns` 
* `TestMeanInNSigmas()` for all numerical or specified  `columns`

**Optional parameters**:
*   `columns`
*   `stattest`
*   `cat_stattest`
*   `num_stattest`
*   `per_column_stattest`
*   `text_stattest`
*   `stattest_threshold`
*   `cat_stattest_threshold`
*   `num_stattest_threshold`
*   `per_column_stattest_threshold`
*   `text_stattest_threshold`
*   `embeddings`
*   `embeddings_drift_method`
*   `drift_share`

How to set [data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).

</details>

<details>
 
<summary>Data Stability Test Preset</summary>

Preset name: `DataStabilityTestPreset()`

**Composition**: 
* `TestNumberOfRows()`
* `TestNumberOfColumns()`
* `TestColumnsType()`
* `TestColumnShareOfMissingValues()` for all or specified `columns`
* `TestShareOfOutRangeValues()` for all numerical or specified `columns`
* `TestShareOfOutListValues()` for all categorical or specified  `columns`
* `TestMeanInNSigmas()` for all numerical or specified `columns`

**Optional parameters**: 
* `columns`

</details>

<details>
 
<summary>Data Quality Test Preset</summary>

Preset name: `DataQualityTestPreset()`

**Composition**: 
* `TestColumnShareOfMissingValues()` for all or specified `columns`
* `TestMostCommonValueShare()` for all or specified `columns`
* `TestNumberOfConstantColumns()`
* `TestNumberOfDuplicatedColumns()`
* `TestNumberOfDuplicatedRows()`

**Optional parameters**: 
* `columns`

</details>

<details>
 
<summary>Data Drift Test Preset</summary>

Preset name: `DataDriftTestPreset()`

**Composition**: 
* `TestShareOfDriftedColumns()`
* `TestColumnDrift()` for all or specified `columns`

**Optional parameters**:
*   `columns`
*   `stattest`
*   `cat_stattest`
*   `num_stattest`
*   `per_column_stattest`
*   `text_stattest`
*   `stattest_threshold`
*   `cat_stattest_threshold`
*   `num_stattest_threshold`
*   `per_column_stattest_threshold`
*   `text_stattest_threshold`
*   `embeddings`
*   `embeddings_drift_method`
*   `drift_share`

How to set [data drift parameters](../customization/options-for-statistical-tests.md), [embeddings drift parameters](../customization/embeddings-drift-parameters.md).

</details>

<details>
 
<summary>Regression Test Preset</summary>

Preset name: `RegressionTestPreset()`

**Composition**: 
* `TestValueMeanError()`
* `TestValueMAE()`
* `TestValueRMSE()`
* `TestValueMAPE()`

**Optional parameters**: 
N/A

</details>

<details>
 
<summary>Multiclass Classification Test Preset</summary>

Preset name: `MulticlassClassificationTestPreset()`

**Composition**: 
* `TestAccuracyScore()`
* `TestF1Score()`
* `TestPrecisionByClass()`
* `TestRecallByClass()`
* `TestColumnDrift(column_name=target)`
* `TestNumberOfRows()`
* `TestLogLoss()` - if probabilistic classification
* `TestRocAuc()` - if probabilistic classification

**Optional parameters** for target drift:
* `stattest`
* `stattest_threshold`

How to set [data drift parameters](../customization/options-for-statistical-tests.md)

</details>

<details>
 
<summary>Binary Classification (Top K) Test Preset</summary>

Preset name: `BinaryClassificationTopKTestPreset()`

**Composition**: 
* `TestAccuracyScore(k=k)`
* `TestPrecisionScore(k=k)`
* `TestRecallScore(k=k)`
* `TestF1Score(k=k)`
* `TestColumnDrift(column_name=target)`
* `TestRocAuc()`
* `TestLogLoss()`

**Required parameters**:
* `k`

**Optional parameters**:
* `stattest`
* `stattest_threshold`
* `probas_threshold`

How to set [data drift parameters](../customization/options-for-statistical-tests.md)

</details>

<details>
 
<summary>Binary Classification Test Preset</summary>

Preset name: `BinaryClassificationTestPreset()`

**Composition**: 
* `TestColumnDrift(column_name=target)`
* `TestPrecisionScore()`
* `TestRecallScore()`
* `TestF1Score()`
* `TestAccuracyScore()`
* `TestRocAuc()` - if probabilistic classification

**Optional parameters**:
* `stattest`
* `stattest_threshold`
* `probas_threshold`

How to set [data drift parameters](../customization/options-for-statistical-tests.md)

</details>

<details>
 
<summary>RecSys (Recommender Systems) Test Preset</summary>

Preset name: `RecsysTestPreset()`

**Composition**: 
* `TestPrecisionTopK()`
* `TestRecallTopK()`
* `TestMAPK()`
* `TestNDCGK()`
* `TestHitRateK()`

**Required parameters:**
* `k`

**Optional parameters:**
* `min_rel_score: Optional[int]`
* `no_feedback_users: bool`

</details>

{% hint style="info" %} 
**How to set custom Test conditions?** Use parameters (e.g. equal, not equal, greater than, etc.) to set [Test Conditions](../tests-and-reports/custom-test-suite.md#custom-conditions). 
{% endhint %}

# Data Quality

## Data Integrity

| Test name  | Description | Parameters | Default test condition | 
|---|---|---|---|
| **TestNumberOfRows()** | Dataset-level. <br><br> Tests the number of rows against the reference or a defined condition.|  **Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-10% or >30.<br><br>**With reference**: the test fails if the number of rows differs by over 10% from the reference. <br><br>**No reference**: the test fails if the number of rows is <= 30.|
| **TestNumberOfColumns()** | Dataset-level. <br><br> Tests the number of columns against the reference or a defined condition. | **Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects the same or non-zero.<br><br>**With reference**: the test fails if the number of columns differs from the reference. <br><br>**No reference**: the test fails if the number of columns is 0.|
| **TestNumberOfConstantColumns()** | Dataset-level. <br><br> Tests the number of columns with all constant values against reference or a defined condition. |**Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects =< or none.<br><br>**With reference**: the test fails if the number of constant columns is higher than in the reference.<br><br>**No reference**: the test fails if there is at least one constant column.|
| **TestNumberOfEmptyRows()** | Dataset-level. <br><br> Tests the number of empty rows against reference or a defined condition. |**Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/- 10% or none.<br><br>**With reference**: the test fails if the share of empty rows is over 10% higher or lower than in the reference.<br><br>**No reference**: the test fails if there is at least one empty row.|
| **TestNumberOfEmptyColumns()** | Dataset-level. <br><br> Tests the number of empty columns against reference or a defined condition.|**Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects =< or none.<br><br>**With reference**: the test fails if the number of empty columns is higher than in the reference.<br><br>**No reference**: the test fails if there is at least one empty column.|
| **TestNumberOfDuplicatedRows()** | Dataset-level. <br><br> Tests the number of duplicate rows against reference or a defined condition. |**Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/- 10% or none.<br><br>**With reference**: the test fails if the share of duplicate rows is over 10% higher or lower than in the reference.<br><br>**No reference**: the test fails if there is at least one duplicate row. |
| **TestNumberOfDuplicatedColumns()** | Dataset-level. <br><br> Tests the number of duplicate columns against reference or a defined condition. |**Required**:<br> N/A <br><br> **Optional**:<br> N/A <br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects =< or none.<br><br>**With reference**: the test fails if the number of duplicate columns is higher than in the reference.<br><br>**No reference**: the test fails if there is at least one duplicate column.|
| **TestConflictTarget()**| Dataset-level. <br><br> Tests if there are conflicts in the target (instances where a different label is assigned for an identical input). | N/A | Expects no conflicts in the target (with or without reference). |
| **TestConflictPrediction()**| Dataset-level. <br><br> Tests if there are conflicts in the prediction (instances where a different prediction is made for an identical input). | N/A | Expects no conflicts in the target (with or without reference). |
| **TestColumnsType()**| Dataset-level. <br><br> Tests the types of all columns against the reference.| **Required**:<br> N/A <br><br> **Optional**:<br> `columns_type: dict` <br><br>**Test conditions**:<br> N/A | Expects types to match.<br><br>**With reference**: the test fails if at least one column type does not match. <br>**No reference**: N/A |
| **TestColumnAllConstantValues**(column_name='name') | Column-level. <br><br> Tests if all the values in a given column are constant.|**Required**: <ul><li>`column_name`</li></ul>**Optional**:<br> N/A<br><br>**Test conditions**: <br> N/A| Expects non-constant.<br><br>The test fails if all values in a given column are constant.|
| **TestColumnAllUniqueValues**(column_name='name') | Column-level. <br><br> Tests if all the values in a given column are unique.| **Required**: <ul><li>`column_name`</li></ul>**Optional**:<br> N/A<br><br>**Test conditions**:<br> N/A | Expects all unique (e.g., IDs).<br><br>The test fails if at least one value in a given column is not unique.|
| **TestNumberOfUniqueValues**(column_name='name')<br>    | Column-level. <br><br> Tests the number of unique values in a given column against reference or a defined condition. |   **Required**:<ul><li>`column_name`</li></ul> **Optional:**<br> N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the share of unique values is different by more than 10%.<br><br>**No reference**: N/A |
| **TestUniqueValuesShare**(column_name='name') | Column-level. <br><br> Tests the share of unique values in a given column against reference or a defined condition.  |   **Required**:<ul><li>`column_name`</li></ul> **Optional:**<br> N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the share of unique values is different by more than 10%.<br><br>**No reference**: N/A |
| **TestMostCommonValueShare**(column_name='name') | Column-level. <br><br> Tests the share of the most common value in a given column against reference or a defined condition. |   **Required**:<ul><li>`column_name`</li></ul> **Optional:**<br> N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the share of the most common value is different by more than 10% from the reference.<br><br>**No reference**: the test fails if the share of the most common value is >= 80%. |
| **TestColumnRegExp**(column_name='name, reg_exp='^[0..9]') | Column-level. <br><br> Tests the number of values in a column that do not match a defined regular expression, against reference or a defined condition. |**Required**: <ul><li>`column_name`</li><li>`reg_exp`</li></ul>**Optional**:<br>N/A<br><br>**Test conditions**:<ul><li>*standard parameters* </li></ul>| **With reference**: the test fails if the share of values that match a regular expression is over 10% higher or lower than in the reference.<br><br>**No reference**: the test fails if at least one of the values does not match a regular expression. |

## Missing Values

**Defaults for Missing Values**. The metrics that calculate the number or share of missing values detect four types of the values by default: Pandas nulls (None, NAN, etc.), "" (empty string), Numpy "-inf" value, Numpy "inf" value. You can also pass a custom missing values as a parameter and specify if you want to replace the default list. Example:

```python
TestNumberOfMissingValues(missing_values=["", 0, "n/a", -9999, None], replace=True)
```

| Test name  | Description | Parameters | Default test condition | 
|---|---|---|---|
| **TestNumberOfMissingValues()** | Dataset-level. <br><br> Tests the number of missing values in the dataset against the reference or a defined condition.|**Required**:<br> N/A <br><br> **Optional**: <ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects up to +10% or 0. <br><br>**With reference**: the test fails if the share of missing values is over 10% higher than in reference. <br><br>**No reference**: the test fails if the dataset contains missing values.|
| **TestShareOfMissingValues()**| Dataset-level. <br><br> Tests the share of missing values in the dataset against the reference or a defined condition.|**Required**:<br> N/A <br><br> **Optional**: <ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects up to +10% or 0. <br><br>**With reference**: the test fails if the share of missing values is over 10% higher than in reference.<br><br>**No reference**:  the test fails if the dataset contains missing values.|
| **TestNumberOfColumnsWithMissingValues()**| Dataset-level. <br><br>Tests the number of columns that contain missing values in the dataset against the reference or a defined condition.|**Required**:<br> N/A <br><br> **Optional**: <ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects <= or 0. <br><br>**With reference**: the test fails if the number of columns with missing values is higher than in reference.  <br>**No reference**: the test fails if the dataset contains columns with missing values.|
| **TestShareOfColumnsWithMissingValues()** | Dataset-level. <br><br> Tests the share of columns that contain missing values in the dataset against the reference or a defined condition.| **Required**:<br> N/A <br><br> **Optional**: <ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects <= or 0. <br><br>**With reference**: the test fails if the share of columns with missing values is higher than in reference.  <br><br>**No reference**: the test fails if the dataset contains columns with missing values.|
| **TestNumberOfRowsWithMissingValues()** | Dataset-level. <br><br> Tests the number of rows that contain missing values against the reference or a defined condition. | **Required**:<br>N/A<br><br>**Optional**:<ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul> **Test conditions** <ul><li>*standard parameters*</li></ul>| Expects up to +10% or 0.<br><br>**With reference**: the test fails if the share of rows with missing values is over 10% higher than in reference. <br><br>**No reference**: the test fails if the dataset contains rows with missing values.|
| **TestShareOfRowsWithMissingValues()** | Dataset-level. <br><br> Tests the share of rows that contain missing values against the reference or a defined condition. | **Required**:<br>N/A<br><br>**Optional**:<ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul>**Test conditions** <ul><li>*standard parameters*</li></ul>| Expects up to +10% or 0.<br><br>**With reference**: the test fails if the share of rows with missing values is over 10% higher than in reference. <br><br>**No reference**: the test fails if the dataset contains rows with missing values.|
| **TestNumberOfDifferentMissingValues()**| Dataset-level. <br><br> Tests the number of differently encoded missing values in the dataset against the reference or a defined condition. Detects 4 types of missing values by default and/or values from a user list. | **Required**:<br>N/A<br><br>**Optional**:<ul><li>`missing_values: list <br>replace: bool = True`(default = default list)</li></ul> **Test conditions** <ul><li>*standard parameters*</li></ul> | Expects <= or none.<br><br>**With reference**: the test fails if the current dataset has more types of missing values. <br><br>**No reference**: the test fails if the current dataset contains missing values. 
| **TestColumnNumberOfMissingValues**(column_name='name')| Column-level. <br><br> Tests the number of missing values in a given column against the reference or a defined condition.| **Required**:<ul><li>`column_name`</li></ul>**Optional**:<ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul> **Test conditions** <ul><li>*standard parameters*</li></ul> | Expects up to 10% or none.<br><br>**With reference**: the test fails if the share of missing values in a column is over 10% higher than in reference. <br><br>**No reference**: the test fails if the column contains missing values.|
| **TestColumnShareOfMissingValues**(column_name='name')| Column-level. <br><br> Tests the share of missing values in a given column against the reference or a defined condition.| **Required**:<ul><li>`column_name`</li></ul>**Optional**:<ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul>**Test conditions** <ul><li>*standard parameters*</li></ul> | Expects up to 10% or none.<br><br>**With reference**: the test fails if the share of missing values in a column is over 10% higher than in reference. <br>**No reference**: the test fails if the column contains missing values.|
| **TestColumnNumberOfDifferentMissingValues**(column_name='name')| Column-level. <br><br> Tests the number of differently encoded missing values in the column against reference or a defined condition. Detects 4 types of missing values by default and/or values from a user list. | **Required**:<ul><li>`column_name`</li></ul>**Optional**:<ul><li>`missing_values = [], replace = True/False` (default = default list)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects <= or none.<br><br>**With reference**: the test fails if the current column has more types of missing values. <br><br>**No reference**: The test fails if the column contains missing values.|

## Correlations 

| Test name  | Description | Parameters | Default test conditions | 
|---|---|---|---|
| **TestTargetPredictionCorrelation()** | Dataset-level. <br><br> Tests the strength of correlation between the target and prediction.| **Required**:<br>N/A<br><br> **Optional:**  <ul><li>`method` (default = `pearson`, available = `pearson`, `spearman`, `kendall`, `cramer_v`)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/- 0.25 in correlation strength, or > 0. <br><br>**With reference**: the test fails if there is a 0.25+ change in the correlation strength between target and prediction.<br><br>**No reference**: the test fails if the correlation between target and prediction <=0 |
| **TestHighlyCorrelatedColumns()**| Dataset-level. <br><br> Tests the strongest correlation between a pair of features, against reference or a defined condition. <br> | **Required**:<br>N/A<br><br> **Optional:**  <ul><li>`method` (default = `pearson`, available = `pearson`, `spearman`, `kendall`, `cramer_v`)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/- 10% in max correlation strength, or < 0.9.<br><br>**With reference**: the test fails if there is a 10%+ change in the correlation strength for the most correlated feature pair.<br><br> **No reference**: the test fails if there is at least one pair of features with the correlation >= 0.9 |
| **TestTargetFeaturesCorrelations()**| Dataset-level. <br><br> Tests if any of the features is highly correlated with the target. <br>Example use: to detect target leak. |  **Required**:<br>N/A<br><br> **Optional:**  <ul><li>'`method` (default = `pearson`, available = `pearson`, `spearman`, `kendall`, `cramer_v`)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/- 10% in max correlation strength, or < 0.9.<br><br>**With reference**: the test fails if there is a 10%+ change in the correlation strength for the feature most correlated with the target.<br><br>**No reference**: the test fails if at least one feature is correlated with the target >= 0.9 |
| **TestPredictionFeaturesCorrelations()**| Dataset-level. <br><br> Tests if any of the features is highly correlated with the prediction <br>Example use: to detect when predictions rely on a single feature. | **Required**:<br>N/A<br><br> **Optional:**  <ul><li>`method` (default = `pearson`, available = `pearson`, `spearman`, `kendall`, `cramer_v`)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/- 10% in max correlation strength, or < 0.9.<br><br>**With reference**: the test fails if there is a 10%+ change in the correlation strength for the feature most correlated with the prediction.<br><br>**No reference**: the test fails if at least one feature is correlated with the prediction >= 0.9 |
| **TestCorrelationChanges()** | Dataset-level. <br><br> Tests the number of correlation violations (significant change in the correlation strength between any two columns).|  **Required**:<br>N/A<br><br> **Optional:**  <ul><li>`method` (default = `pearson`, available = `pearson`, `spearman`, `kendall`, `cramer_v`)</li><li>`corr_diff` (default = 0.25) </li><li>`column_name`(checks for correlation changes only between a chosen column and other columns in the dataset) </li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects none.<br><br>**With reference**: the test fails if at least 1 correlation violation is detected. <br><br>**No reference**: N/A |

## Column Values

| Test name  | Description | Parameters | Default test conditions | 
|---|---|---|---|
| **TestColumnValueMin**(column_name='num-column') | Column-level. <br><br> Tests the minimum value of a given numerical column against reference or a defined condition. |  **Required**:<ul><li>`column_name`</li></ul> **Optional:** N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects not lower.<br><br>**With reference**: the test fails if the minimum value is lower than in the reference.<br><br>**No reference**: N/A |
| **TestColumnValueMax**(column_name='num-column') | Column-level. <br><br> Tests the maximum value of a given numerical column against reference or a defined condition. |   **Required**:<ul><li>`column_name`</li></ul> **Optional:** N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects not higher.<br><br>**With reference**: the test fails if the maximum value is higher than in the reference.<br><br>**No reference**: N/A |
| **TestColumnValueMean**(column_name='num-column') | Column-level. <br><br> Tests the mean value of a given numerical column against reference or a defined condition. |   **Required**:<ul><li>`column_name`</li></ul> **Optional:**<br> N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the mean value is different by more than 10%.<br><br>**No reference**: N/A |
| **TestColumnValueMedian**(column_name='num-column') | Column-level. <br><br> Tests the median value of a given numerical column against reference or a defined condition. |   **Required**:<ul><li>`column_name`</li></ul> **Optional:**<br> N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the median value is different by more than 10%.<br><br>**No reference**: N/A |
| **TestColumnValueStd**(column_name='num-column')<br>| Column-level. <br><br> Tests the standard deviation of a given numerical column against reference or a defined condition. |   **Required**:<ul><li>`column_name`</li></ul> **Optional:**<br> N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the standard deviation is different by more than 10%.<br><br>**No reference**: N/A |
|**TestColumnQuantile**(column_name='num_column', quantile=0.25) | Column-level. <br><br> Computes a quantile value and compares it to the reference or against a defined condition. |  **Required**:<ul><li>`column_name`</li><li>`quantile`</li></ul> **Optional:** N/A <br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10%.<br><br>**With reference**: the test fails if the quantile value is over 10% higher or lower. <br><br>**No reference**: N/A |
| **TestMeanInNSigmas**(column_name='num-column') | Column-level. <br><br> Tests if the mean value in a given numerical column is within the expected range , defined in standard deviations. This test requires reference. | **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`n_sigmas`</li></ul> | Expects +/- 2 std dev.<br><br>**With reference**: the test fails if the current mean value is out of the +/- 2 std dev interval from the reference mean value. <br><br>**No reference**: N/A |
| **TestValueRange**(column_name='num_column') | Column-level. <br><br> Tests if a numerical column contains values out of the min-max range. |  **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`left`</li><li>`right`</li></ul> **Test conditions**:<br>N/A | Expects all values to be in range.<br><br>**With reference**: the test fails if the column contains values out of the min-max range as seen in the reference. <br><br>**No reference**: N/A |
| **TestShareOfOutRangeValues**(column_name='num_column')| Column-level. <br><br> Tests the share of values out of the min-max range against reference or a defined condition. | **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`left`</li><li>`right`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>|| Expects all values to be in range.<br><br>  | Expects all values to be in range.<br><br>**With reference**: the test fails if at least 1 value is out of range (as seen in reference).<br><br>**No reference**: N/A |
| **TestNumberOfOutRangeValues**(column_name='num_column') | Column-level. <br><br> Tests the number of values out of the min-max range against reference or a defined condition. | **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`left`</li><li>`right`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>|| Expects all values to be in range.<br><br>**With reference**: the test fails if at least 1 value is out of range (as seen in reference). <br><br>**No reference**: N/A |
| **TestCategoryShare**(column_name='education', category='Some-college', lt=0.5)) | Column-level. <br><br> Tests if the number of objects belonging to a defined category (or having a defined numerical value) is within the threshold.|**Required**: <ul><li>`column_name`</li><li>`category`</li></ul>**Optional**:<br> N/A<br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects the category to be present.<br><br>The test fails if the category is not present.|
| **TestCategoryCount**(column_name='education', category='Some-college', lt=0.5)) | Column-level. <br><br>  Tests if the share of objects belonging to a defined category (or having a defined numerical value) is within the threshold.|**Required**: <ul><li>`column_name`</li><li>`category`</li></ul>**Optional**:<br> N/A<br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects the category to be present.<br><br>The test fails if the category is not present.|
| **TestValueList**(column_name='cat_column')   | Column-level. <br><br> Tests if a categorical column contains values out of the list.  |  **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`values: List[str]`</li></ul> **Test conditions**:<br>N/A| Expects all values to be in the list.<br><br>**With reference**: the test fails if the column contains values out of the list (as seen in reference). <br><br>**No reference**: N/A |
| **TestNumberOfOutListValues**(column_name='cat_column')| Column-level. <br><br> Tests the number of values in a given column that are out of list, against reference or a defined condition. | **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`values: List[str]`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects all values to be in the list. <br><br>**With reference**: the test fails if the column contains values out of the list (as seen in reference). <br><br>**No reference**: N/A |
| **TestShareOfOutListValues**(column_name='cat_column')| Column-level. <br><br> Tests the share of values in a given column that are out of list against reference or a defined condition. |  **Required**:<ul><li>`column_name`</li></ul> **Optional:** <ul><li>`values: List[str]`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects all values to be in the list. <br><br>**With reference**: the test fails if the column contains values out of the list (as seen in reference). <br>**No reference**: N/A |

# Data Drift

By default, all data drift tests use the Evidently [drift detection logic](data-drift-algorithm.md) that selects a different statistical test or metric based on feature type and volume. You always need a reference dataset. To modify the logic or select a different test, you should set [data drift parameters](../customization/options-for-statistical-tests.md). 

| Test name | Description | Parameters | Default test conditions | 
|---|---|---|---|
| **TestNumberOfDriftedColumns()** | Dataset-level. <br><br> Compares the distribution of each column in the current dataset to the reference and tests the number of drifting features against a defined condition.| **Required**:<br>N/A<br><br>**Optional:**<ul><li>`сolumns`</li><li>`stattest`(default=automated selection)</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`(default=test default)</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul>**Test conditions**:<ul><li>*standard parameters*</li></ul> | Expects =< ⅓ features to drift.<br><br>**With reference:** If > 1/3 of features drifted, the test fails.<br><br>**No reference:** N/A |
| **TestShareOfDriftedColumns()** | Dataset-level. <br><br> Compares the distribution of each column in the current dataset to the reference and tests the share of drifting features against a defined condition.| **Required**:<br>N/A<br><br>**Optional:**<ul><li>`сolumns`</li><li>`stattest`(default=automated selection)</li><li>`cat_stattest`</li><li>`num_stattest`</li><li>`per_column_stattest`</li><li>`stattest_threshold`(default=test default)</li><li>`cat_stattest_threshold`</li><li>`num_stattest_threshold`</li><li>`per_column_stattest_threshold`</li></ul>**Test conditions**:<ul><li>*standard parameters*</li></ul> | Expects =< ⅓ features to drift.<br><br>**With reference:** If > 1/3 of features drifted, the test fails.<br><br>**No reference:** N/A  |
| **TestColumnDrift(column_name='name')**| Column-level. <br><br> Tests if there is a distribution shift in a given column compared to the reference.| **Required**: <ul><li>column_name</ul></li> **Optional**:<ul><li>`stattest`(default=automated selection)</li><li>`stattest_threshold`(default=test default)</li></ul>| Expects no drift.<br><br>**With reference:** the test fails if the distribution drift is detected in a given column.<br><br>**No reference:** N/A |
| **TestEmbeddingsDrift(embeddings_name='small_subset')**| Column-level. <br><br> Tests if there is drift in embeddings compared to reference.| **Required**: <ul><li>`embeddings_name`</ul></li> **Optional**:<ul><li>`drift_method`(default=model)</li></ul>| Expects no drift.<br><br>**With reference:** the test fails if the drift is detected in a given subset of columns.<br><br>**No reference:** N/A |

# Regression

**Defaults for Regression tests**: if there is no reference data or defined conditions, Evidently will compare the model performance to a dummy model that predicts the optimal constant (varies by the metric). You can also pass the reference dataset and run the test with default conditions, or define custom test conditions.

| Test name  | Description | Parameters | Default test conditions |  
|---|---|---|---|
| **TestValueMAE()**<br> | Dataset-level. <br><br> Computes the Mean Absolute Error (MAE) and compares it to the reference or against a defined condition.  | **Required**:<br>N/A<br><br> **Optional:**<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>  | Expects +/-10% or better than a dummy model.<br><br>**With reference**: if MAE is higher or lower by over 10%, the test fails. <br><br>**No reference**: the test fails if the MAE value is higher than the MAE of the dummy model that predicts the optimal constant (median of the target value). |
| **TestValueRMSE()** | Dataset-level. Computes the Root Mean Square Error (RMSE) and compares it to the reference or against a defined condition. |**Required**:<br>N/A<br><br> **Optional**:<br>N/A<br><br> **Test conditions** <ul><li>*standard parameters*</li></ul>| Expects +/-10% or better than a dummy model.<br><br>**With reference**: if RMSE is higher or lower by over 10%, the test fails.<br><br>**No reference**: the test fails if the RMSE value is higher than the RMSE of the dummy model that predicts the optimal constant (mean of the target value). |
| **TestValueMeanError()**<br>| Dataset-level. <br><br> Computes the Mean Error (ME) and tests if it is near zero or compares it against a defined condition. | **Required**:<br>N/A<br><br> **Optional**:<br>N/A<br><br> **Test conditions** <ul><li>*standard parameters*</li></ul>| Expects the Mean Error to be near zero.<br><br>**With/without reference**: the test fails if the Mean Error is skewed and the condition is violated. <br>Condition: eq = approx(absolute=0.1\*error_std)<br>error_std  =  (curr_true - curr_preds).std() |
| **TestValueMAPE()** | Dataset-level. <br><br> Computes the Mean Absolute Percentage Error (MAPE) and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% or better than a dummy model.<br><br>**With reference**: if MAPE is higher or lower by over 10%, the test fails.<br><br>**No reference**: the test fails if the MAPE value is higher than the MAPE of the dummy model that predicts the optimal constant (weighted median of the target value). |
| **TestValueAbsMaxError()** | Dataset-level. <br><br> Computes the absolute maximum error and compares it to the reference or against a defined condition.| **Required**:<br>N/A<br><br> **Optional:**<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-10% or better than a dummy model.<br><br>**With reference**: if the absolute maximum error is higher or lower by over 10%, the test fails. <br><br>**No reference**: the test fails if the absolute maximum error is higher than the absolute maximum error of the dummy model that predicts the optimal constant (median of the target value). |
| **TestValueR2Score()** | Dataset-level. <br><br> Computes the R2 Score (coefficient of determination) and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% or > 0.<br><br>**With reference**: if R2 is higher or lower by over 10%, the test fails.<br><br>**No reference**: the test fails if the R2 value is =< 0. |

# Classification

You can apply the tests for non-probabilistic, probabilistic classification, and ranking. The underlying metrics will be calculated slightly differently depending on the provided inputs: only labels, probabilities, decision threshold, and/or K (to compute, e.g., precision@K). 

**Defaults for Classification tests**. If there is no reference data or defined conditions, Evidently will compare the model performance to a dummy model. It is based on a set of heuristics to verify that the quality is better than random. You can also pass the reference dataset and run the test with default conditions, or define custom test conditions.

| Test name | Description | Parameters | Default test conditions | 
|---|---|---|---|
| **TestAccuracyScore()**| Dataset-level. <br><br>Computes the Accuracy and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional**:<ul><li>`threshold_probas`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k`</li></ul> **Test conditions**:<ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: if the Accuracy is over 20% higher or lower, the test fails.<br><br>**No reference**: if the Accuracy is lower than the Accuracy of the dummy model, the test fails.|
| **TestPrecisionScore()**| Dataset-level. <br><br> Computes the Precision and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional**:<ul><li>`threshold_probas`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-20% or better than a dummy model.<br><br>**With reference**: if the Precision is over 20% higher or lower, the test fails.<br><br>**No reference**: if the Precision is lower than the Precision of the dummy mode, the test fails.|
| **TestRecallScore()**| Dataset-level. <br><br> Computes the Recall and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional**:<ul><li>`threshold_probas`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: if the Recall is over 20% higher or lower, the test fails.<br><br>**No reference**: if the Recall is lower than the Recall of the dummy model, the test fails.  |
| **TestF1Score()**| Dataset-level. <br><br> Computes the F1 score and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional**:<ul><li>`threshold_probas`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-20% or better than a dummy model.<br><br>**With reference**: if the F1 is over 20% higher or lower, the test fails.<br><br>**No reference**: if the F1 is lower than the F1 of the dummy model, the test fails.|
| **TestPrecisionByClass**(label='classN') | Dataset-level. <br><br> Computes the Precision for the specified class and compares it to the reference or against a defined condition. | **Required**:<ul><li>`label`</li></ul> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: if the Precision is over 20% higher or lower, the test fails.<br><br>**No reference**: if the Precision is lower than the Precision of the dummy model, the test fails.|
| **TestRecallByClass**(label='classN') | Dataset-level. <br><br> Computes the Recall for the specified class and compares it to the reference or against a defined condition.| **Required**:<ul><li>`label`</li></ul> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: if the Recall is over 20% higher or lower, the test fails.<br><br>**No reference**: if the Recall is lower than the Recall of the dummy model, the test fails. |
|**TestF1ByClass**(label='classN') | Dataset-level. <br><br> Computes the F1 for the specified class and compares it to the reference or against a defined constraint. | **Required**:<ul><li>`label`</li></ul> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: the test fails if the F1 is over 20% higher or lower.<br><br>**No reference**: the test fails if the F1 is lower than the F1 of the dummy model.|
| **TestTPR()**| Dataset-level. <br><br> Computes the True Positive Rate and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: the test fails if the TPR is over 20% higher or lower.<br><br>**No reference**: the test fails if the TPR is lower than the TPR of the dummy model.|
| **TestTNR()**| Dataset-level. <br><br> Computes the True Negative Rate and compares it to the reference or against a defined condition. |**Required**:<br>N/A<br><br> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-20% or better than a dummy model.<br><br>**With reference**: the test fails if the TNR is over 20% higher or lower.<br><br>**No reference**: the test fails if the TNR is lower than the TNR of the dummy model. |
| **TestFPR()** | Dataset-level. <br><br> Computes the False Positive Rate and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-20% or better than a dummy model.<br><br>**With reference**: the test fails if the FPR is over 20% higher or lower.<br><br>**No reference**: the test fails if the FPR is higher than the FPR of the dummy model. |
| **TestFNR()**| Dataset-level. <br><br> Computes the False Negative Rate and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<ul><li>`probas_threshold`(default for classification = None; default for probabilistic classification = 0.5)</li><li>`k` (default = None)</li></ul>**Test conditions**: <ul><li>*standard parameters*</li></ul>| Expects +/-20% or better than a dummy model.<br><br>**With reference**: the test fails if the FNR is over 20% higher or lower.<br><br>**No reference**: the test fails if the FNR is higher than the FNR of the dummy model. |
|  **TestRocAuc()**| Dataset-level. <br><br> Applies to probabilistic classification. <br><br>Computes the ROC AUC and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or > 0.5 <br><br>**With reference**: the test fails if the ROC AUC is over 20% higher or lower than in the reference.<br><br>**No reference**: the test fails if ROC AUC is <= 0.5. |
|  **TestLogLoss()** | Dataset-level. <br><br>Applies to probabilistic classification. <br><br> Computes the LogLoss and compares it to the reference or against a defined condition. | **Required**:<br>N/A<br><br> **Optional:**<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-20% or better than a dummy model.<br><br>**With reference**: the test fails if the LogLoss is over 20% higher or lower than in the reference. <br><br>**No reference**: the test fails if LogLoss is higher than the LogLoss of the dummy model (equals 0.5 for a constant model). |

# Ranking and Recommendations 

Check individual metric descriptions [here](ranking-metrics.md).

Optional shared parameters:
* `no_feedback_users: bool = False`. Specifies whether to include the users who did not select any of the items, when computing the quality metrics. Default: False.
* `min_rel_score: Optional[int] = None`. Specifies the minimum relevance score to consider relevant when calculating the quality metrics for non-binary targets (e.g., if a target is a rating or a custom score).

| Test name | Description | Parameters | Default test conditions | 
|---|---|---|---|
| **TestPrecisionTopK(k=k)** | Dataset-level. <br><br> Computes the Precision at the top K and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Precision at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if precision > 0.|
| **TestRecallTopK(k=k)** | Dataset-level. <br><br> Computes the Recall at the top K and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Recall at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if recall > 0.|
| **TestFBetaTopK(k=k)** | Dataset-level. <br><br> Computes the F-beta score at the top K and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the F-beta score at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if F-beta > 0. |
| **TestHitRateK(k=k)** | Dataset-level. <br><br> Computes the Hit Rate at the top K recommendations and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Hit Rate at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if Hit Rate > 0.|
| **TestMAPK(k=k)** | Dataset-level. <br><br> Computes the Mean Average Precision at the top K and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the MAP at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if MAP > 0.|
| **TestMRRK(k=k)** | Dataset-level. <br><br> Computes the Mean Reciprocal Rank at the top K and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the MRR at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if MRR > 0.|
| **TestNDCGK(k=k)** | Dataset-level. <br><br> Computes the Normalized Discounted Cumulative Gain at the top K and compares it to the reference or against a defined condition. | **Required**: <ul><li>`k`</li></ul>**Optional**:<ul><li>`no_feedback_users`</li><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Normalized Discounted Cumulative Gain at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if NDCG > 0. |
| **TestNovelty(k=k)** | Dataset-level. <br><br> Computes the Novelty at the top K recommendations and compares it to the reference or against a defined condition. <br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li></ul> **Optional**:<br>N/A<br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Novelty at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if novelty > 0. |
| **TestPersonalization(k=k)** | Dataset-level. <br><br> Computes the Personalization at the top K recommendations and compares it to the reference or against a defined condition. | **Required**: <ul><li>`k`</li></ul> **Optional**:<br>N/A<br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Personalization at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if personalization > 0.|
| **TestSerendipity**(k=k, item_features=item_features) | Dataset-level. <br><br> Computes the Serendipity at the top K recommendations considering item features and compares it to the reference or against a defined condition. <br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li><li>`item_features`</li></ul> **Optional**:<ul><li>`min_rel_score`</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Serendipity at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if serendipity > 0.|
| **TestDiversity**(k=k, item_features=item_features) | Dataset-level. <br><br> Computes the Diversity at the top K recommendations considering item features and compares it to the reference or against a defined condition. | **Required**:<ul><li>`k`</li><li>`item_features`</li></ul> **Optional**:<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Diversity at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if diversity > 0.|
| **TestARP(k=k)** | Dataset-level. <br><br> Computes the Average Recommendation Popularity at the top K recommendations and compares it to the reference or against a defined condition. <br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li></ul> **Optional**:<ul><li>`normalize_arp` (default: False)</li></ul> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the ARP at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if ARP > 0.|
| **TestGiniIndex(k=k)** | Dataset-level. <br><br> Computes the Gini Index at the top K recommendations and compares it to the reference or against a defined condition.<br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li></ul> **Optional**:<br>N/A<br><br> **Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Gini Index at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if Gini Index < 1. |
| **TestCoverage(k=k)** | Dataset-level. <br><br> Computes the Coverage at the top K recommendations and compares it to the reference or against a defined condition. <br><br>Requires a training dataset. | **Required**:<ul><li>`k`</li></ul> **Optional**:<br>N/A<br><br>**Test conditions**: <ul><li>*standard parameters*</li></ul> | Expects +/-10% from reference.<br><br>**With reference**: if the Coverage at the top K is over 10% higher or lower, the test fails.<br><br>**No reference**: Tests if Coverage > 0.|

