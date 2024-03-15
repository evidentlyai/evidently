---
description: Using Evidently in Colab and other notebook environments.
---

You can use Evidently Python library to generate visual HTML reports, JSON, and Python dictionary output directly in the notebook environment. You can also save the HTML reports externally and open them in the browser.

By default, Evidently is tested to work in **Jupyter notebook** on MAC OS and Linux and **Google Colab**.

# Jupyter notebooks 

You can generate the visual reports in **Jupyter notebooks** on MAC OS and Linux. 

You should then follow the steps described in the User Guide to [generate reports](../tests-and-reports/get-reports.md) and [run test suites](../tests-and-reports/run-tests.md).

# Google Colab 

You can also generate visual reports in **Google Collaboratory**.

To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```

Then follow the steps described in the User Guide.

# Other notebook environments 

You can also use Evidently in other notebook environments, including **Jupyter notebooks on Windows**, **Jupyter lab** and hosted notebooks such as **Kaggle Kernel**, **Databricks** or **Deepnote** notebooks. Consult the [installation instructions for details](../installation/install-evidently.md).

For most hosted environments, you would need to run the following command in the notebook cell:

```
!pip install evidently
```

## Visual reports in the notebook cell

```python
report.show()
```

Here is a complete example of how you can call the report after installation, imports, and data preparation:

```python
report = Report(metrics=[
    DataDriftPreset(), 
])

report.run(reference_data=reference, current_data=current)
report.show()
```

## Standalone HTML

If the report does not appear in the cell, consider generating a standalone HTML file and opening it in a browser. 

```python
report = Report(metrics=[
    DataDriftPreset(), 
])

report.run(reference_data=reference, current_data=current)
report.save_html("file.html")
```

You can also specify the path where to save the file.
