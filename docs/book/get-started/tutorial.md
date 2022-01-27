# Getting Started Tutorial

In this tutorial, we will use Evidently to generate profiles and visual reports on data drift and model performance. You can reproduce the steps in Jupyter notebooks or Colab. 

We suggest going through this tutorial once to understand the key tool functionality on a toy dataset. Once you’ve completed it, you can further explore more advanced features such as customization and setting up real-time monitoring. 

To complete the tutorial, you need basic knowledge of Python and familiarity with notebook environments. You should be able to complete it in under 10 minutes.

If you prefer a **video** version, here is a **10-min Quick Start** on how to generate Data and Target Drift reports and JSON profiles in the Jupyter notebook.

{% embed url="https://www.youtube.com/watch?v=g0Z2e-IqmmU&ab_channel=EvidentlyAI" %}

In this tutorial, we will go through the following steps for Jupyter notebook and Colab:
* Install Evidently
* Prepare the data
* Understand output formats
* Generate data drift dashboards 
* Generate prediction drift dashboards 
* Generate model performance dashboards  
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

After installing the tool, import `evidently` and the required tabs. Each tab corresponds to a specific report type. In this example, you'd use 3 different reports. 

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import (
    DataDriftTab,
    CatTargetDriftTab,
    ProbClassificationPerformanceTab,
)
```
{% hint style="info" %}
**What is included in the reports?** You can explore [this section](../reports) to understand the components, statistical tests and metrics included in each report by default.
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

![Part of the Data Drift Report.](.gitbook/assets/evidently\_github.png)

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

## 6. Generate the Model Performance dashboard

If you have the labels, you can also generate the model performance dashboard. It helps explore the model quality and understand the errors.




{% hint style="info" %}
**Large reports might take time to load.** In this simple example, we work with a small dataset, so the report should appear quickly. If you use a larger dataset, the report might take time to show, since it contains the data needed for interactive plots. The size limitation depends on your infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. 
{% endhint %}


## 7. Modify the dashboard

Model Performance reports can be generated for a **single** dataset, with no comparison performed. You can simply pass a single `DataFrame`or `csv` file.&#x20;

The data structure is different depending on the report type.

* For the **Data Drift** report, include the input features only.&#x20;
* For the **Target Drift** reports, include the input features and the column with the Target and/or the Prediction.&#x20;
* For the **Model Performance** reports, include the input features, the column with the Target, and the column with the Prediction.

If you include more columns than needed for a given report, they will be ignored. &#x20;

## Decide on the output format

Calculation results can be available in one of the following formats:

* An interactive visual **Dashboard** displayed inside the Jupyter notebook.
* An exportable **HTML report**. The same as dashboard, but standalone.&#x20;
* A **JSON profile** with a summary of metrics and statistical test results.&#x20;

**Dashboards** are best for ad-hoc analysis, debugging, and team sharing.

**Profiles** are best for integration into prediction pipelines or with external visualization tools.

You can proceed to work with Jupyter notebook or generate JSON profiles and HTML reports via Terminal.

| Output format    | Jupyter notebook | Terminal |
| ---------------- | ---------------- | -------- |
| **Dashboard**    | +                | -        |
| **HTML report**  | +                | +        |
| **JSON profile** | +                | +        |

All options are described below.

## Jupyter notebook&#x20;

### Generating dashboards and HTML reports

Note about column mapping. We do not perform any further data preparation



`Dashboard` generates an interactive report that includes the selected `Tabs`.&#x20;

## 4. Understand which other Tabs and Sections are available

You can choose the following **Tabs**:

* `DataDriftTab` to estimate the **data drift**
* `NumTargetDriftTab` to estimate **target drift** for the numerical **** target&#x20;
* `CatTargetDriftTab` to estimate **target drift** for the categorical target&#x20;
* `RegressionPerformanceTab` to explore the **performance** of a regression model
* `ClassificationPerformanceTab` to explore the **performance** of a classification **** model
* `ProbClassificationPerformanceTab` to explore the **performance** of a probabilistic classification model&#x20;

To generate the **Data Drift** report and save it as HTML, run:

## 4. Understand which other Tabs and Sections are available


If you get a security alert, press "trust html". The HTML report does not open automatically. To explore it, you should open it from the destination folder.

To generate the **Classification Model Performance report**, run:

```python
classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
classification_performance_report.show()
```

For **Probabilistic Classification Model Performance report**, run:

```python
classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab])
classification_performance_report.calculate(reference_data, current_data, 
    column_mapping=column_mapping)
classification_performance_report.show()
```

For a **classification reports** from a single `DataFrame`, run:

```python
classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab])
classification_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping) 
classification_single_model_performance.show()
```

For a **probabilistic classification report** from a single `DataFrame`, run:

```python
prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab])
prob_classification_single_model_performance.calculate(reference_data, None, 
    column_mapping=column_mapping)
prob_classification_single_model_performance.show()
```

{% hint style="info" %}
**It might take some time to display the report. If it does not show, this might be due to the dataset size.** The dashboard contains the data necessary to generate interactive plots and can become large. The limitation depends on infrastructure. In this case, we suggest applying sampling to your dataset. In Jupyter notebook, that can be done directly with pandas. You can also generate a JSON profile instead 👇🏼
{% endhint %}


--- adapt 

## Google Colab, Kaggle Kernel, Deepnote

You can run `evidently` in [Google Colab](https://colab.research.google.com), [Kaggle Notebook](https://www.kaggle.com/code) and [Deepnote](https://deepnote.com).

First, install `evidently`. Run the following command in the notebook cell:

```
!pip install evidently
```

There is no need to enable nbextension for this case. Evidently uses an alternative way to display visuals in the hosted notebooks.

To build a `Dashboard` or a `Profile` simply repeat the steps described in the previous paragraph. For example, to build the **Data Drift** dashboard, run:

```
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)

iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:], column_mapping = None)
```

To display the dashboard in the Google Colab, Kaggle Kernel, Deepnote, run:

```
iris_data_drift_report.show()
```

The `show()` method has the argument `mode`, which can take the following options:

* **auto** - the default option. Ideally, you will not need to specify the value for `mode` and use the default. But, if it does not work (in case we failed to determine the environment automatically), consider setting the correct value explicitly.
* **nbextension** - to show the UI using nbextension. Use this option to display dashboards in Jupyter notebooks (it should work automatically).
* **inline** - to insert the UI directly into the cell. Use this option for Google Colab, Kaggle Kernels and Deepnote. For Google Colab, this should work automatically, for **Kaggle Kernels** and **Deepnote** the option should be specified explicitly.

Understand all reports.

You can later refere to the Dashboard and Profile pages that sum up all the functionality.

Join Discord
