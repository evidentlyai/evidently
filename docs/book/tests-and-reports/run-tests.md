---
description: How run the Tests in Evidently.
---

**TL;DR**: You can start with ready-made Test presets. You can also create custom Test Suites from 50+ individual Tests. All Tests have in-built defaults but can be customized.

# Installation and prep

After [installation](../get-started/install-evidently.md), import the TestSuite component and the required tests or test suites:

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
Refer to the [input data](input-data.md) and [column mapping](column-mapping.md) for more details on data preparation and requirements.
{% endhint %}

# Test presets 

Evidently has `test_presets` that group relevant tests together. You can use them as templates to test a specific aspect of the data or model performance.

You need to create a `TestSuite` object and specify the presets to include. You should also point to the current and reference dataset (if available).

If nothing else is specified, the tests will run with the default parameters.

## How to run test presets

**Example 1**. To apply the DataStabilityTestPreset:

```python
data_stability = TestSuite(tests=[
DataStabilityTestPreset(),
])
data_stability.run(reference_data=ref, current_data=curr)
```

You get the visual report automatically if you call the object in Jupyter notebook or Colab:

```python
data_stability
```

**Example 2**. To apply and call NoTargetPerformanceTestPreset:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformanceTestPreset(columns=['education-num', 'hours-per-week']),
])
no_target_performance.run(reference_data=ref,current_data=curr)
no_target_performance
```
You can use the `columns` argument as shown above. In this case, some of the per-feature tests only apply to the features from the list. This way, you decrease the overall number of tests. 

## Available presets 

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
Refer to the [Test Suites](../tests/README.md) section to see the contents of each preset, and to the [All tests](../reference/all-tests.md) table to see the individual tests and their default parameters.
{% endhint %}

## Output formats 

You can get the test results in different formats. 

**HTML**. You can get the Test Suite output as an interactive visual report. It is best for exploration and debugging. You can also document test results and share them with the team. 

To see in Jupyter notebook or Colab, call the object: 
```python
data_stability
```

To export HTML as a separate file: 
```python
data_stability.save_html(“file.html”)
```
**JSON**. You can get the test output as a JSON. It is best for test automation and integration in your prediction pipelines. 

To get the JSON:

```python
data_stability.json()
```
To export JSON as a separate file: 

```python
data_stability.save_json(“file.json”)
```

**Python dictionary**. You can get the test output in the Python dictionary format. Using a Python object might be more convenient if you want to apply multiple transformations to the output.

To get the dictionary:
```python
data_stability.as_dict()
```

# Custom test suite

You can create a custom test suite from individual tests.

You need to create a `TestSuite` object and specify which tests to include. 

## Dataset-level tests

You can apply some of the tests on the dataset level. For example, to evaluate data drift for the whole dataset. 

To create a custom data drift test suite with dataset-level tests:

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

You can apply some tests to the individual columns. For example, to check if a specific feature or model prediction stays within the range. (Note that you can still apply column-level tests to all the individual columns in the dataset).

To create a custom data drift test suite with column-level tests:

```python
feature_suite = TestSuite(tests=[
    TestColumnShareOfNulls(column_name='hours-per-week'),
    TestColumnValueDrift(column_name='education'),
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
my_data_quality_report = TestSuite(tests=[
    DataQualityTestPreset(),
    TestColumnAllConstantValues(column_name='education'),
    TestNumberOfDriftedColumns()
])

my_data_quality_report.run(reference_data=ref,current_data=curr)
my_data_quality_report
```

## Available tests

Evidently library has dozens of individual tests. Here are some examples of individual tests: 

```python
TestShareOfOutRangeValues()
TestMostCommonValueShare()
TestNumberOfConstantColumns()
TestNumberOfDuplicatedColumns()
TestHighlyCorrelatedColumns()
```

{% hint style="info" %} 
**Reference**: The complete list of tests is available in the [All tests](../reference/all-tests.md) table.
{% endhint %}

# Custom test parameters

**Defaults**. Each test compares the value of a specific metric in the current dataset against the reference. If you do not specify the condition explicitly, Evidently will use a default. 

For example, the `TestShareOfOutRangeValues` test will fail if over 10% of values are out of range. The normal range for each feature will be automatically derived from the reference.

{% hint style="info" %} 
**Reference**: The defaults are described in the same [All tests](../reference/all-tests.md) table.
{% endhint %}

## How to set the parameters

You can override the default and set the parameters for specific tests.

For example, you can set the upper or lower boundaries of a specific value by defining `gt` (greater than) and `lt` (less than).

Here is an example:

```python
feature_level_tests = TestSuite(tests=[
TestMeanInNSigmas(column_name='hours-per-week', n_sigmas=3),
TestShareOfOutRangeValues(column_name='hours-per-week', lte=0),
TestNumberOfOutListValues(column_name='education', lt=0),
TestColumnShareOfNulls(column_name='education', lt=0.2),
])

feature_level_tests.run(reference_data=ref, current_data=curr)

Feature_level_test
```
## Available parameters

### Standard parameters 

The following standard parameters are available: 

| Condition parameter name | Explanation                                | Usage Example                                                   |
|--------------------------|--------------------------------------------|-----------------------------------------------------------------|
| eq: val                  | test_result == val                         | TestFeatureMin(feature_name=”numeric_feature”, eq=5)            |
| not_eq: val              | test_result != val                         | TestFeatureMin(feature_name=”numeric_feature”, ne=0)            |
| gt: val                  | test_result > val                          | TestFeatureMin(feature_name=”numeric_feature”, gt=5)            |
| gte: val                 | test_result >= val                         | TestFeatureMin(feature_name=”numeric_feature”, gte=5)           |
| lt: val                  | test_result <=val                          | TestFeatureMin(feature_name=”numeric_feature”, lt=5)            |
| lte: val                 | test_result <= val                         | TestFeatureMin(feature_name=”numeric_feature”, lte=5)           |
| is_in: list              | test_result == one of the values from list | TestFeatureMin(feature_name=”numeric_feature”, is_in=[3,5,7])   |
| not_in: list             | test_result != any of the values from list | TestFeatureMin(feature_name=”numeric_feature”, not_in=[-1,0,1]) |

### Approx

If you want to set an upper and/or lower limit to the value, you can use **approx** instead of calculating the value itself. You can set the relative or absolute range. 

```python
approx(value, relative=None, absolute=None)
```
To apply approx, you need to first import this component:

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

### Additional parameters

Some tests require additional parameters or might have optional parameters.

For example, if you want to test a quantile value, you need to pass the quantile as a parameter (required). Or, you can pass the K parameter to evaluate classification precision@K instead of using the default decision threshold of 0.5 (optional). 

{% hint style="info" %} 
**Reference**: the additional parameters that apply to specific tests and defaults are described in the same [All tests](../reference/all-tests.md) table.
{% endhint %}

# Tests generation 

There are several features that simplify generating multiple column-level tests. 

## List comprehension

You can pass a list of parameters or a list of columns. 

**Example 1**. Pass the list of multiple quantile values to test for the same column. 

```python
suite = TestSuite(tests=[
   TestValueQuantile(column_name="education-num", quantile=quantile) for quantile in [0.5, 0.9, 0.99]
])

suite.run(current_data=current_data, reference_data=reference_data)
suite
```

**Example 2**. Apply the same test with a defined custom parameter for all columns in the list: 

```python
suite = TestSuite(tests=[
   TestColumnValueMin(column_name=column_name, gt=0) for column_name in ["age", "fnlwgt", "education-num"]
])
 
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

## Column test generator

You can also use the `generate_column_tests` function to create multiple tests.

By default, it generates tests with the default parameters for all the columns:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfNulls)])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

You can also pass the parameters:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfNulls, columns="all", parameters={"lt": 0.5})])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

You can generate tests for different subsets of columns. Here is how you generate tests only for **numerical columns**:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnValueMin, columns="num")])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

Here is how you generate tests only for **categorical columns**:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfNulls, columns="cat", parameters={"lt": 0.1})])
suite.run(current_data=current_data, reference_data=refernce_data)
suite
```
 
You can also generate tests with defined parameters, for a custom defined column list:
 
```python
suite = TestSuite(tests=[generate_column_tests(TestColumnValueMin, columns=["age", "fnlwgt", "education-num"],
                                              parameters={"gt": 0})])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```
 
### Column parameter

You can use the parameter `columns` to define a list of columns to which you apply the tests. If it is a list, just use it as a list of the columns. If `columns` is a string, it can take the following values:
* `"all"` - apply tests for all columns, including target/prediction columns.
* `"num"` - for numerical features, as provided by column mapping or defined automatically
* `"cat"` - for categorical features, as provided by column mapping or defined automatically
* `"features"` - for all features, excluding the target/prediction columns.
* `"none"` -  the same as "all."
