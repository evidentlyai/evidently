---
description: Introduction to Projects in Evidently Platform. 
---   

{% hint style="success" %}
Projects are available in `Evidently OSS`, `Evidently Cloud` and `Evidently Enterprise`. 
{% endhint %}

**Note**: You can also run evaluations locally with the Evidently Python library without creating a Project. You need a Project only if you are using the Evidently web application.

# What is a Project?

To start working in the Evidently UI, you must create at least one evaluation or monitoring Project. 

**Home Page**. You can see all your Projects on the home page of the Evidently platform:

![](../.gitbook/assets/cloud/projects-min.png)

**Project Dashboard**. A Project helps you organize all data and evaluations for a specific use case. 

Each Project has its own Dashboard and alerting rules. Inside the Project, you can also access the results of all experimental evaluations, regression testing, or ongoing online monitoring. 

![](../.gitbook/assets/cloud/project_dashboard-min.png)

You can organize Projects in a way that suits your workflow, for example:
* create separate Projects for the experimental and production phases
* create separate Projects for each ML model or different components of an LLM-based application
* group evaluation results for different models / components within a single Project, but use Tags (such as model version, etc.) to differentiate between them.

Once you create a Project, it gets a unique ID. You can then connect via the Python API or through the UI to send data, edit the Dashboard, and manage the Project.
