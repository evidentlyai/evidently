---
description: How to add and configure monitoring panels.
---   

By default, the monitoring dashboard for each new project is empty. You must define the dashboard composition in the code and select which metrics and test results to show. You can add multiple panels to the dashboard for each project.

**Note**: we plan to add the ability to add panels from the interface in the next releases. 

# Code example

Refer to the ML Monitoring QuickStart for a complete Python script that shows how to add several monitoring panels for a toy dataset. 

{% content-ref url="../get-started/tutorial-monitoring.md" %}
[Get started tutorial](../get-started/tutorial-monitoring.md). 
{% endcontent-ref %}

# How it works 

Evidently `snapshots` contain multiple measurements. For example, when you log the `DataDriftTable()` Metric in a `snapshot`, it will contain the dataset drift summary, like this: 

```python
'number_of_columns': 15,
'number_of_drifted_columns': 5,
'share_of_drifted_columns': 0.3333333333333333,
'dataset_drift': False,
```

It will also contain data on individual column drift. Here is a partial example:

```python
'column_name': 'age',
'column_type': 'num',
'stattest_name': 'Wasserstein distance (normed)',
'stattest_threshold': 0.1,
'drift_score': 0.18534692319042428,
'drift_detected': True,
```

You can visualize any individual measurements over time as long as you capture them inside `snapshots`. To do that, you must add `panels` to a monitoring dashboard inside a specific `project`. You must pass the chosen `value` (the **MetricResult** contained inside the logged `snapshot`) to specify what to plot. 

For example, you might want to plot the `share_of_drifted_columns`, `number_of_drifted_columns`, or a `drift_score` for a specific column: all these measurements are available as a **MetricResult** inside the `DataDriftTable()` metric.

# Add panel

To add a new `panel` to an existing `project`, use the `add_panel()` method. Here is an example of adding a new Counter type `panel` to show the share of drifting columns. 

```python
project.dashboard.add_panel(
    DashboardPanelCounter(
        title="Share of Drifted Features",
        filter=ReportFilter(metadata_values={}, tag_values=[]),
        value=PanelValue(
            metric_id="DatasetDriftMetric",
            field_path="share_of_drifted_columns",
            legend="share",
         ),
         text="share",
         agg=CounterAgg.LAST,
         size=1,
    )
)
```

*Note: `project.dashboard` is an exemplar of the `DashboardConfig` class.*

You can add multiple panels to the same project dashboard. They will appear in the order listed in the project. 
 
## Panel parameters

When you add a panel, you must specify its type and properties, such as width, title, etc. To define which measurements to visualize on a given panel, you will use the `value` parameter.  

The sections below explains the available panel types and parameters. 

## Panel types

You can choose between the following panel types.
 
* `DashboardPanelCounter`. It can include a single number with text or any custom text (this is a way to add a title to your dashboard). 

![](../.gitbook/assets/monitoring/panel_counter_example-min.png)

* `DashboardPanelPlot`. Displays any measurement as a line plot, bar plot, scatter plot or histogram. Here is the line plot example:

![](../.gitbook/assets/monitoring/panel_plot_example-min.png)

## Class DashboardPanel

This is a base class for `DashboardPanelPlot` and `DashboardPanelCounter`. The parameters below apply to both types of panels.

| Parameter | Description  |
|---|---|
| `id: uuid.UUID = uuid.uuid4()` | Unique ID of the panel. Assigned automatically. |
| `title: str`<br><br>**Usage:**<br>`title="My New Panel”` | The name of the panel. It will be visible at the header of a panel on a dashboard.  |
| `filter: ReportFilter`<br><br>`metadata_values: Dict[str, str]`<br>`tag_values: List[str]`<br><br>**Usage**:<br>`filter=ReportFilter(metadata_values={}, tag_values=[])` | Filters allow you to choose a subset of snapshots from which to display values on the panel. <br><br>To use filtering, you must provide metadata or tags when you log Reports or Test Suites.When you create a panel, you can reference these `metadata_values` or `tag_values`.  |
| `size: WidgetSize = WidgetSize.FULL`<br><br>**Available**: `1`, `2`<br><br>**Usage:**<br>`size=1` | Sets the size of the panel: <br>`1` for a half-width panel<br>`2` for a full-sized panel (Default)  |

## Class DashboardPanelCounter
`DashboardPanelCounter` allows you to add a Counter panel. You can also use this panel type to create text panels.

**Example 1**. To create a panel with the dashboard title only:

```python
project.dashboard.add_panel(
        DashboardPanelCounter(
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            agg=CounterAgg.NONE,
            title="Bike Rental Demand Forecast",
        )
    )
```

**Example 2**. To create a panel that sums up measurements (number of rows) over time.

```python
project.dashboard.add_panel(
        DashboardPanelCounter(
            title="Model Calls",
            filter=ReportFilter(metadata_values={}, tag_values=[]),
            value=PanelValue(
                metric_id="DatasetSummaryMetric",
                field_path=DatasetSummaryMetric.fields.current.number_of_rows,
                legend="count",
            ),
            text="count",
            agg=CounterAgg.SUM,
            size=1,
        )
)
```
| Parameter | Description |
|---|---|
| value: Optional[PanelValue] = None | Value (MetricResult) to show in the Counter.<br>You can create a simple text panel if you do not pass the Value. <br>See the section below on Panel Values. |
| text: Optional[str] = None | Supporting text to be shown on the Counter. |
| agg: CounterAgg<br>Available: SUM, LAST, NONE | Data aggregation options:<br>SUM - sums the values from different snapshots over time<br>LAST - shows the last available value<br>NONE - to be used for text panels  |


![](../.gitbook/assets/monitoring/metric_fields_autocomplete-min.png)
