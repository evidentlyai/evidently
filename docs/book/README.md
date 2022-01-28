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

## [1. Interactive visual reports](dashboards/README.md)

Evidently generates interactive HTML reports from `pandas.DataFrame` or `csv` files. You can use them for visual model evaluation, debugging and documentation. 

Each report covers a certain aspect of the model performance. You can display reports as `Dashboard` objects in Jupyter notebook or Colab or export as an HTML file.

Evidently currently works with **tabular data**. 6 reports are available.

|   |   |
| :----: | :----: |
| [Data Drift](get-started/reports/data-drift.md)| [Categorical Target Drift](get-started/reports/categorical-target-drift.md)|
| Detects changes in feature distribution. | Detects changes in categorical target and feature behavior. |
| ![](../images/01\_data\_drift.png)| ![](../images/02\_cat\_target\_drift.png)|
| [Numerical Target Drift](get-started/reports/num-target-drift.md)| [Regression Performance](get-started/reports/reg-performance.md)|
| Detects changes in numerical target and feature behavior.| Analyzes the performance and errors of a regression model.|
| ![](../images/03\_num\_target\_drift.png)| ![](../images/04\_reg\_performance.png)|
| [Classification Performance](get-started/reports/classification-performance.md)| [Probabilistic Classification Performance](get-started/reports/probabilistic-classification-performance.md)|
| Analyzes the performance and errors of a classification model.| Analyzes the performance and errors of a probabilistic classification model. |
| [![Classification Performance](../images/05\_class\_performance.png)](get-started/reports/classification-performance.md) | [![Probabilistic Classification Performance](../images/06\_prob\_class\_performance.png)](get-started/reports/probabilistic-classification-performance.md) |

You can combine, customize the reports or contribute your own report. 

## [2. Data and ML model profiling](profiling/README.md)

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

## [3. Real-time ML monitoring](integrations/evidently-and-grafana.md)

Evidently also has `Monitors` that collect data and model metrics from a deployed ML service. You can use them to build live monitoring dashboards. 
Evidently helps configure the monitoring on top of the streaming data and emits the metrics. You can log and use the metrics elsewhere. 

There is a lightweight [integration with Prometheus and Grafana](integrations/evidently-and-grafana.md) that comes with pre-built dashboards.

![](.gitbook/assets/grafana\_dashboard.jpg)

## Community and support 

Evidently is in active development, and we are happy to receive and incorporate feedback. If you have any questions, ideas or want to hang out and chat about doing ML in prodiction, [join our Discord community](https://discord.com/invite/xZjKRaNp8b)!

