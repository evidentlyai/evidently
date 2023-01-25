**TL;DR:** You can create a custom Test Suite from 50+ individual Tests. You can use auto-generated test conditions or pass your own.

# 1. Choose tests

To design a Test Suite, first define which Tests to include. You can use Presets as a starting point to explore available types of analysis. Note that there are additional Tests that are not included in the Presets.   

{% hint style="info" %} 
**Reference**: The complete list of Tests is available in the [All tests](../reference/all-tests.md) table. To see interactive examples, refer to the [Example notebooks](../examples/examples.md).
{% endhint %}

There are two types of tests: dataset-level and column-level.

## Dataset-level tests

You can apply some of the Tests on the dataset level. For example, to evaluate data drift for the whole dataset. 

Create a `TestSuite` object and specify the `tests` to include:

```python
data_drift_suite = TestSuite(tests=[
    TestShareOfDriftedColumns(),
    TestNumberOfDriftedColumns(),
])
```

To run the Tests and get the visual report:

```python
data_drift_suite.run(
    reference_data=ref,
    current_data=curr,
    column_mapping=ColumnMapping(),
)
data_drift_suite
```

## Column-level tests

You can apply some Tests to the individual columns. For example, to check if a specific feature or model prediction stays within the range. 

To create a custom Test Suite with column-level tests:

```python
feature_suite = TestSuite(tests=[
    TestColumnShareOfMissingValues(column_name='hours-per-week'),
    TestColumnDrift(column_name='education'),
    TestMeanInNSigmas(column_name='hours-per-week')
])
```

To run the Tests and get the visual report:

```python
feature_suite.run(reference_data=ref, current_data=curr)
feature_suite
```

## Combining tests

You can freely combine column-level and dataset-level Tests in a single Test Suite. You can also include Presets and individual Tests in the same list.

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

{% hint style="info" %} 
**Note**: If you want to generate multiple column-level Tests, you can use [test generator helper function](test-metric-generator.md).
{% endhint %}

# 2. Set test parameters

Some test have **required parameters**.

**Example 1**. If you want to test a quantile value, you need to pass the quantile:

```python
column_tests_suite = TestSuite(tests=[
    TestColumnQuantile(column_name='mean perimeter', quantile=0.25),
])
```

Some tests have **optional parameters**. They change how the metrics are calculated. If you do not specify it, Evidently will apply a default.

**Example 2:** To override the default drift detection method, pass the chosen statistical test as a parameter: 

```python
dataset_suite = TestSuite(tests=[
    TestShareOfDriftedColumns(stattest=psi),
])
```

**Example 3:** To change the decision threshold for probabilistic classification, pass it as a parameter: 

```python
model_tests = TestSuite(tests=[
    TestPrecisionScore(probas_threshold=0.8),
    TestRecallScore(probas_threshold=0.8)
])
```

{% hint style="info" %} 
**Reference**: you can browse available test parameters and defaults in the [All tests](../reference/all-tests.md) table.
{% endhint %}

# 3. Set test conditions

To define when the test should return "pass" or "fail," you must set a condition. For example, you can set the lower boundary for the expected model precision. If the condition is violated, the test fails. 

There are several ways to define the conditions for each test in a test suite.  

## Auto-generated conditions

If you do not define a Test condition manually, Evidently will use the defaults.

* **Based on the reference dataset**. If you pass the reference, Evidently will auto-generate test conditions. For example,`TestShareOfOutRangeValues` test fails if over 10% of values are out of range. Evidently will automatically derive the value range for each feature. 10% is an encoded heuristic.

* **Based on heuristics**. Some tests can work even without a reference dataset. In this case, Evidently will use heuristics and dummy models. For example, `TestAccuracyScore()` fails if the model quality is worse than the quality of a dummy model. Evidently will automatically create a dummy model.

{% hint style="info" %} 
**Reference**: Default test conditions are described in the same [All tests](../reference/all-tests.md) table.
{% endhint %}

## Custom conditions

You can also set a custom condition for each test to encode your expectations. You can use the standard parameters: 

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

**Example 1**. You can set the upper or lower boundaries of a specific value by defining `gt` (greater than) and `lt` (less than):

```python
feature_level_tests = TestSuite(tests=[
TestMeanInNSigmas(column_name='hours-per-week', n_sigmas=3),
TestShareOfOutRangeValues(column_name='hours-per-week', lte=0),
TestNumberOfOutListValues(column_name='education', lt=0),
TestColumnShareOfMissingValues(column_name='education', lt=0.2),
])
```

**Example 2**. You can specify both the Test condition (expected precision and recall) and metric parameters (decision threshold) for the classification model quality test:

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

**Example 1**. Here is how you can set the upper boundary as 5+10%:

```python
lte=approx(5, relative=0.1)
```

**Example 2**. Here is how you can set the boundary as 5 +/-10%:

```python
eq=approx(5, relative=0.1)
```
