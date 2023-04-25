---
description: How to customize data drift detection methods for embeddings.
---

**Pre-requisites**:
* You know how to generate Reports or Test Suites with default parameters.
* You know how to pass custom parameters for Reports or Test Suites.
* You know how to use Column Mapping to map embeddings in the input data. 

# Default
When you calculate embeddings drift (for example, using EmbeddingsDriftMetric()), Evidently automatically applies the default drift detection method (“model”).

```python
report = Report(metrics=[
    EmbeddingsDriftMetric('small_subset')
])
```

You can override the defaults by passing a custom parameter to the relevant Test, Metric, or Preset. You can define the embeddings drift detection method, the threshold, or both. 

# Code example

You can refer to an example How-to-notebook showing how to pass parameters for different embeddings drift detection methods:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_calculate_embeddings_drift.ipynb" %}

# Embedding drift detection methods

Currently 4 embeddings drift detection methods are available. You can specify the method using the `drift_method` parameter:

```python
from evidently.metrics.data_drift.embedding_drift_methods import model
report = Report(metrics = [
    EmbeddingsDriftMetric('small_subset', 
                          drift_method = model()
                         )
])
```
