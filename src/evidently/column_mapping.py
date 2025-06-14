"""
column_mapping.py

This module defines the ColumnMapping class, which is used to specify the semantic roles
of columns in a dataset for evaluation purposes. This includes identifying the target column,
prediction column, numerical features, categorical features, and other metadata required
for accurate monitoring and testing of machine learning models.

ColumnMapping is used throughout Evidently to help interpret the input data correctly
when generating Reports, Test Suites, or monitoring dashboards.

Typical usage includes specifying:
- The column containing true labels (target).
- The column with model predictions.
- Which features are numerical or categorical.
- Optional text or datetime columns.

This structure ensures consistency and flexibility across different kinds of evaluations,
whether for tabular ML models or LLM-based systems.
"""
