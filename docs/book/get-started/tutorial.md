# Get Started Tutorial

In this tutorial, you will use the Evidently open-source Python library to evaluate **data stability** and **data drift**. You will run batch checks on a toy dataset and generate visual reports and test suites.

The goal of the tutorial is to introduce the basic functionality of the tool. We recommend going through it once before exploring more advanced worfklows like adjusting test parameters, adding custom metrics or integrating the tool in the prediction pipelines.

To complete the tutorial, you need basic knowledge of Python and familiarity with notebook environments. You should be able to complete it in **about 10 minutes**.

You can reproduce the steps in Jupyter notebooks or Colab or open and run a sample notebook from the links below.  

Colab:
{% embed url="https://colab.research.google.com/drive/1j0Wh4LM0mgMuDY7LQciLaUV4G1khB-zb" %}

Jupyter notebook:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/getting_started_tutorial.ipynb" %}

Video version:
{% embed url="https://colab.research.google.com/drive/1j0Wh4LM0mgMuDY7LQciLaUV4G1khB-zb" %}

Yu will go through the following steps:
* Install Evidently
* Prepare the input data
* Generate a pre-built data drift report
* Customize the report 
* Run and customize data stability tests 


## 1. Install Evidently

### MAC OS and Linux

To install Evidently using the pip package manager, run:

```bash
$ pip install evidently
```
If you want to explore the plots inside a Jupyter notebook, you must install Jupyter **nbextension**. After installing `evidently`, run the **two following commands** in the terminal from the Evidently directory.

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

Unfortunately, building visual HTML reports inside a **Jupyter notebook** is **not yet possible** for Windows. You can still install Evidently and get the output as JSON or a separate HTML file.

To install Evidently, run:

```bash
$ pip install evidently
```

## 2. Import Evidently

After installing the tool, import `evidently` and the required components. In this tutorial, you will use several **test suites** and **reports**. Each of them corresponds to a specific type of analysis. 
 
You will also need to import `pandas`, `numpy`, and the toy `california_housing` dataset.

```python
import pandas as pd
import numpy as np

from sklearn.datasets import fetch_california_housing

from evidently import ColumnMapping

from evidently.report import Report
from evidently.metrics.base_metric import generate_column_metrics
from evidently.metric_preset import DataDriftPreset, TargetDriftPreset
from evidently.metrics import *

from evidently.test_suite import TestSuite
from evidently.tests.base_test import generate_column_tests
from evidently.test_preset import DataStabilityTestPreset,NoTargetPerformanceTestPreset
from evidently.tests import *
```

## 3. Prepare the data

In the example, you will work with a toy dataset. In practice, you should use the model prediction logs. They can include input data, model predictions, and true labels or actuals, if available. 

To prepare the data for analysis, create a `pandas.DataFrame`:

```python
data = fetch_california_housing(as_frame=True)
housing_data = data.frame
```

Rename one of the columns to “target” and create a “prediction” column. This way, the dataset will resemble the model application logs with known labels. 

```python
housing_data.rename(columns={'MedHouseVal': 'target'}, inplace=True)
housing_data['prediction'] = housing_data['target'].values + np.random.normal(0, 5, housing_data.shape[0])
```

Split the dataset by taking 5000 objects for **reference** and **current** datasets. This way, you get two samples to compare.  

```python
reference = housing_data.sample(n=5000, replace=False)
current = housing_data.sample(n=5000, replace=False)
```

The first **reference** dataset is the baseline. This is often the data used in model training or earlier production data. The second dataset is the **current** production data. Evidently will compare the current data to the reference. 
 
If you work with your own data, you can prepare two datasets with an identical schema like in this example or take a single dataset and explicitly identify rows for reference and current data.

{% hint style="info" %}
**Column mapping.** In this example, we directly proceed to analysis. In other cases, you might need to create a **ColumnMapping** object to help Evidently process the input data correctly. For example, you can point to the encoded categorical features or specify the name of the target column. Consult the [Column Mapping section](../tests-and-reports/column-mapping.md) section for help.
{% endhint %}

## 4. Get the Data Drift report

Evidently **reports** help explore and debug data and model quality. They calculate various metrics and generate a dashboard with rich visuals. 

To start, you can use **metric presets**. These are pre-built reports that group relevant metrics to evaluate a specific aspect of the model performance. 

Let’s generate the pre-built report for **Data Drift**. It will compare the distributions of the input model features and highlight which features has drifted. When you do not have ground truth labels or actuals, evaluting input data drift can help understand if an ML model still operates in a familiar environment.

To get the report, create a corresponding Report object, and list the preset you want to include. You will also point to the reference and current datasets created at the previous step: 

```python
report = Report(metrics=[
    DataDriftPreset(), 
])

report.run(reference_data=reference, current_data=current)
report
```

It will display the HTML report directly in the notebook. 

First, you can see the Data Drift summary.

![Data Drift report summary](../.gitbook/assets/tutorial/get_started_3_data_drift_summary-min.png)

If you click on individual features, it will show additional plots to explore. 

![Data Drift report details](../.gitbook/assets/tutorial/get_started_4_data_drift_expand-min.png)

**How does it work?** The data drift report compares the distributions of each feature in the two datasets. It [automatically picks](../reference/data-drift-algorithm.md) an appropriate statistical test or metric based on the feature type and volume. It then returns p-values or distances and visually plots the distributions. You can also [adjust the drift detection method or thresholds](../customization/options-for-statistical-tests.md), or pass your own.

{% hint style="info" %}
**Large reports might take time to load.** The example dataset is small, so the report should appear quickly. If you use a larger dataset, the report might take time to show. The size limitation depends on your infrastructure. In this case, we suggest applying sampling to your dataset before passing it to Evidently. You can do it with pandas.
{% endhint %}

{% hint style="info" %}
**Visualizations might work differently in other notebook environments**. For example, in the Jupyter lab, you won't be able to display the HTML directly in the cell. In this case, try exporting the file as HTML. In other notebooks like Kaggle and Deepnote, you might need to add an argument to display the report inline: iris_data_drift_report.show(mode='inline'). Consult [this section](../tests-and-reports/supported-environments.md) for help.
{% endhint %}

## 5. Customize the report

Evidently reports are very configurable. You can defined which metrics to include, and how to calculate them. 

To create a custom report, you need to list individual **metrics**. Evidently has dozens of metrics that help evaluate anything from descriptive feature statistics to the model quality. You can calculate metrics on the column level (e.g., mean value of a specific column), or dataset-level (e.g., share of drifted features in the whole dataset).  

In this example, you can list several metrics that evaluate different individual statistics for the defined column. 

```python
report = Report(metrics=[
    ColumnSummaryMetric(column_name='AveRooms'),
    ColumnQuantileMetric(column_name='AveRooms', quantile=0.25),
    ColumnDriftMetric(column_name='AveRooms')
])

report.run(reference_data=reference, current_data=current)
report
```
You will see a combined report that includes multiple metrics:

![Part of the custom report, ColumnSummaryMetric.](../.gitbook/assets/tutorial/get-started-column-summary_metric-min.png)

If you want to generate multiple column-level metrics, for example, to calculate the 0.25 quantile value for all the columns in the list, you can use the metric generator function. Here is how you can do for two defined columns.

```
report = Report(metrics=[
    generate_column_metrics(ColumnQuantileMetric, parameters={'quantile':0.25}, columns=['AveRooms', 'AveBedrms']),
])

report.run(reference_data=reference, current_data=current)
report
```

You can easily combine individual metrics, presets and functions to generate multiple column metrics in a single list:

```
report = Report(metrics=[
    ColumnSummaryMetric(column_name='AveRooms'),
    generate_column_metrics(ColumnQuantileMetric, parameters={'quantile':0.25}, columns='num'),
    DataDriftPreset()
])

report.run(reference_data=reference, current_data=current)
report
```

{% hint style="info" %}
**Available metrics and presets**. You can refer to the All Metrics [reference table](../reference/all-metrics.md) to browse available metrics and presets or use one of the example notebooks with presets or metrics in the [Examples](../examples/readme.md) section.
{% endhint %}

## 6. Define the report output format

You can render the visualizations directly in the notebook as shown above. There are also alternative options. 

If you only want to log the metric output, you can export the results as a Python dictionary.

```python
report.as_dict()
```
You can also get the output as JSON. 

```python
report.json()
```

You can also save HTML or JSON externally. 

```python
report.save_html("file.html")
```

## 7. Run data stability tests

Reports are useful when you want to debug data or model quality, or share results with the team. However, it is less convenient if you want to run your checks automatically and only react to meaningful issues.

To integrate Evidently checks in the prediction pipeline, you can use the **test suites** functionality. 

Test suites help compare the two datasets in a structured way. A **test suite** contains several individual tests. Each **test** compares a specific metric against a defined condition and returns an explicit pass/fail result. You can apply tests to the whole dataset or individual columns. 

Just like with reports, you can create a custom test suite or use one of the **presets** that work out of the box. Let's create a custom one!

Imagine you received a new batch of data. Before generating the predictions, you want to check if its quality is good enough to run your model. You can combine several tests to check for missing values, duplicate columns, and so on. 

You need to create a `TestSuite` object and specify the preset to include.

```python
tests = TestSuite(tests=[
    TestNumberOfColumnsWithMissingValues(),
    TestNumberOfRowsWithMissingValues(),
    TestNumberOfConstantColumns(),
    TestNumberOfDuplicatedRows(),
    TestNumberOfDuplicatedColumns(),
    TestColumnsType(),
    TestNumberOfDriftedColumns(),
])

tests.run(reference_data=reference, current_data=current)
tests
```

You will get a summary with the test results:

![Part of the custom Test Suite.](../.gitbook/assets/tutorial/get-started-test-output-min.png)

**How does it work?** Evidently automatically generates the test conditions based on the provided reference dataset. They are based on heuristics, e.g. the individual test fail if the columns types do not match, the number of columns with missing values is higher than in reference, or if the share of drifting features is over 50%. You can also pass custom conditions to set your own constraints.

You can also use **Test Presets**. For example, No Target Performance preset combines multiple checks related to data stability, drift and data quality to help evaluate the model without ground truth labeles available. 

```python
suite = TestSuite(tests=[
    NoTargetPerformanceTestPreset(),
])

suite.run(reference_data=reference, current_data=current)
suite
```

You can group the outputs by test status, feature, test group, and type. By clicking on “details,” you can also explore the visuals related to a specific test. 

![Details on Mean Value Stability test](../.gitbook/assets/tutorial/get_started_2_mean_value_stability-min.png)

If some of the tests fail, you can use supporting visuals to explore the details:

![Failed tests](../.gitbook/assets/tutorial/test-notargetperformance-min.png)

Just like with Reports, you can also combine individual tests and presets in a single Test Suite and use column generator to generate multiple column-level tests:

```python
suite = TestSuite(tests=[
    TestColumnDrift('Population'),
    TestShareOfOutRangeValues('Population'),
    generate_column_tests(TestMeanInNSigmas, columns='num'),
    
])

suite.run(reference_data=reference, current_data=current)
suite
```
{% hint style="info" %}
**Available tests and presets**. You can refer to the All tests [reference table](../reference/all-tests.md) to browse available tests and presets or use one of the example notebooks in the [Examples](../examples/readme.md) section.
{% endhint %}

Just like with reports, you can export the output in other formats.

To integrate Evidently checks in the prediction pipeline, you can get the output as JSON or a Python dictionary: 

```python
suite.as_dict()
```

You can extract necessary information from the JSON or Python dictionary output and design a conditional workflow around it. For example, if some tests fail, you can trigger an alert, retrain the model or generate the report. 

## 8. What else is there?

**Go through the steps in more detail**

If you want to walk through all the described steps in more details, refer to the [User Guide](../tests-and-reports/readme.md). A good next step is to explore how to pass custom tests parameters to define your own [test conditions](../tests-and-reports/run-tests.md#how-to-set-the-parameters).  

**Explore available presets**

Both **tests** and **reports** have multiple presets available. Some, like Data Quality, require only input data. You can use them even without the reference dataset. When you have the true labels, you can run presets like **Regression Performance** and **Classification Performance** to evaluate the model quality and errors. 

To understand the contents of each preset, you can explore the [Reports](../reports) and [Test Suites](../tests). If you want to see the pre-rendered examples of the reports, browse Colab notebooks in the [Examples](../get-started/examples.md) section. 

**Explore available integrations**

If you want to explore more examples of how to integrate Evidently with other tools like MLflow and Airflow, refer to the [Integrations](../integrations). 
 
If you have a real-time ML service and want to collect data and model metrics on top of the live data stream, you can explore the [integration with Grafana and Prometheus](../integrations/evidently-and-grafana.md). 

Evidently is in active development, so expect things to change and evolve. You can subscribe to the [user newsletter]([https://evidentlyai.com/sign-up](https://www.evidentlyai.com/user-newsletter)) or follow our [releases on GitHub](https://github.com/evidentlyai/evidently/releases) to stay updated about the latest functionality. 

## Join our Community!

We run a [Discord community](https://discord.gg/xZjKRaNp8b) to connect with our users and chat about ML in production topics. 

In case you have feedback or need help, just ask in Discord or open a GitHub issue. 

And if you want to support a project, give us a star on [GitHub](https://github.com/evidentlyai/evidently)!

