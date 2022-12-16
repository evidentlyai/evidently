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

The tests will run with the default parameters if nothing else is specified. Evidently will automatically generate test conditions based on the provided reference dataset or heuristics.

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
Refer to the [Presets overview](../presets/README.md) to understand the use case for each preset and to the [All tests](../reference/all-tests.md) table to see the individual tests and their default parameters. To see the interactive examples, refer to the [example notebooks](../examples/examples.md).
{% endhint %}

# Output formats 

You can get the Test Suite output in different formats. 

**HTML**. You can get the Test Suite output as an interactive visual report. It is best for exploration and debugging. You can also document test results and share them with the team. 

To see in Jupyter notebook or Colab, call the object: 
```python
data_stability
```

To export HTML as a separate file: 
```python
data_stability.save_html(“file.html”)
```
**JSON**. You can get the Test Suite output as a JSON. It is best for test automation and integration in your prediction pipelines. 

To get the JSON:

```python
data_stability.json()
```
To export JSON as a separate file: 

```python
data_stability.save_json(“file.json”)
```

**Python dictionary**. You can get the Test Suite output in the Python dictionary format. Using a Python object might be more convenient if you want to apply multiple transformations to the output.

To get the dictionary:
```python
data_stability.as_dict()
```

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

If you want to change the composition of the Test Suite or set custom test conditions, you should create a [custom Test Suite](custom-test-suite.md).
