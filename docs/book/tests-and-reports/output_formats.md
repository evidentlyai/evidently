Applies for both Reports and Tests.

# Output formats 

To see in Jupyter notebook or Colab, call the resulting object: 

```python
drift_report
```

You can also export the Report results in different formats in addition to rendering them in the notebook.

**Evidently snapshot**. You can save the output as an Evidently JSON `snapshot`. This will allow you to visualize the model or data quality over time using the Evidently ML monitoring dashboard. This also allows you to load the JSON back to the Python environment after saving to be able to view the Report or export it in another format.

```python
drift_report.save("snapshot.json")
```

{% hint style="info" %}
**Building a live ML monitoring dashboard**. To better understand how the ML monitoring dashboard works, we recommend going through the [ML Monitoring Quickstart](../get-started/tutorial-monitoring.md).
{% endhint %}

**HTML**. You can save the interactive visual report as an HTML, to be able to open it in the browser or share with the team. 

To export HTML as a separate file: 

```python
drift_report.save_html(“file.html”)
```

{% hint style="info" %} 
Reports contain interactive visualizations inside the HTML, so large reports might take time to load. In this case, downsample your data. 
{% endhint %}

**JSON**. You can get the results of the calculation as a JSON with metrics. It is best for automation and integration in your prediction pipelines. 

To get the JSON:

```python
drift_report.json()
```

To export JSON as a separate file: 

```python
drift_report.save_json("file.json")
```

**Python dictionary**. You can get the output in the Python dictionary format. Using a Python object might be more convenient if you want to apply multiple transformations to the output.

To get the dictionary:

```python
drift_report.as_dict()
```

**Pandas dataframe**. You can get the output in tabular format as a dataframe.

You can also export the results for a specific Metric only. 

```python
drift_report.as_dataframe("DataDriftTable")
```

You can also export results for the complete Report. In this case, you get a dictionary of dataframes.

```python
drift_report.as_dataframe()
```
