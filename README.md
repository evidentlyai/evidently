<h1 align="center">Evidently</h1>

<p align="center">
<a href="https://pepy.tech/project/evidently" target="_blank"><img src="https://pepy.tech/badge/evidently" alt="PyPi Downloads"></a>
<a href="https://github.com/evidentlyai/evidently/blob/main/LICENSE" target="_blank"><img src="https://img.shields.io/github/license/evidentlyai/evidently" alt="License"></a>
<a href="https://pypi.org/project/evidently/" target="_blank"><img src="https://img.shields.io/pypi/v/evidently" alt="PyPi"></a>

</p>

<p align="center"><b>An open-source framework to evaluate, test and monitor ML and LLM-powered systems.</b></p>

<p align="center">
  <a href="https://docs.evidentlyai.com">Documentation</a>
  |
  <a href="https://discord.gg/xZjKRaNp8b">Discord Community</a>
  |
  <a href="https://evidentlyai.com/blog">Blog</a>
  |
  <a href="https://twitter.com/EvidentlyAI">Twitter</a>
  |
  <a href="https://www.evidentlyai.com/register">Evidently Cloud</a>
</p>

# :new: New release

**Evidently 0.4.25**. LLM evaluation -> [Tutorial](https://docs.evidentlyai.com/get-started/tutorial-llm)

# :bar_chart: What is Evidently?

Evidently is an open-source Python library for ML and LLM evaluation and observability. It helps evaluate, test, and monitor AI-powered systems and data pipelines from experimentation to production. 

* 🔡 Works with tabular, text data, and embeddings.
* 📚 100+ built-in metrics from data drift detection to LLM judges.
* 🛠️ Python interface for custom metrics and tests. 
* 🚦 Both offline evals and live monitoring.
* 💻 Open architecture: easily export data and integrate with existing tools. 

Evidently is very modular: you can start with one-off evaluations in Python without complex installs or set it up as a service to get a real-time monitoring dashboard.

|  |  |
| -- | -- |
| **Reports** <br> Compute various data, ML and LLM quality metrics. <ul><li> Out-of-the-box interactive visuals. </li><li> Best for exploratory analysis and debugging.  </li><li> Start with Preset evaluations or customize. </li><li> View results in Python, export as JSON, Python dictionary, HTML, DataFrame, or view in monitoring UI. </li></ul>| ![Report example](docs/book/.gitbook/assets/main/reports-min.png)|
| **Test Suites** <br>Verify set conditions on metric values and return a pass or fail result. <ul><li> Best for regression testing, CI/CD checks, or data validation pipelines.  </li><li> Zero setup option: auto-generate test conditions from the reference dataset.  </li><li> Simple syntax to set custom test conditions as `gt` (greater than), `lt` (less than), etc.  </li><li> View results in Python, export as JSON, Python dictionary, HTML, data frame, or view in monitoring UI. </li></ul> | ![Test example](docs/book/.gitbook/assets/main/tests.gif)|
| **Monitoring Dashboard** <br> User interface to visualize metrics and test results over time. <br><br> You can self-host the open-source dashboard or use [Evidently Cloud](https://www.evidentlyai.com/register). It starts with a generous free tier and offers extra features like user management, built-in alerting, and a no-code interface. | ![Dashboard example](docs/book/.gitbook/assets/main/dashboard.gif)|

# :woman_technologist: Install Evidently

Evidently is available as a PyPI package. To install it using pip package manager, run:

```sh
pip install evidently
```
To install Evidently using conda installer, run:

```sh
conda install -c conda-forge evidently
```

# :arrow_forward: Getting started

### Option 1: Test Suites
> This is a simple Hello World example. Head to docs for a complete [Reports and Test Suite Tutorial](https://docs.evidentlyai.com/get-started/tutorial). For LLMs, check [LLM evaluation Tutorial](https://docs.evidentlyai.com/get-started/tutorial-llm).

Import the **Test Suite**, evaluation Preset and toy tabular dataset. 

```python
import pandas as pd

from sklearn import datasets

from evidently.test_suite import TestSuite
from evidently.test_preset import DataStabilityTestPreset

iris_data = datasets.load_iris(as_frame='auto')
iris_frame = iris_data.frame
```

Split the `DataFrame` into reference and current data. Run the **Data Stability** Test Suite that will automatically generate conditions on column value ranges, share of missing values, etc. from the reference. Display the output in Jupyter notebook:

```python
data_stability= TestSuite(tests=[
    DataStabilityTestPreset(),
])
data_stability.run(current_data=iris_frame.iloc[:60], reference_data=iris_frame.iloc[60:], column_mapping=None)
data_stability
```

You can also save an HTML file. You'll need to open it from the destination folder.

```python
data_stability.save_html("file.html")
```

To get the output as JSON:
```python
data_stability.json()
```
You can choose other Presets, individual Tests and set conditions.
 
### Option 2: Reports

Import the **Report**, evaluation Preset and toy tabular dataset. 

```python
import pandas as pd

from sklearn import datasets

from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

iris_data = datasets.load_iris(as_frame='auto')
iris_frame = iris_data.frame
```

To generate the **Data Drift** Report that will compare the distribution of columns between `current` and `reference`, run:
```python
data_drift_report = Report(metrics=[
    DataDriftPreset(),
])

data_drift_report.run(current_data=iris_frame.iloc[:60], reference_data=iris_frame.iloc[60:], column_mapping=None)
data_drift_report

```
Save the report as HTML. You'll later need to open it from the destination folder.
```python
data_drift_report.save_html("file.html")
```

To get the output as JSON:
```python
data_drift_report.json()
```

You can choose other Presets, individual Metrics, including LLM evaluations, and set conditions.

### Option 3: ML monitoring dashboard
> This will launch a demo project in the Evidently UI. Head to docs for a complete [Self-hosting ML Monitoring Tutorial](https://docs.evidentlyai.com/get-started/tutorial-monitoring) or [Cloud ML Monitoring Tutorial](https://docs.evidentlyai.com/get-started/tutorial-cloud).

Recommended step: create a virtual environment and activate it.
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

After installing Evidently (`pip install evidently`), run the Evidently UI with the demo projects:
```
evidently ui --demo-projects all
```

Access Evidently UI service in your browser. Go to the **localhost:8000**.

# :computer: Contributions
We welcome contributions! Read the [Guide](CONTRIBUTING.md) to learn more.

# :books: Documentation
For more information, refer to a complete <a href="https://docs.evidentlyai.com">Documentation</a>. You can start with the tutorials:
* [Get Started with Tabular and ML Evaluation](https://docs.evidentlyai.com/get-started/tutorial)
* [Get Started with LLM Evaluation](https://docs.evidentlyai.com/get-started/tutorial-llm)
* [Self-hosting ML monitoring Dashboard](https://docs.evidentlyai.com/get-started/tutorial-monitoring)
* [Cloud ML monitoring Dashboard](https://docs.evidentlyai.com/get-started/tutorial-cloud)

See more examples in the [Docs](https://docs.evidentlyai.com/examples).

## How-to guides
Explore the [How-to guides](https://github.com/evidentlyai/evidently/tree/main/examples/how_to_questions) to understand specific features in Evidently.

# :white_check_mark: Discord Community
If you want to chat and connect, join our [Discord community](https://discord.gg/xZjKRaNp8b)!
