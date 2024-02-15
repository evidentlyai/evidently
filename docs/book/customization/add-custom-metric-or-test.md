There are two ways to add a custom Metric to Evidently. 

# 1. Add a new Metric as a Python function. (Recommended).

In this case, you only need to implement the computation of the new Metric as a Python function. The visual render in the Report will default to a simple counter. 

This is a recommended path to add custom Metrics to your monitoring. Using this method, you can later access the Report from Evidently Cloud (or self-hosted Monitoring UI) and track the custom Metric over time on the monitoring panels.

Example notebook: 
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_build_metric_over_python_function.ipynb" %}

**Note**: this functionality currently works for Metrics only. 

**Note 2**: if you want to add a custom drift method specifically, a separate [drift method customization](add-custom-drift-method.md) option is available.  

# 2. Implement a new Metric and Test from scratch. 

To add a custom Metric or Test from scratch, you can also implement both the calculation method and (optional) visualization. 

This is suitable for open-source use when you only want to access the new Metric (or Test) in a Report or a Test Suite. When using this method, you won't be able to view the custom Metric (or Test) in the Evidently Cloud (or self-hosted Monitoring UI ) since the code that defines the custom render won't be accessible from the UI service. 

**Note**: this is advanced functionality that expects you to be able to work with the codebase independently. To implement the visualization, you should be familiar with Plotly. 
You can use the metrics and tests in the codebase as an example.

This example Jupyter notebook shows how to implement a simple metric and test and include them in a custom Report and Test Suite:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_make_custom_metric_and_test.ipynb" %}

# Open a GitHub issue 

If you want to suggest adding specific metrics and tests that are currently not covered to the core library, you can also [open a GitHub issue](https://github.com/evidentlyai/evidently/issues) with the feature request or a proposal of the new Metric you'd like to contribute.
