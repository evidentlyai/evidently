<h1 align="center">Evidently</h1>
 
<p align="center"><b>An open-source framework to evaluate, test and monitor ML models in production.</b></p>

<p align="center">
  <a href="https://docs.evidentlyai.com">Docs</a>
  |
  <a href="https://discord.gg/xZjKRaNp8b">Discord Community</a>
  |
  <a href="https://evidentlyai.com/sign-up">Newsletter</a>
  | 
  <a href="https://evidentlyai.com/blog">Blog</a>
  | 
  <a href="https://twitter.com/EvidentlyAI">Twitter</a>
</p>


# :bar_chart: What is Evidently?

Evidently is an open-source Python library for data scientists and ML engineers. It helps evaluate, test, and monitor the performance of ML models from validation to production.

Evidently has a modular approach with 3 interfaces on top of the shared `metrics` functionality. 

## 1. Tests: batch model checks

![Tests example](docs/images/evidently_tests_main-min.png)

Tests perform structured data and ML model quality checks. They verify a condition and return an explicit **pass** or **fail** result. 

You can create a custom Test Suite from 50+ individual tests or run a preset (for example, **Data Drift** or **Regression Performance**). You can get results as an interactive **visual dashboard** inside Jupyter notebook or Colab, or export as **JSON** or Python dictionary. 

Tests are best for automated batch model checks. You can integrate them as a pipeline step using tools like Airlfow. 

## 2. Reports: interactive dashboards

> **Note**
> We added a new Report object starting from v0.1.57.dev0. Reports unite the functionality of Dashboards and JSON profiles with a new, cleaner API. You can still use the old [Dashboards API](https://docs.evidentlyai.com/features/dashboards/generate_dashboards) but it will soon be depreciated.

![Report example](docs/images/evidently_reports_main-min.png)

Reports calculate various data and ML **metrics** and render rich **visualizations**. You can create a custom Report or run a preset to evaluate a specific aspect of the model or data performance. For example, a [**Data Quality**](https://docs.evidentlyai.com/reports/data-quality) or [**Classification Performance**](https://docs.evidentlyai.com/reports/classification-performance) report.

You can get an **HTML report** (best for exploratory analysis and debugging) or export results as **JSON** or Python dictionary (best for logging, documention or to integrate with BI tools). 

## 3. Real-time ML monitoring 

> **Note**
> This functionality is in development and subject to API change.

![Dashboard example](docs/images/evidently_monitoring_main.png)

Evidently has `monitors` that collect data and model metrics from a deployed ML service. You can use it to build live monitoring dashboards. Evidently configures the monitoring on top of streaming data and emits the metrics in Prometheus format. There are pre-built Grafana dashboards to visualize them.

# :woman_technologist: Installing from PyPI

### MAC OS and Linux
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```
If you only want to get results as HTML or JSON files, the installation is now complete. To display the dashboards inside a Jupyter notebook, you need `jupyter nbextension`. After installing `evidently`, run the two following commands in the terminal from the evidently directory.

To install jupyter nbextension, run:
```sh
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```
To enable it, run:
```sh
$ jupyter nbextension enable evidently --py --sys-prefix
```
That's it! A single run after the installation is enough. 

**Note**: if you use Jupyter Lab, the reports might not display in the notebook. However, you can still save them as HTML files. 

### Windows
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```
Unfortunately, building reports inside a Jupyter notebook is not yet possible for Windows. The reason is Windows requires administrator privileges to create symlink. In later versions we will address this issue. You can still generate the HTML to view externally.

# :arrow_forward: Getting started

## Jupyter Notebook
To start, prepare your data as two pandas `DataFrames`. The first should include your reference data, the second - current production data. The structure of both datasets should be identical. 

To run some of the evaluations (e.g. Data Drift), you need input features only. In other cases (e.g. Target Drift, Classification Performance), you need Target and/or Prediction. To load the toy data example:

```python
import pandas as pd
import numpy as np
 
from sklearn.datasets import fetch_california_housing
```

### Option 1: Test Suites

from evidently.report import Report
from evidently.metric_preset import DataDrift, NumTargetDrift
 
from evidently.test_suite import TestSuite
from evidently.test_preset import DataQuality, DataStability
from evidently.tests import *

After installing the tool, import Evidently **dashboard** and required tabs:

```python
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import (
    DataDriftTab,
    CatTargetDriftTab
)

iris = datasets.load_iris(as_frame=True)
iris_frame, iris_frame["target"] = iris.data, iris.target
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

### Option 2: Profile

After installing the tool, import Evidently **profile** and required sections:

```python
from sklearn import datasets

from evidently.model_profile import Profile
from evidently.model_profile.sections import (
    DataDriftProfileSection,
    CatTargetDriftProfileSection
)

iris = datasets.load_iris(as_frame=True)
iris_frame = iris.data
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
## Google Colab, Kaggle Kernel, Deepnote

<details><summary>Read instructions on how to run Evidently in other notebook environments.</summary>
<p>

You can run ```evidently``` in [Google Colab](https://colab.research.google.com/), [Kaggle Notebook](https://www.kaggle.com/code) and [Deepnote](https://deepnote.com/).

First, install ```evidently```. Run the following command in the notebook cell:
```!pip install evidently```

There is no need to enable nbextension for this case, because ```evidently``` uses an alternative way to display visuals in the hosted notebooks.

To build a ```Dashboard``` or a ```Profile``` simply repeat the steps described in the previous paragraph. For example, to build the **Data Drift** dashboard, run:

```python
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

iris = datasets.load_iris(as_frame=True)
iris_frame = iris.data

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

</p>
</details>

# :computer: Contributions
We welcome contributions! Read the [Guide](CONTRIBUTING.md) to learn more. 

# :framed_picture: Community Reports
You can also contribute custom reports with a combination of own metrics and widgets. We'll be glad to showcase some of them!
* A simple dashboard which contains two custom widgets with target distribution information: [link to repository](https://github.com/0lgaF/my_tab_with_evidently)

# :books: Documentation
For more information, refer to a complete <a href="https://docs.evidentlyai.com">Documentation</a>. You can start with this [Tutorial](https://docs.evidentlyai.com/tutorial) for a quick introduction.

# :card_index_dividers: Examples
Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box.

| Report                                                | Jupyter notebook                                                                                 | Colab notebook                                                                    | Data source                                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Evidently Metrics| [link](sample_notebooks/evidently_metrics.ipynb) | [link](https://colab.research.google.com/drive/1IpfQsq5dmjuG_Qbn6BNtghq6aubZBP5A) | Adult data set openml |
| Evidently Metric Presets| [link](sample_notebooks/evidently_metric_presets.ipynb) | [link](https://colab.research.google.com/drive/1wmHWipPd6iEy9Ce8NWBcxs_BSa9hgKgk) | Adult data set openml, California housing sklearn.datasets, Breast cancer sklearn.datasets, Iris plants sklearn.datasets |
| Evidently Tests| [link](sample_notebooks/evidently_tests.ipynb) | [link](https://colab.research.google.com/drive/1nQhfXft4VZ3G7agvXgH_LqVHdCh-WaMl) | Adult data set openml, California housing sklearn.datasets, Breast cancer sklearn.datasets, Iris plants sklearn.datasets |
| Evidently Test Presets| [link](sample_notebooks/evidently_test_presets.ipynb) | [link](https://colab.research.google.com/drive/1CBAFY1qmHHV_72SC7YBeaD4c6LLpPQan) | Adult data set openml, California housing sklearn.datasets, Breast cancer sklearn.datasets, Iris plants sklearn.datasets |
| Data Drift + Categorical Target Drift (Multiclass)    | [link](examples/sample_notebooks/multiclass_target_and_data_drift_iris.ipynb)                    | [link](https://colab.research.google.com/drive/1Dd6ZzIgeBYkD_4bqWZ0RAdUpCU0b6Y6H) | Iris plants sklearn.datasets                                                           |
| Data Drift + Categorical Target Drift (Binary)        | [link](examples/sample_notebooks/binary_target_and_data_drift_breast_cancer.ipynb)               | [link](https://colab.research.google.com/drive/1gpzNuFbhoGc4-DLAPMJofQXrsX7Sqsl5) | Breast cancer sklearn.datasets                                                         |
| Data Drift + Numerical Target Drift                   | [link](examples/sample_notebooks/numerical_target_and_data_drift_california_housing.ipynb)       | [link](https://colab.research.google.com/drive/1TGt-0rA7MiXsxwtKB4eaAGIUwnuZtyxc) | California housing sklearn.datasets                                                    |
| Regression Performance                                | [link](examples/sample_notebooks/regression_performance_bike_sharing_demand.ipynb)               | [link](https://colab.research.google.com/drive/1ONgyDXKMFyt9IYUwLpvfxz9VIZHw-qBJ) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset) |
| Classification Performance (Multiclass)               | [link](examples/sample_notebooks/classification_performance_multiclass_iris.ipynb)               | [link](https://colab.research.google.com/drive/1pnYbVJEHBqvVmHUXzG-kw-Fr6PqhzRg3) | Iris plants sklearn.datasets                                                           |
| Probabilistic Classification Performance (Multiclass) | [link](examples/sample_notebooks/probabilistic_classification_performance_multiclass_iris.ipynb) | [link](https://colab.research.google.com/drive/1UkFaBqOzBseB_UqisvNbsh9hX5w3dpYS) | Iris plants sklearn.datasets                                                           |
| Classification Performance (Binary)                   | [link](examples/sample_notebooks/classification_performance_breast_cancer.ipynb)                 | [link](https://colab.research.google.com/drive/1b2kTLUIVJkKJybYeD3ZjpaREr_9dDTpz) | Breast cancer sklearn.datasets                                                         |
| Probabilistic Classification Performance (Binary)     | [link](examples/sample_notebooks/probabilistic_classification_performance_breast_cancer.ipynb)   | [link](https://colab.research.google.com/drive/1sE2H4mFSgtNe34JZMAeC3eLntid6oe1g) | Breast cancer sklearn.datasets                                                         |
| Data Quality                                          | [link](examples/sample_notebooks/data_quality_bike_sharing_demand.ipynb)                                  | [link](https://colab.research.google.com/drive/1XDxs4k2wNHU9Xbxb9WI2rOgMkZFavyRd) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset) |

## Integrations
See how to integrate Evidently in your prediction pipelines and use it with other tools. 

| Title                                | link to tutorial                                                         |
| ------------------------------------ | ------------------------------------------------------------------------ |
| Real-time ML monitoring with Grafana | [Evidently + Grafana](examples/integrations/grafana_monitoring_service/) |
| Batch ML monitoring with Airflow     | [Evidently + Airflow](examples/integrations/airflow_drift_detection/)    |
| Log Evidently metrics in MLflow UI   | [Evidently + MLflow](examples/integrations/mlflow_logging/)              |

# :phone: Community Call 

We host monthly community call for users and contributors. [Sign up](https://evidentlyai.com/community-call-sign-up) to join the next one. 

# :white_check_mark: Stay updated
- If you want to receive updates, sign up for our [newsletter](https://evidentlyai.com/sign-up). 
- You can also find more tutorials and explanations in our [Blog](https://evidentlyai.com/blog). 
- If you want to chat and connect, join our [Discord community](https://discord.gg/xZjKRaNp8b)!
