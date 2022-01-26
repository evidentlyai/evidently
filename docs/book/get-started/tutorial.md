# Getting Started Tutorial

You can generate the dashboards and JSON profiles using **Jupyter notebook** or **terminal**. You can also use Google Colab, Kaggle Kernel, Deepnote. All options are described below.

{% hint style="info" %}
If you want to **display** the dashboards directly in Jupyter notebook, make sure you [installed](install-evidently.md) the Jupyter **nbextension**.
{% endhint %}

For a more **detailed version**, head to the step-by-step guide on using `evidently` in [Jupyter notebook](../step-by-step-guides/step-by-step-guide-for-jupyter-notebooks.md) or [Command-line interface](../step-by-step-guides/cli.md).

If you prefer a **video** version, here is a **10-min Quick Start** on how to generate Data and Target Drift reports and JSON profiles in the Jupyter notebook.&#x20;

{% embed url="https://www.youtube.com/watch?v=g0Z2e-IqmmU&ab_channel=EvidentlyAI" %}



## Prepare the data

To generate the reports using the **Jupyter notebook** or anther notebook environment, prepare the data as pandas `DataFrames`. To use the **terminal**, prepare it as `csv`files.

You can prepare two datasets. The first should include the **reference** data, the second—**current** production data. The structure of datasets should be identical.

You can also generate comparative reports from a **single** `DataFrame`or `csv` file. You will need to **identify rows** that refer to reference and production data.

Model Performance reports can be generated for a **single** dataset, with no comparison performed. You can simply pass a single `DataFrame`or `csv` file.&#x20;

The data structure is different depending on the report type.

* For the **Data Drift** report, include the input features only.&#x20;
* For the **Target Drift** reports, include the input features and the column with the Target and/or the Prediction.&#x20;
* For the **Model Performance** reports, include the input features, the column with the Target, and the column with the Prediction.

If you include more columns than needed for a given report, they will be ignored. &#x20;

## Decide on the output format

Calculation results can be available in one of the following formats:

* An interactive visual **Dashboard** displayed inside the Jupyter notebook.
* An exportable **HTML report**. The same as dashboard, but standalone.&#x20;
* A **JSON profile** with a summary of metrics and statistical test results.&#x20;

**Dashboards** are best for ad-hoc analysis, debugging, and team sharing.

**Profiles** are best for integration into prediction pipelines or with external visualization tools.

You can proceed to work with Jupyter notebook or generate JSON profiles and HTML reports via Terminal.

| Output format    | Jupyter notebook | Terminal |
| ---------------- | ---------------- | -------- |
| **Dashboard**    | +                | -        |
| **HTML report**  | +                | +        |
| **JSON profile** | +                | +        |

All options are described below.

## Jupyter notebook&#x20;

### Generating dashboards and HTML reports

After installing the tool, import `evidently` and the required tabs:

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

Create a `Pandas DataFrame` with the dataset to analyze:

```python
iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

`Dashboard` generates an interactive report that includes the selected `Tabs`.&#x20;

You can choose the following **Tabs**:

* `DataDriftTab` to estimate the **data drift**
* `NumTargetDriftTab` to estimate **target drift** for the numerical **** target&#x20;
* `CatTargetDriftTab` to estimate **target drift** for the categorical target&#x20;
* `RegressionPerformanceTab` to explore the **performance** of a regression model
* `ClassificationPerformanceTab` to explore the **performance** of a classification **** model
* `ProbClassificationPerformanceTab` to explore the **performance** of a probabilistic classification model&#x20;

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
regression_model_performance = Dashboard(tabs=[RegressionPerfomanceTab]) 
regression_model_performance.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
regression_model_performance.show()
```

For **Regression Model Performance report** from a single`DataFrame` , run:

```python
regression_single_model_performance = Dashboard(tabs=[RegressionPerfomanceTab])
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
**It might take some time to display the report. If it does not show, this might be due to the dataset size.** The dashboard contains the data necessary to generate interactive plots and can become large. The limitation depends on infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. You can also generate a JSON profile instead 👇🏼
{% endhint %}

### Generating JSON profiles&#x20;

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

## Google Colab, Kaggle Kernel, Deepnote

You can run `evidently` in [Google Colab](https://colab.research.google.com), [Kaggle Notebook](https://www.kaggle.com/code) and [Deepnote](https://deepnote.com).

First, install `evidently`. Run the following command in the notebook cell:

```
!pip install evidently
```

There is no need to enable nbextension for this case. Evidently uses an alternative way to display visuals in the hosted notebooks.

To build a `Dashboard` or a `Profile` simply repeat the steps described in the previous paragraph. For example, to build the **Data Drift** dashboard, run:

```
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)

iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
```

To display the dashboard in the Google Colab, Kaggle Kernel, Deepnote, run:

```
iris_data_drift_report.show()
```

The `show()` method has the argument `mode`, which can take the following options:

* **auto** - the default option. Ideally, you will not need to specify the value for `mode` and use the default. But, if it does not work (in case we failed to determine the environment automatically), consider setting the correct value explicitly.
* **nbextension** - to show the UI using nbextension. Use this option to display dashboards in Jupyter notebooks (it should work automatically).
* **inline** - to insert the UI directly into the cell. Use this option for Google Colab, Kaggle Kernels and Deepnote. For Google Colab, this should work automatically, for **Kaggle Kernels** and **Deepnote** the option should be specified explicitly.

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

