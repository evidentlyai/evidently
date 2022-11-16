This is an explanatory page to describe the functionality of the Evidently Tests Suites and Tests. For code instructions, head to the [user guide](../tests-and-reports/run-tests.md).

# What is a test?

Tests help perform structured data and ML model performance checks. They explicitly define the expectations from your data and model.

A **test** is a single check. It calculates a given metric and compares it with the defined condition or threshold. 

If the condition is satisfied, it returns **success**. 

If you choose a visual report, you will see the current value of the metric and the test condition. On expand, you will get a supporting visualization. 

Here is an example of a data-related test:

![Mean value stability test](../.gitbook/assets/tests/test_example_success_data-min.png)

Here is an example of a model-related test:

![Root mean square error test](../.gitbook/assets/tests/test_example_success_model-min.png)

If the condition is not satisfied, the test returns a **fail**:

![Data drift per feature test](../.gitbook/assets/tests/test_example_fail-min.png)

If the test execution fails, it will return an error. 

Evidently contains 50+ individual tests that cover different aspects of model and data quality. 

{% content-ref url="../reference/all-tests.md" %}
[All tests](all-tests.md)
{% endcontent-ref %}


# What is a Test Suite?

In most cases, you’d want to run more than one test. 

You can list multiple tests and execute them together in a **test suite**. You will see a summary of the results:

![Custom test suite example](../.gitbook/assets/tests/test_suite_example-min.png)

If you include a lot of tests, you can navigate the output by groups: 

![No target performance test suite example](../.gitbook/assets/tests/test_suite_navigation-min.png)

You can create your test suite from individual tests or use one of the existing **presets**. 

# What is a Preset?

A **preset** is a pre-built test suite that combines checks for a particular use case. 

You can think of it as a template to start with. For example, there is a preset to check for Data Quality (`DataQualityTestPreset`), Data Stability (`DataStabilityTestPreset`), or Regression model performance (`RegressionTestPreset`).

![Regression performance test suite example](../.gitbook/assets/tests/test_preset_example-min.png)

# When to use tests

For **test-based monitoring** of production ML models: tests are best suited for integration in ML prediction pipelines. You can use them to perform batch checks for your data or models. 

For example, you can run the tests when you:
* get a new batch of the input data 
* generate a new set of predictions
* receive a new batch of the labeled data
* want to check on your model on a schedule

![Model lifecycle](../.gitbook/assets/tests/test_suite_lifecycle-min.png)

You can then build a conditional workflow based on the result of the tests: for example, generate a visual report for debugging, trigger model retraining, or send an alert.

**During model development**: you can also use tests during model development and validation. For example, you can run tests to evaluate the data quality of the new feature set or to compare test performance to training.

# How to use tests

As an input, you can provide two datasets you want to compare: **reference** and **current** data. You can use training or earlier production data as the reference and new data as current. You can also run most tests with a single (current) dataset.

You can execute the tests as a Python script or in Jupyter notebook or Colab. You can also easily integrate Evidently Tests with workflow management tools like Airflow.

Test output is available as an interactive HTML report, JSON, or Python dictionary.

To start, you can run tests with the default Evidently parameters. They use heuristics and dummy models or learn the expectations from the reference dataset. You can also set custom parameters. 

Head here for a complete user guide with the code snippets:
 
{% content-ref url="../tests-and-reports/run-tests.md" %}
[Run tests](run-tests.md)
{% endcontent-ref %}
