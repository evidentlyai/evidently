## When to use it?

You can use the DataStability test preset when you receive a new batch of input data and want to compare it to the previous one. 

It will help compare the key descriptive statistics and the overall data shape between two batches you expect to be similar. For example, you can detect the appearance of new categorical values, new values, or a significant difference in the number of rows. 

### Code example

```python
data_stability = TestSuite(tests=[
   DataStability(),
])
 
data_stability.run(reference_data=ref, current_data=curr)
data_stability
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:


```python
TestNumberOfRows(),
TestNumberOfColumns(),
TestColumnsType(),
TestColumnShareOfNulls(column=’all’),
TestShareOfOutRangeValues(column=numerical_columns)
TestShareOfOutListValues(column=categorical_columns)
TestMeanInNSigmas(column=numerical_columns, n=2)
```

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}
