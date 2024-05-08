---
description: How to create a Project for your monitoring use case.
---   

# What is a Project?

A Project helps gather all Reports and Test Suites associated with the same use case. Each Project has a dedicated monitoring dashboard and snapshot storage.

{% hint style="info" %}
**Should you have one Project for one ML model?** You will often create one project per ML model or dataset, but this is not a strict rule. For example, you can log the performance of a champion and challenger models to the same Project. Or, store data on related models (such as demand forecasting models by country) in one Project and use tags to organize them. You can also set up your monitoring for any data pipeline or dataset.
{% endhint %}

Once you create a Project, you can connect to it from your Python environment to send the data or edit the dashboards. In Evidently Cloud, you can work both via API and a graphic user interface.

# Create a Project

## Add a new Project

{% tabs %}

{% tab title="API" %} 

To create a Project inside a workspace `ws`, assign a name and description, and save the changes:

```
project = ws.create_project("My project name")
project.description = "My project description"
project.save()
```

{% endtab %}

{% tab title="UI" %} 

Click on the “plus” sign on the home page and type your Project name and description.

![](../.gitbook/assets/cloud/add_project_wide-min.png)

After creating a Project, you can click to open a Dashboard. Since there's no data yet, it will be empty. 

{% endtab %}

{% endtabs %}

**Project ID**. Once you run `create_project`, you will see the Project ID. You can later use it to reference the Project. You can also copy the Project ID directly from the UI: it appears above the monitoring dashboard.

## Add a Team Project

{% hint style="success" %}
Team management is a Pro feature available in the Evidently Cloud.
{% endhint %}

You can associate a Project with a particular Team, such as a "Marketing team" for related ML models. A Project inside the Team will be visible to all Team members. 

You must create a Team before adding a Project. Navigate to the “Teams” section in the left menu, and add a new one. You can add other users to this Team at any point after creating it.

{% tabs %}

{% tab title="API" %} 

After creating the team, copy the `team_ID` from the team page. To add a Project to a Team, reference the team_id when creating the Project:

```
project = ws.create_project("Add your project name", team_id="TEAM ID")
project.description = "Add your project description"
project.save()
```

{% endtab %}

{% tab title="UI" %} 

Click on the “plus” sign on the home page and type your Project name and description. Select the team name from the dropdown menu to add a Project to a team.

![](../.gitbook/assets/cloud/add_project_wide-min.png)

{% endtab %}

{% endtabs %}

{% hint style="info" %}
**What's next?** Head to the next section to see how to [send data to a Project](snapshots.md).
{% endhint %}

## Connect to a Project

To connect to an existing Project from your Python environment (for example, if you first created the Project in the UI and now want to send data to it), use the `get_project` method.

```python
project = ws.get_project("PROJECT_ID")
```

## Save changes

After you make any changes to a Project via API (such as editing description or adding new monitoring panels), you must use the `save()` command:

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

# [DANGER] Delete Project 

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

Go to the "home page", and hover over a Project name. Click on the bin sign and confirm that you want to delte the Project.

{% endtab %}

{% endtabs %}

# What’s next?

Once you create or connect to a Project, you can:
* [Send snapshots](snapshots.md) using the `add_report` or `add_test_suite` methods. 
* [Configure the monitoring dashboard](design_dashboard.md) in the user interface or specify the `DashboardConfig`.

