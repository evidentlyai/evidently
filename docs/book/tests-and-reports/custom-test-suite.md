**TL;DR:** You can create a custom Test Suite from 50+ individual Tests. You can use auto-generated test conditions or pass your own.

# 1. Choose tests

To design the test suite, first define which tests to include. You can use Test Presets as a starting point to explore available types of analysis. Note that there are additional tests that are not included in the presets that you can choose from. 

{% hint style="info" %} 
**Reference**: The complete list of tests is available in the [All tests](../reference/all-tests.md) table. To see interactive examples, refer to the [Example notebooks](../examples/examples.md).
{% endhint %}

## Dataset-level tests

You can apply some of the tests on the dataset level. For example, to evaluate data drift for the whole dataset. 

Create a `TestSuite` object and specify which tests to include:

```python
data_drift_suite = TestSuite(tests=[
    TestShareOfDriftedColumns(),
    TestNumberOfDriftedColumns(),
])
```

To run the tests and get the visual report:

```python
data_drift_suite.run(
    reference_data=ref,
    current_data=curr,
    column_mapping=ColumnMapping(),
)
data_drift_suite
```

## Column-level tests

You can apply some tests to the individual columns. For example, to check if a specific feature or model prediction stays within the range. 

To create a custom data drift test suite with column-level tests:

```python
feature_suite = TestSuite(tests=[
    TestColumnShareOfMissingValues(column_name='hours-per-week'),
    TestColumnDrift(column_name='education'),
    TestMeanInNSigmas(column_name='hours-per-week')
])
```

To run the tests and get the visual report:

```python
feature_suite.run(reference_data=ref, current_data=curr)
feature_suite
```

**Combining tests**. When you define the contents of the TestSuite, you can include presets and individual tests in the same list. You can also combine feature-level and dataset-level tests. 

Here is an example:

```python
my_data_quality_tests = TestSuite(tests=[
    DataQualityTestPreset(),
    TestColumnAllConstantValues(column_name='education'),
    TestNumberOfDriftedColumns()
])

my_data_quality_tests.run(reference_data=ref,current_data=curr)
my_data_quality_tests
```

# 2. Set test parameters

Some tests have required and optional parameters. You can use them to define how the underlying metric is calculated.  

For example, if you want to test a quantile value, you need to pass the quantile as a parameter (required):

```python
column_tests_suite = TestSuite(tests=[
    TestColumnQuantile(column_name='mean perimeter', quantile=0.25),
])
```

Or, you set a different statistical method when evaluating data drift (optional): 

```python
dataset_suite = TestSuite(tests=[
    TestShareOfDriftedColumns(stattest=psi),
])
```

{% hint style="info" %} 
**Reference**: test parameters and defaults are described in the [All tests](../reference/all-tests.md) table.
{% endhint %}

# 3. Set test conditions

For tests, you have both parameters and **conditions**. Parameters define how the underlying metrics are calculated (e.g., you can change the decision threshold for the classification model, which will affect the precision and recall values). Conditions define when the test will return pass or fail (e.g., you can set your expectation on the acceptable precision and recall values). 

There are several ways how you can define the conditions for each test in a test suite.  

## Auto-generated conditions

If you do not define a test condition manually, Evidently will use the defaults for each test.

**Based on reference dataset**. If you pass the reference, Evidently will auto-generate test conditions based on provided reference and set of heuristics. 

*Example*: `TestShareOfOutRangeValues` test fails if over 10% of values are out of range. Evidently will automatically derive the value range for each feature.

**Based on heuristics**. Some tests can work even without a reference dataset or a custom condition. In this case, Evidently will use heuristics and dummy models.

*Example*: `TestAccuracyScore()` fails if the model quality is worse than the quality of a dummy model.

{% hint style="info" %} 
**Reference**: Default test conditions are described in the same [All tests](../reference/all-tests.md) table.
{% endhint %}

## Custom conditions

You can also set a custom condition for each test. You can use standard parameters: 

| Condition parameter name | Explanation                                | Usage Example                                                   |
|--------------------------|--------------------------------------------|-----------------------------------------------------------------|
| eq: val                  | test_result == val                         | TestFeatureMin(feature_name=”numeric_feature”, eq=5)            |
| not_eq: val              | test_result != val                         | TestFeatureMin(feature_name=”numeric_feature”, ne=0)            |
| gt: val                  | test_result > val                          | TestFeatureMin(feature_name=”numeric_feature”, gt=5)            |
| gte: val                 | test_result >= val                         | TestFeatureMin(feature_name=”numeric_feature”, gte=5)           |
| lt: val                  | test_result < val                          | TestFeatureMin(feature_name=”numeric_feature”, lt=5)            |
| lte: val                 | test_result <= val                         | TestFeatureMin(feature_name=”numeric_feature”, lte=5)           |
| is_in: list              | test_result == one of the values from list | TestFeatureMin(feature_name=”numeric_feature”, is_in=[3,5,7])   |
| not_in: list             | test_result != any of the values from list | TestFeatureMin(feature_name=”numeric_feature”, not_in=[-1,0,1]) |

For example, you can set the upper or lower boundaries of a specific value by defining `gt` (greater than) and `lt` (less than):

```python
feature_level_tests = TestSuite(tests=[
TestMeanInNSigmas(column_name='hours-per-week', n_sigmas=3),
TestShareOfOutRangeValues(column_name='hours-per-week', lte=0),
TestNumberOfOutListValues(column_name='education', lt=0),
TestColumnShareOfMissingValues(column_name='education', lt=0.2),
])

Here is how you can specify the custom condition and parameters for the classification model quality test:

```python
model_tests = TestSuite(tests=[
    TestPrecisionScore(probas_threshold=0.8, gt=0.99),
    TestRecallScore(probas_threshold=0.8, gt=0.99)
])
```

## Custom conditions with Approx

If you want to set an upper and/or lower limit to the value, you can use **approx** instead of calculating the value itself. You can set the relative or absolute range. 

```python
approx(value, relative=None, absolute=None)
```

To apply `approx`, you need to first import this component:

```python
from evidently.tests.utils import approx
```

Here is how you can set the upper boundary as 5+10%:

```python
lte=approx(5, relative=0.1)
```

Here is how you can set the boundary as 5 +/-10%:
```python
eq=approx(5, relative=0.1)
```
