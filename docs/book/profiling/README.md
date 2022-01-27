## **Create a JSON profile**

Alternatively, you can generate and view the output as a JSON profile.

```python
data_drift_profile = Profile(sections=[DataDriftProfileSection()])
data_drift_profile.calculate(reference_data, recent_data, 
    column_mapping=column_mapping)
data_drift_profile.json()
```

For each profile, you should specify `sections` to include. They work just like Tabs. You can choose among:

* `DataDriftProfileSection` to estimate the data drift,
* `NumTargetDriftProfileSection` to estimate target drift for numerical target,
* `CatTargetDriftProfileSection`to estimate target drift for categorical target,
* `ClassificationPerformanceProfileSection` to explore the performance of a classification model,
* `ProbClassificationPerformanceProfileSection` to explore the performance of a probabilistic classification model,
* `RegressionPerformanceProfileSection` to explore the performance of a regression model.
