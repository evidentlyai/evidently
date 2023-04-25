---
description: How to set custom data drift conditions and thresholds for tabular and text data. 
---

**Pre-requisites**:
* You know how to generate Reports or Test Suites with default parameters.
* You know how to pass custom parameters for Reports or Test Suites.

# Default 

All Presets, Tests, and Metrics that include data or target (prediction) drift evaluation use the default [Data Drift algorithm](../reference/data-drift-algorithm.md). It automatically selects an appropriate drift detection method based on the feature type and volume. 

You can override the defaults by passing a custom parameter to the chosen Test, Metric, or Preset. You can define the drift detection method, the threshold, or both. 

# Examples

To set a custom drift method and threshold on the **column level**:

```python
ColumnDriftMetric(column_name='feature1', stattest='wasserstein', stattest_threshold=0.2) 
```

If you have a Preset, Test or Metric that checks for drift in **multiple columns** at the same time, you can set a custom drift method for all columns, all numerical/categorical columns, or for each column individually.

Here is how you set the drift detection method for all categorical columns:

```python
DataDriftPreset(cat_stattest='ks', cat_statest_threshold=0.05)
```

To set a custom condition for the **dataset drift** (share of drifting columns in the dataset) in the relevant Metrics or Presets:

```python
DatasetDriftMetric(drift_share=0.7)
```

Note that this works slightly differently for the **individual Tests**. The reason is that Tests expect you to define a condition to the **Test output**. You should use standard Test parameters like `lt` and `gt` to set the condition. 

To set a custom condition for the **dataset drift** when you run a relevant **Test**, you should set a condition for the share of drifted features using standard parameters:

```python
TestShareOfDriftedColumns(lt=0.5)
```
# Tabular drift detection 

All the following drift detection methods and parameters are available in the `DataDriftTable()`, `DatasetDriftMetric()`, `ColumnDriftMetric()`, related Tests, and Presets that contain them. They apply to **tabular** data. 

## Available drift parameters - Tabular

| Parameter | Description |
|---|---|
| `stattest` | Defines the drift detection method for a given column (if a single column is tested), or all columns in the dataset (if multiple columns are tested).  |
| `stattest_threshold` | Sets the drift threshold in a given column or all columns.<br>The threshold meaning varies based on the drift detection method, e.g., it can be the value of a distance metric or a p-value of a statistical test. |
| `drift_share` | Defines the share of drifting columns as a condition for Dataset Drift in `DatasetDriftMetric` or inside a Preset.  |
| `cat_stattest` <br>`cat_stattest_threshold` | Sets the drift method and/or threshold for all categorical columns in the dataset. |
| `num_stattest` <br>`num_stattest_threshold` | Sets the drift method and/or threshold for all numerical columns in the dataset. |
| `per_column_stattest`<br>`per_column_stattest_threshold` | Sets the drift method and/or threshold for the listed columns (accepts a dictionary).  |

{% hint style="info" %}
**How to check available parameters.** You can verify which parameters are available for a specific test, metric, or preset in the [All tests](../reference/all-tests.md) or [All metrics](../reference/all-metrics.md) tables or consult the [API reference]([../reference/api-reference](https://docs.evidentlyai.com/reference/api-reference))
{% endhint %}

## Drift detection methods - Tabular

| StatTest  | Applicable to | Drift score |
|---|---|---|
| `ks`<br>Kolmogorov–Smirnov (K-S) test | tabular data<br>only numerical <br><br>**Default method for numerical data, if <= 1000 objects** | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `chisquare`<br>Chi-Square test | tabular data<br>only categorical<br><br>**Default method for categorical with > 2 labels, if <= 1000 objects** | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `z`<br>Z-test | tabular data<br>only categorical<br><br>**Default method for binary data, if <= 1000 objects** | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `wasserstein`<br> Wasserstein distance (normed) | tabular data<br>only numerical<br><br>**Default method for numerical data, if > 1000 objects** | returns `distance`<br>drift detected when `distance` >= `threshold`<br>default threshold: 0.1 |
| `kl_div`<br>Kullback-Leibler divergence | tabular data<br>numerical and categorical | returns `divergence`<br>drift detected when `divergence` >= `threshold`<br>default threshold: 0.1 |
| `psi`<br> Population Stability Index (PSI) | tabular data<br>numerical and categorical | returns `psi_value`<br>drift detected when `psi_value` >= `threshold`<br>default threshold: 0.1 |
| `jensenshannon`<br> Jensen-Shannon distance | tabular data<br>numerical and categorical<br><br>**Default method for categorical, if > 1000 objects** | returns `distance`<br>drift detected when `distance` >= `threshold`<br>default threshold: 0.1 |
| `anderson`<br> Anderson-Darling test | tabular data<br>only numerical  | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `fisher_exact`<br> Fisher's Exact test | tabular data<br>only categorical  | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `cramer_von_mises`<br> Cramer-Von-Mises test | tabular data<br>only numerical  | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `g-test`<br> G-test | tabular data<br>only categorical  | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `hellinger`<br> Hellinger Distance (normed) | tabular data<br>numerical and categorical | returns `distance`<br>drift detected when `distance` >= `threshold`<br>default threshold: 0.1 |
| `mannw`<br> Mann-Whitney U-rank test | tabular data<br>only numerical  | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `ed`<br> Energy distance | tabular data<br>only numerical | returns `distance`<br>drift detected when `distance` >= `threshold`<br>default threshold: 0.1 |
| `es`<br> Epps-Singleton tes | tabular data<br>only numerical | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `t_test`<br> T-Test | tabular data<br>only numerical | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `emperical_mmd`<br> Emperical-MMD | tabular data<br>only numerical | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |
| `TVD`<br> Total-Variation-Distance | tabular data<br>only categorical | returns `p_value`<br>drift detected when `p_value` < `threshold`<br>default threshold: 0.05 |

# Text drift detection 

Text drift detection methods and parameters are available in the `DataDriftTable()`, `DatasetDriftMetric()`, `ColumnDriftMetric()`, related Tests and Presets that contain them. Text drift detection applies to columns with **raw text data**, as specified in column mapping. 

## Available drift parameters - Text

| Parameter | Description |
|---|---|
| `stattest` | Defines the drift detection method for a given column that contains text data. |
| `stattest_threshold` | Sets the threshold as a drift detection parameter. |

# Drift detection methods - Text

| StatTest  | Description | Drift score |
|---|---|---|
| `text_content_drift`<br> Text content drift (domain classifier) | Applies only to text data. Trains a classifier model to distinguish between text in “current” and “reference” datasets.<br><br>**Default for text data.** | <ul><li>returns `roc_auc` of the classifier as a `drift_score`</li><li>drift detected when `roc_auc` > ROC AUC of the random classifier at a set percentile</li><li>`threshold` sets the percentile of the possible ROC AUC values of the random classifier to compare against</li><li>default threshold: 0.95 (95th percentile)</li><li> `roc_auc` values can be 0 to 1 (typically 0.5 to 1); a higher value means more confident drift detection</ul> |
