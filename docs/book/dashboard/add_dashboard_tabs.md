---
description: Get a pre-built monitoring Dashboard using templates.
---   

# Pre-built Tabs
{% hint style="success" %}
Dashboard templates is a Pro feature available in the Evidently Cloud and Enterprise. 
{% endhint %}

Template Tabs include a preset combination of monitoring Panels, so you don't have to add them one by one.

To use a template:
* Enter the "Edit" mode by clicking on the top right corner of the Dashboard. 
* Click on the "Add tab" button.
* Choose a template Tab in the dropdown.

![](../.gitbook/assets/cloud/qs_add_data_quality_tab_2.gif)

Optionally, give a custom name to the Tab.

# Available Tabs

You have the following options:

| Tab Template | Description | Data source |
|---|---|---|
| Descriptors | Shows the results of text evaluations over time. | `TextEvalPreset()`, or individual `ColumnSummaryMetric()` Metrics or Tests that use Descriptors. |
| Columns | Plots column distributions over time for categorical and numerical columns. | `DataQualityPreset()` or `ColumnSummaryMetric()` for individual columns. |
| Data Quality | Shows dataset quality metrics (e.g., missing values, duplicates, etc.) over time and results of Data Quality Tests. | For the Metric Panels: `DataQualityPreset()` or `DatasetSummaryMetric()`. For the Test Panel: any individual Tests from Data Quality or Data Integrity groups.|
| Data Drift | Shows the share of drifting features over time and the results of Column Drift Tests. | For the Metric Panel: `DataDriftPreset()` or `DataDriftTestPreset()`. For the Test Panel: `DataDriftTestPreset()` or individual `TestColumnDrift()` Tests. |

# What’s next?

* Understand available [monitoring Panels types](design_dashboard.md).
* See how to [customize your Dashboard](design_dashboard_api.md).
