---
description: Set up an Evidently Cloud account or self-hosted workspace.
---   
-----

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
| `dashboard: DashboardConfig` | Configuration of the project dashboard. It describes the monitoring panels which will appear on the dashboard.<br><br>**Note**: Explore the [Dashboard Design](design_dashboard.md) section for details. There is no need to explicitly pass `DashboardConfig` as a parameter if you use the `.dashboard.add_panel` method. |
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

## Log snapshots

Once you create a project within a workspace, you can add Reports, Test Suites, or `snapshots` to a project. 

Here is how you add a Report and Test Suite to an earlier created project.

```python
my_workspace.add_report(my_project.id, my_report)
my_workspace.add_test_suite(my_project.id, my_test_suite)
```

When you add a Report or a Test Suite to a project, Evidently will automatically save a `snapshot`. There is no need to generate a snapshot explicitly.  

If you already generated a snapshot, you can add it as well: 
```python
my_workspace.add_snapshot(my_project.id, snapshot.load("data_drift_snapshot.json")) 
```



# Workspace API Reference 

All available methods in the class Workspace:

```python
create_project(self, name: str, description: Optional[str] = None) 
add_project(self, project: ProjectBase) 
add_report(project.id, report)
add_test_suite(project.id, test_suite)
add_snapshot(self, project_id: Union[str, uuid.UUID], snapshot: Snapshot)
get_project(self, project_id: Union[str, uuid.UUID])
list_projects(self) 
search_project(self, project_name: str)
```



