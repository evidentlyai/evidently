---
description: How to run evaluations for text data with Descriptors. 
---

A Descriptor is a row-level score that evaluates a specific quality or dimension of provided text data. A simple example of Descriptor is text length. It can get more complex, for example, you can use an external LLM evaluator to label each answer as "relevant" or "not relevant", or measure semantic similarity between two answers. All this is implemented through the same Descriptor interfcae.

You can compute a Descriptor as part of the:
* Report. This visualize and gives a summary of the computed values, such as to help you understand the distribution of Text Length across all texts.
* Test Suite. This allows testing a condition, such as to get a True/False result on whether all texts are within expected length range.

{% content-ref url="introduction.md" %}
[Overview of Reports, Tests and Descriptors](introduction.md)
{% endcontent-ref %}

# Code examples

Using descriptors to evaluate LLM outputs using `TextEvals` preset:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_evaluate_llm_with_text_descriptors.ipynb" %}

Using descriptors with tabular Metrics and Tests:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_apply_table_metrics_and_tests_to_text_descriptors.ipynb" %}

# Imports

After [installing Evidently](../installation/install-evidently.md) import the relevant components (depending on whether you want to get Reports or run Tests) and selected `descriptors`.  

```python
from evidently import ColumnMapping
from evidently.report import Report
from evidently.test_suite import TestSuite
from evidently.metric_preset import TextEvals
from evidently.metrics import ColumnSummaryMetric, ColumnDriftMetric 
from evidently.tests import TestColumnValueMin, TestColumnValueMean, TestCategoryShare, TestShareOfOutRangeValues
from evidently.descriptors import Contains, TextLength, Sentiment
```

**Note**. To run some Descriptors that use vocabulary-based checks (like `IncludesWords` that also checks for variant words, or `OOV` that checks for out-of-vocabulary words), you may need to additionally import `nltk` components:

```python
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')
```

# How it works

Here is the general flow.

**Input data**. Prepare the data as a Pandas DataFrame. Include at least one text column. This will be your current data to run evals on. Optionally, prepare the `reference` dataset.
**Schema mapping**. Define your data schema using [Column Mapping](../input-data/column-mapping.md). Optional, but highly recommended.
**Define the Report or Test Suite**. Create a `Report` or a `TestSuite` object with selected checks.
**Run the Report**. Run the Report on your `current_data`, passing the `column_mapping`. Optionally, pass the `reference_data`.
**Get the summary results**. Get a visual report in Jupyter notebook, export the metrics, or upload it to Evidently Platform.
**Get the scored datasets**. If you'd like to see row-level scores, export the Pandas DataFrame with added descriptors. (Or view on Evidently Platform). 

{% hint style="info" %} 
**Available Descriptors**. See the list of available descriptors in the [All Metrics](../reference/all-metrics.md) page. There are different types of descriptors: from regular expressions and texts statistics to model and LLM-based checks.
{% endhint %}

{% hint style="info" %} 
**Reports and Test Suites**. To understand the basic API, read guides on the [running Reports](get-reports.md) and [generating Test Suite](run-tests.md).
{% endhint %}

## Text Evals

By default, we recommend using the `TextEvals` Preset. It is simplified interface to create a Report that summarizes the values of computed Descriptors for a given column. 

**Basic example**. To evaluate Sentiment and Text Length in symbols for the `response` column:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Sentiment(),
        TextLength(),
    ]),
])
```

Run the Report for your DataFrame `df`:

```python
report.run(reference_data=None, 
           current_data=df)
```

You can access the Report as usual, including exporting the results as HTML, JSON, Python dictionary, etc. To view the interactive Report directly in Jupyter notebook or Colab:

```python
report 
```

![](../.gitbook/assets/cloud/llm_report_preview-min.gif)

Additionally, you can export the DataFrame with the generated Descriptor scores added to the original dataset. To view the dataset:

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

**Display name**. We recommended to add a display name parameter to each Descriptor. It will appear in the visualizations and column names. This is especially useful when you have a lengthy Regular Expression or list of Words when the default generated title can become very long.

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Sentiment(display_name="Response sentiment"),
        TextLength(display_name="Response length"),
    ]),
])
```

**Evaluations for multiple columns at once**. If you want to combine evaluations for multiple columns at once, for example, for "response" and "question" columns, just list multiple Presets in the same Report and include the descriptors you need for each of them.

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

**Descriptor parameters**. Some descriptor require parameter you define, such as to specify the exact regular expression or list of words you are testing for.

To Test for competitor mentions using `Contains` descriptor, you must include the brand as `items` in the list:

```python
report = Report(metrics=[
    TextEvals(column_name="response", descriptors=[
        Contains(display_name="Competitor Mentions", 
                items=["AcmeCorp", "YetAnotherCorp"]),
    ]),
])
```

Some descriptors, like custom LLM judges, may require more complex parameterization, but they can be included in the Report just like others.

{% hint style="info" %} 
**Reference**. See the all Descriptor parameters, check the [All Metrics](../reference/all-metrics.md) page.
{% endhint %}

{% hint style="info" %} 
**LLM-as-a-judge**. Check the detailed instructions on how to set up [LLM as a jugde](../customization/llm_as_a_judge.md) page.
{% endhint %}

## Using Metrics

Under the hood, the `TextEvals` Preset generates a `ColumnSummaryMetric` for each calculated descriptor. You can get the same result by explicitly generating this Metric for the descriptor using the following API:

```python
report = Report(metrics=[
    ColumnSummaryMetric(TextLength().for_column("response")),
    ColumnSummaryMetric(Sentiment().for_column("response")),
])
```

**Semantic Similariy**. Using this metric directly is useful to compare Semantic Similarity between two columns. You would need to pass both columns in a lost.

```python
report = Report(metrics=[
    ColumnSummaryMetric(column_name=SemanticSimilarity().on(["answer", "reference_answer"]))
])
```

**Text Descriptor Drift detection**. On some occasions, you want to use a different Metric, such as `ColumnDriftMetric`. Here is how you can do this:

```python
report = Report(metrics=[
   ColumnDriftMetric(column_name = TextLength().for_column("response")),
])
```

In this case, you must pass both `reference` and `current` datasets. Instead of simply returning the summary, the Metric will compare the distribution of the "reponse" Text Length in two datasets and return a drift score. 

You can use other column-level Metrics this way: 

```python
report = Report(metrics=[
    ColumnSummaryMetric(TextLength().for_column("response")),
    ColumnDriftMetric(TextLength().for_column("response")),
    ColumnCorrelationsMetric(TextLength().for_column("response")),
    ColumnDistributionMetric(TextLength().for_column("response")),
    ColumnValueRangeMetric(TextLength().for_column("response"), left=0, right=20)
])
```

However, in most scenarios it's best to first generate the DataFrame with scores, and then run the evaluations over a new dataset by directly referencing the new added column.

## Run Tests 

More importantly, you can also run Tests with these Descriptors. This allows you to explicitly verify a specific condition and return a Pass or Fail result.

**Example 1**. To Test that the average response sentiment is greater or equal (`gte`) to 0, and that maximum text length is less than or equal (`lte`) to 200 symbols:

```python
test_suite = TestSuite(tests=[
    TestColumnValueMean(column_name = Sentiment().on("response"), gte=0),
    TestColumnValueMax(column_name = TextLength().on("response"), lte=200),
])
```

**Example 2**. To Test that the number responses that mention competitors is 0:

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

**Example 3**. To Test that Semantic similarity between to columns is greater or equal to 0.9:

```python
test_suite = TestSuite(tests=[
    TestColumnValueMin(
        column_name=SemanticSimilarity(
        display_name="Response Similarity").
        on(["target_response", "new_response"]),
        gte=0.9),
])
```

**Available Tests**. You can use any column-level Tests with Descriptors. Here are the ones that are particularly useful.

For numerical Descriptors:

```python
test_suite = TestSuite(tests=[
    TestValueRange(column_name = TextLength().on("response")), #test if response length is within min-max range
    TestNumberOfOutRangeValues(column_name = TextLength().on("respone")), #test the number of responses with text length out of range
    TestShareOfOutRangeValues(column_name = TextLength().on("Review_Text")), #test the share of responses with text length out of range
    TestColumnValueMin(column_name = TextLength().on("Review_Text")), #test the minimum response length
    TestColumnValueMax(column_name = TextLength().on("Review_Text")), #test the max response length
    TestColumnValueMean(column_name = TextLength().on("Review_Text")), #test the mean response length
    TestColumnValueMedian(column_name = TextLength().on("Review_Text")),  #test the median response length
])
```

In these examples, the Test conditions are derived from reference. You can also pass custom conditions.

{% hint style="info" %} 
**Test conditions.** Refer to the [All tests](../reference/all-tests.md) table to see the default conditions for individual Tests, and [How to set test conditions](../tests-and-reports/run_tests.md) to learn how to specify conditions manually.
{% endhint %}

For categorical descriptors (like those that return "True" or "False" for pattern match, or binary classifiers with LLM-as-a-judge), use `TestCategoryCount` or `TestCategoryShare` tests. To test if the share of responses that contain travel-related words is less than or equal to 20%:

```python
test_suite = TestSuite(tests=[
    TestCategoryShare(
        column_name=IncludesWords(words_list=['booking', 'hotel', 'flight'], display_name="Travel Mentions").
        on("new_response"),
        category=True,
        lte=0.2),
])
```
