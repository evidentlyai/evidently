---
description: How to generate test presets in Evidently.
---

**TL;DR**: Pre-built test presets work out of the box without additional configuration.

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

**Example 1**. To apply the `DataStabilityTestPreset`:

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

**Example 2**. To apply and call `NoTargetPerformanceTestPreset`:

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
