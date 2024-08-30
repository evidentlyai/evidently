---
description: How to run evaluations for text data with Descriptors. 
---

A Descriptor is a row-level score that assesses a specific quality or aspect of text data. A simple example of a Descriptor is text length.

It can be more complex, like using an LLM to label each text as "relevant" or "not relevant" (a categorical Descriptor) or calculate the similarity between two texts (a numerical Descriptor).

You can use Descriptors in two ways:
* **In a Report**. This helps visualize and summarize the scores, like how the text length varies across all texts.
* **In a Test Suite**. This helps check if defined conditions are met, like whether all texts are within a certain length (True/False).

{% content-ref url="introduction.md" %}
[Overview of Reports, Tests and Descriptors](introduction.md)
{% endcontent-ref %}

# Code examples

Using descriptors to evaluate LLM outputs using `TextEvals` Preset:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_evaluate_llm_with_text_descriptors.ipynb" %}

Using descriptors with tabular Metrics and Tests:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_apply_table_metrics_and_tests_to_text_descriptors.ipynb" %}

# Imports

After [installing Evidently](../installation/install-evidently.md), import the selected descriptors and the relevant components based on whether you want to generate Reports or run Tests.

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.metric_preset import TextEvals
from evidently.metrics import ColumnSummaryMetric, ColumnDriftMetric 
from evidently.tests import TestColumnValueMin, TestColumnValueMean, TestCategoryShare, TestShareOfOutRangeValues
from evidently.descriptors import Contains, TextLength, Sentiment
```

**Note** To run some Descriptors that use vocabulary-based checks (like `IncludesWords`, which also checks for word variants, or `OOV` for out-of-vocabulary words), you may need to additionally download `nltk` dictionaries:

```python
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')
```

# How it works

Here is the general flow.

* **Input data**. Prepare the data as a Pandas DataFrame. Include at least one text column. This will be your `current_data` to run evals on. Optionally, prepare the `reference` dataset.
* **Schema mapping**. Define your data schema using [Column Mapping](../input-data/column-mapping.md). Optional, but highly recommended.
* **Define the Report or Test Suite**. Create a `Report` or a `TestSuite` object with the selected checks.
* **Run the Report**. Run the Report on your `current_data`, passing the `column_mapping`. Optionally, pass the `reference_data`.
* **Get the summary results**. Get a visual report in Jupyter notebook, export the metrics, or upload it to Evidently Platform.
* **Get the scored datasets**. To see row-level scores, export the Pandas DataFrame with added descriptors. (Or view this on Evidently Platform). 

{% hint style="info" %} 
**Available Descriptors**. See the list of available descriptors in the [All Metrics](../reference/all-metrics.md) page. Descriptors range from regular expressions and text statistics to model and LLM-based checks
{% endhint %}

{% hint style="info" %} 
**Reports and Test Suites**. To understand the basic API, read guides on the [running Reports](get-reports.md) and [generating Test Suite](run-tests.md).
{% endhint %}

## Text Evals

For most cases, we recommend using the `TextEvals` Preset. It provides an easy way to create a Report that summarizes Descriptor values for a specific column.

**Basic example**. To evaluate the Sentiment and Text Length in symbols for the `response` column:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Sentiment(),
        TextLength(),
    ]),
])
```

Run the Report on your DataFrame `df`:

```python
report.run(reference_data=None, 
           current_data=df)
```

You can access the Report just like usual, and export the results as HTML, JSON, a Python dictionary, etc. To view the interactive Report directly in Jupyter Notebook or Colab:

```python
report 
```

![](../.gitbook/assets/cloud/llm_report_preview-min.gif)

You can also export the DataFrame with the Descriptor scores added to your original dataset. To see the dataset:

```
report.datasets().current
```

![](../.gitbook/assets/reports/descriptors_export.png)

To create a DataFrame:

```
df_with_scores = pd.DataFrame(report.datasets().current)
```

{% hint style="info" %} 
**How to get the outputs**. Check the details on all available [Output Formats](output_formats.md).
{% endhint %}

**Display name**. It’s a good idea to add a `display_name` to each Descriptor. This name shows up in visualizations and column headers. It’s especially handy if you’re using checks like regular expressions with word lists, where the auto-generated title could get very long.

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Sentiment(display_name="Response sentiment"),
        TextLength(display_name="Response length"),
    ]),
])
```

**Evaluations for multiple columns**. If you want to evaluate several columns, like "response" and "question", just list multiple Presets in the same Report and include the Descriptors you need for each one.

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Sentiment(),
        TextLength(),
    ]),
    TextEvals(column_name="question", descriptors=[
        Sentiment(),
        TextLength(),
    ])
])
```

**Descriptor parameters**. Some Descriptors have required parameters. For example, if you’re testing for competitor mentions using the `Contains` Descriptor, you’ll want to include the brand names in the `items` list:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Contains(display_name="Competitor Mentions", 
                items=["AcmeCorp", "YetAnotherCorp"]),
    ]),
])
```

Some Descriptors, like custom LLM judges, might require a more complex setup, but you can still include them in the Report just like any other Descriptor.

{% hint style="info" %} 
**Reference**. To see the Descriptor parameters, check the [All Metrics](../reference/all-metrics.md) page.
{% endhint %}

{% hint style="info" %} 
**LLM-as-a-judge**. For a detailed guide on setting up LLM-based evals, check the guide to [LLM as a jugde](../customization/llm_as_a_judge.md).
{% endhint %}

## Using Metrics

The `TextEvals` Preset works by generating a `ColumnSummaryMetric` for each Descriptor you calculate. You can achieve the same results by explicitly creating this Metric for each Descriptor using the following API:

```python
report = Report(metrics=[
    ColumnSummaryMetric(TextLength().on("response")),
    ColumnSummaryMetric(Sentiment().on("response")),
])
```

**Semantic Similariy**. To compare Semantic Similarity between two columns, you should use this approach instead of `TextEvals` to be able to process two columns at once. Pass both columns in a list:

```python
report = Report(metrics=[
    ColumnSummaryMetric(column_name=SemanticSimilarity().on(["answer", "reference_answer"]))
])
```

**Text Descriptor Drift detection**. Sometimes, you might want to use a different Metric, like `ColumnDriftMetric`. Here is how to do this:

```python
report = Report(metrics=[
   ColumnDriftMetric(column_name = TextLength().on("response")),
])
```

In this case, you’ll need to pass both `reference` and `current` datasets. Instead of just summarizing, the Metric will compare the distribution of "response" Text Length in the two datasets and return a drift score.

You can use other column-level Metrics this way: 

```python
report = Report(metrics=[
    ColumnSummaryMetric(TextLength().on("response")),
    ColumnDriftMetric(TextLength().on("response")),
    ColumnCorrelationsMetric(TextLength().on("response")),
    ColumnDistributionMetric(TextLength().on("response")),
    ColumnValueRangeMetric(TextLength().on("response"), left=0, right=20)
])
```

However, in most cases, it's better to first generate a DataFrame with the scores through `TextEvals`. You can then run evaluations on the new dataset by referencing the newly added column directly.

## Run Tests 

You can also run Tests with text Descriptors, allowing you to verify specific conditions and return a Pass or Fail result.

**Example 1**. To test that the average response sentiment is greater or equal (`gte`) to 0, and that the maximum text length is less than or equal (`lte`) to 200 characters:

```python
test_suite = TestSuite(tests=[
    TestColumnValueMean(column_name = Sentiment().on("response"), gte=0),
    TestColumnValueMax(column_name = TextLength().on("response"), lte=200),
])
```

**Example 2**. To test that the number of responses mentioning competitors is zero:

```python
test_suite = TestSuite(tests=[
    TestCategoryCount(
        column_name=Contains(
            items=["AcmeCorp", "YetAnotherCorp"],
            display_name="Competitor Mentions").
        on("new_response"),
        category=True,
        eq=0),
])
```

**Example 3**. To test that Semantic similarity between two columns is greater or equal to 0.9:

```python
test_suite = TestSuite(tests=[
    TestColumnValueMin(
        column_name=SemanticSimilarity(
        display_name="Response Similarity").
        on(["target_response", "new_response"]),
        gte=0.9),
])
```

![](../.gitbook/assets/tests/test_descriptor_example.png)

**Available Tests**. You can use any column-level Tests with Descriptors. Here are some that are particularly useful:

For numerical Descriptors:

```python
test_suite = TestSuite(tests=[
    TestValueRange(column_name = TextLength().on("response")), #test if response length is within min-max range
    TestNumberOfOutRangeValues(column_name = TextLength().on("response")), #test the number of responses with text length out of range
    TestShareOfOutRangeValues(column_name = TextLength().on("response")), #test the share of responses with text length out of range
    TestColumnValueMin(column_name = TextLength().on("response")), #test the minimum response length
    TestColumnValueMax(column_name = TextLength().on("response")), #test the max response length
    TestColumnValueMean(column_name = TextLength().on("response")), #test the mean response length
    TestColumnValueMedian(column_name = TextLength().on("response")),  #test the median response length
])
```

In these examples, the Test conditions must be derived from the `reference`. You can also pass custom conditions.

{% hint style="info" %} 
**Test conditions.** Refer to the [All tests](../reference/all-tests.md) table to see the default conditions for individual Tests, and [How to set test conditions](../tests-and-reports/run_tests.md) to learn how to specify conditions manually.
{% endhint %}

For categorical descriptors (like those that return "True" or "False" for pattern match, or binary classifiers with LLM-as-a-judge), use `TestCategoryCount` or `TestCategoryShare` tests. 

For example, to test if the share of responses that contain travel-related words is less than or equal to 20%:

```python
test_suite = TestSuite(tests=[
    TestCategoryShare(
        column_name=IncludesWords(words_list=['booking', 'hotel', 'flight'], display_name="Travel Mentions").
        on("new_response"),
        category=True,
        lte=0.2),
])
```
