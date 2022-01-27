# Getting Started Tutorial

In this tutorial, you will use Evidently to generate profiles and visual reports on data and target drift.

We suggest going through this tutorial once to understand the key tool functionality on a toy dataset. Once you’ve completed it, you can further explore more advanced features such as customization and setting up real-time monitoring. 

To complete the tutorial, you need basic knowledge of Python and familiarity with notebook environments. You should be able to complete it in under 10 minutes.

You can reproduce the steps in Jupyter notebooks or Colab on your own, or explore the sample notebooks:

{% embed url="https://colab.research.google.com/drive/1Dd6ZzIgeBYkD_4bqWZ0RAdUpCU0b6Y6H" %}

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/multiclass_target_and_data_drift_iris.ipynb" %}

If you prefer a **video** version, here is a **10-min Quick Start** on how to generate Data and Target Drift reports and JSON profiles in the Jupyter notebook.

{% embed url="https://www.youtube.com/watch?v=g0Z2e-IqmmU&ab_channel=EvidentlyAI" %}

In this tutorial, you will go through the following steps:
* Install Evidently
* Prepare the data
* Generate data drift dashboards 
* Generate prediction drift dashboards 
* Generate JSON profiles 

## 1. Install Evidently

### MAC OS and Linux

To install Evidently using the pip package manager, run:

```bash
$ pip install evidently
```
If you want to see reports inside a Jupyter notebook, you need to also install the Jupyter **nbextension**. After installing `evidently`, run the **two following commands** in the terminal from the Evidently directory.

To install jupyter nbextension, run:

```
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```

To enable it, run:

```
$ jupyter nbextension enable evidently --py --sys-prefix
```

That's it!

### Google Colab, Kaggle Kernel, Deepnote


To install `evidently`, run the following command in the notebook cell:

```
!pip install evidently
```
### Windows

Unfortunately, building reports inside a **Jupyter notebook** is **not yet possible** for Windows. You can still install Evidently and use it to generate reports as a separate HTML file.

To install Evidently, run:

```bash
$ pip install evidently
```

## 2. Import Evidently

After installing the tool, import `evidently` and the required tabs. Each tab corresponds to a specific report type. In this example, you'd use 2 different reports. 

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab, CatTargetDriftTab
```
{% hint style="info" %}
**What is included in the reports?** You can explore [Reports section](../reports) in documentation to understand the components, statistical tests and metrics included in each report by default.
{% endhint %}

## 3. Prepare the data

In this example, you will work with `pandas.DataFrames`. For simplicity, we take a toy dataset. In the real use case, you can swap it for the real logs with input data, model predictions and true lables, if available.  

Create a `Pandas DataFrame` with the dataset to analyze:

```python
iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```
To evaluate things like data drift, you would need two datasets to perform a comparison. The first one is the baseline: this can often be the data used in training. We call it **reference** data. The second dataset is the **current** production data. 

You can prepare two separate datasets with identical schema. You can also proceed with one dataset but explicitly **identify rows** that refer to reference and production data. That is what we do now to generate the first report. 

Let us split the data in half, and treat the first 75 rows as reference, and the remaining as the current data.

{% hint style="info" %}
**Column_mapping.** In this simple example, we can directly display the dashboard in the next step. In other cases, you might need to add column_mapping dictionary to help the tool process the input data correctly. For example, if you have encoded categorical features, or need to point to the name of the target column. Consult this section ADD LINK for help.
{% endhint %}

## 4. Generate the Data Drift dashboard

![Part of the Data Drift Report.](../.gitbook/assets/evidently\_github.png)

Data drift dashboard helps visualize the change in the input data distributions, and see the results of the statistical tests. This helps understand if the data has shifted and serve as proxy to evaluate model performance, even if you do not have the true labels yet.   

To generate the Data Drift dashboard, run:

```python
iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
iris_data_drift_report.calculate(iris_frame[:75], iris_frame[75:], 
    column_mapping = None)
iris_data_drift_report.show()
```
If you use Jupyter notebook or Colab, the report will appear directly in the notebook. 

You can also save it as an HTML file externally. If you get a security alert, press "trust html".

```
iris_data_drift_report.save("reports/my_report.html")
```

To see the report, go to the specified directory and open the file. 

{% hint style="info" %}
**This might work slightly differently in other notebook environments.** In some environments, like Jupyter lab, you might not be able to display the dashboard directly in the cell. In this case, try exporting the file as an HTML. Consult this section ADD LINK to check the supported environments. In other notebooks like Kaggle and Deepnote, you might need to explicitly add an argument: iris_data_drift_report.show(mode='inline'). Consult this section ADD LINK for help.
{% endhint %}

## 5. Generate the Target Drift dashboard

Next, you will generate a Target Drift dashboard.

There are two use cases for this report. If you have the model predictions, you can use this report to evaluate the **prediction drift**. This will help see if there is a statistically significant change in the model outputs, for example, if a certain category is predicted more frequently. If you have the true labels, you can use the report to evaluate **target drift**. This will help see if the concept behind the model has evolved, for example, if a certain label in fact appears more frequently. 

In the toy dataset, we already have the true labels. Let us treat it as such, and add the target column to the initial dataset.

```python
iris_frame['target'] = iris.target
```
This toy dataset is meant to perform a classification task, and the target is categorical. You should use the Categorical Target Drift report.

To generate the Target Drift report, run:

```python
iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab, CatTargetDriftTab])
iris_data_and_target_drift_report.calculate(iris_frame[:75], iris_frame[75:], 
    column_mapping=None)
iris_data_and_target_drift_report.show()
```

{% hint style="info" %}
**Large reports might take time to load.** In this simple example, we work with a small dataset, so the report should appear quickly. If you use a larger dataset, the report might take time to show, since it contains the data needed for interactive plots. The size limitation depends on your infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. 
{% endhint %}

## 6. Get a short version of the dashboard

You might have noticed that the Target Drift dashboard is quite long and includes a lot of visualizations to explore relationships between the features and the target. You don't always need them all. 

A complete dashboard corresponds to the verbose_level=1.

To get a shorter version of a dashboard, set the verbose_level to 0.

```python
iris_target_drift_dashboard = Dashboard(tabs=[CatTargetDriftTab(verbose_level=1)])
iris_target_drift_dashboard.calculate(iris_frame[:75], iris_frame[75:], column_mapping=None)
iris_target_drift_dashboard.show()
```

{% hint style="info" %}
**Report Customization.** You can make other changes to the default Evidently reports, for example to change the statistical test or other options, or add a custom widgets. To explore this advanced functionality, head to [Customization](../customization) section.  
{% endhint %}

## 7. Other dashboards

There are more report types!

If you have both the predictions and true labels, you can also generate the model performance dashboard. It helps explore the model quality and understand the errors. In our case, we could have generated a Classification Performance or Probabilistic Classification Performance reports.

We skip this step in the quick tutorial. It would have required us to train a model and generate the predictions we can compare with true labels. You can instead explore the sample notebooks in the [examples](../examples) section that do just that.

If you have a regression task, Evidently has matching dashboard tabs for Numerical Target Drift and Regression Model Performance. 

We plan to add more report types in the future. 

{% hint style="info" %}
**Dashboards documentation.** To see the complete guide to using Dashboards for future reference, you can always consult [Dashboards](../dashboards) section of documentation.  
{% endhint %}

## 8. Generate JSON profiles

Interactive reports are best for visual analysis, model performance debugging, or sharing with the team. However, they are not that convenient if you want to intgerate Evidently calculations in the prediction pipeline. 

In this case, we suggest using JSON profiles. They help profile the data and model performance and get the summary of metrics and simple historgrams as a JSON. You can log it for future analysis, or design a conditional workflow based on the result of the check (e.g. to trigger alert, retraining, or generate a visual report). 

Profiles behave very similarly to the dashboards. Just like `Dashboards` have `Tabs`, `Profiles` have `Sections`. 

First, you should import the required Profiles.

```python
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection, CatTargetDriftProfileSection
```

To generate the **Data Drift** and the **Categorical Target Drift** profiles, run:

```python
iris_target_and_data_drift_profile = Profile(sections=[DataDriftProfileSection, CatTargetDriftProfileSection])
iris_target_and_data_drift_profile.calculate(iris_frame[:75], iris_frame[75:], column_mapping=None) 
iris_target_and_data_drift_profile.json() 
```

The JSON profile will show directly in the notebook. 

There is also CLI interface ADD LINK in case you want to generate HTML dashboards or JSONs from the Terminal without opening the notebook.

{% hint style="info" %}
**JSON profiles documentation.** To see the complete guide to using JSON profiles for future reference, you can always consult [Profiling](../profiling) section of documentation.  
{% endhint %}

## What else is there?

While you can treat JSON profile as a "text version" of the report to look at, it is intented for use with other tools. We suggest to explore [Integrations](../integrations) section of documentation to see how you can use it in your machine learning workflow with tools like MLflow and Airflow to log and profile the models and data. 

If you have a deployed ML service and want to collect data and model metrics on top of the live data stream, you can explore the [intgeration with Grafana and Prometheus](../integrations/evidently_and_grafana.md). In this case, Evidently acts as a monitoring service, and you can configure the options to design more sophisticated logic as such size of the reference windows, moving reference, etc. It also comes with pre-built Grafana dashboards that act as a versions of Evidently dashboards meant for real-time monitoring. 

Evidently is in active development, so expect things to change and evolve. You can subscribe to the [newsletter]() or follow our [releases on GitHub]() to stay updated about the latest functionality. 

## Join our Community!

We run a [Discord community](https://discord.gg/xZjKRaNp8b) to connect with our users and chat about ML in production topics. 

In case you have feedback or need help, just ask in Discord or open a GitHub is [GitHub](https://github.com/evidentlyai/evidently).
