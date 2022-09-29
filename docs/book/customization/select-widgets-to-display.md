---
description: You can decide which components to include in the Dashboards or HTML Reports.
---

# Select Widgets

There are two ways to modify the composition of the default Evidently [reports](../reports/).

### 1. Choose between the short and full version

We have two levels of verbosity for each Tab. To change it, you need to specify the **verbose\_level** parameter when you define the Dashboard.

```
dashboard = Dashboard(tabs=[RegressionPerformanceTab(verbose_level=1)])
```

* **verbose\_level==1** - full report
* **verbose\_level==0** - short report

The short report contains a reduced number of widgets.

### 2. Specify the exact list of widgets in the Tabs

![](../.gitbook/assets/customization\_select\_widgets.png)

You can also specify the individual widgets you want to include in a given Tab.

To select the widgets in the Tab, you should define the **include\_widgets** parameter in the Tab class. To see the available widgets, run the `list_widgets()` method of the Tab object:

```
RegressionPerformanceTab.list_widgets()
```

![](<../.gitbook/assets/image (10) (1).png>)

Next, choose the widgets you need (**include\_widgets** overwrites the **verbose\_level** parameter):

```
dashboard = Dashboard(tabs=[RegressionPerformanceTab(verbose_level=0, include_widgets=[
    "Regression Model Performance Report.",
    "Reference: Error Distribution",
    "Current: Error Distribution",
])])
```

The widgets will appear in the Tab in the same order as listed.

You can also add your own [custom](add-a-custom-widget-or-tab.md) widgets.
