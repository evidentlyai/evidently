## When to use it?

You can use the NoTargetPerformanceTestPreset when you generate model predictions in batches and get the true labels or values with a delay. 

This preset helps evaluate the production model quality through proxy metrics. It combines several metrics that check for data quality, data integrity, and data and prediction drift. For example, it will help detect when inputs or predictions are far off the expected range that signals that the model operates in an unfamiliar environment.   


### Code example

```python
no_target_performance_all = TestSuite(tests=[
   NoTargetPerformanceTestPreset(),
])
 
no_target_performance_all.run(reference_data=ref, current_data=curr)
no_target_performance_all
```

**Arguments:**

You can pass the list of the most important features for data drift evaluation. 

```python
no_target_performance_top = TestSuite(tests=[
   NoTargetPerformanceTestPreset(most_important_features=['education-num', 'hours-per-week']),
])

no_target_performance_top.run(reference_data=ref,current_data=curr)
no_target_performance_top
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:

```python
TestShareOfDriftedFeatures()
TestValueDrift(column=prediction)
TestColumnsType()
TestColumnShareOfNulls(column=’all’)
TestShareOfOutRangeValues(column=numerical_columns)
TestShareOfOutListValues(column=categorical_columns)
TestMeanInNSigmas(column=numerical_columns, n=2)

```

If the most important feature list specified: `TestValueDrift(column=most_important_feature_list)`

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}
