---
description: What is a Project.
---   

{% hint style="info" %}
This feature is available in <mark style="color:black;background-color:lightgray;">Evidently OSS UI</mark>, <mark style="color:white;background-color:darkred;">Evidently Cloud</mark>, <mark style="color:white;background-color:mediumpurple;">Evidently Enterprise</mark>.
You can run evaluations locally with Evidently Python library without creating a Project.
{% endhint %}

# What is a Project?

To start using the Evidently web application, you must create at least one Project.

A Project helps you organize all data, Reports, and Test Suites related to a specific use case. Each Project has its own Dashboard, alerting rules and is clearly separated from others in the interface.

A Project can include results from experimental evaluations, regression testing, or ongoing online monitoring. You can organize Projects in a way that suits your workflow: for example, by creating separate Projects for the experimental and production phases, individual Projects for each ML model, or for different components of an LLM-based application. Alternatively, you can group the results within a single Project, using Tags (such as model version, A/B test status, or other dimensions) to differentiate between evaluation results on the dashboard.

Once you create a Project, it gets a unique ID. You can then connect via the Python API or through the UI to send data, edit the Dashboard, and manage the Project.
