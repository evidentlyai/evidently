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
NoTargetPerformance
DataStability
DataQuality
DataDrift
Regression
MulticlassClassification
BinaryClassificationTopK
BinaryClassification
```

Refer to the Test Suites to see the complete list of presets and contents, and to the All Tests list to learn about defaults.

---
You can use the `most_important_features` argument as shown above. In this case, some of the per-feature tests will only apply to the features from the list. This way, you will decrease the overall number of tests. 

**Available presets**. Here are other Test presets you can try:

```python
no_target_performance = TestSuite(tests=[
NoTargetPerformance(most_important_features=['education-num', 'hours-per-week']),
])
no_target_performance.run(reference_data=ref,current_data=curr)
No_target_performance
```


You can get the test output as a JSON:
```python
data_drift.json()
```

Or in Python dictionary format:
```python
data_drift.as_dict()
```
