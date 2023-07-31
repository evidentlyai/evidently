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

## Project parameters

You can pass the following parameters to a project:

| Parameter | Description |
|---|---|
| `name: str` | Project name. |
| `id: UUID4 = Field(default_factory=uuid.uuid4)` | Unique identifier of the project. Assigned automatically. |
| `description: Optional[str] = None` | Optional description. It will be visible in the interface when you browse projects. |
| `dashboard: DashboardConfig` | Configuration of the project dashboard. It describes the monitoring panels which will appear on the dashboard.<br><br>**Note**: Explore [this Add Dashboard](add_dashboard.md) section for details. There is no need to explicitly pass `DashboardConfig` as a parameter if you use the `.dashboard.add_panel` method. |
| `date_from: Optional[datetime.datetime] = None` | Start DateTime of the monitoring dashboard. By default, Evidently will show all available periods based on the snapshot timestamps. <br><br>You can set a specific date or a relative DateTime. For example, to refer to the last 30 days:<br>`from datetime import datetime, timedelta`<br>`datetime.now() + timedelta(-30)`<br>When you view the dashboard, the data will be visible from this start date. You can switch to other dates in the interface. |
| `date_to: Optional[datetime.datetime] = None` | End datetime of the monitoring dashboard. <br>Works the same as above. |

## Save project

To save changes made to a project, you must use the method `save()`. 

For instance, after you create a project, add a name and description, and define monitoring panels, you must save the project to record the changes in the workspace. 

```python
project.save()
```

{% hint style="info" %}
**Designing monitoring panels.** To understand how to design monitoring panels, head to this [section](add_panels.md) in the docs.
{% endhint %}
