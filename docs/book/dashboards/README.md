---
description: How to generate visual reports on data and model performance.
---

# Dashboards 

`Dashboard` helps visually explore and evaluate the data and model performance.

You can generate dashboards in certain notebook environments (see full list below) or using the command-line interface. The dashboards can be displayed directly in the notebook, or exported as a separate HTML file. 

To specify which analysis you want to perform, you should select a `Tab` (for example, a `DataDriftTab`). You can combine several tabs in a single Dashboard (for example, for Data Drift and Prediction Drift). Each tab contains a combination of metrics, interactive plots, and tables for a chosen [Report](../reports/) type.

For a step-by-step introduction, we recommend you to go first through the [Getting Started tutorial](../get-started/tutorial.md).

## Supported environments

You can generate the dashboards in **Jupyter notebooks**. 

{% hint style="info" %}
If you want to display the dashboards in Jupyter notebook, make sure you [installed](../get-started/install-evidently.md) the Jupyter **nbextension**.
{% endhint %}

You can also use **Google Colab**, **Kaggle Kernel**, or **Deepnote**. Review the related section for some details. 

If you use **Jupyter Lab**, you won't be able to explore the reports inside a Jupyter notebook. However, the report generation in a separate HTML file will work correctly.
