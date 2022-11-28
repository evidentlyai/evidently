---
description: How to set custom data drift detection conditions and thresholds. 
---

**Pre-requisites**:
* You know how to generate reports or test suites with default parameters.
* You know how to pass custom parameters for reports or test suites.

# Default 

All presets, tests, and metrics that include data or prediction drift evaluation use the default [Data Drift algorithm](../reference/data-drift-algorithm.md). It automatically selects an appropriate statistical test based on the feature type and volume. 

You can override the defaults by passing a custom parameter to the chosen test, metric, or preset. You can define the drift method, the threshold, or both. 

# Examples

To set a custom drift method and threshold on the **column level**:

```python
ColumnDriftMetric(column_name=”feature1”, stattest=wasserstein, stattest_threshold=0.2) 
```

If you have a preset, test or metric that checks for drift in **multiple columns** at the same time, you can set a custom drift method for all columns, all numerical/categorical columns, or for each column individually.

Here is how you set the drift detection method for all numerical columns:

```python
DataDriftPreset(cat_stattest=ks, cat_statest_threshold=0.05)
```

To set a custom condition for the **dataset drift** (share of drifting features) in the relevant metrics or presets:

```python
DatasetDriftMetric(drift_share=0.7)
```

Note that this works slightly differently for the **individual tests**. The reason is that tests expect you to define a condition to the **test output**. You should use standard test parameters like `lt` and `gt` to set the condition. 

To set a custom condition for the **dataset drift** when you run a relevant **test**, you should set a condition for the share of drifted features using standard parameters:

```python
TestShareOfDriftedColumns(lt=0.5)
```

# Available drift parameters

| Parameter | Description |
|---|---|
| `stattest` | Defines the drift detection method for a given column (if a single column is tested), or all columns in the dataset (if multiple columns are tested).  |
| `stattest_threshold` | Sets the drift threshold in a given column or all columns.<br>The threshold meaning varies based on the drift detection method, e.g., it can be the value of a distance metric or a p-value of a statistical test. |
| `drift_share` | Defines the share of drifting columns as a condition for Dataset Drift metric or inside a preset.  |
| `cat_stattest` <br>`cat_stattest_threshold` | Sets the drift method and/or threshold for all categorical columns in the dataset. |
| `num_stattest` <br>`num_stattest_threshold` | Sets the drift method and/or threshold for all numerical columns in the dataset. |
| `per_column_stattest`<br>`per_column_stattest_threshold` | Sets the drift method and/or threshold for the listed columns (accepts a dictionary).  |

{% hint style="info" %}
**How to check available parameters.** You can verify which parameters are available for a specific test, metric, or preset in the [All tests](../reference/all-tests.md) or [All metrics](../reference/all-metrics.md) tables or consult the [API reference]([../reference/api-reference](https://docs.evidentlyai.com/reference/api-reference))
{% endhint %}

## Available StatTest Functions:

- `ks` - Kolmogorov–Smirnov (K-S) test
  - default for numerical features
  - only for numerical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `chisquare` - Chi-Square test
  - default for categorical features if the number of labels for feature > 2
  - only for categorical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `z` - Z-test
  - default for categorical features if the number of labels for feature <= 2
  - only for categorical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `wasserstein` - Wasserstein distance (normed)
  - only for numerical features
  - returns `distance`
  - drift detected when `distance >= threshold`
- `kl_div` - Kullback-Leibler divergence
  - for numerical and categorical features
  - returns `divergence`
  - drift detected when `divergence >= threshold`
- `psi` - Population Stability Index (PSI)
  - for numerical and categorical features
  - returns `psi_value`
  - drift detected when `psi_value >= threshold`
- `jensenshannon` - Jensen-Shannon distance
  - for numerical and categorical features
  - returns `distance`
  - drift detected when `distance >= threshold`
- `anderson` - Anderson-Darling test
  - only for numerical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `fisher_exact` - Fisher's Exact test
  - only for categorical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `cramer_von_mises` - Cramer-Von-Mises test
  - only for numerical features
  - returns `p-value`
  - drift detected when `p_value < threshold`
- `g-test` - G-test
  - only for categorical features
  - returns `p-value`
  - drift detected when `p_value < threshold`
- `hellinger` - Hellinger Distance (normed)
  - for numerical and categorical features
  - returns `distance`
  - drift detected when `distance >= threshold`
- `mannw` - Mann-Whitney U-rank test
  - only for numerical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `ed` - Energy distance
  - only for numerical features
  - returns `distance`
  - drift detected when `distance >= threshold`
- `es` - Epps-Singleton test
  - only for numerical features
  - returns `p_value`
  - drift detected when `p_value < threshold`
- `t_test` - T-Test
  - only for numerical features
  - returns `p-value`
  - drift detected when `p_value < threshold`
- `emperical_mmd` - Emperical-MMD
  - only for numerical features
  - returns `p_value`
  -drift detected when `p_value < threshold`
- `TVD` - Total-Variation-Distance
  - only for categorical features
  - returns `p-value`
  - drift detected when `p_value < threshold`
