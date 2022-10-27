## When to use it?

You can use the `DataDriftTestPreset` when you receive a new batch of input data or generate a new set of predictions.

It will help detect data and concept drift. It compares the feature and predictions distributions using statistical tests and distance metrics. By default, it uses the in-built Evidently [drift detection logic](../reference/data-drift-algorithm.md) that selects the detection method based on data volume and type.

### Code example

```python
data_drift = TestSuite(tests=[
   DataDriftTestPreset(),
])
 
data_drift.run(reference_data=ref, current_data=curr)
data_drift
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:


```python
TestShareOfDriftedColumns()
TestValueDrift(column=all)
```

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}
