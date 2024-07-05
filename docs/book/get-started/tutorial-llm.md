---
description: Evaluate and test your LLM use case in 15 minutes. 
---

Evaluating quality of LLM outputs is a necessary part of building production-grade LLM application. You first need evaluation during development - to compare different prompts and detect regressions as you make changes. Once your app is live, you must run online evaluations to ensure the outputs are safe and accurate and understand user behavior.

Manually review of individual outputs doesn't scale. This tutorial shows how you can automate LLM evaluations from experiments to production.

You will learn both about different evaluation methods, and the workflow to run your evaluations and track results.

{% hint style="success" %}
**Want a very simple example first?** This ["Hello World"](quickstart-llm.md) will take a couple minutes.
{% endhint %}

In this tutorial, you will:
* Prepeare a toy chatbot dataset
* Evaluate responses using different methods:
    * Text statistics
    * Text patterns
    * Model-based evaluations
    * LLM-as-a-judge
    * Metadata analysis
* Generate visual Reports to explore the evaluation results
* Get a monitoring Dashboard to track results over time
* Build a custom Test Suite to run conditional checks

You can run this tutorial locally, with the option to use Evidently Cloud for monitoring dashboards. We'll use a Q&A chatbot as an example, but these methods apply to other use cases like RAGs and agents.

**Requirements:**
* Basic Python knowledge.
* The open-source Evidently Python library.

**Optional**:
* An OpenAI API key (to use LLM-as-a-judge).
* An Evidently Cloud account (for live monitoring).

Let's get started!

To complete the tutorial, use the provided code snippets or run a sample notebook.

Jupyter notebook:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/sample_notebooks/llm_evaluation_tutorial.ipynb" %}

Or click to [open in Colab](https://colab.research.google.com/github/evidentlyai/evidently/blob/main/examples/sample_notebooks/llm_evaluation_tutorial.pynb).

You can also follow the video version: {% embed url="https://youtu.be/qwn0UqXJptY" %}

# 1. Installation and imports

Install Evidently in your Python environment:

```python
!pip install evidently[llm]
```

Import the components to prepare the toy data:

```python
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from io import BytesIO
```

Import the components to run the evals:

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.metric_preset import TextEvals
from evidently.descriptors import *
from evidently.metrics import *
from evidently.tests import *
```

To be able to send results to Evidently Cloud:

```python
from evidently.ui.workspace.cloud import CloudWorkspace
```

**Optional**. To remotely manage the dashboard design in Evidently Cloud:

```python
from evidently.ui.dashboards import DashboardPanelTestSuite
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import ReportFilter
from evidently.ui.dashboards import TestFilter
from evidently.ui.dashboards import TestSuitePanelType
from evidently.renderers.html_widgets import WidgetSize
```

# 2. Prepare a dataset

We'll use a dialogue dataset that imitates a company Q&A system where employees ask questions about HR, finance, etc. You can download the [example CSV file](https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/chat_df.csv) from source, or import it using `requests`:

```python
response = requests.get("https://raw.githubusercontent.com/evidentlyai/evidently/main/examples/how_to_questions/chat_df.csv")
csv_content = BytesIO(response.content)
```

Convert it into the pandas DataFrame. Parse dates and set conversation "start_time" as index:

```python
assistant_logs = pd.read_csv(csv_content, index_col=0, parse_dates=['start_time', 'end_time'])
assistant_logs.index = assistant_logs.start_time
assistant_logs.index.rename('index', inplace=True)
```

To get a preview:

```python
pd.set_option('display.max_colwidth', None)
assistant_logs.head(3)
```

![](../.gitbook/assets/cloud/llm_data_preview-min.png)

{% hint style="success" %}
**How do I pass my own data?** You can import a pandas DataFrame with flexible structure. Include any text columns (e.g., inputs and responses), DateTime, and optional metadata like ID, feedback, model type, etc. If you have multi-turn conversations, parse them into a table by session or input-output pairs.
{% endhint %}

# 3. Create a Project 
{% hint style="info" %}
**This step is optional**. You can also run the evaluations locally without sending results to the Cloud. 
{% endhint %}

To be able to save and share results and get a live monitoring dashboard, create a Project in Evidently Cloud. Here's how to set it up:

* **Sign up**. If you do not have one yet, create a free [Evidently Cloud account](https://app.evidently.cloud/signup) and name your Organization.
* **Add a Team**. Click **Teams** in the left menu. Create a Team, copy and save the Team ID. ([Team page](https://app.evidently.cloud/teams)).
* **Get your API token**. Click the **Key** icon in the left menu to go. Generate and save the token. ([Token page](https://app.evidently.cloud/token)).
* **Connect to Evidently Cloud**. Pass your API key to connect. 

```python
ws = CloudWorkspace(token="YOUR_API_TOKEN", url="https://app.evidently.cloud")
```
* **Create a Project**. Create a new Project inside your Team, adding your title and description:

```python
project = ws.create_project("My сhatbot project", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```
# 4. Run evaluations

You will now learn how to apply different methods to evaluate your text data. 
* **Text statistics**. Evaluate simple properties like text length.
* **Text patterns**. Detect specific words or regular patterns.
* **Model-based evals**. Use ready-made ML models to score data (e.g., by sentiment).
* **LLM-as-a-judge**. Prompt LLMs to categorize or score texts by custom criteria.
* **Similarity metrics**. Measure semantic similarity between pairs of text.

To view the evaluation results, you will generate visual Reports in your Python environment. You will later explore other formats like Test Suite.

This section introduces different LLM evaluation methods one by one. Each section is self-contained, so you can freely skip any of them and head to Step 6 to see the end-to-end monitoring example.

## Text statistics 

Let's run a first simple evaluation to understand the basic flow.

**Create column mapping**. This optional step helps correctly parse the data schema. For example, pointing to a "datetime" column will add a time index to the plots.

```python
column_mapping = ColumnMapping(
    datetime='start_time',
    datetime_features=['end_time'],
    text_features=['question', 'response'],
    categorical_features=['organization', 'model_ID', 'region', 'environment', 'feedback'],
)
```

**Evaluate text length**. Let's generate a Report to evaluate the length of texts in the "response" column. You will run this check for the first 100 rows in the `assistant_logs` dataframe:

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="response",
              descriptors=[
                  TextLength(),
                  ]
              )
])

text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[:100],
                      column_mapping=column_mapping)
text_evals_report
```

This will calculate the number of symbols in each text and show a summary. You can see the distribution of text length across all responses, and statistics that help you understand e.g. the mean or minimal text length. 

![](../.gitbook/assets/cloud/llm_report_preview-min.gif) NEW IMAGE TO BE ADDED

If you click on "details", you can see the mean text length changes over time.  The index comes from the `datetime` column you mapped earlier. This can help notice any temporal patterns, like if texts are longer or shorter during specific periods.

![](../.gitbook/assets/cloud/llm_report_preview-min.gif) NEW IMAGE TO BE ADDED

**Get a side-by-side comparison**. You can also generate the statistics for two datasets at once. For example, you might want to compare the outputs of two different prompts, or production data from today against yesterday.

You must pass one dataset as `reference`, and another as `current`. For simplicity, let's compare the first 50 rows and next 100 from the same dataframe:


```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="response",
              descriptors=[
                  TextLength(),
                  ]
              )
])

text_evals_report.run(reference_data=assistant_logs[:50],
                      current_data=assistant_logs[50:100],
                      column_mapping=column_mapping)
text_evals_report
```

You will now see the results for both dataset at once:

![](../.gitbook/assets/cloud/llm_report_preview-min.gif) NEW IMAGE TO BE ADDED

Each such evaluation that computes a score for every text in the dataset is called as `descriptor`. Descriptors can be numerical (like the `TextLength()` you just used) or categorical. 

Evidently has a lot of built-in descriptors. For example, try other simple statistics like `SentenceCount()` or `WordCount()`. We'll show more complex examples below.  

{% hint style="success" %}
**List of all descriptors** See available descriptors in the "Descriptors" section of [All Metrics](https://docs.evidentlyai.com/reference/all-metrics) table. 
{% endhint %}

## Text patterns

You can use regular expressions to identify text patterns. For example, you check if the responses mentions competitors, named company products, include emails or specific topical words. Such descriptors return a binary score ("True" or "False") for pattern match.  

Let's check if responses contain words related to the topic of compensation (such as `salary', 'benefits' or 'payroll'). You can pass this word list to the `IncludesWords` descriptor. 

Add an optional display name for this eval:

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="response",
              descriptors=[
                  IncludesWords(
                      words_list=['salary', 'benefits', 'payroll'],
                      display_name="Mention Compensation")
            ]
        ),
        ]
)

text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[:100],
                      column_mapping=column_mapping)
text_evals_report
```

Here is an example result. You can see that 10 responses out of 100 indeed related to the topic of compensation as defined by this word list. "Details" show occurrences in time.

![](../.gitbook/assets/cloud/llm_mentions_salary-min.png) NEW IMAGE TO BE ADDED

Such pattern evals are fast and cheap to compute at scale. You can try other descriptors like `Contains(items=[])` (for non-vocabulary words like competitor names or longer expressions), `BeginsWith(prefix="")` (for specific starting sequence), custom `RegEx(reg_exp=r"")`, etc.

## Model-based scoring

You can use pre-trained machine learning model to score your texts. Evidently has:
* In-built model-based descriptors like `Sentiment`.
* Wrappers to call external models published on HuggingFace.

Let's start with a **Sentiment** check. This will return a sentiment score from -1 (very negative) to 1 (very positive).

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
            Sentiment(),
        ]
    ),
])

text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[:100],
                      column_mapping=column_mapping)
text_evals_report
```

You will see the distribution of sentiment in responses. While most are positive or neutral, in some instances the sentiment is below zero.

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

In "details", you can look at specific time when the average sentiment of responses dipped:

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

You might then want to look at specific responses with sentiment below zero. This is possible through the dataset export - we'll show this in the following tutorial section.

Let's first see how you can use external models from HuggingFace. You will use two options:
* **Pre-selected models**. Some of the models like **Toxicity** are pre-selected. You can simply pass the `HuggingFaceToxicityModel()` descriptor. This [model](https://huggingface.co/spaces/evaluate-measurement/toxicity) will return the predicted toxicity score between 0 to 1.
* **Custom models**. You can also call other named models, and specify the output (e.g., label or score) to use. In this case, you must parametrize the general `HuggingFaceModel` descriptor. Let's use it to call the `SamLowe/roberta-base-go_emotions` [model](https://huggingface.co/SamLowe/roberta-base-go_emotions) that classifies text into 28 emotions. We'll pick the "neutral" label. This means that the descriptor will return the predicted score from 0 to 1 on whether responses convey neutral emotion.

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
            HuggingFaceToxicityModel(),
            HuggingFaceModel(
                model="SamLowe/roberta-base-go_emotions",
                params={"label": "neutral"},
                display_name="Response Neutrality"),
        ]
    ),
])

text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[:100],
                      column_mapping=column_mapping)
text_evals_report
```


In each case, the descriptor will first download the model from HuggingFace to your environment and then use it to score the data. It will first take a few moments to load the model.

How to interpret the results? For such classifier models, it's typical to use predicted score above 0.5 as a "positive" label. You can notice that the predicted toxicity score is near 0 for all responses - nothing to worry about! For neutrality, you can see that while most responses have predicted scores above the 0.5 threshold, there are few that are below. You can further review them individually. 

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

{% hint style="info" %}
**Choosing other models**. You can choose other models, e.g. to score texts by topic. See [docs](../customization/llm_as_a_judge.md)  
{% endhint %}

## LLM as a judge

{% hint style="info" %}
**This step is optional**. You will neeed an OpenAI API key and incur costs by running the eval. Skip if you don't want to use external LLMs.  
{% endhint %}

For more complex or nuanced checks, you can use LLMs as a judge. This requires creating an evaluation prompt asking LLMs to assess the text by specific criteria, for example, tone or conciseness.

{% hint style="info" %}
**Recommended: pass the key as an environment variable**. [See Open AI docs](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety) on best practices. 
{% endhint %}

```python
## import os
## os.environ["OPENAI_API_KEY"] = "YOUR KEY"
```

To illustrate, let's create a prompt to ask the LLM to judge if the provided response are concise. 

```python
conciseness_prompt = """
Conciseness refers to the quality of being brief and to the point, while still providing all necessary information.

A concise response should:
- Provide the necessary information without unnecessary details or repetition.
- Be brief yet comprehensive enough to address the query.
- Use simple and direct language to convey the message effectively.

Please evaluate the following chatbot response for conciseness.

response: REPLACE

Use the following categories for conciseness evaluation:
CONCISE if the response is concise and to the point
VERBOSE if the response is overly detailed or contains unnecessary information
UNKNOWN if the information provided is not sufficient to make a clear determination

Return a category only
"""
```

Include an `OpenAIPrompting` descriptor to the Report, refering this prompt. We will pass only 10 lines of code to the current data to minimize API calls.

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        OpenAIPrompting(prompt=conciseness_prompt,
                        prompt_replace_string="REPLACE",
                        model="gpt-3.5-turbo-instruct",
                        feature_type="cat",
                        display_name="Response Conciseness"),
    ])
])

report.run(reference_data= None,
           current_data= assistant_logs[:10],
           column_mapping=column_mapping)

#report
```

All our responses are concise - great!

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

{% hint style="info" %}
**How to create your own judge**. You can create your own prompts, and optionally pass the context for scoring alongside the response. See [docs](../customization/huggingface_descriptor.md).  
{% endhint %}

## Metadata summary

Our dataset also includes user upvotes and downvotes in a categorical `feedback` column. You can easily add summaries for any numerical or categorical column in the Report.

To add a summary on the “feedback” column, use `ColumnSummaryMetric()`:

```python
data_report = Report(metrics=[
   ColumnSummaryMetric(column_name="feedback"),
   ]
)

data_report.run(reference_data=None, current_data=assistant_logs[:100], column_mapping=column_mapping)
data_report
```

You will see a distribution of upvotes and downvotes.

![](../.gitbook/assets/cloud/llm_feedback_one-min.png)

## Semantic Similarity

You can also evaluate how close two texts are in meaning using an embedding model. This is a pairwise descriptor that requires you to define two columns. You can use it many scenarios: for example, to compare new generated answers against reference examples that serve as a benchmark. 

In our case, we can use it to compare the semantic similarity between Response and Question columns. This may help detect if chatbot answers are not related to the question the user asks.

This descriptor converts all texts into embeddings using an embedding model, measures Cosine Similarity between them and returns a score from 0 to 1:
* 0 means that texts are opposite in meaning;
* 0.5 means that text are unrelated;
* 1 means that texts are similar. 

To compute the Semantic Similarity between responses and questions:

```python
text_evals_report = Report(metrics=[
    ColumnSummaryMetric(
        column_name=SemanticSimilarity(
            display_name="Response-Question Similarity"
        )
        .on(["response", "question"])
    )
])

text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[:100],
                      column_mapping=column_mapping)
text_evals_report
```

In our examples, the semantic similarity always stays above 0.81, which means that answers generally relate to the question.

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

# 5. Export results

{% hint style="info" %}
**This is optional**. You can proceed without exporting the results.
{% endhint %}

You can export the evaluation results beyond viewing the visual Reports in Python. Here are some options.

**Publish a DataFrame**. You can add the individual computed scores (like semantic similarity) directly to your original dataset. This allows you to further analyze your data, like finding the examples with the lowest scores.

```python
text_evals_report.datasets()[1]
```

**Python dictionary**. Get summary scores as a dictionary. You can use it to export specific values and use them further in your pipeline for any conditional actions:
```python
text_evals_report.as_dict()
```

**JSON**. Export summary scores as JSON:
```python
text_evals_report.json()
```

**HTML**. Save a visual HTML report as a file:
```python
text_evals_report.save_html("report.html")
```

You can also send the results to Evidently Cloud for monitoring!

# 6. Monitor results over time

You will learn how to monitor the results of your evaluations using Evidently Cloud. You can use this to:
* **Track experiment results**. You can record the results of different experiments over time. For example, you can keep track of the evaluation scores for different prompts or models on the same evaluation dataset to see how you progress.
* **Run batch evaluations for live data**. You can run evaluations in batches over your real production data. For example, you can take a sample or all conversations on an houly or daily basis, and score them using your prefered method.

In this flow, you will first run the evaluations in your Python environment, and send the results to get a cloud monitoring dashboard.

**Define the evaluations**. First, let's design a combined Report. This will define what you will evaluate. Say, you want to compute summaries for all metadata columns, and evaluate Text Length, Sentiment and the share of Compensation Mentions in the chatbot responses:

```python
text_evals_report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
            Sentiment(),
            TextLength(),
            IncludesWords(words_list=['salary', 'benefits', 'payroll'],
                          display_name="Mention Compensation")

        ],
    ),
    ColumnSummaryMetric(column_name="feedback"),
    ColumnSummaryMetric(column_name="region"),
    ColumnSummaryMetric(column_name="organization"),
    ColumnSummaryMetric(column_name="model_ID"),
    ColumnSummaryMetric(column_name="environment"),
])
```
You can use more complex checks like LLM-as-a-judge in the same way.

**Run the Report**. Let's run the Report for the first 50 rows:

```python
text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[:50],
                      column_mapping=column_mapping)
```

**Upload the results**. Send the Report to Evidently Cloud to the Project you created earlier:

```python
ws.add_report(project.id, text_evals_report)
```

**View the Report**. You access the Report in Evidently Cloud just like you did in Python before. Go to the Project, open the Reports section, and view the Report:

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW GIF TO BE ADDED

**Get a Monitoring Dashboard**. Now, let's add a dashboard where you can track the results over time. You can choose monitoring panels one by one, but it is easier to start with pre-built Tabs. 
* Go to Project Dashboard.
* Enter the edit mode clicking on the "Edit" button in the top right corner.
* Choose "Add Tab",
* Add a "Descriptors" Tab and then "Columns" Tab.

This way, you will get a ready-made dashboard that will allow you to see the evaluation results over time. 

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW GIF TO BE ADDED

However, we only have a single datapoint from a single Report, so the dashboard is not very informative. Let's imitate a few consecutive runs to evaluate batches of data as they come. 

**Imitate ongoing monitoring**. You will now run and send several Reports, each time running the evaluation for the next 50 rows in the dataset. For illustration, we repeat the same code in a spaghetti manner. In practice, you would compute each Report after a new experimental iteration, or after you get a new batch of data to evaluate. 

Run 2:

```python
text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[50:100],
                      column_mapping=column_mapping)
ws.add_report(project.id, text_evals_report)
```

<details>

<summary>And a few more times!</summary>

Run 3:

```python
text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[100:150],
                      column_mapping=column_mapping)
ws.add_report(project.id, text_evals_report)
```

Run 4:

```python
text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[150:200],
                      column_mapping=column_mapping)
ws.add_report(project.id, text_evals_report)
```

Run 5:

```python
text_evals_report.run(reference_data=None,
                      current_data=assistant_logs[200:250],
                      column_mapping=column_mapping)
ws.add_report(project.id, text_evals_report)
```

</details>

Let's take a look at the dashboard now! Use the "Show in Order" toggle above the dashboard to ignore the time gaps between evaluations.

In the "Desriptors" tab, you will see how the distributions of scores over the five evaluation runs. For example, you can notice a dip in Sentiment in the last evaluation run.

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

In the "Columns" tab, you can see all the associated metadata. For example, how the user upvotes and downvotes are distributed over time.

![](../.gitbook/assets/cloud/llm_toxicity_hf-min.png) NEW IMAGE TO BE ADDED

You can also add alerting conditions for specific values.

{% hint style="success" %}
**Monitoring Panel types**. You can plot selected statistics and metrics as bar, line chart, etc. See more on [available Panels](https://docs.evidentlyai.com/user-guide/monitoring/design_dashboard).
{% endhint %}

# 7. Run conditional tests

Up to now, you used Reports to summarize evaluation results. However, you might often want to set specific conditions on the metric values and only review results when something goes wrong. For example, you might want to check that all the texts are within the expected range. 

You can use Evidently `Test Suites` for this purpose. They have a similar API to `Reports`, but instead of listing `metrics`, you list `tests` and pass conditions using parameters like `gt` (greater than), `lt` (less than), `eq` (equal), etc.

**Define a Test Suite**. Let’s prepare a very simple example:

```python
test_suite = TestSuite(tests=[
    TestColumnValueMean(column_name = Sentiment().on("response"), gte=0),
    TestColumnValueMin(column_name = TextLength().on("response"), gt=0),
    TestColumnValueMax(column_name = TextLength().on("response"), lte=2000),
    TestColumnValueMean(column_name = TextLength().on("response"), gt=500),
])
```

This test sets the following conditions:
* Average response sentiment should be positive.
* Response length should always be non-zero.
* The maximum response length should be 2000 symbols. (This could be a hard limitation due to chat window size).
* The mean response length should be above 500 symbols. (You might expect this as a known pattern and want to detect if texts get shorter on average).

You can use any other descriptors with different Tests in the same manner: for examples, test for average Semantic Similarity, share of responses that are labeled "Concise", etc.

{% hint style="success" %}
**Setting Test conditions**. Read more on how to set test conditions. You can also automatically generate conditions from a reference dataset (e.g. expect +/- 10% of the reference values). [Read more about Tests](https://docs.evidentlyai.com/user-guide/tests-and-reports/custom-test-suite).
{% endhint %}

**Compute multiple Test Suites**. Let write a cycle to imitate that you compute 5 Test Suites sequentially, each time taking 50 rows. You also add a timestamp with hourly difference:

```python
for i in range(5):
    test_suite.run(
        reference_data=None,
        current_data=assistant_logs.iloc[50 * i : 50 * (i + 1), :],
        column_mapping=column_mapping,
        timestamp=datetime.now() + timedelta(hours=i)
    )
    ws.add_test_suite(project.id, test_suite)
```

Note that we do this loop for demonstration to have multiple runs on the dashboard. In production, you would simply run checks sequentially.

**Add a test monitoring panel**. Let's add a simple Panel to show Test results over time. This time, you will see how to use the Python API to manage dashboards as code. This is an option: you can always add panels from the UI as well.

First, connect to the Project to load the updated dashboard configuration back to Python. You need this if you just added the Panels in the UI. If you skip this step, the new Test panels will override the Tabs you already have.

You can copy the Project ID from above the dashboard:

```python
project = ws.get_project("PROJECT_ID")
```

Next, let's create the Test panel inside the new "Tests" tab that will show all detailed test results. 

```python
project.dashboard.add_panel(
    DashboardPanelTestSuite(
        title="Test results",
        filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
        size=WidgetSize.FULL,
        panel_type=TestSuitePanelType.DETAILED,
        time_agg="1D",
    ),
    tab="Tests"
)
project.save()
```

**View test results over time**. Once you go to the Evidently Cloud, you can see the Test results over time. You can see that all the tests passed on each run, except for the last run. If you hover on the specific test, you can see that we failed the minimum sentiment check.

![](../.gitbook/assets/cloud/llm_test_suite_panel-min.png) NEW IMAGE TO BE ADDED

**View individual Test Suite**. To debug, you might want to view the individual Test Suite. Head to the Test section in the left menu, and open the latest test run. You can open up test "Details" to see information about the distribution of predicted scores.   

![](../.gitbook/assets/cloud/llm_tests-min.gif) NEW IMAGE TO BE ADDED

Using the Test Suite interface is useful when you can define specific conditions based on your initial analysis. You can use it for:
* Regression testing. Run Test Suite every time you modify something in the prompt or app parameters, and compare new responses against reference.
* Continous testing. Run Test Suites over your production logs to make sure model output quality and user behavior stays within expectations.

You can also set up alerting to get a notification if your Tests contain failures. 

{% hint style="success" %}
**What is regression testing?**. Check a separate tutorial that introduces the [regression testing workflow](https://www.evidentlyai.com/blog/llm-testing-tutorial).
{% endhint %}

# What's next?

Here are some of the things you might want to explore next:

* **Explore other Reports**. For example, if you have a classification use case and can obtain ground truth labels, there are other checks to run.  See available [Presets](https://docs.evidentlyai.com/presets), [Metrics](https://docs.evidentlyai.com/reference/all-metrics), and [Tests](https://docs.evidentlyai.com/reference/all-tests) to see other checks you can run.
* **Designing monitoring**. Read more about how to design monitoring panels, configure alerts, or send data in near real-time in the [Monitoring User Guide](https://docs.evidentlyai.com/user-guide/monitoring/monitoring_overview). 

Need help? Ask in our [Discord community](https://discord.com/invite/xZjKRaNp8b).
