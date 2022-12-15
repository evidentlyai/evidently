**TL;DR:** You can combine different types of checks to test data quality, stability and drift when you have a model with delayed feedback.

For Test Suite, use the `NoTargetPerformanceTestPreset`.

# Use Case

This test suite is designed for a specific scenario:

**To monitor the model performance without ground truth.** You can use it to perform batch checks for a model that has delayed feedback (true labels or actuals come only later). The test suite combines several checks for data quality, integrity, and drift.

# NoTargetPerformance Test

If run the test suite, create a new Test Suite object and include `NoTargetPerformanceTestPreset`.

![](../.gitbook/assets/tests/test_preset_notargetperformance-min.png)

## Code example

```python
no_target_performance = TestSuite(tests=[
   NoTargetPerformanceTestPreset()
])
 
no_target_performance.run(reference_data=past_week, current_data=curr_week)
no_target_performance
```

## How it works

The preset combines several checks that go well together.

**Data stability**. They verify if the input column types match the reference and whether you have features out of range (for numerical columns) or out of the list (for categorical data). The preset also checks for missing data. 

![](../.gitbook/assets/tests/test_column_type.png)

**Prediction drift**. This test checks if there is a distribution shift in the model prediction. The default [drift detection algorithm](../reference/data-drift-algorithm.md) is used.

![](../.gitbook/assets/tests/test_mean_in_sigmas.png)

**Input data drift**. The preset also tests for distribution shifts in the model input features. It returns the overall share of drifting features (alerting if more than ⅓ of the features drifted). The default drift detection algorithm is used.



![](../.gitbook/assets/tests/test_share_of_drifted_features.png)

When you do not have true labels or actuals, you 

can monitor the input feature drift to check if the model is operating in a familiar environment. You can typically combine it with the [Prediction Drift monitoring](prediction-drift.md). If the drift is detected, you can trigger labeling and retraining, or decide to pause and switch to a different decision method.  

**2. When you are debugging the model quality decay.** If you observe a drop in the model quality, you can evaluate Data Drift to explore the change in the feature patterns, e.g., to understand the change in the environment or discover the appearance of a new segment. 

**3. To understand model drift in an offline environment.** You can explore the historical data drift to understand past changes in the input data and define the optimal drift detection approach and retraining strategy. Read more in a [blog](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) about it.

**4. To decide on the model retraining.** Before feeding fresh data into the model, you might want to verify whether it even makes sense. If there is no data drift, the environment is stable, and retraining might not be necessary.

To run data drift checks as part of the pipeline, use the Test Suite. To explore and debug, use the Report.


## When to use it?

You can use the `NoTargetPerformanceTestPreset` when you generate model predictions in batches and get the true labels or values with a delay. 

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
   NoTargetPerformanceTestPreset(columns=['education-num', 'hours-per-week']),
])

no_target_performance_top.run(reference_data=ref,current_data=curr)
no_target_performance_top
```

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

### Preset contents

The preset contains the following tests:

```python
TestShareOfDriftedColumns()
TestValueDrift(column=prediction)
TestColumnsType()
TestColumnShareOfMissingValues(column=’all’)
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
