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
| `drift_method=model` <br>(Default) | <ul><li>A binary classifier model to distinguish between embeddings in “current” and “reference” distributions.</li><li>Returns **ROC AUC** as a `drift_score`.</li><li>Drift detected when `drift_score` > `threshold` or when `drift_score` > ROC AUC of the random classifier at a set `quantile_probability`.</li><li>Default threshold: 0.55 (ROC AUC). </li><li>Default quantile_probability: 0.95. Applies when bootstrap is True; default True if <= 1000 objects.</li></ul> |
| `drift_method=ratio` | <ul><li>Computes the distribution drift between individual embedding components using any of the tabular numerical drift detection methods available in Evidently. </li><li>Default tabular drift detection method: Wasserstein distance, with the 0.1 threshold.</li><li>Returns the **share of drifted embeddings** as `drift_score`. </li><li>Drift detected when `drift_score` > `threshold` </li><li>Default threshold: 0.2 (share of drifted embedding components).</li></ul> |
| `drift_method=distance` | <ul><li>Computes the distance between average embeddings in “current” and “reference” datasets using a specified distance metric (euclidean, cosine, cityblock, chebyshev). Default: `euclidean`. </li><li>Returns the **distance metric value** as `drift_score`.</li><li>Drift detected when drift_score > threshold or when `drift_score` > obtained distance in reference at a set `quantile_probability`.</li><li>Default threshold: 0.2 (relevant for Euclidean distance).</li><li>Default quantile_probability: 0.95. Applies when bootstrap is True; default True if <= 1000 objects.</li></ul> |
| `drift_method=mmd` | <ul><li>Computes the Maximum Mean Discrepancy (MMD)</li><li>Returns the **MMD value** as a `drift_score`</li><li>Drift detected when `drift_score` > `threshold` or when `drift_score` >  obtained MMD values in reference at a set `quantile_probability`.</li><li>Default threshold: 0.015 (MMD). </li><li>Default quantile_probability: 0.95. Applies when bootstrap is True; default True if <= 1000 objects.</li></ul> |

If you specify an embedding drift detection method but do not pass additional parameters, defaults will apply. 

You can also specify parameters for any chosen method. Since the methods are different, each has a different set of parameters. Note that you should pass the parameters **directly to the chosen drift detection method**, not to the Metric. 

## Model-based (“model”) 

```python
report = Report(metrics = [
    EmbeddingsDriftMetric('small_subset', 
                          drift_method = model(
                              threshold = 0.55,
                              bootstrap = None,
                              quantile_probability = 0.05,
                              pca_components = None,
                          )
                         )
])
```
| threshold | Sets the threshold for drift detection (ROC AUC). Drift is detected when drift_score > threshold. <br>Applies when bootstrap != True.<br>Default: 0.55. |
| bootstrap (optional)  | Boolean parameter (True/False) to determine whether to apply statistical hypothesis testing. <br>If applied, the ROC AUC of the classifier is compared to the ROC AUC of the random classifier at a set percentile. The calculation is repeated 1000 times with randomly assigned target class probabilities. This produces a distribution of random roc_auc scores with a mean of 0,5. We then take the 95th percentile (default) of this distribution and compare it to the ROC-AUC score of the classifier. If the classifier score is higher, data drift is detected.<br>Default: True if <= 1000 objects, False if > 1000 objects. |
| quantile_probability (optional)  | Sets the percentile of the possible ROC AUC values of the random classifier to compare against. <br>This applies when bootstrap is True.<br>Default: 0.95 |
| pca_components (optional)  | The number of PCA components. If specified, dimensionality reduction will be applied to project data to n-dimensional space based on the number of pca_components.<br>Default: None. |
