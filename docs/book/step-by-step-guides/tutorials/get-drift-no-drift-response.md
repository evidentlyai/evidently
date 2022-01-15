# Get Drift/No Drift response

**TL;DR:** You can use Evidently to evaluate drift for individual features and then add custom parameters to get a boolean TRUE/FALSE response for the overall dataset drift. Here is an example [Jupyter notebook](../../evidently/tutorials/drift\_detection.ipynb).

### **Overview**

Evidently returns the results of the statistical tests by providing P-values for individual feature drift. However, it is often convenient to get an aggregated response on "Did my data drift?" by introducing some logic on top of it.&#x20;

You can define a combination of parameters (e.g., number of features drifting) to set conditions that trigger the "Drift" response.

The exact choice of parameters requires an understanding of the use case and model (e.g., feature importances, stability, etc.)

### Example

In this example [Jupyter notebook](../../evidently/tutorials/drift\_detection.ipynb), we use Evidently profiles to calculate data drift. Then, we add the following custom parameters:

* **Confidence interval** for **** individual feature drift. (Default: 0.95)
* **Drift threshold** on the share of drifting features. (Default: 0.5).

This will return the TRUE response for dataset drift if more than 50% of features drift at a defined confidence level.

```
    def detect_dataset_drift(reference, production, column_mapping, confidence=0.95, threshold=0.5, get_ratio=False):

    data_drift_profile = Profile(sections=[DataDriftProfileSection])
    data_drift_profile.calculate(reference, production, column_mapping=column_mapping)
    report = data_drift_profile.json()
    json_report = json.loads(report)

    drifts = []
    num_features = column_mapping.get('numerical_features') if column_mapping.get('numerical_features') else []
    cat_features = column_mapping.get('categorical_features') if column_mapping.get('categorical_features') else []
    for feature in num_features + cat_features:
        drifts.append(json_report['data_drift']['data']['metrics'][feature]['p_value']) 
        
    n_features = len(drifts)
    n_drifted_features = sum([1 if x<(1. - confidence) else 0 for x in drifts])
    if get_ratio:
        return n_drifted_features/n_features
    else:
        return True if n_drifted_features/n_features >= threshold else False
```

We can then test data drift for select periods by specifying reference and current data. Here, we also set the drift threshold at 0.8.

```
#February to March drift
detect_dataset_drift(raw_data.loc['2011-02-01 00:00:00':'2011-02-28 23:00:00'], 
             raw_data.loc['2011-03-01 00:00:00':'2011-03-31 23:00:00'], 
             column_mapping=data_columns,
             threshold=0.8
            )
```

The output of the cell returns a TRUE/FALSE drift response.
