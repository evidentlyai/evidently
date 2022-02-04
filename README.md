<h1 align="center">Evidently</h1>
 
<p align="center"><b>An open-source framework to evaluate, test and monitor ML models in production.</b></p>

<p align="center">
  <a href="https://evidentlyai.gitbook.io/docs/">Docs</a>
  |
  <a href="https://discord.gg/xZjKRaNp8b">Discord Community</a>
  |
  <a href="https://evidentlyai.com/sign-up">Newsletter</a>
  | 
  <a href="https://evidentlyai.com/blog">Blog</a>
  | 
  <a href="https://twitter.com/EvidentlyAI">Twitter</a>
</p>


## What is it?

Evidently helps analyze and track data and ML model quality throughout the model lifecycle. You can think of it as an evaluation layer that fits into the existing ML stack.

Evidently has a modular approach with 3 interfaces on top of the shared `analyzer` functionality. 

# 1. Interactive visual reports 

![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/docs/images/evidently_4_reports_preview_small.png)

Evidently generates interactive `dashboards` from pandas `DataFrame` or `csv` files. You can use them for model evaluation, debugging and documentation. 

Each report covers a particular aspect of the model performance. You can display reports in Jupyter notebook or Colab or export as an HTML file. Currently 6 pre-built reports are available:
* **Data Drift**. Detects changes in the input feature distribution. 
* **Target Drift**: Numerical, Categorical. Detects changes in the model output.
* **Model Performance**: Classification, Probabilistic Classification, Regression. Evaluates the quality of the model and model errors.

# 2. Data and ML model profiling 

Evidently also generates JSON `profiles`. You can use them to integrate the data or model evaluation step into the ML pipeline. 

You can log and store JSON profiles for further analysis, or build a conditional workflow based on the result of the check (e.g. to trigger alert, retraining, or generate a visual report). The profiles calculate the same metrics and statistical tests as visual reports. 

You can explore example integrations with tools like Airflow and Mlflow.

# 3. Real-time ML monitoring 

![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/docs/images/evidently_data_drift_grafana_dashboard_top.png)

Evidently has `monitors` that collect the data and model metrics from a deployed ML service. You can use it to build live monitoring dashboards. Evidently configures the monitoring on top of the streaming data and emits the metrics. You can log and use the metrics elsewhere. 

There is a lightweight integration with Prometheus and Grafana that comes with pre-built dashboards.

## Installing from PyPI
### MAC OS and Linux
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```

The tool allows building interactive reports both inside a Jupyter notebook and as a separate HTML file. If you only want to generate interactive reports as HTML files or export as JSON profiles, the installation is now complete.

To enable building interactive reports inside a Jupyter notebook, we use jupyter nbextension. If you want to create reports inside a Jupyter notebook, then after installing `evidently` you should run the two following commands in the terminal from evidently directory.

To install jupyter nbextension, run:
```sh
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```
To enable it, run:
```sh
$ jupyter nbextension enable evidently --py --sys-prefix
```
That's it!

**Note**: a single run after the installation is enough. No need to repeat the last two commands every time.

**Note 2**: if you use Jupyter Lab, you may experience difficulties with exploring report inside a Jupyter notebook. However, the report generation in a separate .html file will work correctly.

### Windows
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```
The tool allows building interactive reports both inside a Jupyter notebook and as a separate HTML file. Unfortunately, building reports inside a Jupyter notebook is not yet possible for Windows. The reason is Windows requires administrator privileges to create symlink. In later versions we will address this issue.

## Getting started

### Jupyter Notebook
To start, prepare your data as two pandas `DataFrames`. The first should include your reference data, the second - current production data. The structure of both datasets should be identical. 

* For **Data Drift** report, include the input features only.
* For **Target Drift** reports, include the column with Target and/or Prediction.
* For **Model Performance** reports, include the columns with Target and Prediction.

Calculation results can be available in one of the two formats:
* Option 1: an interactive **Dashboard** displayed inside the Jupyter notebook or exportable as a HTML report.
* Option 2: a JSON **Profile** that includes the values of metrics and the results of statistical tests.  

#### Option 1: Dashboard

After installing the tool, import Evidently **dashboard** and required tabs:

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

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
iris_frame['target'] = iris.target
```

To generate the **Data Drift** report, run:
```python
iris_data_drift_report = Dashboard(tabs=[DataDriftTab()])
iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
iris_data_drift_report.save("reports/my_report.html")
```

To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
```python
iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab(), CatTargetDriftTab()])
iris_data_and_target_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
iris_data_and_target_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html".
HTML report does not open automatically. To explore it, you should open it from the destination folder.

To generate the **Regression Model Performance** report, run:
```python
regression_model_performance = Dashboard(tabs=[RegressionPerformanceTab()]) 
regression_model_performance.calculate(reference_data, current_data, column_mapping = column_mapping) 
```

You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
```python
regression_single_model_performance = Dashboard(tabs=[RegressionPerformanceTab()])
regression_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

To generate the **Classification Model Performance** report, run:
```python
classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab()])
classification_performance_report.calculate(reference_data, current_data, column_mapping = column_mapping)
```
 
For **Probabilistic Classification Model Performance** report, run:
```python
classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab()])
classification_performance_report.calculate(reference_data, current_data, column_mapping = column_mapping)
```
 
You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
```python
classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab()])
classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```
or
```python
prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab()])
prob_classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

#### Option 2: Profile

After installing the tool, import Evidently **profile** and required sections:

```python
import pandas as pd
from sklearn import datasets

from evidently.model_profile import Profile
from evidently.model_profile.sections import (
    DataDriftProfileSection,
    CatTargetDriftProfileSection,
    RegressionPerformanceProfileSection,
    ClassificationPerformanceProfileSection,
    ProbClassificationPerformanceProfileSection,
)

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

To generate the **Data Drift** profile, run:
```python
iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
iris_data_drift_profile.calculate(iris_frame, iris_frame, column_mapping = None)
iris_data_drift_profile.json() 
```

To generate the **Data Drift** and the **Categorical Target Drift** profile, run:
```python
iris_target_and_data_drift_profile = Profile(sections=[DataDriftProfileSection(), CatTargetDriftProfileSection()])
iris_target_and_data_drift_profile.calculate(iris_frame[:75], iris_frame[75:], column_mapping = None) 
iris_target_and_data_drift_profile.json() 
```

You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
```python
regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection()])
regression_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

To generate the **Classification Model Performance** profile, run:
```python
classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection()])
classification_performance_profile.calculate(reference_data, current_data, column_mapping = column_mapping)
```

For **Probabilistic Classification Model Performance** profile, run:
```python
classification_performance_report = Profile(sections=[ProbClassificationPerformanceProfileSection()])
classification_performance_report.calculate(reference_data, current_data, column_mapping = column_mapping)
```

You can also generate either of the **Classification** profiles for a single `DataFrame`. In this case, run:
```python
classification_single_model_performance = Profile(sections=[ClassificationPerformanceProfileSection()])
classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```
or
```python
prob_classification_single_model_performance = Profile(sections=[ProbClassificationPerformanceProfileSection()])
prob_classification_single_model_performance.calculate(reference_data, None, column_mapping=column_mapping)
```

## Community Reports
* A simple dashboard which contains two custom widgets with target distribution information [link to repository](https://github.com/0lgaF/my_tab_with_evidently)

## Google Colab, Kaggle Kernel, Deepnote
You can run ```evidently``` in [Google Colab](https://colab.research.google.com/), [Kaggle Notebook](https://www.kaggle.com/code) and [Deepnote](https://deepnote.com/).

First, install ```evidently```. Run the following command in the notebook cell:
```!pip install evidently```

There is no need to enable nbextension for this case, because ```evidently``` uses an alternative way to display visuals in the hosted notebooks.

To build a ```Dashboard``` or a ```Profile``` simply repeat the steps described in the previous paragraph. For example, to build the **Data Drift** dashboard, run:

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)

iris_data_drift_report = Dashboard(tabs=[DataDriftTab()])
iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
```

To display the dashboard in the Google Colab, Kaggle Kernel, Deepnote, run:
```python
iris_data_drift_report.show()
```

The ```show()``` method has the argument ```mode```, which can take the following options:

* **auto** - the default option. Ideally, you will not need to specify the value for ```mode``` and use the default. But, if it does not work (in case we failed to determine the environment automatically), consider setting the correct value explicitly.
* **nbextension** - to show the UI using nbextension. Use this option to display dashboards in Jupyter notebooks (it should work automatically).
* **inline** - to insert the UI directly into the cell. Use this option for PyLab, Google Colab, Kaggle Kernels and Deepnote. For Google Colab, this should work automatically, for **PyLab**, **Kaggle Kernels** and **Deepnote** the option should be specified explicitly.

## Telemetry
When you use Evidently in the command-line interface, we collect basic telemetry (starting from 0.1.21.dev0 version). It includes data on the environment (e.g. Python version) and usage (type of report or profile generated). You can read more about what we collect [here](https://docs.evidentlyai.com/support/telemetry). 

You can opt-out from telemetry collection by setting the environment variable EVIDENTLY_DISABLE_TELEMETRY=1

## Large datasets
As you can see from the above example, you can specify **sampling** parameters for large files. You can use different sampling strategies for reference and current data, or apply sampling only to one of the files. 
Currently we have 3 sampling types available:
* `none` - there will be no sampling for the file,
* `nth` - each Nth row of the file will be taken. This option works together with `n` parameter (see the example with the Dashboard above)
* `random` - random sampling will be applied. This option works together with `ratio` parameter (see the example with the Profile above)

## Documentation
For more information, refer to a complete <a href="https://evidentlyai.gitbook.io/docs/">Documentation</a>.

## Examples
- See **Data Drift** Dashboard and Profile generation to explore the results both inside a Jupyter notebook and as a separate .html file:
[Iris](https://colab.research.google.com/drive/1TCdDjuiMzvSyjkIJOwYl2dkN8N56c00Z), 
[Boston](https://colab.research.google.com/drive/1J8FvINy5nX47L5-iklsGD4C4y1Zi1Wlo)

- See **Categorical Target and Data Drift** Dashboard and Profile generation to explore the results both inside a Jupyter notebook and as a separate file:
[Iris](https://colab.research.google.com/drive/18HvFvZeIjOmbAV7KVL103PlWlFuIjdGj),
[Breast Cancer](https://colab.research.google.com/drive/157kTbk-uZKi4Q6Eea3yaEbLrpR_h_Pow)

- See **Numerical Target and Data Drift** Dashboard and Profile generation to explore the results both inside a Jupyter notebook and as a separate file:
[Boston](https://colab.research.google.com/drive/1IDE02r-Xh-T4k5Yw3SpRGlewHOS8ZsmX) 

- See **Regression Performance** Dashboard and Profile generation to explore the results both inside a Jupyter notebook and as a separate file:
[Bike Sharing Demand](https://colab.research.google.com/drive/1VA1KjBYxMRfccSS5IXAClBGKB9Lw7WtP)

- See **Classification Performance** Dashboard and Profile generation to explore the results both inside a Jupyter notebook and as a separate file:
[Iris](https://colab.research.google.com/drive/1SAsaUTUaIzg3FyI_EbmO9hzuEu1hVl4v) 
 
- See **Probabilistic Classification Performance** Dashboard and Profile generation to explore the results both inside a Jupyter notebook and as a separate .html file:
[Iris](https://colab.research.google.com/drive/1uFN0ZWNLk3ExylBywq_M8oGkmac0lDrq), 
[Breast Cancer](https://colab.research.google.com/drive/1vwEBgGnDVk5BJG2PXT1w41VfZ-_bq_Sw)

## Stay updated
We will be releasing more reports soon. If you want to receive updates, follow us on [Twitter](https://twitter.com/EvidentlyAI), or sign up for our [newsletter](https://evidentlyai.com/sign-up). You can also find more tutorials and explanations in our [Blog](https://evidentlyai.com/blog). If you want to chat and connect, join our [Discord community](https://discord.gg/xZjKRaNp8b)!

