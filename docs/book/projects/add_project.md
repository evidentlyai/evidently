---
description: Set up a Project for your evaluation or monitoring use case.
---   

Before creating a Project, you need a workspace.

* In Evidently Cloud, your account is your Workspace. [Set up an account and connect from Python](../installation/cloud_account.md).
* In self-hosted deployments, a Workspace is a remote or local directory. [Create a workspace](../installation/self_hosting.md).

# Create a Project

You can create a Project using the Python API or directly in the user interface.

## Add a new Project - API

{% hint style="success" %}
Team management is a Pro feature available in the Evidently Cloud.
{% endhint %}

To create a Project inside a workspace `ws` and Team with a `team_id`, assign a name and description, and save the changes:

```
project = ws.create_project("My test project", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```

In Evidently Cloud, you must create a Team before adding a Project. To get your Team ID, go to the [Teams page](https://app.evidently.cloud/teams), select your Team, and copy the ID from there.

In self-hosted open-source installation, you do not need to pass the Team ID. To create a Project:

```
project = ws.create_project("My test project")
project.description = "My project description"
project.save()
```

## Add a new Project - UI

Click on the “plus” sign on the home page, create a Team if you do not have one yet and type your Project name and description.

![](../.gitbook/assets/cloud/add_project_wide-min.png)

After creating a Project, you can click to open a Dashboard. Since there's no data yet, it will be empty. 

**Project ID**. Once you run `create_project`, you will see the Project ID. You can later use it to reference the Project. You can also copy the Project ID directly from the UI: it appears above the monitoring Dashboard.

# Manage Project

## Connect to a Project

To connect to an existing Project from Python, use the `get_project` method.

```python
project = ws.get_project("PROJECT_ID")
```

## Save changes

After making changes to the Project (such as editing description or adding monitoring Panels), always use the `save()` command:

```python
project.save()
```

## Browse Projects

You can see all available Projects on the monitoring homepage, or request a list programmatically. To get a list of all Projects in a workspace `ws`, use:

```python
ws.list_projects()
```

To find a specific Project by its name, use the `search_project` method: 

```python
ws.search_project("project_name")
```

## [DANGER] Delete Project 

{% hint style="danger" %}
**You are deleting the data in a Project**. If you delete a Project, you will delete all the associated snapshots stored in a Project.
{% endhint %}

{% tabs %}

{% tab title="API" %} 

To delete the Project and all the data inside it:

```
# ws.delete_project("PROJECT ID")
```

{% endtab %}

{% tab title="UI" %} 

Go to the "home page", and hover over a Project name. Click on the bin sign and confirm that you want to delete the Project.

{% endtab %}

{% endtabs %}

# Project parameters

Each Project has the following parameters.

| Parameter | Description |
|---|---|
| `name: str` | Project name. |
| `id: UUID4 = Field(default_factory=uuid.uuid4)` | Unique identifier of the Project. Assigned automatically. |
| `description: Optional[str] = None` | Optional description. Visible when you browse Projects. |
| `dashboard: DashboardConfig` | Dashboard configuration that describes the composition of the monitoring Panels.<br><br>**Note**: See [Dashboard Design](../monitoring/design_dashboard_api.md) for details. You don't need to explicitly pass `DashboardConfig` if you use the `.dashboard.add_panel` method to add Panels. |
| `date_from: Optional[datetime.datetime] = None` | Start DateTime of the monitoring Dashboard. By default, Evidently shows data for all available periods based on the snapshot timestamps. <br><br>You can set a different DateTime. E.g., to refer to the last 30 days:<br>`from datetime import datetime, timedelta`<br>`datetime.now() + timedelta(-30)`|
| `date_to: Optional[datetime.datetime] = None` | End DateTime of the monitoring Dashboard. <br>Works the same as above. |

# What’s next?

Once you create or connect to a Project, you can:
* [Send snapshots](../dashboard/snapshots.md) using the `add_report` or `add_test_suite` methods. 
* Configure the monitoring Dashboard in the [user interface](../dashboard/add_dashboard_tabs.md) or via the [Python API](../monitoring/design_dashboard_api.md).
