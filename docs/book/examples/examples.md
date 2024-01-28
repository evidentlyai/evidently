---
description: Sample notebooks and tutorials
---

# Quick start

This is the best place to start. 

Title| Code example | Guide 
-- | -- | --
Quickstart for Reports and Test Suites| [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/getting_started_tutorial.ipynb)<br> [Colab](https://colab.research.google.com/drive/1j0Wh4LM0mgMuDY7LQciLaUV4G1khB-zb)| [Tutorial](https://docs.evidentlyai.com/get-started/tutorial)
Quickstart for ML Monitoring| [Python script](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/get_started_monitoring.py) | [Tutorial](https://docs.evidentlyai.com/get-started/tutorial-monitoring)

# Sample notebooks

Simple examples show different Metrics, Tests and Presets. Head to Colab examples to see the pre-rendered visuals.

Title| Code example | Contents
-- | -- | --
Evidently Test Presets| [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_test_presets.ipynb)<br> [Colab](https://colab.research.google.com/drive/15YIqTWbjzGHRIvxrP7HxwtvBCFgbNIps)| Pre-built Test Suites on tabular data: <ul><li>Data Drift</li><li>Data Stability</li><li> Data Quality</li><li>NoTargetPerformance</li><li>Regression</li><li>Classification (Multi-class, binary, binary top-K)</li></ul>    
Evidently Tests| [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_tests.ipynb) <br> [Colab](https://colab.research.google.com/drive/1p9bgJZDcr_NS5IKVNvlxzswn6er9-abl) | <ul><li>All individual Tests (50+) that one can use to create a custom Test Suite. Tabular data examples.</li><li>How to set test conditions and parameters.</li></ul>
Evidently Metric Presets| [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_metric_presets.ipynb) <br> [Colab](https://colab.research.google.com/drive/1-0-itoET4dQHo8dcoC0fKZ5VhugliLxj) | All pre-built Reports: <ul><li>Data Drift</li><li>Target Drift</li><li>Data Quality</li><li>Regression</li><li>Classification</li></ul>     
Evidently Metrics| [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_metrics.ipynb) <br> [Colab](https://colab.research.google.com/drive/1c7HQz920Q-BPazDOujL4PgckuKIzFebn) | <ul><li>All individual metrics (30+) that one can use to create a custom Report.</li><li>How to set simple metric parameters.</li></ul>

For more examples showing specific features, including text data support, head to the "How to" examples.

{% content-ref url="../how-to-guides/README.md" %}
[How to guides](../how-to-guides/README.md)
{% endcontent-ref %}

# Tutorials

To better understand the Evidently use cases, refer to the **detailed tutorials** accompanied by the blog posts.

Title | Code example | Blog post 
--- | --- | --- 
Understand ML model decay in production (regression example) | [Jupyter notebook](../../../examples/data_stories/bicycle_demand_monitoring.ipynb) | [How to break a model in 20 days. A tutorial on production model analytics.](https://evidentlyai.com/blog/tutorial-1-model-analytics-in-production) 
Compare two ML models before deployment (classification example) | [Jupyter notebook](../../../examples/data_stories/ibm_hr_attrition_model_validation.ipynb) | [What Is Your Model Hiding? A Tutorial on Evaluating ML Models.](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition) 
Evaluate and visualize historical data drift | [Jupyter notebook](../../../examples/integrations/mlflow_logging/historical_drift_visualization.ipynb) | [How to detect, evaluate and visualize historical drifts in the data.](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) 
Monitor NLP models in production | [Colab](https://colab.research.google.com/drive/15ON-Ub_1QUYkDbdLpyt-XyEx34MD28E1) | [Monitoring NLP models in production: a tutorial on detecting drift in text data](https://www.evidentlyai.com/blog/tutorial-detecting-drift-in-text-data) 
Create ML model cards |[Jupyter notebook](https://github.com/evidentlyai/community-examples/tree/main/tutorials/How_to_create_an_ML_model_card.ipynb) | [A simple way to create ML Model Cards in Python](https://www.evidentlyai.com/blog/ml-model-card-tutorial) 
Use descriptors to monitor text data | [Jupyter notebook](https://github.com/evidentlyai/community-examples/tree/main/tutorials/How_to_add_a_custom_text_descriptor.ipynb) | [Monitoring unstructured data for LLM and NLP with text descriptors](https://www.evidentlyai.com/blog/unstructured-data-monitoring)|  

You can find more examples in the [Community Examples](https://github.com/evidentlyai/community-examples) repository. 

## Integrations

To see how to integrate Evidently in your prediction pipelines and use it with other tools, refer to the **integrations**.

{% content-ref url="../integrations/evidently-integrations.md" %}
[integrations/evidently-integrations.md](../integrations/evidently-integrations.md)
{% endcontent-ref %}
