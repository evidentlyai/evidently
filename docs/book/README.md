Evidently is an open-source Python library for data scientists and ML engineers. 

It helps evaluate, test, and monitor the performance of ML models from validation to production. It works with tabular, text data and embeddings.

# Quick Start

Quickly check it out (1 min):
{% content-ref url="get-started/hello-world.md" %}
["Hello world" example](get-started/hello-world.md). 
{% endcontent-ref %}

Get Started with Reports and Test Suites (15 minutes). Learn how to run ad hoc checks and test your pipelines:
{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/tutorial.md). 
{% endcontent-ref %}

More [examples](examples/examples.md) 

Get Started with ML Monitoring (15 minutes). Learn how to self-host a dashboard to track metrics over time:
{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/tutorial-monitoring.md). 
{% endcontent-ref %}

# How it works 

Evidently helps evaluate and test data and ML model quality throughout the model lifecycle.

Evidently has a modular approach with 3 components: **Reports**, **Test Suites**, and **Monitoring Dashboard**. These interfaces cover alternative usage scenarios: from  visual analysis to automated pipeline testing and real-time monitoring.

Evidently has a simple, declarative API and a library of metrics, tests, and visualizations to choose from.

# 1. Tests suites: batch model checks 

Tests perform structured data and ML model quality checks. You typically compare two datasets: **reference** and **current**. You can set test parameters manually or let Evidently learn the expectations from the reference. Tests verify a condition and return an explicit **pass** or **fail** result. 
 
You can create a **Test Suite** from 50+ tests or run one of the **Presets**: for example, to test Data Stability or Regression Performance.

Tests are best for automated batch checks.
 
![Example of an Evidently test](.gitbook/assets/main/evidently_tests_main-min.png)

**Input**: one or two datasets as pandas.DataFrames or csv.
 
**How you get the output**: inside Jupyter notebook or Colab, as an exportable HTML, JSON, or Python dictionary.
 
**Primary use case: test-based ML monitoring**. You can run tests as a step in the ML pipeline. For example, when you receive a new batch of data, new labels, or generate predictions. You can build a conditional workflow based on the test results, e.g., to trigger an alert, retrain, or get a visual report to debug.  

**Read more**:
* [Overview: what is a test and a test suite](introduction/core-concepts.md) 
* [User guide: how to generate tests](tests-and-reports/run-tests.md) 
* [Reference: available tests and presets](reference/all-tests.md) 

# 2. Reports: interactive visualizations

Reports calculate various metrics and provide rich interactive visualizations. 
 
You can create a custom **Report** from individual metrics or run one of the **Presets** that cover a specific aspect of the model or data performance. For example, Data Quality or Classification Performance.
 
Reports are best for exploratory analysis, debugging, and documentation.

![Evidently reports](.gitbook/assets/main/evidently_reports_main-min.png)

**Input**: one or two datasets as pandas.DataFrames or csv. 
 
**How you get the output**: inside Jupyter notebook or Colab, as an exportable HTML file, JSON, or Python dictionary.
 
**Primary use case**: debugging and exploration. Reports help visually evaluate the data or model performance. For example, during exploratory data analysis, model evaluation on the training set, when debugging the model quality decay, or comparing several models.  
 
**Secondary use cases**: 
* **Performance logging**. You can integrate a model/data evaluation step in the ML pipeline, get outputs as JSON, and log it for further analysis. For example, you can later visualize it using other BI tools.
* **Reporting and documentation**. You can generate visual HTML reports to document your model performance.   

**Read more**:
* [Overview: what is a report and a metric](introduction/core-concepts.md) 
* [User guide: how to run reports](tests-and-reports/get-reports.md) 
* [Reference: available metrics and metric presets](reference/all-metrics.md) 

# 3. ML monitoring dashboard

*Available starting from v0.4.0*. 

You can self-host an ML monitoring dashboard to visualize metrics and test results over time. This functionality sits on top of Reports and Test Suites. You must store their outputs as Evidently JSON `snapshots` that serve as a data source for the Evidently Monitoring UI.

You can visualize any and track 100+ metrics available in Evidently, from number nulls in data to text sentiment and embbedding drift.

![ML monitoring](.gitbook/assets/main/evidently_ml_monitoring_main-min.png)

**Input**: Evidently `snapshots`, logged to an object storage. 

**Output**: a self-hostable dashboard available as a web app.
  
**Primary use case: continious monitoring**. When you need a live dashboard to see all your models and metrics over time. 
 
**Read more**:
* [Get Started](get-started/tutorial-monitoring.md)

# Community and support 

Evidently is in active development, and we are happy to receive and incorporate feedback. If you have any questions, ideas or want to hang out and chat about doing ML in production, [join our Discord community](https://discord.com/invite/xZjKRaNp8b)!

# User newsletter

To get updates on new features, integrations and code tutorials, sign up for the [Evidently User Newsletter](https://www.evidentlyai.com/user-newsletter). 
