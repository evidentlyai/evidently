---
description: Sample notebooks and tutorials
---

# Examples

## Sample notebooks

Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box. 

Title| Jupyter notebook | Colab notebook | Contents
--- | --- | --- | --- 
Evidently Test Presets| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_test_presets.ipynb) | [link](https://colab.research.google.com/drive/15YIqTWbjzGHRIvxrP7HxwtvBCFgbNIps)| All pre-built Test Suites for Data Drift, Data Stability, Data Quality, NoTargetPerformance, Regression Performance, Classification Performance.    
Evidently Tests| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_tests.ipynb) | [link](https://colab.research.google.com/drive/1p9bgJZDcr_NS5IKVNvlxzswn6er9-abl) | All individual tests (50+) that one can use to create a custom Test Suite.
Evidently Metric Presets| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_metric_presets.ipynb) | [link](https://colab.research.google.com/drive/1-0-itoET4dQHo8dcoC0fKZ5VhugliLxj) | All pre-built Reports for Data Drift, Target Drift, Data Quality, Regression Performance, Classification Performance.     
Evidently Metrics| [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/evidently_metrics.ipynb) | [link](https://colab.research.google.com/drive/1c7HQz920Q-BPazDOujL4PgckuKIzFebn) | All individual metrics (30+) that one can use to create a custom Report.

## Tutorials

To better understand potential use cases for Evidently (such as model evaluation and monitoring), refer to the **detailed tutorials** accompanied by the blog posts.

Title | Jupyter notebook | Colab notebook | Blog post | Data source 
--- | --- | --- | --- | --- 
Monitor production model decay | [link](../../../examples/data_stories/bicycle_demand_monitoring.ipynb) | [link](https://colab.research.google.com/drive/1xjAGInfh_LDenTxxTflazsKJp_YKmUiD) | [How to break a model in 20 days. A tutorial on production model analytics.](https://evidentlyai.com/blog/tutorial-1-model-analytics-in-production) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Compare two models before deployment | [link](../../../examples/data_stories/ibm_hr_attrition_model_validation.ipynb) | [link](https://colab.research.google.com/drive/12AyNh3RLSEchNx5_V-aFJ1_EnLIKkDfr) | [What Is Your Model Hiding? A Tutorial on Evaluating ML Models.](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition) | HR Employee Attrition: [link](https://www.kaggle.com/pavansubhasht/ibm-hr-analytics-attrition-dataset)
Evaluate and visualize historical drift | [link](../../../examples/integrations/mlflow_logging/historical_drift_visualization.ipynb) | [link](https://colab.research.google.com/drive/12AyNh3RLSEchNx5_V-aFJ1_EnLIKkDfr) | [How to detect, evaluate and visualize historical drifts in the data.](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Create a custom report (tab) with PSI widget for drift detection | [link](../../../examples/data_stories/california_housing_custom_PSI_widget_and_tab.ipynb) | [link](https://colab.research.google.com/drive/1FuXId8p-lCP9Ho_gHeqxAdoxHRuvY9d0) | --- | California housing sklearn.datasets 


## Integrations

To see how to integrate Evidently in your prediction pipelines and use it with other tools, refer to the **integrations**.&#x20;

{% content-ref url="../integrations/" %}
[integrations](../integrations/)
{% endcontent-ref %}
