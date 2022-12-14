**TL;DR:** You can use the pre-built reports and test suites to analyze the performance of a classification model. The presets work for binary and multi-class classification, probabilistic and non-probabilistuc classification. 

For Reports, you can use the `ClassificationPreset`. For Test Suites, you can use the `MulticlassClassificationTestPreset`, `BinaryClassificationTopKTestPreset`, `BinaryClassificationTestPreset`.

# Use Case

These presets help evaluate the quality of classification models. You can use them:

**1. To monitor the performance of a classification model in production.** You can run the test suite as a regular job (e.g., weekly or every time you get the labels) to contrast the model performance against expected.

**2. To trigger or decide on the model retraining.** You can use the test suite to check if the model performance is below the threshold to initiate a model update.

**3. To debug or improve model performance.** If you detect a quality drop, you can use the visual report to explore the model errors and underperforming segments. By manipulating the input data frame, you can explore how the model performs on different data segments (e.g., users from a specific region). You can also combine it with the [Data Drift](data-drift.md) report.

**4. To analyze the results of the model test.** You can explore the results of an online or offline test and contrast it to the performance in training. Though this is not the primary use case, you can use this report to compare the model performance in an A/B test or during a shadow model deployment.

To run performance checks as part of the pipeline, use the Test Suite. To explore and debug, use the Report.

# Classification Performance Report 

## Code example

```python
classification_performance_report = Report(metrics=[
    ClassificationPreset,
])

classification_performance_report.run(reference_data=bcancer_ref, current_data=bcancer_cur)

classification_performance_report
```

## How it works

This report evaluates the quality of a classification model.

* Can be generated for a **single dataset**, or compare the performance **against reference** (e.g. past performance or alternative model).
* Works for **binary** and **multi-class**, **probabilistic** and non-probabilistic classification.
* Displays a variety of plots related to the model **performance**.
* Helps **explore regions** where the model makes different types of **errors**.

## Data Requirements

To run this report, you need to have **both target and prediction** columns available. Input features are optional. Pass them if you want to explore the relations between features and target.

Refer to the [column mapping section](../test-and-reports/column-mapping.md) to see how to pass model predictions and labels in different cases. 

The tool does not yet work for multi-label classification. It expects a single true label.

To generate a comparative report, you will need **two** datasets. 
![](<../.gitbook/assets/two\_datasets\_classification (1) (1).png>)

You can also run this report for a **single** dataset, with no comparison performed.

## How it looks

The report includes multiple components. The composition might vary based on problem type (there are more plots in the case of probabilistic classification). All plots are interactive.

### **1. Model Quality Summary Metrics**

Evidently calculates a few standard model quality metrics: Accuracy, Precision, Recall, F1-score, ROC AUC, and LogLoss.

**To support the model performance analysis, we also generate interactive visualizations. They help analyze where the model makes mistakes and come up with improvement ideas.**

### 2. Class Representation

Shows the number of objects of each class.

![](<../.gitbook/assets/prob\_class\_perf\_class\_representation (1).png>)

### 3. Confusion Matrix

Visualizes the classification errors and their type.

![](<../.gitbook/assets/prob\_class\_perf\_confusion\_matrix (1).png>)

### 4. Quality Metrics by Class

Shows the model quality metrics for the individual classes. In the case of multi-class problems, it will also include ROC AUC.

![](<../.gitbook/assets/prob\_class\_perf\_quality\_by\_class (1).png>)

### **5. Class Separation Quality**

A scatter plot of the predicted probabilities that shows correct and incorrect predictions for each class.

It serves as a representation of both model accuracy and the quality of its calibration. It also helps visually **choose the best probability threshold for each class.**

![](<../.gitbook/assets/prob\_class\_perf\_class\_separation\_quality (1).png>)

### 6. Probability Distribution

A similar view as above, it shows the distribution of predicted probabilities.

![](<../.gitbook/assets/prob\_class\_perf\_probability\_distr (1).png>)

### **7. ROC Curve**

ROC Curve (**receiver operating characteristic curve**) shows the share of true positives and true negatives at different classification thresholds.

![](../.gitbook/assets/prob\_class\_perf\_roc.png)

### 8. **Precision-Recall Curve**

The **precision**-**recall curve** shows the trade-off between **precision** and **recall** for different classification thresholds.

![](<../.gitbook/assets/prob\_class\_perf\_pr (1).png>)

### 9. Precision-Recall Table

The table shows possible **outcomes for different classification thresholds** and **prediction coverage**. If you have two datasets, the table is generated for both.

![](<../.gitbook/assets/prob\_class\_perf\_pr\_table\_current (1).png>)

Each line in the table defines a case when only _top-X%_ predictions are considered, with a 5% step. It shows the absolute number of predictions _(Count)_ and the probability threshold _(Prob)_ that correspond to this combination.

The table then shows the quality metrics for a given combination. It includes _Precision_, _Recall_, the share of _True Positives (TP)_, and _False Positives (FP)_.

This helps explore the quality of the model if you choose to act only on some of the predictions.

### 10. Classification Quality by Feature

In this table, we show a number of plots for each feature. To expand the plots, click on the feature name.

![](<../.gitbook/assets/prob\_class\_perf\_classification\_quality\_by\_feature (1).png>)

In the tab “ALL”, you can see the distribution of classes against the values of the feature. If you compare the two datasets, it visually shows the changes in the feature distribution and in the relationship between the values of the feature and the target.

![](<../.gitbook/assets/prob\_class\_perf\_classification\_quality\_by\_feature\_example\_all (1).png>)

For each class, you can seee the predicted probabilities alongside the values of the feature.

![](<../.gitbook/assets/prob\_class\_perf\_classification\_quality\_by\_feature\_example\_class (1).png>)

It visualizes the regions where the model makes errors of each type and reveals the low-performance segments. You can compare the distributions and see **if the errors are sensitive to the values of a given feature**.

## Metrics output

You can get the report output as a JSON or a Python dictionary:

```yaml
{
  "probabilistic_classification_performance": {
    "name": "probabilistic_classification_performance",
    "datetime": "datetime",
    "data": {
      "utility_columns": {
        "date": null,
        "id": null,
        "target": "target",
        "prediction": [
          "label1",
          "label2",
          "label3"
        ]
      },
      "cat_feature_names": [],
      "num_feature_names": [],
      "metrics": {
        "reference": {
          "accuracy": accuracy,
          "precision": precision,
          "recall": recall,
          "f1": f1,
          "roc_auc": roc_auc,
          "log_loss": log_loss,
          "metrics_matrix": {
            "label1": {
              "precision": precision,
              "recall": recall,
              "f1-score": f1,
              "support": support
            },
            "accuracy": accuracy,
            "macro avg": {
              "precision": precision,
              "recall": recall,
              "f1-score": f1,
              "support": support
            },
            "weighted avg": {
              "precision": precision,
              "recall": recall,
              "f1-score": f1,
              "support": support
            }
          },
          "roc_aucs": [
            roc_auc_label_1,
            roc_auc_label_2,
            roc_auc_label_3
          ],
          "confusion_matrix": {
            "labels": [],
            "values": []
          },
          "roc_curve": {
            "label1": {
              "fpr": [],
              "tpr": [],
              "thrs": []
          },  
          "pr_curve": {
            "label1": []
        },
        "current": {
          "accuracy": accuracy,
          "precision": precision,
          "recall": recall,
          "f1": f1,
          "roc_auc": roc_auc,
          "log_loss": log_loss,
          "metrics_matrix": {
            "label1": {
              "precision": precision,
              "recall": recall,
              "f1-score": f1,
              "support": support
          },
          "roc_aucs": [
            roc_auc_label_1,
            roc_auc_label_2,
            roc_auc_label_3
          ],
          "confusion_matrix": {
            "labels": [],
            "values": [],
          },
          "roc_curve": {
            "label1": {
              "fpr": [],
              "tpr": [],
              "thrs": []
          },
          "pr_curve": {
            "label1": []
          }
        }
      }
    }
  },
  "timestamp": "timestamp"
}
```

## Report customization

* You can pass relevant parameters to change the way some of the metrics are calculated, such as decision threshold or K to evaluate precision@K. See the available parameters [here](../reference/all-metrics.md)
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* If you want to exclude some of the metrics, you can create a custom report by combining the chosen metrics. See the complete list [here](../reference/all-metrics.md)

# Classification Performance Test Suite

![](<../.gitbook/assets/tests/test_preset_binarytopKclass-min.png>)

If you want to run classification performance checks as part of a pipeline, you can create a Test Suite and use one of the classification presets. There are several presets for different classification tasks. They apply to Multiclass Classification, Binary Classification, and Binary Classification at topK accordingly: 

```python
MulticlassClassificationTestPreset
BinaryClassificationTopKTestPreset
BinaryClassificationTestPreset
```

## Code example

```python
binary_topK_classification_performance = TestSuite(tests=[
    BinaryClassificationTopKTestPreset(k=10),
])

binary_topK_classification_performance.run(reference_data=ref, current_data=cur)
binary_topK_classification_performance
```

## How it works

You can use the test presets to evaluate the quality of a classification model when you have the ground truth labels.

* Each preset compares **relevant quality metrics** for the model type and **against the defined expectation**. 
* They also test for the **target drift** to detect shift in the distribution of classes and/or probabilities. It might indicate emerging concept drift.  
* For Evidently to **generate the test conditions automatically**, you should pass the reference dataset (e.g., performance during model validation or a previous period). You can also set the performance expectations manually by passing a custom test condition. 
* If you neither pass the reference dataset nor set custom test conditions, Evidently will compare the model performance to a **dummy model**.

Head here to the [All tests](../reference/all-tests.md) table to see the composition of each preset and default parameters. 

## Test Suite customization

* You can set custom test conditions.
* You can pass relevant parameters to change how some of the metrics are calculated, such as decision threshold or K to evaluate precision@K. See the available parameters [here](../reference/all-tests.md).
* If you want to exclude some tests or add additional ones, you can create a custom test suite by combining the chosen tests. See the complete list [here](../reference/all-tests.md).

## Examples

* Browse the [examples](../get-started/examples.md) for sample Jupyter notebooks and Colabs.
* See a blog post and a tutorial "[What is your model hiding](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition)" where we analyze the performance of two models with identical ROC AUC to choose between the two.
