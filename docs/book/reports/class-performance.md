# TL;DR

You can use the pre-built reports and test suites to analyze the performance of a classification model. The presets work for binary and multi-class classification, probabilistic and non-probabilistuc classification. 

* Works for a **single model** or helps compare the **two**
* Works for **binary** and **multi-class** classification
* Displays a variety of plots related to the model **performance**
* Helps **explore regions** where the model makes different types of **errors**

## Summary

**Probabilistic Classification Performance** report evaluates the quality of a probabilistic classification model. It works both for binary and multi-class classification.

If you have a non-probabilistic classification model, refer to a [separate report](classification-performance.md).

This report can be generated for a single model, or as a comparison. You can contrast your current production model performance against the past or an alternative model.

## Requirements

To run this report, you need to have input features, and **both target and prediction** columns available.

**In the column mapping, you need to specify the names of your Prediction columns**. The tool expects a separate column for each class, even for binary classification.

**NOTE: Column order in Binary Classification.** For binary classification, class order matters. The tool expects that the target (so-called positive) class is the **first** in the `column_mapping['prediction']` list.

The column names can be **numerical labels** like "0", "1", "2" or **class names** like "virginica", "setoza", "versicolor". Each column should contain the predicted probability \[0;1] for the corresponding class.

You can find an example below:

```
column_mapping['prediction'] = [‘class_name1’, ‘class_name2’, ‘class_name3’]
```

The **Target column** should contain the true labels that match the **Prediction column** names. The tool performs the matching and evaluates the model quality by looking for the names from the "prediction" list inside the Target column.

The tool does not yet work for multi-label classification. It expects a single true label.

To generate a comparative report, you will need **two** datasets. The **reference** dataset serves as a benchmark. We analyze the change by comparing the **current** production data to the **reference** data.

![](<../.gitbook/assets/two\_datasets\_classification (1) (1).png>)

You can also run this report for a **single** `DataFrame` , with no comparison performed. In this case, pass it as `reference_data`.

## How it looks

The report includes 10 components. All plots are interactive.

### **1. Model Quality Summary Metrics**

We calculate a few standard model quality metrics: Accuracy, Precision, Recall, F1-score, ROC AUC, and LogLoss.

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

In the tab “ALL”, we plot the distribution of classes against the values of the feature. This is the “Target Behavior by Feature” plot from the [Categorical Target Drift ](categorical-target-drift.md)report.

If you compare the two datasets, it visually shows the changes in the feature distribution and in the relationship between the values of the feature and the target.

![](<../.gitbook/assets/prob\_class\_perf\_classification\_quality\_by\_feature\_example\_all (1).png>)

Then, for each class, we plot the predicted probabilities alongside the values of the feature.

![](<../.gitbook/assets/prob\_class\_perf\_classification\_quality\_by\_feature\_example\_class (1).png>)

It visualizes the regions where the model makes errors of each type and reveals the low-performance segments. You can compare the distributions and see **if the errors are sensitive to the values of a given feature**.

## Report customization

You can set [options-for-quality-metrics.md](../customization/options-for-quality-metrics.md "mention") to set a custom classification threshold or сut the data above the given quantile from the histogram plots in the "Classification Quality by Feature" table.

You can select which components of the reports to display or choose to show the short version of the report: [select-widgets-to-display.md](../customization/select-widgets-to-display.md "mention").

If you want to create a new plot or metric, you can [add-a-custom-widget-or-tab.md](../customization/add-a-custom-widget-or-tab.md "mention").

## When to use the report

Here are our suggestions on when to use it—you can also combine it with the [Data Drift](data-drift.md) and [Categorical Target Drift](categorical-target-drift.md) reports to get a comprehensive picture.

**1. To analyze the results of the model test.** You can explore the results of an online or offline test and contrast it to the performance in training. Though this is not the primary use case, you can use this report to compare the model performance in an A/B test, or during a shadow model deployment.

**2. To generate regular reports on the performance of a production model.** You can run this report as a regular job (e.g. weekly or at every batch model run) to analyze its performance and share it with other stakeholders.

**3. To analyze the model performance on the slices of data.** By manipulating the input data frame, you can explore how the model performs on different data segments (e.g. users from a specific region).

**4. To trigger or decide on the model retraining.** You can use this report to check if your performance is below the threshold to initiate a model update and evaluate if retraining is likely to improve performance.

**5. To debug or improve model performance.** You can use the Classification Quality table to identify underperforming segments and decide on the ways to address them.

## JSON Profile

If you choose to generate a JSON profile, it will contain the following information:

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

## Examples

* Browse our [examples](../get-started/examples.md) for sample Jupyter notebooks.
* See a tutorial "[What is your model hiding](https://evidentlyai.com/blog/tutorial-2-model-evaluation-hr-attrition)" where we analyze the performance of two models with identical ROC AUC to choose between the two.

You can also read the [release blog](https://evidentlyai.com/blog/evidently-018-classification-model-performance).
