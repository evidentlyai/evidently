---
description: An overview of the types of analysis you can do with Evidently. 
---

Evidently has several pre-built reports and test suites. We call them `presets`. Each preset evaluates or tests a particular aspect of the data or model quality. 

This page links to the description of each preset. If you want to see the code and interactive examples instead in Jupyter notebook or Colab, head here instead:

{% content-ref url="../get-started/examples.md" %}
[Examples](../get-started/examples.md). 
{% endcontent-ref %}

# Metric Presets

|         |                                                        |   |
| ------- | ------------------------------------------------------ | - |
| [**Data Quality**](data-quality.md)<br><br>Evaluates the dataset statistics and feature behavior. <br><br> Requirements: model inputs. | [**Data Drift**](data-drift.md)<br><br>Explores the distribution shift between two datasets. <br><br>Requirements: model inputs, a reference dataset. | [**Target Drift**](target-drift.md)<br><br>Explores the distribution shift in the model predictions. <br><br>Requirements: model predictions and/or target values; a reference dataset. |
| [**Classification**](class-performance.md)<br><br>Evaluates the classification model quality and errors. <br><br>Requirements: model predictions and true labels. | [**Regression**](reg-performance.md)<br><br>Evaluates the regression model quality and errors. <br><br>Requirements: model predictions and actuals. |  |

# Test Presets

|         |                                                        |   |
| ------- | ------------------------------------------------------ | - |
| **NoTargetPerformance**<br><br>Tests the model performance when you do not have ground truth or actuals. Includes several checks for data quality, integrity, and drift. <br><br> Requirements: model inputs, predictions, a reference dataset. | **Data Quality**<br><br>Tests if the batch is similar to the previous one. Tests data schema, column types, value ranges. <br><br> Requirements: model inputs, a reference dataset. | **Data Stability**<br><br>Explores the distribution shift in the model predictions. <br><br>Requirements: model predictions and/or target values; a reference dataset. |
| **Data Drift**<br><br>Tests for distribution drift per column and overall dataset drift. <br><br>Requirements: model inputs, a reference dataset. | **Regression** <br><br>Tests the performance of the regression model against expectation. <br><br>Requirements: model predictions and actuals. | **Multi-class Classification** <br><br>Tests the performance of a multi-class classification model against expectation. <br><br>Requirements: model predictions, true labels |
| **Binary Classification**<br><br>Tests the performance of a binary classification model against expectation. <br><br>Requirements: model predictions, true labels. | **Binary Classification top-K** <br><br>Tests the performance of a binary classification model at top-K against expectation. <br><br>Requirements: model predictions, true labels. |  |


# Individual Metrics and Tests

