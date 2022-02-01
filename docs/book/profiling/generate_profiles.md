---
description: How to generate JSON profiles in Evidently.
---

# Generate profiles

After [installation](../get-started/install-evidently.md), import `evidently` and the required profiles sections:

```python
import pandas as pd
from sklearn import datasets

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
```

`Sections` in Profiles work just like `Tabs` in Dashboards. You can choose among:

* `DataDriftProfileSection` to estimate the data drift,
* `NumTargetDriftProfileSection` to estimate target drift for numerical target,
* `CatTargetDriftProfileSection`to estimate target drift for categorical target,
* `ClassificationPerformanceProfileSection` to explore the performance of a classification model,
* `ProbClassificationPerformanceProfileSection` to explore the performance of a probabilistic classification model,
* `RegressionPerformanceProfileSection` to explore the performance of a regression model.

Create a `pandas.DataFrame` with the dataset to analyze:

```python
iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

Generate and view the output as a JSON profile.

```python
data_drift_profile = Profile(sections=[DataDriftProfileSection()])
data_drift_profile.calculate(reference_data, recent_data, 
    column_mapping=column_mapping)
data_drift_profile.json()
```

### Code examples

To generate the **Data Drift** profile, run:

```python
iris_data_drift_profile = Profile(sections=[DataDriftProfileSection])
iris_data_drift_profile.calculate(iris_frame, iris_frame, column_mapping=None)
iris_data_drift_profile.json() 
```

To generate the **Data Drift** and the **Categorical Target Drift** profile, run:

```python
iris_target_and_data_drift_profile = Profile(sections=[DataDriftProfileSection, CatTargetDriftProfileSection])
iris_target_and_data_drift_profile.calculate(iris_frame[:75], iris_frame[75:], column_mapping=None) 
iris_target_and_data_drift_profile.json() 
```

You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:

```python
regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection])
regression_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
regression_single_model_performance.json()
```

To generate the **Classification Model Performance** profile, run:

```python
classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection])
classification_performance_profile.calculate(reference_data, current_data, column_mapping=column_mapping)
classification_performance_profile.json()
```

For **Probabilistic Classification Model Performance** profile, run:

```python
classification_performance_report = Profile(sections=[ProbClassificationPerformanceProfileSection])
classification_performance_report.calculate(reference_data, current_data, column_mapping=column_mapping)
classification_performance_report.json()
```

You can also generate either of the **Classification** profiles for a single `DataFrame`. In this case, run:

```python
classification_single_model_performance = Profile(sections=[ClassificationPerformanceProfileSection])
classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
classification_single_model_performance.json()
```

or

```python
prob_classification_single_model_performance = Profile(sections=[ProbClassificationPerformanceProfileSection])
prob_classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
prob_classification_single_model_performance.json()
```
