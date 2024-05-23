---
description: ML Monitoring “Hello world.” From data to dashboard in a couple of minutes. 
---

# 1. Create an account  

If not already, [sign up for an Evidently Cloud account](https://app.evidently.cloud/signup).

# 2. Create a team 

Go to the main page, and click "plus" to create a new Team. For example, "Personal".

Copy and save the Team ID from the [Teams page](https://app.evidently.cloud/teams).

# 3. Get an access token

Click on the left menu with a key sign, select "personal token," generate and save the token.

# 4. Install the Python library

Install the Evidently Python library. You can run this example in Colab or another Python environment.

```
!pip install evidently
```

Import the components to work with the dataset and send the metrics. 

```python
import pandas as pd
from sklearn import datasets

from evidently.ui.workspace.cloud import CloudWorkspace
from evidently.report import Report
from evidently.metric_preset import DataQualityPreset
```

# 5. Create a new Project 

Connect to Evidently Cloud using your access token and create a Project inside your Team.

```python
ws = CloudWorkspace(token="YOUR_TOKEN_HERE", url="https://app.evidently.cloud")

project = ws.create_project("My test project", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```

# 6. Collect metrics

Import the demo "adult" dataset as a pandas DataFrame. 

```python
adult_data = datasets.fetch_openml(name="adult", version=2, as_frame="auto")
adult = adult_data.frame
```

Run a Data Quality Report and upload it to the Project.

```
data_report = Report(
       metrics=[
           DataQualityPreset(),
       ],
    )
data_report.run(reference_data=None, current_data=adult)
ws.add_report(project.id, data_report)
```

We call each such evaluation a `snapshot`.

# 7. View the Report

Visit Evidently Cloud, open your Project, and navigate to the "Report" tab to see the data stats.

![](../.gitbook/assets/cloud/qs_view_reports.gif)

# 8. Add a monitoring panel

Go to the "Dashboard" tab and enter the "Edit" mode. Add a new tab, and select the "Data quality" template.

![](../.gitbook/assets/cloud/qs_add_data_quality_tab_2.gif)

You'll see a set of panels with a single data point. As you send more snapshots, you can track trends and set up alerts. You can choose from 100+ metrics and tests on data quality, data drift, ML quality (regression, classification, ranking, recsys), LLM quality and text data, and add your own metrics.

# Want to see more?

Check out a more in-depth tutorial to learn the key workflows: 

{% content-ref url="tutorial-cloud.md" %}
[Evidently Cloud Tutorial](tutorial-cloud.md). 
{% endcontent-ref %}
