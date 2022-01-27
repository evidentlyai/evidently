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

### Generating JSON profiles

After installing the tool, import Evidently **profile** and the required sections:

```python
import pandas as pd
from sklearn import datasets

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

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


## Terminal

To generate the HTML report, run the following command in bash:

```bash
$ python -m evidently calculate dashboard --config config.json 
--reference reference.csv --current current.csv --output output_folder --report_name output_file_name
```

To generate a JSON profile, run the following command in bash:

```bash
$ python -m evidently calculate profile --config config.json 
--reference reference.csv --current current.csv --output output_folder --report_name output_file_name
```

Here:

* `reference` is the path to the reference data,
* `current` is the path to the current data,
* `output` is the path to the output folder,
* `config` is the path to the configuration file,
* `pretty_print` to print the JSON profile with indents (for profile only).

You can choose the following **Tabs**:

* `data_drift` to estimate the **data drift**,
* `num_target_drift` to estimate **target drift** for the numerical target
* `cat_target_drift` to estimate target drift for the categorical target
* `regression_performance` to explore the **performance** of a regression model
* `classification_performance` to explore the **performance** of a classification model
* `prob_classification_performance` to explore the **performance** of a probabilistic classification model

To configure the report you need to create the `config.json` file or a `config.yaml` file. This file configures the way of reading your input data and the type of the report.

### Configuration examples

Here is an example of a simple configuration, where we have comma-separated `csv` files with headers and there is no `date` column in the data.

**Dashboard**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":null
  },
  "column_mapping":{},
  "dashboard_tabs":["cat_target_drift"]
}
```

**Profile**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":null
  },
  "column_mapping":{},
  "profile_sections":["data_drift"],
  "pretty_print":true
}
```

Here is an example for a more complicated configuration, where we have comma-separated `csv` files with headers and `datetime` column. We also specified the `column_mapping` dictionary, where we added information about the `datetime`, `target` and `numerical_features`.

**Dashboard**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":"datetime"
  },
  "column_mapping":{
    "datetime":"datetime",
    "target":"target",
    "numerical_features":["mean radius", "mean texture", "mean perimeter", 
      "mean area", "mean smoothness", "mean compactness", "mean concavity", 
      "mean concave points", "mean symmetry"]},
  "dashboard_tabs":["cat_target_drift"],
  "sampling": {
      "reference": {
      "type": "none"
    },
      "current": {
      "type": "nth",
      "n": 2
    }
  }
}
```

**Profile**:

```yaml
{
  "data_format":{
    "separator":",",
    "header":true,
    "date_column":null
  },
  "column_mapping":{
    "target":"target",
    "numerical_features":["mean radius", "mean texture", "mean perimeter", 
      "mean area", "mean smoothness", "mean compactness", "mean concavity", 
      "mean concave points", "mean symmetry"]},
  "profile_sections":["data_drift", "cat_target_drift"],
  "pretty_print":true,
  "sampling": {
    "reference": {
      "type": "none"
    },
    "current": {
      "type": "random",
      "ratio": 0.8
    }
  }
}
```

### Telemetry

Telemetry is collected in Evidently starting from version 0.1.21.dev0.

When you use Evidently in the command-line interface, we collect some basic telemetry. It includes data on the environment (e.g. Python version) and usage (type of report or profile generated). You can read more about what we collect [here](../support/telemetry.md).

You can opt-out from telemetry collection by setting the environment variable:

```yaml
 EVIDENTLY_DISABLE_TELEMETRY=1
```

### Large datasets

As shown in the configuration example above, you can specify **sampling** parameters for large files. You can use different sampling strategies for the reference and current data, or apply sampling only to one of the files.

Currently, you can choose from the following options:

* `none`- **no sampling** will be applied
* `nth` - each **Nth row** of the file will be taken. This option works together with the `n` parameter (see the example with the Dashboard above)
* `random` - **random sampling** will be applied. This option works together with `ratio` parameter (see the example with the Profile above)

If you do not specify the sampling parameters in the configuration, it will be treated as none and no sampling will be applied.


