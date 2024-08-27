Each Project has a monitoring Dashboard to visualize metrics and test results over time. A Dashboard can have multiple monitoring Panels, such as counters, line or bar plots, etc.

The Dashboard lets you monitor live data or track ad hoc experiments and tests. Use the "Show in order" toggle to switch between two views:
* Time series view: Displays data points with their actual time intervals (great for live monitoring).
* Sequential view: Shows results in order with equal spacing (ideal for experiments). 

![](../.gitbook/assets/main/evidently_ml_monitoring_main.png)

{% hint style="info" %}
**Data source**. To populate the Dashboard, you must send the evaluation results from Python, or create Reports or Test Suites directly in the UI. The Panels will be empty otherwise.  
{% endhint %}

Initially, the Dashboard for a new Project is empty. You can organize it and select values to plot. 

For both Evidently Cloud and open-source, you can define monitoring Panels via API. This is great for version control.

In Evidently Cloud, you can also:
* Get pre-built Dashboards.
* Add Panels directly in the user interface.
* Add multiple Tabs on the Dashboard to logically group the Panels.
