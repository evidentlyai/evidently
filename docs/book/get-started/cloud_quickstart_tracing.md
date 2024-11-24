---
description: LLM tracing "Hello world." 
---

This quickstart shows how to instrument a simple LLM app to send inputs and outputs to Evidently Cloud. You will use the open-source **Tracely** library.

You will need an OpenAI key to create a toy LLM app.

Need help? Ask on [Discord](https://discord.com/invite/xZjKRaNp8b).

# 1. Set up Evidently Cloud 

Set up your Evidently Cloud workspace:
* **Sign up**. If you do not have one yet, sign up for a free [Evidently Cloud account](https://app.evidently.cloud/signup).
* **Create an Organization**. When you log in the first time, create and name your Organization.
* **Create a Project**. Click **+** button under Project List.  Create a Project, copy and save the Project ID. ([Projects page](https://app.evidently.cloud/))
* **Get your API token**. Click the **Key** icon in the left menu. Generate and save the token. ([Token page](https://app.evidently.cloud/token)).

You can now go to your Python environment.

# 2. Installation

Install the Tracely library to instrument your app:

```python
!pip install tracely
```

Install the Evidently library to interact with Evidently Cloud:

```python
!pip install evidently
```

Install the OpenAI library to create a toy app:

```python
!pip install openai
```

Imports:
```python
import os
import openai
import time
from tracely import init_tracing
from tracely import trace_event
```

# 2. Initialize Tracing

Initialize the OpenAI client. Pass the token as an environment variable:

```python
# os.environ["OPENAI_API_KEY"] = "YOUR_KEY"
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

Set up tracing parameters. Copy the Team ID from the [Teams page](https://app.evidently.cloud/teams), and give a name to identify your tracing dataset.

```python
init_tracing(
    address="https://app.evidently.cloud/",
    api_key="EVIDENTLY_API_KEY",
    project_id="YOUR_PROJECT_ID"
    export_name="LLM tracing example"
    )
```

# 3. Trace a simple function

Create a simple function to send questions to Open AI API and receive a completion. Set the questions list:

```python
question_list = [
    "What is Evidently Python library?",
    "What is LLM observability?",
    "How is MLOps different from LLMOps?"
]
```

Create a function and use the ```trace_event()``` decorator to trace it:

```python
@trace_event()
def pseudo_assistant(question):
    system_prompt = "You are a helpful assistant. Please answer the following question concisely."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]
    return client.chat.completions.create(model="gpt-4o-mini", messages=messages).choices[0].message.content

# Iterate over the list of questions and pass each to the assistant
for question in question_list:
    response = pseudo_assistant(question=question)
    time.sleep(1)
```

# 4. View Traces

Go to the Evidently Cloud, open Datasets in the left menu ([Datasets Page](https://app.evidently.cloud/datasets)), and view your Traces.

![](../.gitbook/assets/cloud/qs_tracing_dataset.png)

# What's next?

Want to run evaluations over this data? See a Quickstart. 

{% content-ref url="cloud_quickstart_llm.md" %}
[LLM Evaluation Quickstart](cloud_quickstart_llm.md). 
{% endcontent-ref %}

Check out a more in-depth tutorial to learn more about tracing:

{% content-ref url="../examples/tutorial_tracing.md" %}
[LLM Tracing Tutorial](../examples/tutorial_tracing.md). 
{% endcontent-ref %}
