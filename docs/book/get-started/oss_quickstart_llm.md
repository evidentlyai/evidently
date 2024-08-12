---
description: Run your first LLM evaluation using Evidently open-source.
---

This quickstart shows how to run evaluations over text data: for example, inputs and outputs of your LLM system. 

You can run this example in Colab or any Python environment.

# 1. Installation

Install the Evidently Python library. 

```python
!pip install evidently[llm]
```

Import the necessary components:

```python
import pandas as pd
from evidently.report import Report
from evidently.metric_preset import TextEvals
from evidently.descriptors import *
```

# 2. Create a toy dataset 

To run the evals, prepare your data as a pandas dataframe. It can contain multiple texts and metadata columns. 

Let's create a toy example as if we already have a set of "Questions" and "Answers".

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

**Note**: To collect the inputs and outputs from the live LLM app, you can use the open-source **tracely** library. 

# 3. Run your first eval

Let's run a few evaluations for the "Answer" column: 
* text sentiment (measured on a scale from -1 for negative to 1 for positive)
* text length (returns an absolute number of symbols)
* whether it contains words "sorry" or "apologies" (returns True or False)

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

There are multiple built-in evals to choose from. You can also create custom ones, including LLM-as-a-judge. We call the result of each such evaluation a `descriptor`. 

View the Report in Python:

```
text_evals_report
```

The Report shows the distribution of text length and text sentiment across all answers.

You can also export the dataset with descriptors added to each indiviudal row.

```
text_evals_report.datasets().current
```


# Want to see more?

Check out a more in-depth tutorial to learn key workflows. It covers using LLM-as-a-judge, running conditional Test Suites, monitoring results over time, and more.

{% content-ref url="../examples/tutorial-llm.md" %}
[Evidently LLM Tutorial](../examples/tutorial-llm.md). 
{% endcontent-ref %}
