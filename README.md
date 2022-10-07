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
> **Note**
> This is a simple Hello World example. You can find a complete [Getting Started Tutorial](https://docs.evidentlyai.com/tutorial) in the docs.

## Jupyter Notebook
To start, prepare your data as two pandas `DataFrames`. The first should include your reference data, the second - current production data. The structure of both datasets should be identical. 

To run some of the evaluations (e.g. Data Drift), you need input features only. In other cases (e.g. Target Drift, Classification Performance), you need Target and/or Prediction. We'll use a simple toy dataset and s. 

### Option 1: Test Suites

After installing the tool, import Evidently **test suite** and required presets:

```python
import pandas as pd

from sklearn import datasets

from evidently.test_suite import TestSuite
from evidently.test_preset import DataStability, DataQuality

iris_data = datasets.load_iris(as_frame='auto')
iris = iris_data.frame
```

To run the **Data Stability** test suite and display the reports in the notebook:
```python
data_stability= TestSuite(tests=[
    DataStability(),
])
data_stability.run(current_data=iris_frame[:75], reference_data=iris_frame[75:], column_mapping=None)
data_stability 
```

To save the results as an HTML file:
```python
data_stability.save_html("file.html")
```

You'll need to open it from the destination folder.

To get the output as JSON:
```python
data_stability.json()
```

### Option 2: Reports

After installing the tool, import Evidently **report** and required presets:

```python
import pandas as pd

from sklearn import datasets

from evidently.report import Report
from evidently.metric_preset import DataDrift, CatTargetDrift

iris_data = datasets.load_iris(as_frame='auto')
iris = iris_data.frame
```

To generate the **Data Drift** report, run:
```python
data_drift_report = Report(metrics=[
    DataDrift(),
])

data_drift_report.run(current_data=iris_frame[:75], reference_data=iris_frame[75:], column_mapping=None)
data_drift_report

```
To save the report as HTML:
```python
data_drift_report.save_html("file.html")
```

You'll need to open it from the destination folder.

To get the output as JSON:
```python
data_drift_report.json()
```

# :computer: Contributions
We welcome contributions! Read the [Guide](CONTRIBUTING.md) to learn more. 

# :books: Documentation
For more information, refer to a complete <a href="https://docs.evidentlyai.com">Documentation</a>. You can start with this [Tutorial](https://docs.evidentlyai.com/tutorial) for a quick introduction.

# :card_index_dividers: Examples
Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box.

| Contents                                               | Jupyter notebook                                                                                 | Colab notebook                                                                    | Data source                                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Evidently Tests| [link](sample_notebooks/evidently_tests.ipynb) | [link](https://colab.research.google.com/drive/1nQhfXft4VZ3G7agvXgH_LqVHdCh-WaMl) | Adult data set openml, California housing sklearn.datasets, Breast cancer sklearn.datasets, Iris plants sklearn.datasets |
| Evidently Test Presets| [link](sample_notebooks/evidently_test_presets.ipynb) | [link](https://colab.research.google.com/drive/1CBAFY1qmHHV_72SC7YBeaD4c6LLpPQan) | Adult data set openml, California housing sklearn.datasets, Breast cancer sklearn.datasets, Iris plants sklearn.datasets |
| Evidently Metrics| [link](sample_notebooks/evidently_metrics.ipynb) | [link](https://colab.research.google.com/drive/1IpfQsq5dmjuG_Qbn6BNtghq6aubZBP5A) | Adult data set openml |
| Evidently Metric Presets| [link](sample_notebooks/evidently_metric_presets.ipynb) | [link](https://colab.research.google.com/drive/1wmHWipPd6iEy9Ce8NWBcxs_BSa9hgKgk) | Adult data set openml, California housing sklearn.datasets, Breast cancer sklearn.datasets, Iris plants sklearn.datasets |

You can see examples from old Dashboard API [here](https://github.com/evidentlyai/evidently/tree/main/examples/sample_notebooks). 

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
