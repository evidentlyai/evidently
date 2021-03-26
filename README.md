# evidently
## What is it?
Evidently helps analyze machine learning models during development, validation, or production monitoring. The tool generates interactive reports from pandas `DataFrame`.
Currently 6 reports are available.  

### 1. Data Drift
Detects changes in feature distribution. 
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_github.png)

### 2. Numerical Target Drift
Detects changes in numerical target (see example below) and feature behavior.
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_num_target_drift_github.png)

### 3. Categorical Target Drift
Detects changes in categorical target and feature behavior (see example below).
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_cat_target_drift_github.png)

### 4. Regression Model Performance
Analyzes the performance of a regression model and model errors (see example below).
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_regression_performance_report_github.png)

### 5. Classification Model Performance
Analyzes the performance and errors of a classification model. Works both for binary and multi-class models (see example below).
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_classification_performance_report_github.png)

### 6. Probabilistic Classification Model Performance
Analyzes the performance of a probabilistic classification model, quality of model calibration, and model errors. Works both for binary and multi-class models (see example below).
![Dashboard example](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/evidently_prob_classification_performance_report_github.png)

## Installing from PyPI
### MAC OS and Linux
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```

The tool allows building interactive reports both inside a Jupyter notebook and as a separate .html file. If you only want to generate interactive reports as .html files, the installation is now complete.

To enable building interactive reports inside a Jupyter notebook, we use jupyter nbextension. If you want to create reports inside a Jupyter notebook, then after installing `evidently` you should run the two following commands in the terminal from evidently directory.

To install jupyter nbextention, run:
```sh
$ jupyter nbextension install --sys-prefix --symlink --overwrite --py evidently
```
To enable it, run:
```sh
jupyter nbextension enable evidently --py --sys-prefix
```
That's it!

**Note**: a single run after the installation is enough. No need to repeat the last two commands every time.

**Note 2**: if you use Jupyter Lab, you may experience difficulties with exploring report inside a Jupyter notebook. However, the report generation in a separate .html file will work correctly.

### Windows
Evidently is available as a PyPI package. To install it using pip package manager, run:
```sh
$ pip install evidently
```
The tool allows building interactive reports both inside a Jupyter notebook and as a separate .html file. Unfortunately, building reports inside a Jupyter notebook is not yet possible for Windows. The reason is Windows requires administrator privileges to create symlink. In later versions we will address this issue.

## Getting started

### Jupyter Notebook
To start, prepare your data as two pandas `DataFrames`. The first should include your reference data, the second -  current production data. The structure of both datasets should be identical. 

For Data Drift report, include the input features only.
For Target Drift reports, include the column with Target and/or Prediction.
For Model Performance reports, include the columns with Target and Prediction.

```python
import pandas as pd
from sklearn import datasets

from evidently.dashboard import Dashboard
from evidently.tabs import DriftTab

iris = datasets.load_iris()
iris_frame = pd.DataFrame(iris.data, columns = iris.feature_names)
```

To generate the Data Drift report, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab])
iris_data_drift_report.save("reports/my_report.html")
```

To generate the Data Drift and the Categorical Target Drift reports, run:
```python
iris_data_drift_report = Dashboard(iris_frame[:100], iris_frame[100:], tabs = [DriftTab, CatTargetDriftTab])
iris_data_drift_report.save("reports/my_report_with_2_tabs.html")
```

If you get a security alert, press "trust html".
Html report does not open automatically. To explore it, you should open it from the destination folder.

To generate the Regression Model Performance report, run:
```python
regression_model_performance = Dashboard(reference_data, current_data,  column_mapping = column_mapping, tabs=[RegressionPerfomanceTab]) 
```

You can also generate a Regression Model Performance for a single `DataFrame`. In this case, run:
```python
regression_single_model_performance = Dashboard(reference_data, None, column_mapping=column_mapping, tabs=[RegressionPerformanceTab])
```

To generate the Classification Model Performance report, run:
```python
classification_performance_report = Dashboard(reference_data, current_data, column_mapping = column_mapping,
                   	tabs=[ClassificationPerformanceTab])
```
 
For Probabilistic Classification Model Performance report, run:
```python
classification_performance_report = Dashboard(reference_data, current_data, column_mapping = column_mapping,
                   	tabs=[ProbClassificationPerformanceTab])
```
 
You can also generate either of the Classification reports for a single `DataFrame`. In this case, run:
```python
classification_single_model_performance = Dashboard(reference_data, None, column_mapping=column_mapping, tabs=[ClassificationPerformanceTab])
```
or
```python
prob_classification_single_model_performance = Dashboard(reference_data, None, column_mapping=column_mapping, tabs=[ProbClassificationPerformanceTab])
```

### Terminal
Now you can run a report generation directly from bash shell. To do this, prepare your data as two `csv` files (in case you run one of the performance report, you might have only one file). The first should include your reference data, the second -  current production data. The structure of both datasets should be identical. 

To gererate report run in bash the following command:

```bash
python -m evidently analyze --config config.json 
--reference reference.csv --current current.csv --output output_folder
```
Here:
- `reference` is the path to the reference data, 
- `current` is the path to the current data, 
- `output` is the path to the output folder,
- `config` is the path to the configuration file.

Currently, you can choose the following Tabs:
- `drift` to estimate the data drift,
- `num_target_drift` to estimate target drift for numerical target,
- `cat_target_drift` to estimate target drift for categorical target.,
- `classification_performance` to explore the performance of a classification model,
- `prob_classification_performance` to explore the performance of a classification model,
- `regression_performance` to explore the performance of a regression model.

To configure the report you need to create `config.json` file. This file configures the way of reading your input data and the type of the report. 

Here is an example of the simple configurations, where we have comma separated `csv` files with headers and there is no `date` column in the data.

```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": null
  },
  "dashboard_tabs": ["cat_target_drift"]
}
```

Here is an example of the more complicated configurations, where we have comma separated `csv` files with headers and `datetime` column. And we also specified the `column_mapping` dictionary, where we added information about `datetime`, `target` and `numerical_features`. 

```bash
{
  "data_format": {
    "separator": ",",
    "header": true,
    "date_column": "datetime"
  },
  "column_mapping" : {
  	"datetime":"datetime",
  	"target":"target",
  	"numerical_features": ["mean radius", "mean texture", "mean perimeter", 
  		"mean area", "mean smoothness", "mean compactness", "mean concavity", 
  		"mean concave points", "mean symmetry"]},
  "dashboard_tabs": ["cat_target_drift"]
}
```

## More details
`Dashboard` generates an interactive report that includes the selected `Tabs`. 
Currently, you can choose the following Tabs:
- `DriftTab` to estimate the data drift.
- `NumTargetDriftTab` to estimate target drift for numerical target. It is an option for a problem statement with a numerical target function: regression, probabilistic classification or ranking, etc.
- `CatTargetDriftTab` to estimate target drift for categorical target. It is an option for a problem statement with a categorical target function: binary classification, multi-class classification, etc.
- `RegressionPerformanceTab` to explore the performance of a regression model. 
- `ClassificationPerformanceTab` to explore the performance of a classification model.
- `ProbClassificationPerformanceTab` to explore the performance of a probabilistic classification model and quality of model calibration.

We will be adding more tabs soon!

To create a `Dashboard`, take the following steps:

1. **Prepare your data as two pandas DataFrames**. 
To analyze model performance or drift, you will need two datasets. 
The first one is the “reference” dataset. It can include training or earlier production data. The second is the "current" dataset that should include the most recent production data. Performance or drift will be evaluated by comparing the current data to the reference data. 

We expect that DataFrames:
- Have only `string` column names;
- Have only numerical type (`np.number`) for feature columns that are analyzed for data drift. **All non-numerical columns will be ignored**. The datetime column is the only exception. If available, it will be used as the x-axis in the data plots. 

**Note**: you can also prepare a single pandas DataFrame. When calling the dashboard, you can specify the rows that belong to the reference dataset, and rows that belong to the current dataset. See Boston housing and Breast Cancer notebooks for examples. 

2. **Pass `column_mapping` into `Dashboard`**. 
If the `column_mapping` is not specified or set as `None`, we use the default mapping strategy:
- All features will be treated as numerical.
- Column with 'id' name will be treated as an ID column.
- Column with 'datetime' name will be treated as a datetime column. 
- Column with 'target' name will be treated as a target function.
- Column with 'prediction' name will be treated as a model prediction.

ID, datetime, target and prediction are utility columns. 

For data drift report, they are not required. If you specify id, target and prediction, they will be excluded from the data drift report. 
If you specify the datetime, it will be used in data plots.

For target drift reports, either target or prediction column (or both) are required. 

For model performance reports, both target and prediction column are required.

You can create a `column_mapping` to specify if your dataset includes utility columns, and split features into numerical and categorical types. 

`Column_mapping` is a python `dictionary` with the following format:
```python
column_mapping = {}

column_mapping['target'] = 'y' #'y' is the name of the column with the target function
column_mapping['prediction'] = 'pred' #'pred' is the name of the column(s) with model predictions
column_mapping['id'] = None #there is no ID column in the dataset
column_mapping['datetime'] = 'date' #'date' is the name of the column with datetime 

column_mapping['numerical_features'] = ['temp', 'atemp', 'humidity'] #list of numerical features
column_mapping['categorical_features'] = ['season', 'holiday'] #list of categorical features
```

**Note for PROBABILISTIC CLASSIFICATION**
`column_mapping['prediction'] = [‘class_name1’, ‘class_name2’, ‘class_name3’,… etc]`
The tool expects your pd.DataFrame(s) to contain columns with the names matching the ones from the ‘prediction’ list. Each column should include information about the predicted probability [0;1] for the corresponding class.

For binary classification class order matters. The tool expects that the target (so called positive) class is the first in the column_mapping['prediction'] list.

**Note for DATA DRIFT** 
Though the data drift tool works only with numerical data, you can also estimate drift for categorical features. To do that, you should encode the categorical data with [numerical labels](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html). You can use other strategies to represent categorical data as numerical, for instance [OneHotEncoding](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.get_dummies.html). Then you should create `column_mapping` `dict` and list all encoded categorical features in the `categorical_feature` section, like:
```python
column_mapping['categorical_features'] = ['encoded_cat_feature_1', 
'encoded_cat_feature_2']
```
Categorical features will be actually treated as categorical. Data drift estimation will use chi-squared test.

3. **Generate the report**.
You can generate the report without specifying the `column_mapping`:
```python
drift_dashboard = Dashboard(reference_data, recent_data, tabs=[DriftTab])
```
And with `column_mapping` specification:
```python
drift_dashboard_with_mapping = Dashboard(reference_data, recent_data, 
	column_mapping = column_mapping, tabs=[DriftTab])
```

4. **Explore the report inside the Jupyter notebook**.
```python
drift_dashboard.show()
```

5. **Export the report as an html file and open it in your browser**.
```python
drift_dashboard.save("reports/my_report.html")
```
If you get security alert, press "trust html".

You will need to specify the path where to save your report and the report name. 
Report will not open automatically. To explore it, you should open it from the destination folder.

## How it works
To evaluate drift or production model performance, we need two datasets. The reference dataset will serve as a benchmark. We analyze drift and performance by comparing the most recent data to the reference data. 

You can potentially choose any two datasets for comparison. But keep in mind that only “reference” dataset will be used as a basis for comparison. 

### Data Drift
To estimate the data drift, we compare distributions of each individual feature in the two datasets. We use statistical tests to detect if the distribution has changed significantly. For numerical features, we use [two-sample Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test). For categorical features, we will use [chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test). Both tests use 0.95 confidence level. We will add some levers later on, but this is a good enough default approach.

Currently, we estimate data drift for each feature individually. Integral data drift is not evaluated.

By clicking on each feature, you can explore the values mapped in a plot. The dark green line is the mean, as seen in the reference dataset. The green area covers one standard deviation from the mean. You can also zoom on distributions to understand what has changed.

Read more in the [release blog](https://evidentlyai.com/blog/evidently-001-open-source-tool-to-analyze-data-drift). 

### Numerical Target Drift
We estimate the drift for the target (actual values) and predictions in the same manner. If both columns are passed to the dashboard, we build two sets of plots. If only one of them (either target or predictions) is provided, we build one set of plots. If neither target nor predictions column is available, you will get an error.

To estimate the numerical target drift, we compare the distribution of the target in the two datasets. We use the Kolmogorov-Smirnov statistical test with a 0.95 confidence level to detect if the distribution has changed significantly.

We also calculate the Pearson correlation between the target and each individual feature in the two datasets. We create a plot with correlations to show correlation changes between the reference and the current dataset. 

We visualize the target values by index or time (if `datetime` column is available or defined in the `column_mapping` dictionary). This plot helps explore the target behavior and compare it between datasets.

Finally, we generate an interactive table with the visualizations of dependencies between the target and each feature. These plots help analyze how feature values relate to the target values and identify the differences between the datasets. We recommend paying attention to the behavior of the most important features since significant changes might confuse the model and cause higher errors.

Read more in the [release blog](https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift). 

### Categorical Target Drift
Just as above, we estimate the drift for the target and predictions in the same manner. If both columns are passed to the dashboard, we build two sets of plots. If only one of them (either target or predictions) is provided, we build one set of plots. If neither target nor predictions column is available, you will get an error.

To estimate the categorical target drift, we compare the distribution of the target in the two datasets. We use chi-squared statistical test with 0.95 confidence level to detect if the distribution has changed significantly.

We also generate an interactive table with the visualizations of each feature distribution for different the target labels. These plots help analyze how feature values relate to the target labels and identify the differences between the datasets. We recommend paying attention to the behavior of the most important features since significant changes might confuse the model and cause higher errors.

Read more in the [release blog](https://evidentlyai.com/blog/evidently-014-target-and-prediction-drift).

### Regression Performance Report 
We evaluate the quality of a regression model and compare it to past performance. To run this report, you need to have both target and prediction columns available. 

You can also run this report if you have only one `DataFrame`. In this case, pass it as reference_data. 

To evaluate the regression model quality we calculate Mean Error (ME), Mean Absolute Error (MAE) and Mean Absolute Percentage Error (MAPE) metrics. To support the model performance analysis, we generate interactive visualizations: 
- Predicted vs Actual values scatter plot
- Predicted and Actual values over time/index
- Model Error over time/index
- Absolute Percentage Error in time/index
- Error Distribution
- Error Normality Q-Q plot

These plots help analyse where the model makes mistakes and come up with improvement ideas. 

We also generate an interactive Error Bias table. It visualizes the regions where the regression model underestimates and overestimates the target function. To generate it, we take 5% of the highest negative and positive errors. Then, we create histograms with feature values for these data segments with extreme errors and for the rest of the data. You can compare distributions and see if the error is sensitive to the values of a given feature.

Read more in the [release blog](https://evidentlyai.com/blog/evidently-016-regression-model-performance).

### Classification Performance Report
We evaluate the quality of a classification model and compare it to the past performance. To run this report, you need to have both target and prediction columns available.
 
For non-probabilistic classification, you can use both numerical labels like 0, 1,2 or class names like ‘virginica’, ’setoza’, ‘versicolor’ inside the target and prediction columns. The labels should be the same for the target and predictions.
 
You can also run this report if you have only one DataFrame. In this case, pass it as reference_data.
 
To evaluate the classification model quality we calculate Accuracy, Precision, Recall, and F1-score metrics. To support the model performance analysis, we generate interactive visualizations:
- Class representation
- Confusion matrix
- Quality Metrics for each class
   	     
These plots help analyze where the model makes mistakes and come up with improvement ideas.

We also generate an interactive Classification Quality table. It shows the distribution of each given feature and plots the correct predictions (True Positives - TP, True Negatives - TN), and model errors (False Positives - FP, False Negatives - FN) against it. It helps visualize the regions where the model makes errors of each type. The plots are available for all classes and all features. This way, you can compare the distributions and see if the specific error is sensitive to the values of a given feature.

Read more in the [release blog](https://evidentlyai.com/blog/evidently-018-classification-model-performance).
 
### Probabilistic Classification Performance Report
We evaluate the quality of a classification model and compare it to the past performance. To run this report, you need to have both target and prediction columns available.
 
In column mapping, you need to specify the names of your prediction columns. The tool expects a separate column for each class, that should contain predicted probability. (This applies even if you have a binary classification problem). Column names can be numerical labels like 0, 1,2 or class names like ‘virginica’, ’setoza’, ‘versicolor’.
 
You can find the example below:
```python
column_mapping['prediction'] = [‘class_name1’, ‘class_name2’, ‘class_name3’]
```

The tool expects your pd.DataFrame(s) to contain columns with the names matching the ones from the ‘prediction’ list. Each column should include information about the predicted probability [0;1] for the corresponding class.

The Target column should contain labels that match the column names for each class. The tool performs the matching and evaluates the model quality by looking for the names from the ‘prediction’ list inside the Target column.
 
You can also run this report if you have only one DataFrame. In this case, pass it as reference_data.
 
To evaluate the classification model quality we calculate Accuracy, Precision, Recall, F1-score, ROC AUC, and LogLoss metrics. To support the model performance analysis, we generate interactive visualizations:
- Class representation
- Confusion matrix
- Quality Metrics for each class
- Class Separation Quality
- ROC Curve
- Precision-Recall Curve
- Precision-Recall Table
 
These plots help analyze where the model makes mistakes and come up with improvement ideas.

We also generate an interactive Classification Quality table. It shows the distribution of each given feature values and plots the probabilities predicted by the model alongside it. It helps visualize the regions where the model makes errors of each type. The plots are available for all classes and all features. This way, you can compare the distributions and see if the specific error is sensitive to the values of a given feature.

Read more in the [release blog](https://evidentlyai.com/blog/evidently-018-classification-model-performance).

## Examples
- See Iris **Data Drift**, **Categorical Target Drift** and **Classification Performance** report generation to explore the reports both inside a Jupyter notebook and as a separate .html file: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/iris_data_drift.ipynb) 
- See Boston **Data Drift** and **Numerical Target Drift** report generation to explore the reports with and without column mapping: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/boston_data_drift.ipynb)
- See Breast cancer **Data Drift** and **Probabilistic Classification Performance** report generation to explore the reports with and without datetime specification: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/breast_cancer_data_drift.ipynb)
- See Bike Demand Prediction **Regression Model Performance** report with datetime and column mapping inside a Jupyter notebook: [Jupyter notebook](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/bike_sharing_demand_regression_performance.ipynb)

## Stay updated
We will be releasing more reports soon. If you want to receive updates, follow us on [Twitter](https://twitter.com/EvidentlyAI), or sign up for our [newsletter](https://evidentlyai.com/sign-up). You can also find more tutorials and explanations in our [Blog](https://evidentlyai.com/blog). If you want to chat and connect, join our [Discord community](https://discord.gg/xZjKRaNp8b)!
