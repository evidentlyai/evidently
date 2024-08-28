---
description: How to use Test Presets in Evidently.
---

**TL;DR**: Evidently has pre-built Test Suites that work out of the box. To use them, simply pass your data and choose the Preset.

# Installation and prep

After [installation](../installation/install-evidently.md), import the `TestSuite` component and the required `tests` or `presets`:

```python
from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.test_preset import NoTargetPerformanceTestPreset
from evidently.test_preset import DataQualityTestPreset
from evidently.test_preset import DataStabilityTestPreset
from evidently.test_preset import DataDriftTestPreset
from evidently.test_preset import RegressionTestPreset
from evidently.test_preset import MulticlassClassificationTestPreset
from evidently.test_preset import BinaryClassificationTopKTestPreset
from evidently.test_preset import BinaryClassificationTestPreset
```
You need two datasets for comparison: **reference** and **current**. The reference dataset is optional. 

{% hint style="info" %} 
Refer to the [input data](../input-data/data-requirements.md) and [column mapping](../input-data/column-mapping.md) for more details on data preparation.
{% endhint %}

# Using test presets 

Evidently has **Test Presets** that group relevant Tests together. You can use them as templates to check a specific aspect of the data or model performance.

To apply the Preset, create a `TestSuite` object and specify the `presets` to include in the list of `tests`. You must also point to the current and reference dataset (if available).

If nothing else is specified, the tests will run with the default parameters for all columns in the dataset. Evidently will automatically generate test conditions based on the provided reference dataset or heuristics.

**Example 1**. To apply the `DataStabilityTestPreset`:

```python
data_stability = TestSuite(tests=[
DataStabilityTestPreset(),
])
data_stability.run(reference_data=ref, current_data=curr)
```

To get the visual report, call the object in Jupyter notebook or Colab:

```python
data_stability
```

**Example 2**. To apply and call `NoTargetPerformanceTestPreset`:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformanceTestPreset(columns=['education-num', 'hours-per-week']),
])
no_target_performance.run(reference_data=ref,current_data=curr)
no_target_performance
```

You can use the `columns` argument as shown above. In this case, some of the per-feature tests only apply to the features from the list. This way, you decrease the overall number of tests. 

# Available presets 

Here are other test presets you can try:

```python
NoTargetPerformanceTestPreset
DataStabilityTestPreset
DataQualityTestPreset
DataDriftTestPreset
RegressionTestPreset
MulticlassClassificationTestPreset
BinaryClassificationTopKTestPreset
BinaryClassificationTestPreset
```

{% hint style="info" %} 
Refer to the [Presets overview](../presets/all-presets.md) to understand the use case for each preset and to the [All tests](../reference/all-tests.md) table to see the individual tests and their default parameters. To see the interactive examples, refer to the [example notebooks](../examples/examples.md).
{% endhint %}

# Output formats 

To see the get the Test Suite output as an interactive visual report in Jupyter notebook or Colab, call the resulting object: 

```python
data_stability
```

To get a text summary, use a Python dictionary.

```python
data_stability.as_dict()
```

{% hint style="info" %} 
***There are more output formats!**. You can also export and save Report results in different formats: HTML, JSON, dataframe, etc. Refer to the [Output Formats](output_formats.md) for details.
{% endhint %}


# Preset parameters

You can customize some of the Presets using parameters. For example, you can pass a different data drift detection method:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformanceTestPreset(cat_stattest=ks, cat_statest_threshold=0.05),
])
no_target_performance.run(reference_data=ref,current_data=curr)
no_target_performance
```

{% hint style="info" %} 
Refer to the [All tests](../reference/all-tests.md) table to see available parameters that you can pass for each preset. 
{% endhint %}

# Custom Test Suite

If you want to change the composition of the Test Suite or set custom test conditions, per Test, can create a custom Test Suite from individual Tests. You can use auto-generated test conditions or pass your own.

## 1. Choose tests

To design a Test Suite, first define which Tests to include. You can use Presets as a starting point to explore available types of analysis. Note that there are additional Tests that are not included in the Presets.   

{% hint style="info" %} 
**Reference**: The complete list of Tests is available in the [All tests](../reference/all-tests.md) table. To see interactive examples, refer to the [Example notebooks](../examples/examples.md).
{% endhint %}

There are two types of tests: dataset-level and column-level.

### Dataset-level tests

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

### Column-level tests

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

### Combining tests

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

## 2. Set test parameters

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

### Auto-generated conditions

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
| eq: val                  | test_result == val                         | TestColumnValueMin(column_name=”num_feature”, eq=5)            |
| not_eq: val              | test_result != val                         | TestColumnValueMin(column_name=”num_feature”, not_eq=0)            |
| gt: val                  | test_result > val                          | TestColumnValueMin(column_name=”num_feature”, gt=5)            |
| gte: val                 | test_result >= val                         | TestColumnValueMin(column_name=”num_feature”, gte=5)           |
| lt: val                  | test_result < val                          | TestColumnValueMin(column_name=”num_feature”, lt=5)            |
| lte: val                 | test_result <= val                         | TestColumnValueMin(column_name=”num_feature”, lte=5)           |
| is_in: list              | test_result == one of the values from list | TestColumnValueMin(column_name=”num_feature”, is_in=[3,5,7])   |
| not_in: list             | test_result != any of the values from list | TestColumnValueMin(column_name=”num_feature”, not_in=[-1,0,1]) |

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

### Custom conditions with Approx

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

## 4. Set test criticality

By default, all Tests will return a `Fail` if the Test condition is not fulfilled. If you want to get a `Warning` instead, use the `is_critical` parameter and set it to `False`. Example: 

```python
data_integrity_column_tests = TestSuite(tests=[
    TestColumnAllConstantValues(column_name='education', is_critical=False),
    TestColumnAllUniqueValues(column_name='education', is_critical=False),
])
```

Notebook example on setting Test criticality:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_specify_test_criticality.ipynb" %} 

