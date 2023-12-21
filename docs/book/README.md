Evidently is an open-source Python library for data scientists and ML engineers. 

It helps evaluate, test, and monitor data and ML models from validation to production. It works with tabular, text data and embeddings.

# Quick Start

Have only 1 minute? Check out this example:
{% content-ref url="get-started/hello-world.md" %}
["Hello world" example](get-started/hello-world.md). 
{% endcontent-ref %}

New to Evidently? This tutorial shows how to run ad hoc data and model checks. (15 min).
{% content-ref url="get-started/tutorial.md" %}
[Get started tutorial](get-started/tutorial.md). 
{% endcontent-ref %}

Want an ML monitoring dashboard to track metrics over time? 

Self-host an ML monitoring dashboard: 
{% content-ref url="get-started/tutorial-monitoring.md" %}
[Get started tutorial](get-started/tutorial-cloud.md). 
{% endcontent-ref %}

Get started with Evidently Cloud: 
{% content-ref url="get-started/tutorial-monitoring.md" %}
[Get started tutorial](get-started/tutorial-monitoring.md). 
{% endcontent-ref %}

You can explore more code [examples](examples/examples.md). 

Don't want to self-host? Sign up for the [Evidently Cloud]([https://www.evidentlyai.com/product/cloud](https://www.evidentlyai.com/cloud-signup)!

# How it works 

Evidently helps evaluate and test data and ML model quality throughout the model lifecycle.

Evidently has a modular approach with 3 components: **Reports**, **Test Suites**, and a **Monitoring Dashboard**. They cover different usage scenarios: from ad hoc analysis to automated pipeline testing and continuous monitoring.

Evidently has a simple, declarative API and a library of in-built metrics, tests, and visualizations.

# 1. Tests suites: batch model checks 

Tests perform structured data and ML model quality checks. You can set the conditions manually or let Evidently generate them based on the reference dataset. Tests will return an explicit **pass** or **fail** result. 
 
You can create a **Test Suite** from 50+ tests or run one of the **Presets**. For example, to test Data Stability or Regression Performance.

Tests are best for automated batch checks.
 
![](.gitbook/assets/main/evidently_tests_main-min.png)

**Input**: one or two datasets as pandas.DataFrames or csv.
 
**How you get the output**: inside Jupyter notebook or Colab, as an exportable HTML, JSON, or Python dictionary.
 
**Primary use case: test-based ML monitoring**. You can run tests as a step in the ML pipeline. For example, when you receive a new batch of data, labels, or generate predictions. You can build a conditional workflow based on the results, e.g., to trigger an alert, retrain, or get a report.  

**Read more**:
* [Overview: what is a test and a test suite](introduction/core-concepts.md) 
* [User guide: how to generate tests](tests-and-reports/run-tests.md) 
* [Reference: available tests and presets](reference/all-tests.md) 

# 2. Reports: interactive visualizations

Reports calculate various metrics and provide rich interactive visualizations. 
 
You can create a custom **Report** from individual metrics or run one of the **Presets** that cover a specific aspect of the model or data performance. For example, Data Quality or Classification Performance.
 
Reports are best for exploratory analysis, debugging, and documentation.

![](.gitbook/assets/main/evidently_reports_main-min.png)

**Input**: one or two datasets as pandas.DataFrames or csv. 
 
**How you get the output**: inside Jupyter notebook or Colab, as an exportable HTML file, JSON, or Python dictionary.
 
**Primary use case**: analysis and exploration. Reports help visually evaluate the data or model performance. For example, during exploratory data analysis, model evaluation on the training set, when debugging the model quality decay, or comparing several models.  
 
**Secondary use cases**:
* **Reporting and documentation**. You can generate visual HTML reports and ML model cards.
* **Performance logging**. You can integrate an evaluation step in the data/ML pipeline, get outputs as JSON, and log it for further analysis or to visualize using BI tools.

**Read more**:
* [Overview: what is a report and a metric](introduction/core-concepts.md) 
* [User guide: how to run reports](tests-and-reports/get-reports.md) 
* [Reference: available metrics and metric presets](reference/all-metrics.md) 

# 3. ML monitoring dashboard

*Available starting from v0.4.0*. 

You can self-host an ML monitoring dashboard to visualize metrics and test results over time. This functionality sits on top of Reports and Test Suites. You must store their outputs as Evidently JSON `snapshots` that serve as a data source for the Evidently Monitoring UI.

You can visualize any and track 100+ metrics available in Evidently, from number nulls in data to text sentiment and embedding drift.

![](.gitbook/assets/main/evidently_ml_monitoring_main.png)

**Input**: Evidently `snapshots`, logged to an object storage. 

**Output**: a self-hostable dashboard available as a web app.
  
**Primary use case: continuous monitoring**. When you need a live dashboard to see all your models and metrics over time. 
 
**Read more**:
* [Get Started](get-started/tutorial-monitoring.md)

# Community and support 

Evidently is in active development, and we are happy to receive and incorporate feedback. If you have any questions, ideas or want to hang out and chat about doing ML in production, [join our Discord community](https://discord.com/invite/xZjKRaNp8b)!

# User newsletter

To get updates on new features, integrations and code tutorials, sign up for the [Evidently User Newsletter](https://www.evidentlyai.com/user-newsletter). 
