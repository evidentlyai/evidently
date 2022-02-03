---
description: How to generate dashboards in Evidently.
---

# Generate Dashboards

After [installation](../get-started/install-evidently.md), import `evidently` and the required tabs:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import (
    DataDriftTab,
    CatTargetDriftTab,
    RegressionPerformanceTab,
    ClassificationPerformanceTab,
    ProbClassificationPerformanceTab,
)
```

Create a `pandas.DataFrame` with the dataset to analyze:

```python
iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

You can choose one or several of the following **Tabs**.

* `DataDriftTab` to estimate the **data drift**
* `NumTargetDriftTab` to estimate **target drift** for the numerical target (for problem statements with the numerical target function: regression, probabilistic classification or ranking, etc.)
* `CatTargetDriftTab` to estimate **target drift** for the categorical target (for problem statements with the categorical target function: binary classification, multi-class classification, etc.)
* `RegressionPerformanceTab` to explore the **performance** of a regression model.
* `ClassificationPerformanceTab` to explore the **performance** of a classification model.
* `ProbClassificationPerformanceTab` to explore the **performance** of a probabilistic classification model and the quality of the model calibration.

You can generate the report without specifying the `ColumnMapping`:

```python
drift_dashboard = Dashboard(tabs=[DataDriftTab()])
drift_dashboard.calculate(reference_data, recent_data)
```

And with the `column_mapping` specification:

```python
drift_dashboard_with_mapping = Dashboard(tabs=[DataDriftTab()])
drift_dashboard_with_mapping.calculate(reference_data, recent_data, 
    column_mapping=column_mapping)
```
### Display the dashboard in Jupyter notebook

You can display the chosen Tabs in a single Dashboard directly in the notebook:

```python
drift_dashboard.show()
```

{% hint style="info" %}

**If the report is not displayed, this might be due to the dataset size.** The dashboard contains the data necessary to generate interactive plots and can become large. The limitation depends on infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. You can also generate JSON profiles instead.
{% endhint %}

### Export the report as an HTML file

You can save the report as an HTML file, and open it in your browser.

```python
drift_dashboard.save("reports/my_report.html")
```

If you get a security alert, press "trust HTML".

You will need to specify the path where to save your report and the report name. The report will not open automatically. To explore it, you should open it from the destination folder.

### Code examples

To generate the **Data Drift** report and save it as HTML, run:

```python
iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
iris_data_drift_report.calculate(iris_frame[:75], iris_frame[75:], 
    column_mapping = None)
iris_data_drift_report.save("reports/my_report.html")
```

To generate the **Data Drift** and the **Categorical Target Drift** reports, first add a target (and/or prediction) column to the initial dataset:&#x20;

```python
iris_frame['target'] = iris.target
```

Then run:

```python
iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab, CatTargetDriftTab])
iris_data_and_target_drift_report.calculate(iris_frame[:75], iris_frame[75:], 
    column_mapping=None)
iris_data_and_target_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html". The HTML report does not open automatically. To explore it, you should open it from the destination folder.

To generate the **Regression Model Performance** report, run:

```python
regression_model_performance = Dashboard(tabs=[RegressionPerformanceTab]) 
regression_model_performance.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
regression_model_performance.show()
```

For **Regression Model Performance report** from a single`DataFrame` , run:

```python
regression_single_model_performance = Dashboard(tabs=[RegressionPerformanceTab])
regression_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping)
regression_single_model_performance.show()
```

To generate the **Classification Model Performance report**, run:

```python
classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
classification_performance_report.show()
```

For **Probabilistic Classification Model Performance report**, run:

```python
classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
classification_performance_report.show()
```

For a **classification reports** from a single `DataFrame`, run:

```python
classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab])
classification_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping) 
classification_single_model_performance.show()
```

For a **probabilistic classification report** from a single `DataFrame`, run:

```python
prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab])
prob_classification_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping)
prob_classification_single_model_performance.show()
```

{% hint style="info" %}
