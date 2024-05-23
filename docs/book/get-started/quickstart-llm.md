---
description: LLM evaluation “Hello world.” Open-source and cloud workflow.
---

# 1. Installation

Install the Evidently Python library. You can run this example in Colab or any Python environment.

```
!pip install evidently
```

Import the necessary components:

```python
import pandas as pd
from sklearn import datasets
from evidently.report import Report
from evidently.metric_preset import TextEvals

import nltk
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')
```

**Optional**. Import components to send evaluation results to Evidently Cloud:

```python
from evidently.ui.workspace.cloud import CloudWorkspace
```

# 2. Import the toy dataset 

Import a toy dataset with e-commerce reviews. 

```python
reviews_data = datasets.fetch_openml(name='Womens-E-Commerce-Clothing-Reviews', version=2, as_frame='auto')
reviews = reviews_data.frame[:100]
```
# 3. Run the evals

Run basic numeric evaluations to check text sentiment (on a scale of -1 to 1), text length, etc., for the "Reviews" column.

```
text_evals_report = Report(metrics=[
    TextEvals(column_name="Review_Text")
    ]
)

text_evals_report.run(reference_data=None, current_data=reviews)
```

This runs a pre-built set of checks. You can pick others or create custom evaluations, including LLM-as-a-judge.

View a Report in Python:

```
text_evals_report
```

You can export results as HTML, JSON, or a Python dictionary to use elsewhere, or send to Evidently Cloud for monitoring.

# 4. Send results to Evidently Cloud 

To record and track evaluation results over time, send them to Evidently Cloud. You need an API key.
* Sign up for [an Evidently Cloud account](https://app.evidently.cloud/signup).
* Once you log in, click "plus" to create a new Team. For example, "Personal". Copy the team ID from [Team's page](https://app.evidently.cloud/teams).
* Click the key icon in the left menu, select "personal token," generate and save the token.

Connect to Evidently Cloud using your token and create a Project inside your Team:

```python
ws = CloudWorkspace(token="YOUR_TOKEN_HERE", url="https://app.evidently.cloud")

project = ws.create_project("My test project", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```

Visit Evidently Cloud, open your Project, and navigate to the "Report" to see evaluation results.

![](../.gitbook/assets/cloud/toy_text_report_preview.gif)

In the future, you can log ongoing evaluation results to build monitoring panels and send alerts.

# Want to see more?

Check out a more in-depth tutorial to learn key workflows. It covers using LLM-as-a-judge, running conditional test suites, and more.

{% content-ref url="tutorial-cloud.md" %}
[Evidently LLM Tutorial](tutorial-llm.md). 
{% endcontent-ref %}
