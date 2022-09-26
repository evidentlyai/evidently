## When to use it?

You can use the Regression Performance test preset to evaluate the quality of a regression model, when you have the ground truth data (actuals).

### Code example

```python
regression_performance = TestSuite(tests=[
   Regression(),
])
 
regression_performance.run(reference_data=ref, current_data=curr)
regression_performance
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:

```python
TestValueMeanError(),
TestValueMAE(),
TestValueRMSE(),
TestValueMAPE(),
```

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}
