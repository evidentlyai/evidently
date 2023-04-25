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

| Embeddings drift detection method | Description and default |
|---|---|
| `drift_method=model` <br>(Default) | <ul><li>A binary classifier model to distinguish between embeddings in “current” and “reference” distributions.<li/li>Returns ROC AUC as a drift_score.<li/li>Drift detected when drift_score > threshold or when  drift_score > quantile_probability.<br>Default threshold: 0.55 (ROC AUC). <li/li>>Default quantile_probability: 0.95. Applies when bootstrap is True; default True if <= 1000 objects.</li></ul> |
| `drift_method=ratio` | <ul><li>Computes the distribution drift between individual embedding components using any of the tabular numerical drift detection methods available in Evidently. <li/li>Default tabular drift detection method: Wasserstein distance, with the 0.1 threshold. <br>Returns the share of drifted embeddings as drift_score. <li/li>Drift detected when drift_score > threshold  <li/li>Default threshold: 0.2 (share of drifted embeddings)</li></ul> |
| `drift_method=distance` | <ul><li>Computes the distance between average embeddings in “current” and “reference” datasets using a specified distance metric (euclidean, cosine, cityblock, chebyshev). Default: euclidean distance. <br>Returns the distance metric value as drift_score.<li/li>Drift detected when drift_score > threshold or when  drift_score > quantile_probability.<li/li>Default threshold: 0.2 (relevant for Euclidean distance).<li/li>>Default quantile_probability: 0.95. Applies when bootstrap is True; default True if <= 1000 objects.</li></ul> |
| `drift_method=mmd` | <ul><li>Computes the Maximum Mean Discrepancy (MMD) <br>Returns the MMD value as a drift_score<br>Drift detected when drift_score > threshold or when  drift_score > quantile_probability.<br>Default threshold: 0.015 (MMD). <li/li>Default quantile_probability: 0.95. Applies when bootstrap is True; default True if <= 1000 objects.</li></ul> |
