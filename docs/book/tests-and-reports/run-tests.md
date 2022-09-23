---
description: How run the Tests in Evidently.
---

**TL;DR**: You can start with ready-made Test presets. You can also create custom Test Suites from 50+ individual Tests. All Tests have in-built defaults but can be customized.

# Installation and prep

After [installation](../get-started/install-evidently.md), import evidently and the required tests or test suites:

```python
from evidently.test_suite import TestSuite
from evidently.tests import *
from evidently.test_preset import NoTargetPerformance, DataQuality, DataStability, DataDrift, Regression, MulticlassClassification, BinaryClassificationTopK, BinaryClassification
```
You need to prepare two datasets for comparison: **reference** and **current**. The reference dataset is optional. 

{% hint style="info" %} Refer to the [input data](input-data.md) and [column mapping](column-mapping.md) for more details on data preparation and requirements.{% endhint %}

# Test presets 

Evidently has ready-made `presets` that group relevant tests together. You can use them as templates to test a specific aspect of the data or model performance.

You need to create a `TestSuite` object and include the specific preset in the list of tests. You should also point to the current dataset and reference dataset (if available).

If nothing else is specified, the tests will run with the default parameters.

## How to run test presets

**Example 1**. To apply the DataStability test preset:

```python
data_stability = TestSuite(tests=[
DataStability(),
])
data_stability.run(reference_data=ref, current_data=curr)
```

You get the visual report automatically if you call the object in Jupyter notebook or Colab:

```python
data_stability
```

**Example 2**. To apply and call NoTargetPerformance preset:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformance(most_important_features=['education-num', 'hours-per-week']),
])
no_target_performance.run(reference_data=ref,current_data=curr)
No_target_performance
```
You can use the `most_important_features` argument as shown above. In this case, some of the per-feature tests will only apply to the features from the list. This way, you will decrease the overall number of tests. 

{% hint style="info" %} Refer to the Test Suites to see the complete list of presets and contents, and to the All Tests [All tests](../reference/all-tests.md) to learn about defaults.{% endhint %}

## Available presets 

Here are other Test presets you can try:

```python
NoTargetPerformance
DataStability
DataQuality
DataDrift
Regression
MulticlassClassification
BinaryClassificationTopK
BinaryClassification
```

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

You can apply some of the tests on the dataset level, for example, to evaluate data drift for all features. 

To create a custom data drift test suite with dataset-level tests:

```python
data_drift_suite = TestSuite(tests=[
TestShareOfDriftedFeatures(),
TestNumberOfDriftedFeatures(),
])
```

To run the tests and get the visual report:

```python
data_drift_suite.run(reference_data=ref, current_data=curr,
column_mapping=ColumnMapping()
data_drift_suite
```

## Column-level tests

You can apply some tests to the individual columns, for example, to check if a feature or model prediction stays within the range. 

To create a custom data drift test suite with column-level tests:

```python
feature_suite = TestSuite(tests=[
TestColumnShareOfNulls(column_name='hours-per-week'),
TestFeatureValueDrift(column_name='education'),
TestMeanInNSigmas(column_name='hours-per-week')
])
```

To run the tests and get the visual report:

```python
feature_suite.run(reference_data=ref, current_data=curr)
feature_suite
```

**Combining tests**. When you define the composition of the TestSuite, you can include presets and individual tests in the same list. You can also combine feature-level and dataset-level tests in a single suite. 

## Available tests

Evidently library has dozens of individual tests. Here are some examples of individual tests: 

```python
TestShareOfOutRangeValues()
TestMostCommonValueShare()
TestNumberOfConstantColumns()
TestNumberOfDuplicatedColumns()
TestHighlyCorrelatedFeatures()
```

{% hint style="info" %} Reference: The complete list of tests is available [here](../reference/all-tests.md).{% endhint %}

# Custom test parameters

**Defaults**. Each test compares the value of a specific metric in the current dataset against the reference. If you do not specify the condition explicitly, Evidently will use a default. For example, the TestShareOfOutRangeValues will fail if over 10% of values are out of range. The normal range for each feature will be automatically derived from the reference.

{% hint style="info" %} Reference:  All defaults are described in the same table with [all tests](../reference/all-tests.md).{% endhint %}

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

**Approx**. If you want to set an upper and/or lower limit to the value, you can use approx instead of calculating the value itself. You can set the relative or absolute range. 

```python
approx(value, relative=None, absolute=None)
```

This simplifies the definition of parameters.

`eq=approx(5, relative=0.1, absolute=None)` is the same as `lte=5 + 5 * 0.1` and `gte=5 - 5 * 0.1`

`eq=approx(5, relative=None, absolute=0.1)` is the same as `lte=5 + 0.1` and `gte=5 - 0.1`

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
