---
description: LLM evaluation "Hello world." 
---

This quickstart shows how to run evaluations over text data, such as inputs and outputs of your LLM system. 

You will run evaluations locally in your Python environment and send results to Evidently Cloud for analysis and monitoring.

# 1. Set up Evidently Cloud 

Set up your Evidently Cloud workspace:
* **Sign up**. If you do not have one yet, sign up for an [Evidently Cloud account](https://app.evidently.cloud/signup).
* **Create an Organization**. When you log in the first time, create and name your Organization.
* **Create a Team**. Click **Teams** in the left menu. Create a Team, copy and save the Team ID. ([Team page](https://app.evidently.cloud/teams)).
* **Get your API token**. Click the **Key** icon in the left menu. Generate and save the token. ([Token page](https://app.evidently.cloud/token)).

You can now go to your Python environment.

# 2. Installation

Install the Evidently Python library. 

```python
!pip install evidently[llm]
```

Import the components to run the evals:

```python
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import TextEvals
from evidently.descriptors import *
```

Import the components to connect with Evidently Cloud:

```python
from evidently.ui.workspace.cloud import CloudWorkspace
```

# 3. Create a Project

**Connect to Evidently Cloud**. Pass the Evidently API token you generated earlier: 

```python
ws = CloudWorkspace(token="YOUR_API_TOKEN", url="https://app.evidently.cloud")
```

**Create a Project**. Create a new evaluation Project inside your Team, adding your title and description:

```python
project = ws.create_project("My test project", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```

# 4. Import the toy dataset 

To run the evals, you must prepare your data as a pandas dataframe. It can contain multiple texts and metadata columns.

Let's create a toy chatbot dataset as if we already have a set of "Questions" and "Answers".

```python
data = [
    ["What is the chemical symbol for gold?", "The chemical symbol for gold is Au."],
    ["What is the capital of Japan?", "The capital of Japan is Tokyo."],
    ["Tell me a joke.", "Why don't programmers like nature? It has too many bugs!"],
    ["What is the boiling point of water?", "The boiling point of water is 100 degrees Celsius (212 degrees Fahrenheit)."],
    ["Who painted the Mona Lisa?", "Leonardo da Vinci painted the Mona Lisa."],
    ["What’s the fastest animal on land?", "The cheetah is the fastest land animal, capable of running up to 75 miles per hour."],
    ["Can you help me with my math homework?", "I'm sorry, but I can't assist with homework. You might want to consult your teacher for help."],
    ["How many states are there in the USA?", "There are 50 states in the USA."],
    ["What’s the primary function of the heart?", "The primary function of the heart is to pump blood throughout the body."],
    ["Can you tell me the latest stock market trends?", "I'm sorry, but I can't provide real-time stock market trends. You might want to check a financial news website or consult a financial advisor."]
]

# Columns
columns = ["question", "answer"]

# Creating the DataFrame
evaluation_dataset = pd.DataFrame(data, columns=columns)

```
{% hint style="info" %}
**How to collect the real data?** To collect the inputs and outputs from the live LLM app, you can use the open-source `tracely` library. Check the [Tracing Quickstart](cloud_quickstart_tracing.md). 
{% endhint %}

# 5. Run your first eval

You can choose between two options.
* Run the evals using only methods that work locally.
* Run the evals using LLM-as-a-judge. This will require an OpenAI token. 

{% tabs %}

{% tab title="Only local methods" %} 

Let's run a few evaluations for all "Answers". You will check: 
* text sentiment (measured on a scale from -1 for negative to 1 for positive)
* text length (returns an absolute number of symbols)
* presence of words "sorry" or "apologize" (returns a binary "True" or "False")

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="answer", descriptors=[
        Sentiment(),
        TextLength(),
        IncludesWords(words_list=['sorry', 'apologize'], display_name="Denials"),
        ]
    ),
])

text_evals_report.run(reference_data=None, current_data=evaluation_dataset)
```

{% endtab %}

{% tab title="LLM as a judge" %}

**Pass the OpenAI key**. It is recommended to pass the key as an environment variable. [See Open AI docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) for best practices. 

```python
## import os
## os.environ["OPENAI_API_KEY"] = "YOUR KEY"
```
Run a few evaluations for all "Answers". You will check: 
* text sentiment (measured on a scale from -1 for negative to 1 for positive)
* text length (returns an absolute number of symbols)
* whether the chatbot denied an answer (returns "OK" or "Denial" labels with an explanation). This evaluator will use LLM-as-a-judge (defaults to `gpt-4o-mini`) with a template Evidently-provided prompt.  

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="answer", descriptors=[
        Sentiment(),
        TextLength(),
        DeclineLLMJudge(),
        ]
    ),
])

text_evals_report.run(reference_data=None, current_data=evaluation_dataset)
```

{% endtab %}

{% endtabs %}

There are multiple evals to choose from. You can also create custom ones, including LLM-as-a-judge. We call the result of each such evaluation a `descriptor`. 

# 6. Send results to Evidently Cloud 

**Upload the Report**. Include the raw data so that you can analyze the scores row by row: 

```python
ws.add_report(project.id, text_evals_report, include_data=True)
```

**View the Report**. Go to the Evidently Cloud. Open your Project and head to the "Reports" in the left menu. ([Cloud home](https://app.evidently.cloud/)).

You will see the summary statistics for all scores, as well as the evaluated dataset with descriptor. For example, you can sort to find all answers with "Denials".

![](../.gitbook/assets/cloud/qs_denials.png)

# 7. Get a dashboard 

Go to the "Dashboard" tab and enter the "Edit" mode. Add a new tab, and select the "Descriptors" template.

You'll see a set of panels that show descriptor values. Each has a single data point. As you log ongoing evaluation results, you can track trends and set up alerts. 

![](../.gitbook/assets/cloud/add_descriptor_tab.gif)

# What's next?

Check out a more in-depth tutorial to learn key workflows. It covers building custom LLM judges, running conditional test suites, monitoring results over time, and more.

{% content-ref url="../examples/tutorial-llm.md" %}
[Evidently LLM Tutorial](../examples/tutorial-llm.md). 
{% endcontent-ref %}

Need help? Ask in our [Discord community](https://discord.com/invite/xZjKRaNp8b).