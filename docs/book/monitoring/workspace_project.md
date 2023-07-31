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
