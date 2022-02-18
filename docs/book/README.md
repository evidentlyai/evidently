Evidently is an open-source Python library for data scientists and ML engineers. It helps evaluate, test and monitor the performance of ML models from validation to production.

You can think of it as an evaluation layer that fits into the existing ML stack.

## Quick Start 

Walk through a basic implementation to understand key Evidently features in under 10 minutes:
{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/tutorial.md). 
{% endcontent-ref %}

Explore the examples of the Evidently reports on different datasets and code tutorials:
{% content-ref url="get-started/examples.md" %}
[Example](get-started/examples.md). 
{% endcontent-ref %}

# How it works 

Evidently has a modular approach with 3 interfaces on top of the shared `Analyzer` functionality. 
1. Interactive visual reports
2. Data and model profiling
3. Real-time ML monitoring 

# [1. Interactive visual reports](dashboards/README.md)

Evidently generates interactive HTML reports from `pandas.DataFrame` or `csv` files. You can use them for visual model evaluation, debugging and documentation. 

Each report covers a certain aspect of the model performance. You can display reports as `Dashboard` objects in Jupyter notebook or Colab or export as an HTML file.

Evidently currently works with **tabular data**. 6 reports are available. You can combine, customize the reports or contribute your own report. 

## Data Drift and Quality

[Data Drift](reports/data-drift.md): detects changes in feature distribution. Data quality: provides the feature overview.

![Data Drift](../images/01\_data\_drift.png) ![Data Quality](../images/07\_data\_quality.png)

## Categorical and Numerical Target Drift

Detect changes in [Numerical](reports/num-target-drift.md) or [Categorical](reports/categorical-target-drift.md) target and feature behavior.

![Categorical target drift](../images/02\_cat\_target\_drift.png) ![Numerical target drift](../images/03\_num\_target\_drift.png)

## Classification Performance

Analyzes the performance and errors of a [Classification](reports/classification-performance.md) or [Probabilistic Classification](reports/probabilistic-classification-performance.md) model. Works both for binary and multi-class.

![Classification Performance](../images/05\_class\_performance.png) ![Probabilistic Classification Performance](../images/06\_prob\_class\_performance.png)

## Regression Performance

Analyzes the performance and errors of a [Regression](reports/reg-performance.md) model. Time series version coming soon.

![Regression Performance](../images/04\_reg\_performance.png) ![Time Series](../images/08\_time\_series.png)

# [2. Data and ML model profiling](profiling/README.md)

Evidently also generates JSON `Profiles`. You can use them to integrate the data or model evaluation step into the ML pipeline. 

For example, you can use it to perform scheduled batch checks of model health or log JSON profiles for further analysis. You can also build a conditional workflow based on the result of the check, e.g. to trigger alert, retraining, or generate a visual report. 

Each Evidently dashboard has a corresponding JSON profile that returns the summary of metrics and statistical test results. 

You can explore integrations with other tools: 

{% content-ref url="integrations/evidently-and-mlflow.md" %}
[Evidently and MLflow](evidently-and-mflow.md)
{% endcontent-ref %}

{% content-ref url="integrations/evidently-and-airflow.md" %}
[Evidently and Airflow](evidently-and-airflow.md)
{% endcontent-ref %}

# [3. Real-time ML monitoring](integrations/evidently-and-grafana.md)

Evidently also has `Monitors` that collect data and model metrics from a deployed ML service. You can use them to build live monitoring dashboards. 
Evidently helps configure the monitoring on top of the streaming data and emits the metrics. You can log and use the metrics elsewhere. 

There is a lightweight [integration with Prometheus and Grafana](integrations/evidently-and-grafana.md) that comes with pre-built dashboards.

![](../images/evidently\_data\_drift\_grafana\_dashboard\_top.png)

# Overview

Here is a quick visual summary on how Evidently works. You can track and explore different facets of the ML model quality via reports, profiles or monitoring interface and flexibly fit it into your existing stack. 

![](../images/evidently\_overview.png)

# Community and support 

Evidently is in active development, and we are happy to receive and incorporate feedback. If you have any questions, ideas or want to hang out and chat about doing ML in production, [join our Discord community](https://discord.com/invite/xZjKRaNp8b)!

