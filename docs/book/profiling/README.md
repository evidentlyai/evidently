## JSON Profiles

To get the calculation results as a JSON file, you should create a **Profile**.

To specify which analysis you want to perform, you should select a **Section**. You can combine several sections together in a single Profile. Each section will contain a summary of metrics, results of statistical tests, and simple histograms that correspond to the chosen [Report](../get-started/reports/) type.&#x20;

You can generate profiles from Jupyter notebook or using Terminal.&#x20;

**This option helps integrate Evidently in your prediction pipelines:** for example, you can use Evidently to calculate drift, and then log the needed metrics externally (e.g. using [Mlflow](../step-by-step-guides/integrations/evidently-+-mlflow.md)).


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
