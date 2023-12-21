In this tutorial, you will monitor a toy ML model using Evidently Cloud. 

It will take 3 minutes to launch a demo dashboard and 10 minutes to complete the tutorial for a new dataset. You must have basic knowledge of Python. 

# Part 1. Demo dashboard

## 1. Create an account

Evidently Cloud is currently in private beta. Once you get the registration link from us, create your login credentials and confirm the email.

To request a free trial, fill out [this form](https://www.evidentlyai.com/cloud-signup).

<details>

<summary>What can you do with Evidently Cloud?</summary>

In Evidently Cloud, you can:

* Monitor data quality, feature, and prediction drift over time.
* Track ML model quality for classification, regression, ranking, and recommendations. This includes assessing models in champion/challenger and shadow mode.
* Keep an eye on text data (e.g., sentiment, drift, trigger words) for NLP and LLM models by tracking inputs and output properties.
* Monitor embeddings drift.
* Track the results of test suites that include multiple evaluations.

Evidently computes and visualizes 100+ pre-built metrics and tests. You can customize them or add your metrics.

You can conduct evaluations in batch mode, e.g., hourly, daily, weekly, or on demand. You can also monitor data directly from a live ML service for near real-time insights.

Evidently Cloud uses the open-source [Evidently Python library](https://github.com/evidentlyai/evidently) for tests and metric computation. All evaluations are open-source.
</details>

## 2. View a demo project 

After you log in, you will see an empty dashboard. Click on "Generate Demo Project" to see a pre-built example dashboard.

![](../.gitbook/assets/cloud/generate_demo_project.png)

It will take a few moments to generate sample data and load the project. You can then see a sample dashboard wih different tabs and panels that show data quality, data drift and model quality for a regression model. You can customize your choice of panels - this is just an example.

![](../.gitbook/assets/cloud/demo_dashboard.gif)

Now, let's see how you can create something similar for your project!

# Part 2. New project.

You will now create a dashboard to monitor data quality and drift. You will use a toy dataset to imitate a production ML model.

You will go through the following steps:
* Prepare the tabular dataset.
* Compute the data quality and data drift reports in daily batches.
* Send them to the Evidently Cloud.
* Create simple dashboards to visualize metrics in time.
* (Optional) Run test suites to perform conditional tests.
