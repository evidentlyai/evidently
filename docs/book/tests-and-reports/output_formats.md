---
description: How to export the results of evaluations.
---   

You can view or export results from Evidently Reports or Test Suites in multiple formats.

# View in Jupyter notebook 

You can directly render the visual summary of evaluation results in interactive Python environments like Jupyter notebook or Colab. 

After running the Report, simply call the resulting Python object:

```python
drift_report
```

This will render the HTML object directly in the notebook cell.

# HTML

You can also save this interactive visual report as an HTML file to open in a browser: 

```python
drift_report.save_html(“file.html”)
```

This option is useful for sharing Reports with others or if you're working in a Python environment that doesn’t display interactive visuals.

# JSON

You can get the results of the calculation as a JSON. It is useful for storing and exporting results elsewhere.

To view the JSON in Python:

```python
drift_report.json()
```

To save the JSON as a separate file: 

```python
drift_report.save_json("file.json")
```

# Python dictionary

You can get the output as a Python dictionary. This format is convenient for automated evaluations in data or ML pipelines, allowing you to transform the output or extract specific values. 

To get the dictionary:

```python
drift_report.as_dict()
```

# Scored DataFrame

If you generated text Descriptors during your evaluation, you can retrieve a DataFrame with all generated descriptors added to each row of your original input data.

```python
text_evals_report.datasets().current
```

This returns the complete original dataset with new scores.

# Evidently snapshot

You can save the output of a Report or Test Suite as an Evidently JSON `snapshot`.

This is a rich JSON format used for storing the evaluation results on Evidently platform. When you save Reports or Test Suites to the platform, a snapshot is generated automatically.

However, you can also generate and save a snapshot explicitly. To save the Report as a snapshot:

```python
drift_report.save('snapshot.json')
```

This format is different from using `json()` or `save_json("file.json")`. A snapshot contains all supplementary and render data inside, allowing you to restore the output in any available Evidently format without accessing the initial raw data.

To load the snapshot back, use the “load” function. 

```
loaded_report = Report.load('snapshot.json')
```

After you load the snapshot back, you can again view it in Python or export it to other formats.

{% hint style="info" %}
**Generating snaphots**. To better understand how you can upload the evaluation results to the Evidently Platform, check the page on [generating snapshots](../evaluations/snapshots.md).
{% endhint %}

# DataFrame with a Report summary

**Note**: this export option is only supported for Reports, and not Test Suites.

You can get the Report results in a tabular format as a DataFrame. 

To export results for a specific Metric: 

```python
drift_report.as_dataframe("DataDriftTable")
```

To export results for the entire Report, which returns a dictionary of DataFrames:

```python
drift_report.as_dataframe()
```

This will return all relevant values that are computed inside the Metric as the metric result.
