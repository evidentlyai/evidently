---
description: How to visualize data and model quality in the Monitoring UI.
---   

# What is a Dashboard? 

Each Project has a monitoring Dashboard to visualize metrics and test results over time. A Dashboard can have multiple monitoring Panels, such as counters, line or bar plots, etc.

![](../.gitbook/assets/main/evidently_ml_monitoring_main.png)


{% hint style="info" %}
**Data source**. To populate the Dashboard, you must send the relevant data inside the snapshots. The Panels will be empty otherwise. Read more about [sending snapshots](snapshots.md).  
{% endhint %}

You can choose how exactly to organize your Dashboard and which values to plot. By default, the Dashboard for a new Project is empty. 

For both Evidently Cloud and self-hosted, you can design the monitoring Panels via API. This is great for version control.

In Evidently Cloud, you can also:
* Add and modify Panels directly in the user interface.
* Add multiple Tabs on the Dashboard to logically group the Panels.
* Use pre-built Dashboards for Data Quality, Data Drift, etc.

# Pre-built dashboards
{% hint style="success" %}
Dashboard templates is a Pro feature available in the Evidently Cloud. 
{% endhint %}

It is convenient to start with template Dashboard Tabs: you immediately get a set of useful monitoring Panels without manually adding them one by one.

To use a template:
* Enter the “Edit” mode clicking on the top right corner of the Dashboard. 
* Click on the “Add tab” button.
* Choose a template Tab in the dropdown.

Optionally, give a custom name to the Tab.

You can choose between the following options:

| Tab Template | Description | Data source |
|---|---|---|
| Columns | Shows column values (e.g., mean, quantiles) over time for categorical and numerical columns. | Capture the `DataQualityPreset()` or `ColumnSummaryMetric()` for individual columns. |
| Data Quality | Shows data quality metrics (e.g., missing values, duplicates) over time for the complete dataset and results of Data Quality Tests. | Capture the `DataQualityPreset()` or `DatasetSummaryMetric()`. For the Test panel, include any individual Tests from Data Quality or Data Integrity groups.|
| Data Drift | Shows the share of drifting features over time, and the results of Column Drift Tests. | Capture the `DataDriftPreset()` or `DataDriftTestPreset()`. For the Test panel, you must include individual `TestColumnDrift()` or `DataDriftTestPreset()`. |

# What’s next?

* How to create [custom monitoring Panels and Tabs](design_dashboard.md)
* How to configure Dashboard via Python API
