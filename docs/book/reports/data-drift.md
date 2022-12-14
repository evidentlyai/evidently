**TL;DR:** You can detect changes in the input feature distributions.

For Reports, you can use the `DataDriftPreset`. For Test Suites, you can use the `DataDriftTestPreset`.  

# Use Case

You can evaluate data drift: 

**1. To monitor the model performance without ground truth.** When you do not have true labels or actuals, you can monitor Input Feature Drift to check if the model is operating in a familiar environment. You can often monitor input drift only for a subset of features, for example, most important features. You can also apply it to all features but only declare meaningful dataset drift if e.g. only 50% of features drifted. You can typically combine it with the [Prediction Drift monitoring.](prediction-drift.md)

**2. When you are debugging the model decay.** If you observe a drop in the model quality, you can evaluate Data Drift to explore the change in the feature patterns, e.g. to understand the change in the environment or discover the appearance of a new segment. 

**3. To understand model drift in an offline environment.** You can explore the historical data drift to understand past changes in the input data and define optimal drift detection approach and retraining strategy. Read more in a [blog](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) about it.

**4. Before model retraining.** Before feeding fresh data into the model, you might want to verify whether it even makes sense. If there is no data drift drift, the environment is stable, and retraining might not be necessary.

# Report: Data Drift Preset 

## How it works

The **Data Drift** report helps detect and explore changes in the input data.

* Applies as suitable **drift detection method** for numerical and categorical features.
* Plots **feature values and distributions** for the two datasets.

## Data Requirements

You will need **two** datasets. The **reference** dataset serves as a benchmark. Evidently analyzes the change by comparing the **current** production data to the **reference** data.

The dataset should include the features you want to evaluate for drift. The schema of both datasets should be identical.

Evidently can evaluate drift both for numerical and categorical features. You can explicitly specify the type of the column in column mapping. If it is not specified, Evidently will define the column type automatically.

## How it looks

The default report includes 4 components. All plots are interactive.

### 1. Data Drift Summary

The report returns **the share of drifting features** and an aggregate **Dataset Drift** result. For example:

![](../.gitbook/assets/reports\_data\_drift\_summary.png)

Dataset Drift sets a rule on top of the results of the statistical tests for individual features. By default, Dataset Drift is detected if at least 50% of features drift.

Evidently uses the default [data drift detection algorithm](../reference/data-drift-algorithm.md) to select the drift detection method based on feature type and the number of observations in the reference dataset.

{% hint style="info" %}
You can modify the drift detection logic by selecting a different method already available in the library, including PSI, K–L divergence, Jensen-Shannon distance, Wasserstein distance, setting a different threshold and condition for the dataset drift. See more details about [setting data drift options](../customization/options-for-statistical-tests.md). You can also implement a [custom drift detection method](../customization/add-custom-metric-or-test.md). 
{% endhint %}

To build up a better intuition for which tests are better in different kinds of use cases, visit our blog to read [our in-depth guide](https://evidentlyai.com/blog/data-drift-detection-large-datasets) to the tradeoffs when choosing the statistical test for data drift.

### 2. Data Drift Table

The table shows the drifting features first. You can also choose to sort the rows by the feature name or type.

![](../.gitbook/assets/reports\_data\_drift\_table.png)

### 3. Data Drift by Feature

By clicking on each feature, you can explore the values mapped in a plot.

* The dark green line is the **mean**, as seen in the reference dataset.
* The green area covers **one standard deviation** from the mean.

![](<../.gitbook/assets/reports\_data\_drift\_drift\_by\_feature (2).png>)

### 4. Data Distribution by Feature

You can also zoom on distributions to understand what has changed.

![](<../.gitbook/assets/reports\_data\_drift\_distr\_by\_feature (2).png>)


## Metrics output

You can get the report output as a JSON or a Python dictionary:

```yaml
{
  "data_drift": {
    "name": "data_drift",
    "datetime": "datetime",
    "data": {
      "utility_columns": {
        "date": null,
        "id": null,
        "target": null,
        "prediction": null,
        "drift_conf_level": value,
        "drift_features_share": value,
        "nbinsx": {
          "feature_name": value,
          "feature_name": value
        },
        "xbins": null
      },
      },
      "cat_feature_names": [],
      "num_feature_names": [],
      "metrics": {
        "feature_name" :{
          "prod_small_hist": [
            [],
            []
          ],
          "ref_small_hist": [
            [],
            []
          ],
          "feature_type": "num",
          "p_value": p_value
      },
      "n_features": value,
      "n_drifted_features": value,
      "share_drifted_features": value,
      "dataset_drift": false
    }
  },
  "timestamp": "timestamp"
}
```

## Report customization

* You can [specify the drift detection methods and thresholds](../customization/options-for-statistical-tests.md). 
* You can add a [custom drift detection method](../customization/add-custom-metric-or-test.md).
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* You can create a different report or test suite from scratch taking this one as an inspiration. 


# Examples

* Browse the [examples](../get-started/examples.md) for sample Jupyter notebooks and Colabs.

You can also explore [more blog posts](https://www.evidentlyai.com/tags/data-drift) about drift detection. 
