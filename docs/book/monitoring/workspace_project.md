---
description: How to create monitoring workspaces and projects.
---   

To visualize data in the Evidently ML monitoring user interface, you must capture data and model metrics as Evidently JSON `snapshots`. 

To simplify log organization, you can create a `Workspace`. Practically, it defines a directory to store the `snapshots`. This directory will serve as a data source for the Evidently Monitoring UI service. By adding a `project` to the `workspace`, you can organize data for individual models.

{% hint style="info" %}
**Snapshots.** The next [section](snapshots.md) explains how the Evidently snapshots work.
{% endhint %}

# Code example

Refer to the ML Monitoring QuickStart for a complete Python script that shows how to create a workspace and a project and populate it with toy data. 

{% content-ref url="../get-started/tutorial-monitoring.md" %}
[Get started tutorial](../get-started/tutorial-monitoring.md). 
{% endcontent-ref %}

# Local workspace 

This section explains how to create a local workspace. In this scenario, you generate and store the snapshots on the same machine.

## Create a workspace 

To create a `workspace` and assign a name:
```python
my_workspace = Workspace.create(“evidently_ui_workspace”)
```
You can pass a `path` parameter to specify the path to a local directory.

## Create a project

You can add a `project` to a `workspace`. A `project` helps gather all Reports and Test Suites associated with the same task in one place. 

Each `project` will have its dedicated dashboard in the monitoring interface. 

To create a project and assign a name:
```python
project = my_workspace.create_project(“project name”)
```

{% hint style="info" %}
**What to group into one project?** If snapshots belong to the same project, you can visualize the data from multiple snapshots on the same dashboard panel. You can create one project per ML model, but this is not a strict rule. For example, you can log the performance of a model deployed in shadow mode to the same project as an active model. Or, you can store data on multiple related models together. In this case, you can use tags to organize them. 
{% endhint %}

## Project parameters. 

You can pass the following parameters to a project:
