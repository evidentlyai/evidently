## When to use it?

You can use the `DataQualityTestPreset` when you want to evaluate the data quality, even without a reference dataset.

It will help assess whether a data batch is e.g. suitable for training or retraining. It can detect issues like missing data, duplicates, or constant and almost constant features.  

### Code example

```python
data_quality = TestSuite(tests=[
   DataQualityTestPreset(),
])
 
data_quality.run(reference_data=ref,current_data=curr)
data_quality
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:


```python
TestColumnShareOfNulls(column="all"),
TestMostCommonValueShare(column="all")
TestNumberOfConstantColumns(),
TestNumberOfDuplicatedColumns(),
TestNumberOfDuplicatedRows(),
TestHighlyCorrelatedColumns(),

```

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}
