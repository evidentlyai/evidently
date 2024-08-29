---
description: Introduction to Dashboards.
---   

# What is a Dashboard?

Each Project has its Dashboard. A Dashboard lets you evaluation results over time, providing a clear view of the quality of your AI application and data.

When you create a new Project, the Dashboard starts empty. To populate it, run evaluations (using either code or no-code methods) and add Reports or Test Suites to the Project. Once you have data, you can configure the Dashboard to display the values that matter to you.

You can use the Dashboard to monitor live data in production or to keep track of results from batch experiments and tests. The "Show in order" toggle lets you switch between two views:
* **Time series**. Displays data with actual time intervals, ideal for live monitoring.
* **Sequential**. Shows results in order with equal spacing, perfect for experiments.

![](../.gitbook/assets/main/evidently_ml_monitoring_main.png)

All Panels within the same view reflect the date range set by the time range filter. You can also zoom in on any time series visualizations for deeper analysis.

# What is a Panel?

A Dashboard consists of Panels, each visualizing specific values or test results. Panels can be counters, line or bar plots, and more.

{% content-ref url="design_dashboard.md" %}
[Panel types](design_dashboard.md)
{% endcontent-ref %}

You can customize your Dashboard by adding specific Panels through the Python API using dashboard-as-code. 

In Evidently Cloud and Enterprise, you have additional options: 
* Add Panels directly from the UI
* Use multiple Tabs within the same Dashboard
* Start with pre-built Tabs as templates

{% content-ref url="add_dashboard_tabs.md" %}
[Panel types](add_dashboard_tabs.md)
{% endcontent-ref %}

# What is the data source?

Panels pull data from Evidently `snapshots`, which are Reports or Test Suites you've generated and saved to a Project.

Each Test Suite and Report contains a wealth of information and visuals. To add a Panel to the Dashboard, you must choose a specific **value** from the snapshot you'd like to plot and select other parameters, such as the Panel type and title.

{% content-ref url="add_dashboard_tabs.md" %}
[Panel types](design_dashboard_api.md)
{% endcontent-ref %}

For example, if your Reports include the `ColumnSummaryMetric` (the default for any text descriptor), you can visualize values like mean, max, min, etc. within your Panels. This method works for all other Metrics. If you're using a related Test, say `TestColumnValueMin`, you can display either the descriptive values, or the Test result (pass or fail).

You can also use Tags, which you should add to Reports or Test Suites during generation. Tags allow you to filter and visualize data from specific subsets of snapshots when creating a Panel.
