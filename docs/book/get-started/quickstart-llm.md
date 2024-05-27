---
description: LLM evaluation "Hello world." 
---

You can run this example in Colab or any Python environment.

# 1. Installation

Install the Evidently Python library. 

```
!pip install evidently[llm]
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

Import a toy dataset with e-commerce reviews. It contains a column with "Review_Text" that you'll analyze.

```python
reviews_data = datasets.fetch_openml(name='Womens-E-Commerce-Clothing-Reviews', version=2, as_frame='auto')
reviews = reviews_data.frame[:100]
```

# 3. Run the evals

Run an evaluation Preset to check basic text descriptive text properties:
* text sentiment (scale -1 to 1)
* text length (number of symbols)
* number of sentences in a text 
* percentage of out-of-vocabulary words (scale 0 to 100)
* percentage of non-letter characters (scale 0 to 100)

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="Review_Text")
    ]
)

text_evals_report.run(reference_data=None, current_data=reviews)
```

There are more evals to choose from. You can also create custom ones, including LLM-as-a-judge.

View a Report in Python:

```
text_evals_report
```

You will see a summary distribution of results for each evaluation.

# 4. Send results to Evidently Cloud 

To record and monitor evaluations over time, send them to Evidently Cloud. You'll need an API key.
* Sign up for an [Evidently Cloud account](https://app.evidently.cloud/signup), and create your Organization.
* Click on the **Teams** icon on the left menu. Create a Team - for example, "Personal". Copy and save the team ID. [Team page](https://app.evidently.cloud/teams).
* Click the **Key** icon in the left menu to go. Generate and save the token. [Token page](https://app.evidently.cloud/token).

Connect to Evidently Cloud using your token.

```python
ws = CloudWorkspace(token="YOUR_TOKEN_HERE", url="https://app.evidently.cloud")
```

Create a Project inside your Team. Pass the `team_id`:

```python
project = ws.create_project("My test project", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```

Send the Report to the Cloud: 

```python
ws.add_report(project.id, text_evals_report)
```

Go to the Evidently Cloud. Open your Project and head to the "Reports" in the left menu. [Cloud home](https://app.evidently.cloud/).

![](../.gitbook/assets/cloud/toy_text_report_preview.gif)

In the future, you can log ongoing evaluation results to build monitoring panels and send alerts.

# Want to see more?

Check out a more in-depth tutorial to learn key workflows. It covers using LLM-as-a-judge, running conditional test suites, monitoring results over time and more.

{% content-ref url="tutorial-llm.md" %}
[Evidently LLM Tutorial](tutorial-llm.md). 
{% endcontent-ref %}
