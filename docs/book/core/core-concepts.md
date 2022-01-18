# Core concepts

## **Reference and Current Data**

The primary use for Evidently is the comparison between two datasets. These datasets are model application logs. They can include model input features, predictions, and/or actuals (true labels).&#x20;

* **Reference** dataset serves as a basis for the comparison.
* **Current (Production)** dataset is the dataset that is compared to the first.&#x20;

![](../.gitbook/assets/two_datasets_classification.png)

In practice, you can use it in different combinations:

* **Training vs Test**&#x20;
  * To compare the model performance on a hold-out **Test** to the **Training**.&#x20;
  * Pass the training data as "Reference", and test data as "Current".
* **Production vs Training**&#x20;
  * To compare the **Production** model performance to the **Training** period.&#x20;
  * Pass the training data as "Reference", and production data as "Current".
* **Current perfromance vs Past**&#x20;
  * To compare the **Current** production performance to an **Earlier** period.&#x20;
  * For example, to compare the last week to the previous week or month.&#x20;
  * Pass the earlier data as "Reference", and newer data as "Current".&#x20;
* **Compare any two models or datasets**&#x20;
  * For example, to estimate the historical drift for different windows in your training data or to compare how two models perform in the test.&#x20;
  * Pass the first dataset as "Reference", and the second as "Current".&#x20;

You can generate a Performance report for a **single dataset**. Pass it as "Reference". In other cases, we need two datasets to run the statistical tests. &#x20;

Right now, you cannot choose a custom name for your dataset.&#x20;

**Note:** earlier, we referred to the second dataset as "Production". You might notice that in some older examples. &#x20;

## Reports

![](../.gitbook/assets/image%20(2).png)

Evidently includes a set of pre-built Reports. Each of them addresses a specific aspect of the data or model performance.&#x20;

Evidently calculates a number of metrics and statistical tests in each report, and generates interactive visualizations.

Currently, you can choose between 6 different [**Report**](reports/) **** types.  &#x20;

The calculation results can be available in one of the following formats:&#x20;

* An interactive visual **Dashboard** displayed inside the Jupyter notebook.
* An **HTML report.** Same as dashboard, but available as a standalone file.&#x20;
* A **JSON profile.** A summary of the metrics, the results of statistical tests, and simple histograms.&#x20;

Right now, you cannot change the composition of the report, e.g. to add or exclude metrics. Reports are pre-built to serve as good enough defaults. We expect to add configurations in the future.

## Dashboards

To display the output in the Jupyter notebook, you can create a visual **Dashboard.**&#x20;

To specify which analysis you want to perform, you should select a **Tab** (for example, a Data Drift tab)**.** You can combine several tabs in a single Dashboard (for example, Data Drift and Prediction Drift). Each tab will contain a combination of metrics, interactive plots, and tables for a chosen [Report](reports/) type.&#x20;

You can also save the Dashboard as **a standalone HTML file.** You can group several Tabs in one file.&#x20;

You can generate HTML files from Jupyter notebook or using Terminal.&#x20;

**This option helps visually explore and evaluate model performance and errors.**

## JSON Profiles

To get the calculation results as a JSON file, you should create a **Profile**.

To specify which analysis you want to perform, you should select a **Section**. You can combine several sections together in a single Profile. Each section will contain a summary of metrics, results of statistical tests, and simple histograms that correspond to the chosen [Report](reports/) type.&#x20;

You can generate profiles from Jupyter notebook or using Terminal.&#x20;

**This option helps integrate Evidently in your prediction pipelines:** for example, you can use Evidently to calculate drift, and then log the needed metrics externally (e.g. using [Mlflow](step-by-step-guides/integrations/evidently-+-mlflow.md)).



## &#x20;
