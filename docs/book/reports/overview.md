This is an explanatory page to describe the functionality of the Reports and Metrics. For code instructions, head to the [user guide](../tests-and-reports/get-reports.md).

# What is a Report?

A **Report** is a combination of different metrics that evaluate data or ML model quality. 

A **Report** can be visual and interactive: you can display it inside a Jupyter notebook or export it as an HTML file.


Here is an example of a data-related test:

![Mean value stability test](../.gitbook/assets/tests/test_example_success_data-min.png)

Evidently contains 50+ individual tests that cover different aspects of model and data quality. 

{% content-ref url="../reference/all-tests.md" %}
[All tests](all-tests.md)
{% endcontent-ref %}

# Reports

Evidently includes a set of pre-built Reports. Each of them addresses a specific aspect of the data or model performance. You can think of reports as combinations of the metrics and statistical tests that are grouped together.  

The calculation results can be available in one of the following formats:

* An interactive visual **Dashboard** displayed inside the Jupyter notebook.
* An **HTML report.** Same as dashboard, but available as a standalone file.
* A **JSON profile.** A summary of the metrics, the results of statistical tests, and simple histograms.

## Reports by type

Evidently currently works with **tabular data**. 7 reports are available. You can combine, customize the reports or contribute your own report. 

Head here for a complete user guide with the code snippets:
 
{% content-ref url="../tests-and-reports/run-tests.md" %}
[Run tests](run-tests.md)
{% endcontent-ref %}
