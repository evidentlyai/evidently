Evidently is an open-source Python library for data scientists and ML engineers. 

It helps evaluate, test, and monitor the performance of ML models from validation to production.

# Quick Start 

Understand the basic functionality in 15 minutes:
{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/tutorial.md). 
{% endcontent-ref %}

Code examples:
{% content-ref url="examples/examples.md" %}
[Example](examples/examples.md). 
{% endcontent-ref %}

"Hello world" (1 min):
{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/hello-world.md). 
{% endcontent-ref %}

# How it works 

Evidently helps evaluate and test data and ML model quality throughout the model lifecycle.

Evidently has three components: **Reports**, **Tests**, and **Monitors** (in development). These interfaces cover alternative usage scenarios: from  visual analysis to automated pipeline testing and real-time monitoring.

You need to provide the data, choose what to evaluate, and the output format. Evidently has a simple, declarative API and a library of metrics, tests, and visualizations to choose from.

You can integrate Evidently into various ML stacks as a monitoring or evaluation component.

Evidently currently works with tabular data. 

# 1. [Tests](tests/README.md): batch model checks 

Tests perform structured data and ML model quality checks. You typically compare two datasets: **reference** and **current**. You can set test parameters manually or let Evidently learn the expectations from the reference. Tests verify a condition and return an explicit **pass** or **fail** result. 
 
You can create a **Test Suite** from 50+ individual tests or run one of the **Presets** that combine relevant tests. For example, to test Data Stability or Regression Performance.

Tests are best for automated batch checks.
 
![Example of an Evidently test](.gitbook/assets/main/evidently_tests_main-min.png)

**Required input**: one or two datasets as pandas.DataFrames or csv.
 
**How you get the output**: as an HTML inside Jupyter notebook or Colab, as an exportable HTML file, as a JSON, or as a Python dictionary.
 
**Primary use case: test-based ML monitoring**. You can run tests as a step in the ML pipeline. For example, when you receive a new batch of data, new labels, or generate predictions. You can build a conditional workflow based on the test results, e.g., to trigger an alert, retrain, or get a visual report to debug.  

**Read more**:
* [Overview: what is a test and a test suite](introduction/core-concepts.md) 
* [User guide: how to generate tests](tests-and-reports/run-tests.md) 
* [Reference: available tests and presets](reference/all-tests.md) 

# 2. [Reports](reports/README.md): interactive dashboards

{% hint style="info" %}
We added a new Report object starting from **v0.1.57.dev0**. Reports unite the functionality of Dashboards and JSON profiles with a new, cleaner API. 
{% endhint %}

Reports calculate various metrics and provide rich interactive visualizations. 
 
You can create a custom **Report** from individual metrics or run one of the **Presets** that cover a specific aspect of the model or data performance. For example, Data Quality or Classification Performance.
 
Reports are best for exploratory analysis, debugging, and documentation.

![Evidently reports](.gitbook/assets/main/evidently_reports_main-min.png)

**Required input**: one or two datasets as pandas.DataFrames or csv. Due to rich embedded visualizations, it is recommended to take a smaller sample. 
 
**How you get the output**: as an HTML inside Jupyter notebook or Colab, as an exportable HTML file, as JSON, or as a Python dictionary.
 
**Primary use case**: debugging and exploration. Reports help visually evaluate the data or model performance. For example, during exploratory data analysis, model evaluation on the training set, when debugging the model quality decay, or comparing several models.  
 
**Secondary use cases**: 
* **Performance logging**. You can integrate a model/data evaluation step in the ML pipeline, get outputs as JSON, and log it for further analysis. For example, you can later visualize it using other BI tools.
* **Reporting and documentation**. You can generate visual HTML reports to document your model performance.   

**Read more**:
* [Overview: what is a report and a metric](introduction/core-concepts.md) 
* [User guide: how to run reports](tests-and-reports/get-reports.md) 
* [Reference: available metrics and metric presets](reference/all-metrics.md) 

# 3. [Real-time ML monitoring](integrations/evidently-and-grafana.md)

*Note: this functionality is in early development and subject to an API change*. 

Evidently also has `Monitors` that collect data and model metrics from a deployed ML service. 

In this scenario, Evidently is deployed as a monitoring service. You can use configuration to define the monitoring logic. Evidently calculates the metrics over the streaming data and emits them in Prometheus format. There are pre-built Grafana dashboards to visualize them.

![Evidently and Grafana](.gitbook/assets/main/evidently_monitoring_main.png)

**Required input**: POST live data from the ML service. 

**How you get the output**: data and quality metrics in the Prometheus format.
 
**Primary use case: online monitoring**. When you need a live dashboard that is updated close to real-time. 
 
**Read more**:
* [Example integration with Prometheus and Grafana](integrations/evidently-and-grafana.md)

# Community and support 

Evidently is in active development, and we are happy to receive and incorporate feedback. If you have any questions, ideas or want to hang out and chat about doing ML in production, [join our Discord community](https://discord.com/invite/xZjKRaNp8b)!

# User newsletter

To get updates on new features, integrations and code tutorials, sign up for the [Evidently User Newsletter](https://www.evidentlyai.com/user-newsletter). 
