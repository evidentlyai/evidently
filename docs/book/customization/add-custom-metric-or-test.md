There are two ways to add a custom Metric or Test to Evidently:
* Add it as a Python function (Recommended).
* Implement a custom metric with custom Plotly render.

Implementing a new Metric or Test means that you implement a completely custom column- or dataset-level evaluation.

There are other ways to customize your evaluations that do not require creating Metrics or Tests from scratch:
* Add a custom descriptor for row-level evaluations. Read on [adding custom text descriptors](add-custom-descriptor.md).
* Write a custom LLM-based evaluator using templates. Read on [designing LLM judges](llm_as_a_judge.md).
* Add a custom data drift detection method, re-using the existing Data Drift metric render. Read on [drift method customization](add-custom-drift-method.md) option.

# 1. Add a new Metric or Test as a Python function. (Recommended).

You can implement any custom Metric or Test as a Python function. The visual render in the Report will default to a simple counter. 

This is a recommended path to add custom Metrics. Using this method, you can send Reports with custom Metrics to Evidently Cloud (or view them in the self-hosted Monitoring UI).

Example notebook: 
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_build_metric_over_python_function.ipynb" %}

# 2. Implement a new Metric and Test from scratch. 

You can also implement a new Metric or Test from scratch, defining both the calculation method and the optional visualization. 

This is suitable if you want to access the new Metric (or Test) only in a Report or a Test Suite. However, you won't be able to view such custom Metrics in the Monitoring user interface or Evidently Cloud since the code that defines the custom render won't be accessible from the UI service. 

**Note**: this is advanced functionality that expects you to be able to work with the codebase independently. To implement the visualization, you should be familiar with Plotly. 
You can use the metrics and tests in the codebase as an example.

This example Jupyter notebook shows how to implement a simple metric and test and include them in a custom Report and Test Suite:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_make_custom_metric_and_test.ipynb" %}

# Open a GitHub issue 

If you want to suggest adding specific metrics and tests that are currently not covered to the core library, you can also [open a GitHub issue](https://github.com/evidentlyai/evidently/issues) with the feature request or a proposal of the new Metric you'd like to contribute.
