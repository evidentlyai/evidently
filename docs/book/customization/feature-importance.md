---
description: How to show feature importance in Data Drift evaluations.
---

You can add feature importances to the dataset-level data drift Tests, Metrics and Reports:
* `DataDriftTable`
* `DataDriftPreset`
* `DataDriftTestPreset`
* `TestShareOfDriftedColumns`

# Code example

Notebook example on showing feature importance:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_add_feature_importances_to_drift.ipynb" %}

# Compute feature importances

By default, the feature importance column is not shown. To display them, you must set the `feature_importance` parameter as `True`.

```python
report = Report(metrics = [
    DataDriftTable(feature_importance=True)
])
```

If you do not specify anything else, Evidently will train a random forest model using the provided dataset and derive the feature importances. 

**Notes**: 
* This is only possible if your dataset contains the `target` column.
* If you have both `current` and `reference` datasets, two different models will be trained. You will have two columns with feature importance: one for `reference` and one for `current` data.
* If your dataset also contains the `prediction` column, you should clearly label it using Column Mapping to avoid it being treated as a feature. 

## Pass your own importances

You can also pass the list of feature importances derived during the model training process. This is a recommended option. 

In this case, pass it as a list using the `additional_data` parameter when running the Report.

```python
report = Report(metrics = [
    DataDriftTable(feature_importance=True)
])
report.run(reference_data=reference,
           current_data=current.loc['2011-01-29 00:00:00':'2011-02-07 23:00:00'],
           column_mapping=column_mapping,
           additional_data = {'current_feature_importance':
              dict(map(lambda i,j : (i,j), numerical_features + categorical_features, regressor.feature_importances_))
            }
           )
```

You can pass the `current_feature_importance` – a single column will appear in this case. You can also optionally pass `reference_feature_importance`.
