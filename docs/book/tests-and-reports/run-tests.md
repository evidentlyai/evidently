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

# Output formats 

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
