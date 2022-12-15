---
description: An overview of the types of analysis you can do with Evidently. 
---

Evidently has several pre-built reports and test suites. We call them `presets`. Each preset evaluates or tests a particular aspect of the data or model quality. 

This page links to the description of each preset. If you want to see the code and interactive examples instead in Jupyter notebook or Colab, head here instead:

{% content-ref url="../get-started/examples.md" %}
[Examples](../get-started/examples.md). 
{% endcontent-ref %}

# Metric Presets
Data Quality

Evaluates the dataset statistics and feature behavior overview. Requirements: model inputs.

Data Drift

Explores the distribution shift between two datasets. Requirements: model inputs, a reference dataset. 

Target Drift

Explores the distribution shift in the model predictions. Requirements: model predictions and/or target values; a reference dataset. 

Classification

Evaluates the classification model quality and errors. Requirements: model predictions and true labels.

Regression 

Evaluates the regression model quality and errors. Requirements: model predictions and actuals.

# Test Presets

NoTargetPerformance 

Tests the model performance when you do not have ground truth or actuals. Includes several checks for data quality, integrity, and drift. Requirements: model inputs, predictions, a reference dataset.

Data Quality

Tests the dataset for quality issues like missing data, duplicates, or constant features. Requirements: model inputs.

Data Stability

Tests if the batch is similar to the previous one. Tests data schema, column types, value ranges. Requirements: model inputs, a reference dataset.

Data Drift

Tests for distribution drift per column and overall dataset drift. Requirements: model inputs, a reference dataset.

Regression

Tests the performance of the regression model against expectation. Requirements: model predictions, actuals.

Multi-class Classification

Tests the performance of a multi-class classification model against expectation. Requirements: model predictions, true labels.

Binary Classification

Tests the performance of a binary classification model against expectation. Requirements: model predictions, true labels.

Binary Classification top-K

Tests the performance of a binary classification model at top-K against expectation. Requirements: model predictions, true labels.


# Individual Metrics and Tests

