---
description: How to run LLM regression testing.
---

In this tutorial, we'll show you how to run regression testing for LLM outputs: for example, compare new and old responses to the same inputs after you change a prompt.

# Tutorial scope

Here's what we'll do:
* **Create an toy dataset**. Ceate a toy Q&A dataset with questions and reference responses.
* **Imitate genrating new answers**. Imitate generating new answers to the same question we want to compare.
* **Create and run a Test Suite**. Compare two sets of answers using LLM-as-a-judge approach to compare correctness and style match.
* **Get a monitoring Dashboard**. Build a dashboard to monitor the results of Tests over time.

To complete the tutorial, you will need:
* Basic Python knowledge. 
* An OpenAI API key to use for LLM evaluator.
* An Evidently Cloud account to track test results. If not yet, [sign up](../installation/cloud_account.md) for a free account.

Use the provided code snippets or run a sample notebook.

Jupyter notebook:
{% embed url="https://github.com/evidentlyai/community-examples/blob/main/tutorials/Regression_testing_with_debugging" %}

Or click to [open in Colab](https://colab.research.google.com/github/evidentlyai/community-examples/blob/main/tutorials/Regression_testing_with_debugging).

We will work with a toy dataset, which you can replace with your production data or calls to your LLM app to generate a new a set of answers for the input data.

# 1. Installation and Imports

Install Evidently:

```python 
!pip install evidently[llm]
```

Import the required modules:

```python 
import pandas as pd

from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.metric_preset import TextEvals
from evidently.descriptors import *
from evidently.tests import *
from evidently.metrics import *

from evidently.features.llm_judge import BinaryClassificationPromptTemplate
```

To connect to Evidently Cloud:

```python 
from evidently.ui.workspace.cloud import CloudWorkspace
```

(Optional but recommended) To create monitoring panels as code:

```python 
from evidently.ui.dashboards import DashboardPanelPlot
from evidently.ui.dashboards import DashboardPanelTestSuite
from evidently.ui.dashboards import DashboardPanelTestSuiteCounter
from evidently.ui.dashboards import TestSuitePanelType
from evidently.ui.dashboards import ReportFilter
from evidently.ui.dashboards import PanelValue
from evidently.ui.dashboards import PlotType
from evidently.ui.dashboards import CounterAgg
from evidently.tests.base_test import TestStatus
from evidently.renderers.html_widgets import WidgetSize
```

Pass your OpenAI key:

```python 
import os
os.environ["OPENAI_API_KEY"] = "YOUR KEY"
```

# 2. Create a Project

Connect to Evidently Cloud. Replace with your actual token:

```python 
ws = CloudWorkspace(token="YOUR_API_TOKEN", url="https://app.evidently.cloud")
```

Create a Project:

```python 
project = ws.create_project("Regression testing example", team_id="YOUR_TEAM_ID")
project.description = "My project description"
project.save()
```

{% hint style="info" %}
**Need help?** Check how to find API key and [create a Team](../installation/cloud_account.md).
{% endhint %}

# 3. Prepare the Dataset

Create a dataset with questions and reference answers. This data will be used to compare the new responses of your LLM :

```python 
data = [
    ["Why is the sky blue?", "The sky is blue because molecules in the air scatter blue light from the sun more than they scatter red light."],
    ["How do airplanes stay in the air?", "Airplanes stay in the air because their wings create lift by forcing air to move faster over the top of the wing than underneath, which creates lower pressure on top."],
    ["Why do we have seasons?", "We have seasons because the Earth is tilted on its axis, which causes different parts of the Earth to receive more or less sunlight throughout the year."],
    ["How do magnets work?", "Magnets work because they have a magnetic field that can attract or repel certain metals, like iron, due to the alignment of their atomic particles."],
    ["Why does the moon change shape?", "The moon changes shape, or goes through phases, because we see different portions of its illuminated half as it orbits the Earth."]
]

columns = ["question", "target_response"]

ref_data = pd.DataFrame(data, columns=columns)
```

Get a quick preview:

```python 
pd.set_option('display.max_colwidth', None)
ref_data.head()
```

Here is how the data looks:

ADD IMG

You might want to have a quick look at some data statistics, to help you set conditions for Tests. Let's check text length distribution. This will render a summary Report directly in the notebook cell.

```python 
report = Report(metrics=[
    TextEvals(column_name="target_response", descriptors=[
        TextLength(),
    ]),
])

report.run(reference_data=None,
           current_data=ref_data)

report
```

If you run the example in non-interactive Python environment, call `report.as_dict()` or `report.json()` instead.

Here is the distribution of text length:

ADD IMG

# 4. Get new answers

Suppose you generate new responses using your LLM after changing a prompt. We will imitate it by adding a new column with new responses to the DataFrame:

```python 
data = [
    ["Why is the sky blue?",
     "The sky is blue because molecules in the air scatter blue light from the sun more than they scatter red light.",
     "The sky appears blue because air molecules scatter the sun’s blue light more than they scatter other colors."],

    ["How do airplanes stay in the air?",
     "Airplanes stay in the air because their wings create lift by forcing air to move faster over the top of the wing than underneath, which creates lower pressure on top.",
     "Airplanes stay airborne because the shape of their wings causes air to move faster over the top than the bottom, generating lift."],

    ["Why do we have seasons?",
     "We have seasons because the Earth is tilted on its axis, which causes different parts of the Earth to receive more or less sunlight throughout the year.",
     "Seasons occur because of the tilt of the Earth’s axis, leading to varying amounts of sunlight reaching different areas as the Earth orbits the sun."],

    ["How do magnets work?",
     "Magnets work because they have a magnetic field that can attract or repel certain metals, like iron, due to the alignment of their atomic particles.",
     "Magnets generate a magnetic field, which can attract metals like iron by causing the electrons in those metals to align in a particular way, creating an attractive or repulsive force."],

    ["Why does the moon change shape?",
     "The moon changes shape, or goes through phases, because we see different portions of its illuminated half as it orbits the Earth.",
     "The moon appears to change shape as it orbits Earth, which is because we see different parts of its lit-up half at different times. The sun lights up half of the moon, but as the moon moves around the Earth, we see varying portions of that lit-up side. So, the moon's shape in the sky seems to change gradually, from a thin crescent to a full circle and back to a crescent again."]
]

columns = ["question", "target_response", "response"]

eval_data = pd.DataFrame(data, columns=columns)
```

Here is the resulting dataset with the added new column:

ADD IMG

{% hint style="info" %}
**How to run it in production?** In practice, replace this step with calling your LLM app to score the inputs. After you get the new responses, add them to a DataFrame. You can also use our **tracing** library to instrument your app or function and collect traces, that will be automatically converted into a tabular dataset. Evidently will then let you pull a tabular dataset with collected traces. Check the tutorial that shows this [tracing workflow](../tutorial/tutorial_tracing.md). 
{% endhint %}

# 5. Design the Test suite

Now, you must decide on your evaluation metrics. The goal is to compare if the new answers are different to the old ones. You can use some deterministic or embeddings-based metrics like SemanticSimilarity, but often you'd want to make the comparison using more specific criteria you control. In this case, using LLM-as-a-judge is a useful approach that allows you to formulate custom criteria on what you want to detect.

Let's say we want to Test the following:
- That all responses are within expected length. Looking at our previous responses, we've set it as between 80 and 200 symbols.
- That all new responses are giving essentially the same answer without contradiction. We will call this criteria CORRECTNESS and implement it using LLM-as-a-judge.
- That all new responses are the same in style compared to the reference. We will call this criteria STYLE-MATCH and implement it using LLM-as-a-judge.

Evidently has a few built-in LLM-based evaluators, but this time we'll write our custom judges.

## Correctness judge 

Here is how we implement the correctness evaluator, using a built-in Evidenty template for binary classification. Essentially, we are asking LLM to classify every response into correct or not, and give reasoning for that.

```python
correctness_eval= LLMEval(
    subcolumn="category",
    additional_columns={"target_response": "target_response"},
    template = BinaryClassificationPromptTemplate(
        criteria = """
An ANSWER is correct when it is the same as the REFERENCE in all facts and details, even if worded differently.
The ANSWER is incorrect if it contradicts the REFERENCE, adds additional claims, omits or changes details.

REFERENCE:

=====
{target_response}
=====
        """,
        target_category="incorrect",
        non_target_category="correct",
        uncertainty="unknown",
        include_reasoning=True,
        pre_messages=[("system", "You are an expert evaluator. will be given an ANSWER and REFERENCE.")],
        ),
    provider = "openai",
    model = "gpt-4o-mini",
    display_name = "Correctness",
)
```

We strongly recommend splitting evaluationcriteria into individual judges, and using simpler methods like binary classifier for reliability.

{% hint style="info" %}
**Don't forget to evaluate your judge!** Each LLM evaluator is a small ML system you should tune to align with your preferences. We recommend running a couple of iterations to tune it. Check the tutorial on [creating LLM judges](cookbook_llm_judge.md). 
{% endhint %}

{% hint style="info" %}
**Docs on LLM judge**. For explanation of each parameter, check the docs on [LLM judge functionality](../customization/llm_as_a_judge.md). 
{% endhint %}

## Style judge

Following a similar approach we will a create a judge for style. We add additonal clarifications to specify what we mean by style match. 

```python
style_eval= LLMEval(
    subcolumn="category",
    additional_columns={"target_response": "target_response"},
    template = BinaryClassificationPromptTemplate(
        criteria = """
An ANSWER is style-matching when it matches the REFERENCE answer in style.
The ANSWER is style-mismatched when it diverges from the REFERENCE answer in style.

Consider the following STYLE attributes:
- tone (friendly, formal, casual, sarcastic, etc.)
- sentence structure (simple, compound, complex, etc.)
- verbosity level (relative length of answers)
- and other similar attributes that may reflect difference in STYLE.

You must focus only on STYLE. Ignore any differences in contents.

=====
{target_response}
=====
        """,
        target_category="style-matching",
        non_target_category="style-mismatched",
        uncertainty="unknown",
        include_reasoning=True,
        pre_messages=[("system", "You are an expert evaluator. will be given an ANSWER and REFERENCE.")],
        ),
    provider = "openai",
    model = "gpt-4o-mini",
    display_name = "Style",
)
```

## Complete Test Suite

Now, we can create a Test Suite that incorporates the correctness evaluation, style matching, and text length checks. 
* To formulate what we Test, we pick an appropriate Evidently column-level Test like `TestCategoryCount` and `TestShareOfOutRangeValues`. (You can pick other Tests, like `TestColumnValueMin` , `TestColumnValueMean`, etc.)
* Set additional parameters for the Test, if applicable. For example, we use `left` and `right` parameters to set the allowed range for Text Length. 
* To set Test condition, we use parameters like `gt` (greater than), `lt` (less than), `eq` (equal), etc.
* You can also identify some Tests as non-critical. They will give a Warning, but not an Error. This is convenient to divide them visually on monitoring Panels and to set up alerting only for Fails. We mark the style match Test as non-critical.

Here is how we formulate the complete Test Suite: 

```python
test_suite = TestSuite(tests=[
    TestCategoryCount(
        column_name=style_eval.on("response"),
        category="style-mismatched",
        eq=0,
        is_critical=False),
    TestCategoryCount(
        column_name=correctness_eval.on("response"),
        category="incorrect",
        eq=0),
    TestShareOfOutRangeValues(
        column_name=TextLength(display_name="Response Length")
            .on("response"),
        left=80,
        right=200,
        eq=0),
])
```

Note that in these example we always expect the share of failures to be zero using the `eq=0` condition. For example, you can swap the Test condition for text length for `lte=0.1` which would stand for "less than 10%". In this case, the Test will fail only if > 10% of rows in the dataset will be longer than set range.

Allowing some share of Tests to fail is convenient for real-world applications.

You can add additional Tests as you see fit: for regular expressions, word presence, etc. 

{% hint style="info" %} 
**Understand Tests**. Learn how to set [custom Test conditions](../tests-and-reports/run-tests.md) and use [Tests with text Descriptors](../tests-and-reports/text-descriptors.md). See the list of [All tests](../reference/all-tests.md). 
{% endhint %}

# 6. Run the Test Suite

Now that's our Test Suite is ready, let's run it!

To apply this Test Suite to the `eval_data` we prepared:

```python
test_suite.run(reference_data=None, current_data=eval_data)
```

This will compute the Test Suite! But now we need to see it. You can actually preview the results directly in your Python notebook (call `test_suite`)  but we'll now send it to Evidentlu Cloud, together with the scored data:

```python
ws.add_test_suite(project.id, test_suite, include_data=True)
```

Including data is optional, but is useful for most LLM use cases, since you'd want to see not just the aggregate Test results, but also the raw texts to debug when Tests fail.

Now, navigate to the Evidently Platform UI. Go to the ([Home Page](https://app.evidently.cloud/)), enter your Project, and find the "Test Suites" section in the left menu. As you enter it, you will see the resulting Test Suite that you can Explore. Once you open this view, you will both the summary Test results, and the Dataset with the added scores and explanations.

You can edit your view by selecting indiviudal Columns. For example, you might want to sort all columns by Text Length - to find the one that failed the Test, or to view the resulst of the style-match Test. 

ADD IMG

**Note**: your explanations will vary since LLMs are non-deterministic.

{% hint style="info" %} 
**Using Tags**. You can optionally attach Tags to your Test Suite to associate this specific run with some parameter, like a prompt version. Check the [docs on generating snapshots](../evaluations/snapshots.md).
{% endhint %}


# 7. Test again

Now let's say that you made yet another change to the prompt. Our reference dataset stays the same but we generate a new set of answers that we want to compare to this reference. 

Let's imagine that we got the `eval_data_2` as a result of this change.

```python
data = [
    ["Why is the sky blue?",
     "The sky is blue because molecules in the air scatter blue light from the sun more than they scatter red light.",
     "The sky looks blue because air molecules scatter the blue light from the sun more effectively than other colors."],

    ["How do airplanes stay in the air?",
     "Airplanes stay in the air because their wings create lift by forcing air to move faster over the top of the wing than underneath, which creates lower pressure on top.",
     "Airplanes fly by generating lift through the wings, which makes the air move faster above them, lowering the pressure."],

    ["Why do we have seasons?",
     "We have seasons because the Earth is tilted on its axis, which causes different parts of the Earth to receive more or less sunlight throughout the year.",
     "Seasons change because the distance between the Earth and the sun varies throughout the year."],  # This response contradicts the reference.

    ["How do magnets work?",
     "Magnets work because they have a magnetic field that can attract or repel certain metals, like iron, due to the alignment of their atomic particles.",
     "Magnets operate by creating a magnetic field, which interacts with certain metals like iron due to the specific alignment of atomic particles."],

    ["Why does the moon change shape?",
     "The moon changes shape, or goes through phases, because we see different portions of its illuminated half as it orbits the Earth.",
     "The moon's phases occur because we observe varying portions of its lit half as it moves around the Earth."]
]

columns = ["question", "target_response", "response"]

eval_data_2 = pd.DataFrame(data, columns=columns)
```

Now, we can apply the same Test Suite to this data and send it to Evidently Cloud.

```python
test_suite.run(reference_data=None, current_data=eval_data_2)
ws.add_test_suite(project.id, test_suite, include_data=True)
```

If you go and open the new Test Suite results, you can again explore the outcomes and explanations.

ADD IMG

# 8. Get a Dashboard

You can continue running Test Suites in this manner. As you run multiple Test Suites, you might want to clearly track their results over time. 

You can easily create a Dashboard to track Test outcomes over time. You can do edit the monitoring Panels in the UI or programmatically. Let's create a couple Panels using Dashboards as code approach.

The following code will add:
- A counter panel to show the SUCCESS rate of the latest test run.
- A test monitoring panel to show all test results over time.

```python
project.dashboard.add_panel(
     DashboardPanelTestSuiteCounter(
        title="Latest Test run",
        filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
        size=WidgetSize.FULL,
        statuses=[TestStatus.SUCCESS],
        agg=CounterAgg.LAST,
    ),
    tab="Tests"
)
project.dashboard.add_panel(
    DashboardPanelTestSuite(
        title="Test results",
        filter=ReportFilter(metadata_values={}, tag_values=[], include_test_suites=True),
        size=WidgetSize.FULL,
        panel_type=TestSuitePanelType.DETAILED,
        time_agg="1min",
    ),
    tab="Tests"
)
project.save()
```

When you navigate to the UI, you will now see the Dashhboard that shows the summary of Test results (Success, Failure and Warning) for each Test Suite we ran. As you add more Tests to the same Project, the Dashboard will be automatically updated to show new Test results.

{% hint style="info" %} 
**Using Dashboards**. You can design and add other Panels types. Check the [docs on Dashboards](../dashboards/dashboard_overview.md).
{% endhint %}
