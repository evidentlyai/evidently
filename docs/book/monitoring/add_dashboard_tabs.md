---
description: How to visualize data and model quality in the Monitoring UI.
---   

# What is a dashboard? 

Each Project has a monitoring dashboard to visualize metrics and test results over time. A dashboard can have multiple monitoring panels, such as counters, line or bar plots, etc.

![](../.gitbook/assets/main/evidently_ml_monitoring_main.png)


{% hint style="info" %}
**Data source**. To populate the dashboards, you must send the relevant data inside the snapshots. The panels will be empty otherwise. Read more about [sending snapshots](snapshots.md).  
{% endhint %}

You can choose how exactly to organize your dashboard and which values to plot. By default, the dashboard for a new Project is empty. 

For both Evidently Cloud and self-hosted, you can design the monitoring panels via API. This is also great for version control.

In Evidently Cloud, you can also:
* Add and modify Panels directly in the user interface.
* Add multiple Tabs on the Dashboard to logically group the Panels.
* Use pre-built Dashboards for Data Quality, Data Drift, etc.

# Pre-built dashboards
{% hint style="success" %}
Dashboard templates is a Pro feature available in the Evidently Cloud. 
{% endhint %}

It is convenient to start with template Dashboard Tabs: you will get monitoring panels out-of-the-box.

To use a template:
* Enter the “Edit” mode clicking on the top right corner of the dashboard. 
* Click on the “Add tab” button.
* Choose a template Tab in the dropdown.

Optionally, give a custom name to the Tab.

You can choose between the following options:

| Tab Template | Description | How to Populate |
|---|---|---|
| Columns | Shows column values (e.g., mean, quantiles) over time for categorical and numerical columns. | Capture the `DataQualityPreset()` inside snapshots or log `ColumnSummaryMetric` for individual columns. |
| Data Quality | Shows data quality metrics (e.g., missing values, duplicates) over time for the complete dataset and results of Data Quality tests. | Capture the `DataQualityPreset()` inside snapshots or log the `DatasetSummaryMetric()`. For the Test panel, include any individual Tests from Data Quality or Data Integrity groups.|
| Data Drift | Shows the share of drifting features over time. | Capture `DataDriftPreset()` or `DataDriftTestPreset()` inside snapshots. For the Test panel, capture individual `TestColumnDrift()` results per column. |

# What’s next?

* How to create [custom monitoring panels and Tabs](design_dashboard.md)
* How to configure dashboard via Python API
