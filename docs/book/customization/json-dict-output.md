---
description: How to modify what is included in the Evidently JSON or Python dictionary output.
---

**Pre-requisites**:
* You know how to generate Evidently Reports and Test Suites and get the output as JSON or Python dictionary 

# Code example

Notebook example on JSON / Python dictionary customization:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_customize_json_output.ipynb" %}

# Default

Default JSON and Python dictionary output includes the values of Metrics and Test results but does not include visualizations. 

Using the following options, you can customize the JSON/Python dictionary output for Reports and Test Suites. 

# Include render

If you want to include some of the information about the visualizations computed by Evidently (for example, distribution bins), you can specify it:

```python
report.json(include_render=True)
```

This way, you will receive a verbose output with additional info on visualizations.   

This is convenient if you want to integrate Evidently output with other visualization tools.

# Include and exclude components

You can also flexibly define which specific output to include in JSON or Python dictionary. 

To specify which metrics, tests, or components to include, use `include`: 

```python
report.as_dict(include={
    "DataDriftTable": {
        "drift_by_columns":{
            "target":{
                "column_name", "column_type", "drift_score"
            }}}})
```

This is convenient if you want to get a minimalistic output that is easy to parse. 

To understand which components exist, generate the complete example output, and look at the keys. 

Use `exclude` to specify which metrics, tests, or components to omit. You can combine using include and exclude, for example:

```python
report.as_dict(
    include={"DatasetDriftMetric": {"share_of_drifted_columns"}},
    exclude={"DataDriftTable":{"drift_by_columns"}}
)
```

If you want to include all fields for a dictionary, use `True`.

```python
report.as_dict(include={"DataDriftTable":{"drift_by_columns":{"target":True}}})
```

To apply filters to column-based results, use `AllDict`.

```python
report.as_dict(include={
    "DataDriftTable": {
        "drift_by_columns":AllDict({
                "column_name", "column_type", "drift_score"
            })}},
              exclude={"DataDriftTable": {"drift_by_columns":AllDict({
                 "column_type"
            })}})
```

This way, you can flexibly define the exact output format. Sometimes using exclude/include together might be more convenient than simply listing the components. 
