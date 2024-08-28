---
description: How to export the results of evaluations.
---   

You can view or export results of the Evidently Reports or Test Suites in multiple formats.

# View in Jupyter notebook 

You can directly render the interactive visual summary of the evaluation results in interactive Python environments like Jupyter notebook or Colab. 

Simply call the the resulting Python object after you run the Report: 

```python
drift_report
```

This will render the HTML object directly in the notebook cell.

# HTML

You can save the interactive visual report as an HTML file, to be able to open it in the browser or share with the team. 

To export HTML as a separate file: 

```python
drift_report.save_html(“file.html”)
```

# JSON

You can get the results of the calculation as a JSON. It is useful for storing and exporting results elsewhere.

To get the JSON:

```python
drift_report.json()
```

To save the JSON as a separate file: 

```python
drift_report.save_json("file.json")
```

# Python dictionary

You can get the output in the Python dictionary format. Using a Python object might be more convenient if you want to run automated evaluations as part of your data or ML pipelines, and apply transformations to the output, such as extracting specific values or Test results. 

To get the dictionary:

```python
drift_report.as_dict()
```

# Scored DataFrame

If you generated Text descriptors as part of your evalution, you can get a DataFrame with all generated descriptors added to each row of your original input data.


```python
text_evals_report.datasets().current
```

This will return the complete original dataset, and new scores.

# DataFrame with Metrics summary

You can get the output with Metric results in tabular format as a DataFrame.

You can export the results for a specific Metric only: 

```python
drift_report.as_dataframe("DataDriftTable")
```

You can also export results for the complete Report. In this case, you get a dictionary of dataframes.

```python
drift_report.as_dataframe()
```

This will return all relevant values that are computed inside the Metric.


# Evidently snapshot

You can save the output of a Report or Test Suite as an Evidently JSON `snapshot`.

This is a rich JSON format that allows to store the evaluation results on Evidently platform and monitoring them over time. When you save Reports or Test Suites to the platform, a snapshot is generated automatically, so you typically do not have to think about it as it happens on the background.

However, you can also explicitly generate and save the output as a snapshot. This JSON format is different is different from using json() or save_json(“file.json”). When using the usual JSON export, you generate a structured output with limited information. You cannot convert this JSON back to HTML. With “snapshot,” you generate a comprehensive summary of the contents and can restore the output in any available Evidently format without accessing the initial raw data. 


To save the Report as a snapshot:

```python
drift_report.save('snapshot.json')
```

To load the snapshot back, use the “load” function. 

```
loaded_report = Report.load('snapshot.json')
```

After you load the snapshot back, you can again view it in Python or export to other formats.


{% hint style="info" %}
**Generating snaphots**. To better understand how you can upload the evaluation results to the Evidently Platform, check the page on [Generating Snaphots](../get-started/tutorial-monitoring.md).
{% endhint %}
