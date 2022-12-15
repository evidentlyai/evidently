---
description: An overview of the evaluations you can do with Evidently. 
---

Evidently has several pre-built reports and test suites. We call them **Presets**. Each preset evaluates or tests a particular aspect of the data or model quality. 

This page links to the **description** of each preset. If you want to see the code and interactive examples instead in Jupyter notebook or Colab, head here :

{% content-ref url="../get-started/examples.md" %}
[Examples](../get-started/examples.md). 
{% endcontent-ref %}

# Metric Presets

Metric presets are **pre-built reports** that help with visual exploration, debugging and documentation of the data and model performance.

|         |                                                        |   |
| ------- | ------------------------------------------------------ | - |
| [**Data Quality**](data-quality.md)<br><br>Shows the dataset statistics and feature behavior. <br><br> **Requirements**: model inputs. | [**Data Drift**](data-drift.md)<br><br>Explores the distribution shift in the model features. <br><br>**Requirements**: model inputs, a reference dataset. | [**Target Drift**](target-drift.md)<br><br>Explores the distribution shift in the model predictions. <br><br>**Requirements:** model predictions and/or target, a reference dataset. |
| [**Classification**](class-performance.md)<br><br>Evaluates the classification model quality and errors. <br><br>**Requirements**: model predictions and true labels. | [**Regression**](reg-performance.md)<br><br>Evaluates the regression model quality and errors. <br><br>**Requirements**: model predictions and actuals. |  |

# Test Presets

Test presets are **pre-built test suites** that perform structured data and model checks as part of the pipeline.

|         |                                                        |   |
| ------- | ------------------------------------------------------ | - |
| [**NoTargetPerformance**](no-target-performance.md)<br><br>Tests the model performance without ground truth or actuals. <br><br> **Requirements**: model inputs, predictions, a reference dataset. | [**Data Quality**](data-quality.md#data-quality-test-suite)<br><br>Tests if the data quality is suitable for training. Checks nulls, duplicates, etc. <br><br> **Requirements**: model inputs. | [**Data Stability**](data-quality.md#data-stability-test-suite)<br><br>Tests if a batch is similar to the previous one. Checks schema, column types, value ranges.  <br><br>**Requirements**: model inputs, a reference dataset. |
| [**Data Drift**](data-drift.md#data-drift-test-suite)<br><br>Tests for distribution drift per column and overall dataset drift. <br><br>**Requirements**: model inputs, a reference dataset. | [**Regression**](reg-performance.md#regression-performance-test-suite) <br><br>Tests the performance of the regression model against expectation. <br><br>**Requirements**: model predictions and actuals. | [**Multi-class Classification**](class-performance.md#classification-performance-test-suite)<br><br>Tests the performance of a multi-class classification model against expectation. <br><br>**Requirements**: model predictions, true labels.|
| [**Binary Classification**](class-performance.md#classification-performance-test-suite)<br><br>Tests the performance of a binary classification model against expectation. <br><br>**Requirements**: model predictions, true labels. | [**Binary Classification top-K**](class-performance.md#classification-performance-test-suite) <br><br>Tests the performance of a binary classification model at top-K. <br><br>**Requirements**: model predictions, true labels. |  |


# Individual Metrics and Tests

You can also create custom test suites and reports from individual metrics and tests. You can explore 100+ [available tests](../reference/all-tests.md) and [metrics](../reference/all-metrics.md).
