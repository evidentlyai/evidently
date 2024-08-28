---
description: How to run Tests and create Test Suites using Evidently Python library.
---

# Code examples

Check the [sample notebooks](../examples/examples.md) for examples of how to generate Test Suites.

# Imports

After [installing Evidently](../installation/install-evidently.md), import the `TestSuite` component and the necessary `test_presets` or `tests` you plan to use:

```python
from evidently.test_suite import TestSuite
from evidently.test_preset import DataQualityTestPreset, DataStabilityTestPreset
from evidently.tests import *
```

# How it works

Here is the general flow.
* **Input data**. Prepare data as a Pandas DataFrame. This will be your `current` data to test. You may also pass a `reference` dataset to generate Test conditions from this reference or run data distribution Tests. Check the [input data requirements](../input-data/data-requirements.md).
* **Schema mapping**. Optionally, define your data schema using [Column Mapping](../input-data/column-mapping.md).
* **Define the Test Suite**. Create a `TestSuite` object and include the selected Tests or Test Presets in the `tests` list.
* **Set the Test parameters**. Optionally, specify individual test conditions and mark certain tests as non-critical.
* **Run the Test Suite**. Execute the Test Suite on your `current_data`. If applicable, pass the `reference_data` and `column_mapping`.
* **Get the results**. Get a visual summary in Jupyter notebook, export the metrics and tests metadata, or upload it to the Evidently Platform.

You can use Test Presets, which are pre-built Test Suites that automatically generate a set of Tests for a specific aspect of the data or model performance, or create your Test Suite by listing Tests one by one.

# Test Presets 

To use a Test Preset, create a `TestSuite` object and include the chosen Preset in the `tests` list. The Tests will run with default parameters for all columns in the dataset. 

Evidently will also automatically generate Test conditions. There are two ways Evidently does it.
* **Based on the reference dataset**. If you provide a `reference`, Evidently will generate conditions based on it. For example, a Preset may include the `TestShareOfOutRangeValues` Test. It will fail if over 10% of values in the `current` dataset are out of range. Evidently automatically derives the min-max value range for each column from the reference. 10% is an encoded heuristic.
*  **Based on heuristics**. If you don’t provide a reference, Evidently will run Tests it can using heuristics only. For example, `TestAccuracyScore()` fails if the model quality is worse than the quality of a dummy model, which Evidently creates automatically. For data quality, Tests like TestNumberOfEmptyRows() or TestNumberOfMissingValues() assume both should be zero.

{% hint style="info" %} 
**Reference**: Check the default Test conditions in the [All tests](../reference/all-tests.md) table.
{% endhint %}

**Example 1**. To apply the `DataQualityTestPreset` to a single `curr` dataset, with conditions generated based on heuristics:

```python
data_quality = TestSuite(tests=[
    DataQualityTestPreset(),
])

data_quality.run(reference_data=None, 
                   current_data=curr)
```

{% hint style="info" %} 
**Available Test Presets**. There are other Presets: for example, `DataStabilityTestPreset`, `DataDriftTestPreset` or `RegressionTestPreset`. Refer to the [Presets overview](../presets/all-presets.md) to understand individual Presets, and to [All Tests](../reference/all-tests.md) to see all available options and parameters. To see the interactive examples, refer to the [example notebooks](../examples/examples.md).
{% endhint %}

To get the visual report with Test results, call the object in Jupyter notebook or Colab:

```python
data_quality
```

To get the Test results summary, generate a Python dictionary:

```python
data_quality.as_dict()
```

{% hint style="info" %} 
**There are more output formats!**. You can also export the results in formats like HTML, JSON, dataframe, and more. Refer to the [Output Formats](output_formats.md) for details.
{% endhint %}

**Example 2**. To apply the `DataStabilityTestPreset`, with conditions generated from reference, pass the `reference_data`:

```python
data_stability = TestSuite(tests=[
    DataStabilityTestPreset(),
])

data_stability.run(reference_data=ref, 
                   current_data=curr)
```


**Example 3**. To apply the `NoTargetPerformanceTestPreset` with additional parameters: 

```python
no_target_performance = TestSuite(tests=[
    NoTargetPerformanceTestPreset(columns=['education-num', 'hours-per-week'], 
                                  cat_stattest=ks, 
                                  cat_statest_threshold=0.05),
])
```

By selecting specific columns for the Preset, you reduce the number of generated column-level Tests. When you specify the data drift detection method and threshold, it will override the defaults.

{% hint style="info" %} 
Refer to the [All tests](../reference/all-tests.md) table to see available parameters and defaults for each Test and Test Preset. 
{% endhint %}

# Custom Test Suite

You can use Test Presets as a starting point to explore available analyses. In most cases, you'll want to design your Test Suite to pick specific tests and set conditions more precisely. Here’s how:
* **Choose individual Tests**. Select the Tests you want to include in your Test Suite.
* **Pass Test parameters**. Optionally, set custom parameters for applicable Tests.
* **Set custom conditions**. Optionally, define when Tests should pass or fail.
* **Mark Test criticality**. Optionally, mark some tests as non-critical to return a Warning instead of Fail.

## 1. Choose tests

First, decide which Tests to include. Tests can be either dataset-level or column-level.

{% hint style="info" %} 
**List of available Tests**: The complete list of Tests is available in the [All tests](../reference/all-tests.md) table. To see interactive examples, refer to the [Example notebooks](../examples/examples.md).
{% endhint %}

{% hint style="info" %} 
**Row-level evaluations**: If you want to generate row-level scores before running the Tests, which are often relevant for text data, read more about [Text Descriptors](text-descriptors.md.md).
{% endhint %}

**Dataset-level Tests**. Some Tests apply to the entire dataset, such as checking the share of drifting features or accuracy drops.

To create a custom Test Suite, create a `TestSuite` object and list the `tests` one by one:    

```python
data_drift_suite = TestSuite(tests=[
    TestShareOfDriftedColumns(),
    TestNumberOfEmptyRows(),
])
```

**Column-level Tests**. Some Tests focus on individual columns, like checking if a specific column's values stay within a range.

To create a custom Test Suite with column-level Tests, pass the name of the column to each Test:

```python
feature_suite = TestSuite(tests=[
    TestColumnShareOfMissingValues(column_name='hours-per-week'),
    TestColumnDrift(column_name='education'),
    TestMeanInNSigmas(column_name='hours-per-week')
])
```

{% hint style="info" %} 
**Generating multiple column-level Tests**: To simplify listing many Tests at once, use [Test generator helper function](test-metric-generator.md).
{% endhint %}

**Combining Tests**. You can combine column-level and dataset-level Tests in a single Test Suite. You can also include Presets and individual Tests together.

```python
my_data_quality_tests = TestSuite(tests=[
    DataQualityTestPreset(),
    TestColumnAllConstantValues(column_name='education'),
    TestNumberOfDriftedColumns()
])
```

## 2. Set Test parameters

Tests can have optional or required parameters. 

**Example 1**. To test a quantile value, you need to specify the quantile (Required parameter):

```python
column_tests_suite = TestSuite(tests=[
    TestColumnQuantile(column_name='mean perimeter', quantile=0.25),
])
```

**Example 2:** To override the default drift detection method, pass the chosen statistical method (Optional), or modify the Mean Value Test to use 3 sigmas:

```python
dataset_suite = TestSuite(tests=[
    TestShareOfDriftedColumns(stattest=psi),
    TestMeanInNSigmas(column_name='hours-per-week', n_sigmas=3),
])
```

**Example 3:** To change the decision threshold for probabilistic classification to 0.8:

```python
model_tests = TestSuite(tests=[
    TestPrecisionScore(probas_threshold=0.8),
    TestRecallScore(probas_threshold=0.8)
])
```

{% hint style="info" %} 
**Reference**: you can browse available Test parameters and defaults in the [All tests](../reference/all-tests.md) table.
{% endhint %}

# 3. Set test conditions

You can set up your Test conditions in two ways:
* **Automatic**. If you don’t specify individual conditions, the defaults (reference or heuristic-based) will apply, just like in Test Presets.
* **Manual**. You can define when exactly a Test should pass or fail. For example, set a lower boundary for the expected model precision. If the condition is violated, the Test fails.
  
You can mix both approaches in the same Test Suite, where some Tests run with defaults and others with custom conditions.

### Test condition parameters

Use the following standard parameters to set Test conditions:

| Condition parameter | Explanation                                | Usage Example                                                   |
|--------------------------|--------------------------------------------|-----------------------------------------------------------------|
| `eq: val`               | equal <br> `test_result == val`                         | TestColumnValueMin(column_name=”col”, eq=5)            |
| `not_eq: val`             | not equal <br> `test_result != val`                         | TestColumnValueMin(column_name=”col”, not_eq=0)            |
| `gt: val`                  |  greater than  <br> `test_result > val`                          | TestColumnValueMin(column_name=”col”, gt=5)            |
| `gte: val`                 | greater than or equal <br> `test_result >= val`                         | TestColumnValueMin(column_name=”col”, gte=5)           |
| `lt: val`                | less than <br> `test_result < val`                          | TestColumnValueMin(column_name=”col”, lt=5)            |
| `lte: val`               | less than or equal <br> `test_result <= val`                         | TestColumnValueMin(column_name=”col”, lte=5)           |
| `is_in: list`              | `test_result ==` one of the values from list | TestColumnValueMin(column_name=”col”, is_in=[3,5,7])   |
| `not_in: list`             | `test_result !=` any of the values from list | TestColumnValueMin(column_name=”col”, not_in=[-1,0,1]) |

**Example 1**. To Test that the share of values out of range in a specific column is 0, and the share of missing values in another column is less than (`lt`) 20%. 

```python
feature_level_tests = TestSuite(tests=[
TestShareOfOutRangeValues(column_name='hours-per-week', eq=0),
TestColumnShareOfMissingValues(column_name='education', lt=0.2),
])
```

**Example 2**. You can specify both the Test condition and parameters together.

In the first Test in the example above, Evidently still automatically derives the feature range from the reference. You can also manually set the range (e.g., between 2 and 10). The Test fails if any value is out of this range:

```python
feature_level_tests = TestSuite(tests=[
TestShareOfOutRangeValues(column_name='hours-per-week', left=2, right=10, eq=0),
])
```

**Example 3**. To Test that the precision and recall is over 90%, with a set decision for the classification model:

```python
model_tests = TestSuite(tests=[
    TestPrecisionScore(probas_threshold=0.8, gt=0.9),
    TestRecallScore(probas_threshold=0.8, gt=0.9)
])
```


### Custom conditions with Approx

If you want to set an upper and/or lower limit to the value, you can use **approx** instead of calculating the value itself. You can set the relative or absolute range. 

```python
approx(value, relative=None, absolute=None)
```

To use `approx`, first import this component:

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

