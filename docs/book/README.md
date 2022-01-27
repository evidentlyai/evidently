# What is Evidently?

Evidently is an open-source Python library for data scientists and ML engineers. It helps evaluate, test and monitor the performance ML models from validation to production.

You can think of it as an evaluation layer that fits into the existing ML stack.

## Quick Start 

{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/tutorial.md). Walk through a basic implementation to understand key Evidently features in under 10 minutes.
{% endcontent-ref %}

{% content-ref url="get-started/examples" %}
[Example](get-started/examples). Explore the examples of the Evidently reports on different datasets and code tutorials.
{% endcontent-ref %}

Evidently has a modular approach with 3 interfaces on top of the shared analyzer functionality. 

## [Interactive visual reports](dashboards/)

Evidently generates interactive HTML reports from `pandas.DataFrame` or `csv` files. You can use them for visual model evaluation, debugging and documentation. 

Each report covers a certain aspect of the model performance. You can display reports as Dashboard objects in Jupyter notebook or Colab or export as an HTML file.

Evidently currently works with **tabular data**. 6 reports are available.

### [1. Data Drift](get-started/reports/data-drift.md)

Detects changes in feature distribution.

![Part of the Data Drift Report.](.gitbook/assets/evidently\_github.png)

### [2. Numerical Target Drift](get-started/reports/num-target-drift.md)

Detects changes in numerical target and feature behavior.

![Part of the Target Drift Report.](.gitbook/assets/evidently\_num\_target\_drift\_github.png)

### [3. Categorical Target Drift](get-started/reports/categorical-target-drift.md)

Detects changes in categorical target and feature behavior.

![Part of the Categorical Target Drift Report.](.gitbook/assets/evidently\_cat\_target\_drift\_github.png)

### [4. Regression Model Performance](get-started/reports/reg-performance.md)

Analyzes the performance of a regression model and model errors.

![Part of the Regression Model Performance Report.](.gitbook/assets/evidently\_regression\_performance\_report\_github.png)

### [5. Classification Model Performance](get-started/reports/classification-performance.md)

Analyzes the performance and errors of a classification model. Works both for binary and multi-class models.

![Part of the Classification Model Performance Report.](.gitbook/assets/evidently\_classification\_performance\_report\_github.png)

### [6. Probabilistic Classification Model Performance](get-started/reports/probabilistic-classification-performance.md)

Analyzes the performance of a probabilistic classification model, quality of the model calibration, and model errors. Works both for binary and multi-class models.

![Part of the Probabilstic Classification Model Performance Report.](.gitbook/assets/evidently\_prob\_classification\_performance\_report\_github.png)

You can combine, customize the reports or contribute your own report. 

## [2. Data and ML model profiling](profiling/)

Evidently also generates JSON profiles. You can use them to integrate the data or model evaluation step into the ML pipeline. 

For example, you use it to perform scheduled batch checks of model health or log JSON profiles for further analysis. You can also build a conditional workflow based on the result of the check, e.g. to trigger alert, retraining, or generate a visual report. 

Each Evidently dashboard has a corresponding JSON profile that returns the summary of metrics and statistical test results. 

You can explore integrations with other tools: 

{% content-ref url="integrations/evidently-and-mlflow.md" %}
[evidently-and-mlflow.md](evidently-and-mflow.md)
{% endcontent-ref %}

{% content-ref url="integrations/evidently-and-airflow.md" %}
[evidently-and-airflow.md](evidently-and-airflow.md)
{% endcontent-ref %}

## [3. Real-time ML monitoring](integrations/evidently-and-grafana.md)

Evidently has a monitoring_service component that collects data and model metrics from a deployed ML service. You can use it to build live monitoring dashboards. 
Evidently configures the monitoring on top of the streaming data and emits the metrics. You can log and use the metrics elsewhere. 

There is a lightweight [integration with Prometheus and Grafana](integrations/evidently-and-grafana.md) that comes with pre-built dashboards.

![](.gitbook/assets/grafana\_dashboard.jpg)

## Community and support 

Evidently is in active development, and we are happy to take feedback. If you have any questions, ideas or want to hang out and chat about doing ML in prodiction, [join our Discord community](https://discord.com/invite/xZjKRaNp8b)!

