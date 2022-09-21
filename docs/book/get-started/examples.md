---
description: Sample notebooks and tutorials
---

# Examples

## Sample notebooks, new API

Examples of reports and tests using new API (version 0.1.57 and above):  

Contents| Jupyter notebook | Colab notebook | Data source 
--- | --- | --- | --- 
All tests and tests presets | [link](https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/tests_and_test_presets.ipynb) | [link](N/A) | Iris, Breast cancer, California housing from sklearn.datasets; Adult dataset from openml 

## Sample notebooks

Here you can find simple examples on toy datasets to quickly explore what Evidently can do right out of the box. Each example shows how to create a default Evidently dashboard, a JSON profile and an HTML report.

Report | Jupyter notebook | Colab notebook | Data source 
--- | --- | --- | --- 
Data Drift + Categorical Target Drift (Multiclass) | [link](../../../examples/sample_notebooks/multiclass_target_and_data_drift_iris.ipynb) | [link](https://colab.research.google.com/drive/1Dd6ZzIgeBYkD_4bqWZ0RAdUpCU0b6Y6H) | Iris plants sklearn.datasets 
Data Drift + Categorical Target Drift (Binary) | [link](../../../examples/sample_notebooks/binary_target_and_data_drift_breast_cancer.ipynb) | [link](https://colab.research.google.com/drive/1gpzNuFbhoGc4-DLAPMJofQXrsX7Sqsl5) | Breast cancer sklearn.datasets
Data Drift + Numerical Target Drift | [link](../../../examples/sample_notebooks/numerical_target_and_data_drift_california_housing.ipynb) | [link](https://colab.research.google.com/drive/1TGt-0rA7MiXsxwtKB4eaAGIUwnuZtyxc) | California housing sklearn.datasets 
Regression Performance | [link](../../../examples/sample_notebooks/regression_performance_bike_sharing_demand.ipynb) | [link](https://colab.research.google.com/drive/1ONgyDXKMFyt9IYUwLpvfxz9VIZHw-qBJ) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
Classification Performance (Multiclass) | [link](../../../examples/sample_notebooks/classification_performance_multiclass_iris.ipynb) | [link](https://colab.research.google.com/drive/1pnYbVJEHBqvVmHUXzG-kw-Fr6PqhzRg3) | Iris plants sklearn.datasets 
Probabilistic Classification Performance (Multiclass) | [link](../../../examples/sample_notebooks/probabilistic_classification_performance_multiclass_iris.ipynb) | [link](https://colab.research.google.com/drive/1UkFaBqOzBseB_UqisvNbsh9hX5w3dpYS) | Iris plants sklearn.datasets 
Classification Performance (Binary) | [link](../../../examples/sample_notebooks/classification_performance_breast_cancer.ipynb) | [link](https://colab.research.google.com/drive/1b2kTLUIVJkKJybYeD3ZjpaREr_9dDTpz) | Breast cancer sklearn.datasets
Probabilistic Classification Performance (Binary) | [link](../../../examples/sample_notebooks/probabilistic_classification_performance_breast_cancer.ipynb) | [link](https://colab.research.google.com/drive/1sE2H4mFSgtNe34JZMAeC3eLntid6oe1g) | Breast cancer sklearn.datasets
Data Quality | [link](../../../examples/sample_notebooks/data_quality_bike_sharing_demand.ipynb) | [link](https://colab.research.google.com/drive/1XDxs4k2wNHU9Xbxb9WI2rOgMkZFavyRd) | Bike sharing UCI: [link](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)

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
