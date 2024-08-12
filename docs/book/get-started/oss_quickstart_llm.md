---
description: Run your first LLM evaluation using Evidently open-source.
---

This quickstart shows how to evaluate text data, such as inputs and outputs from your LLM system.

You can run this in Colab or any Python environment.

# 1. Installation

Install the Evidently library. 

```python
!pip install evidently[llm]
```

Import the required modules:

```python
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import TextEvals
from evidently.descriptors import *
```

# 2. Create a toy dataset 

Prepare your data as a pandas dataframe, with any texts and metadata columns. Here’s a toy example with chatbot "Questions" and "Answers":

```python
data = [
    ["What's the capital of France?", "The capital of France is Paris."],
    ["Who wrote 1984?", "George Orwell wrote 1984."], 
    ["How does photosynthesis work?", "Photosynthesis is a process where plants use sunlight to convert carbon dioxide and water into glucose and oxygen."],
    ["Can you give me the recipe for making pancakes?", "Sure! Here's a simple recipe: mix 1 cup flour, 1 cup milk, 1 egg, and a pinch of salt. Cook on a hot griddle until golden brown."],
    ["What is the largest planet in our solar system?", "Jupiter is the largest planet in our solar system."],
    ["Tell me a joke.", "Why don't scientists trust atoms? Because they make up everything!"],
    ["Can you translate 'Hello' into Spanish?", "'Hello' in Spanish is 'Hola'."],
    ["What's the code to the universe?", "I'm sorry, I can't provide that information."],
    ["What's the distance between Earth and the Sun?", "The average distance between Earth and the Sun is about 93 million miles or 150 million kilometers."],
    ["How do I fix a flat tire?", "To fix a flat tire, you'll need to locate the puncture, remove the tire, patch the hole, and then re-inflate the tire."]
]

columns = ["question", "answer"]

eval_dataset = pd.DataFrame(data, columns=columns)
```

**Note**: You can use the open-source `tracely` library to collect inputs and outputs from a live LLM app.

# 3. Run your first eval

Run evaluations for the "Answer" column:
* Sentiment (from -1 for negative to 1 for positive)
* Text length (number of symbols))
* Presence of "sorry" or "apologize" (True/False)

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="answer", descriptors=[
        Sentiment(),
        TextLength(),
        IncludesWords(words_list=['sorry', 'apologize'], display_name="Denials"),        
        ]
    ),
])

text_evals_report.run(reference_data=None, current_data=eval_dataset)
```

Each evaluation is a `descriptor`. You can choose from many built-in evaluations or create custom ones.

View the Report in Python to see the distribution of scores:

```
text_evals_report
```

You can also export the dataset with added descriptors for each row.

```
text_evals_report.datasets().current
```

# 4. Use LLM as a judge (Optional)

To run this, you'll need an OpenAI key.

Set the OpenAI key (it's best to pass it as an environment variable). [See Open AI docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) for best practices. 

```python
## import os
## os.environ["OPENAI_API_KEY"] = "YOUR KEY"
```

Run a Report with the new `DeclineLLMEval`. It checks for polite denials and labels responses as "OK" or "Denial" with an explanation.

This evaluator uses LLM-as-a-judge (defaults to `gpt-4o-mini`) and a template prompt.

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="answer", descriptors=[
        Sentiment(),
        TextLength(),
        DeclineLLMEval(),
        ]
    ),
])

text_evals_report.run(reference_data=None, current_data=evaluation_dataset)
```

View the Report in Python:

```
text_evals_report
```

View the dataset with scores and explanation:

```
text_evals_report.datasets().current
```

# What's next?

Explore the full tutorial for advanced workflows: custom LLM-as-a-judge, conditional Test Suites, monitoring, and more.

{% content-ref url="../examples/tutorial-llm.md" %}
[Evidently LLM Tutorial](../examples/tutorial-llm.md). 
{% endcontent-ref %}

Need help? Ask in our [Discord community](https://discord.com/invite/xZjKRaNp8b).
