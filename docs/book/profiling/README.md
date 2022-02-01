---
description: How to profile ML models and data.
---

# JSON Profiles

## Overview

To get the calculation results as a JSON file, you should create a **Profile**.

JSON profiles help integrate Evidently in your prediction pipelines. For example, you can log and store JSON profiles for further analysis, or build a conditional workflow based on the result of the check (e.g. to trigger alert, retraining, or generate a visual report). 

The profiles calculate the same metrics and statistical tests as visual reports. You can think about profiles as "JSON versions" of the Evidently dashboards. 

To specify which analysis you want to perform, you should select a **Section**. You can combine several sections in a single Profile. Each section will contain a summary of metrics, results of statistical tests, and simple histograms that correspond to the chosen [Report](../reports/).

You can generate JSON profiles in Jupyter notebook, Colab and certain other notebooks, or use the command-line interface. 

The requirements for the data inputs and column_mapping are the same for Profiles and Dashboards.

You can also explore specific [integrations](../integrations) to see how Evidently works with other ML tools.

## Supported environments

You can generate profiles in Jupyter notebook and other notebook environments, and in Command-Line interface.
