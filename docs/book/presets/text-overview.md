**TL;DR:** You can explore and compare text datasets.

* For visual analysis using Reports, use `TextOverviewPreset`.

# Use case 

You can evaluate and explore text data: 

**1. To monitor input data for NLP models.** When you do not have true labels or actuals, you can monitor changes in the input data (data drift) and descriptive text characteristics. You can run batch checks, for example, comparing the latest batch of text data to earlier or training data. You can often combine it with evaluating [Prediction Drift](target-drift.md).

**2. When you are debugging the model decay.** If you observe a drop in the model performance, you can use this report to understand changes in the input data patterns.

**3. Exploratory data analysis and comparison.** You can use the visual report to explore the text data you want to use for training. You can also use it to compare any two datasets. 

# Text Overview Report   

If you want to visually explore the text data, you can create a new Report object and use the `TextOverviewPreset`.

## Code example

```python
text_overview_report = Report(metrics=[
    TextOverviewPreset(column_name="Review_Text")
])

text_overview_report.run(reference_data=ref, current_data=cur)
text_overview_report
```

Note that to calculate some of the metrics, you should also import text-specific libraries:

```
import nltk
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## How it works

The `TextOverviewPreset` provides an overview and comparison of text datasets.
* Generates a **descriptive summary** of the text columns in the dataset. 
* Performs **data drift detection** to compare the two texts using the domain classifier approach. 
* Shows distributions of the **text descriptors** in two datasets, and their **correlations** with other features. 
* Performs **drift detection for text descriptors**.

## Data Requirements

* You can pass **one or two** datasets. The **reference** dataset serves as a benchmark. Evidently analyzes the change by comparing the **current** production data to the **reference** data. If you pass a single dataset, there will be no comparison.

* To run this preset, you must have **text columns**. Additional features are optional. Pass them if you want to analyze the correlations between the features and text descriptors. 

* **Column mapping**. You must explicitly specify the columns that contain text features in [column mapping](../input-data/column-mapping.md) to run this report. 

## How it looks

The report includes 5 components. All plots are interactive.

### 1. Text Column Summary

The report first shows the **descriptive statistics** for the text column(s).

![](<../.gitbook/assets/reports/metric_column_summary_text-min.png>)

### 2. Text Descriptors Distribution

The report generates several features that describe different text properties and shows the distributions of these text descriptors. 

#### Text length

![](<../.gitbook/assets/reports/metric_text_descriptors_distribution_text_length-min.png>)

#### Non-letter characters

![](<../.gitbook/assets/reports/metric_text_descriptors_distribution_nlc-min.png>)

#### Out-of-vocabulary words

![](<../.gitbook/assets/reports/metric_text_descriptors_distribution_oov-min.png>)

### 3. Text Descriptors Correlations

If the dataset contains numerical features, the report will show the **correlations between features and text descriptors** in the current and reference dataset. It helps detects shifts in the relationship.

#### Text length

![](<../.gitbook/assets/reports/metric_text_descriptors_correlation_text_length-min.png>)

#### Non-letter characters

![](<../.gitbook/assets/reports/metric_text_descriptors_correlation_nlc-min.png>)

#### Out-of-vocabulary words

![](<../.gitbook/assets/reports/metric_text_descriptors_correlation_oov-min.png>)


### 4. Text Column Drift

If you pass two datasets, the report performs drift detection using the default [data drift method for texts](../reference/data-drift-algorithm.md) (domain classifier). It returns the ROC AUC of the binary classifier model that can discriminate between reference and current data. If the drift is detected, it also shows the top words that help distinguish between the reference and current dataset.

![](<../.gitbook/assets/reports/metric_column_drift_text-min.png>)

### 5. Text Descriptors Drift

If you pass two datasets, the report also performs drift detection for text descriptors to show statistical shifts in patterns between test characteristics.

![](<../.gitbook/assets/reports/metric_text_descriptors_drift_text-min.png>)

## Metrics output

You can get the report output as a JSON or a Python dictionary.

## Report customization

* You can [specify the drift detection threshold](../customization/options-for-statistical-tests.md). 
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* You can create a different report or test suite from scratch, taking this one as an inspiration. 
