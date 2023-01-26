---
description: Sample notebooks and tutorials
---

# Examples

## Sample notebooks

Simple examples on toy datasets to show what Evidently can do out of the box. Colab examples contain pre-rendered reports.

Title| Jupyter notebook | Colab notebook | Contents
--- | --- | --- | --- 
Evidently Test Presets| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_test_presets.ipynb) | [link](https://colab.research.google.com/drive/15YIqTWbjzGHRIvxrP7HxwtvBCFgbNIps)| All pre-built Test Suites: <ul><li>Data Drift</li><li>Data Stability</li><li> Data Quality</li><li>NoTargetPerformance</li><li>Regression</li><li>Classification (Multi-class, binary, binary top-K)</li></ul>    
Evidently Tests| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_tests.ipynb) | [link](https://colab.research.google.com/drive/1p9bgJZDcr_NS5IKVNvlxzswn6er9-abl) | <ul><li>All individual tests (50+) that one can use to create a custom Test Suite.</li><li>How to set simple test parameters.</li></ul>
Evidently Metric Presets| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_metric_presets.ipynb) | [link](https://colab.research.google.com/drive/1-0-itoET4dQHo8dcoC0fKZ5VhugliLxj) | All pre-built Reports: <ul><li>Data Drift</li><li>Target Drift</li><li>Data Quality</li><li>Regression</li><li>Classification</li></ul>     
Evidently Metrics| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_metrics.ipynb) | [link](https://colab.research.google.com/drive/1c7HQz920Q-BPazDOujL4PgckuKIzFebn) | <ul><li>All individual metrics (30+) that one can use to create a custom Report.</li><li>How to set simple metric parameters.</li></ul>

## Tutorials

To better understand potential use cases for Evidently (such as model evaluation and monitoring), refer to the **detailed tutorials** accompanied by the blog posts.

Title | Jupyter notebook | Colab notebook | Blog post | Data source 
--- | --- | --- | --- | --- 
Monitor production model decay | [link](../../../examples/data_stories/bicycle_demand_monitoring.ipynb) | [link](https://colab.research.google.com/drive/1xjAGInfh_LDenTxxTflazsKJp_YKmUiD) | [How to break a model in 20 days. A tutorial on production model analytics.](https://evidentlyai.com/blog/tutorial-1-model-analytics-in-production) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Compare two models before deployment | [link](../../../examples/data_stories/ibm_hr_attrition_model_validation.ipynb) | [link](https://colab.research.google.com/drive/12AyNh3RLSEchNx5_V-aFJ1_EnLIKkDfr) | [What Is Your Model Hiding? A Tutorial on Evaluating ML Models.](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition) | HR Employee Attrition: [link](https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset)
Evaluate and visualize historical drift | [link](../../../examples/integrations/mlflow_logging/historical_drift_visualization.ipynb) | [link](https://colab.research.google.com/drive/12AyNh3RLSEchNx5_V-aFJ1_EnLIKkDfr) | [How to detect, evaluate and visualize historical drifts in the data.](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)


## Integrations

To see how to integrate Evidently in your prediction pipelines and use it with other tools, refer to the **integrations**.&#x20;

{% content-ref url="../integrations/" %}
[integrations](../integrations/)
{% endcontent-ref %}
