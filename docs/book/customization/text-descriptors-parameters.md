---
description: How to work with Metrics and Tests that use text descriptors.
---

**Pre-requisites**:
* You know how to generate Reports or Test Suites for text data.
* You know how to pass custom parameters for Reports or Test Suites.
* You know to specify text data in column mapping.

Text descriptors are various characteristics of the text datasets computed by Evidently. You can use them across different Metrics, Tests, and Presets and treat Descriptors as if they exist as an extra tabular feature that describes the text dataset.   

# Code example
Using descriptors with tabular Metrics and Tests:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_apply_table_metrics_and_tests_to_text_descriptors.ipynb" %}

Using descriptors with text-specific Metrics and Tests:
{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_text_descriptors_in_text_specific_metrics.ipynb" %}

# Available descriptors

| Descriptor | Description |  
|---|---|
| `TextLength()` | (Default). Calculates the length of text in symbols.  |  
| `SentenceCount()` | Calculates the number of sentences.  | 
| `WordCount()` | Calculates the number of words.  |  
| `Sentiment()` | Evaluates the text sentiment, on a scale from -1 (negative) to 1 (positive). |  
| `OOV()` | Default). Calculates the share of out-of-vocabulary words. |  
| `NonLetterCharacterPercentage()` | Default). Calculates the share of non-letter characters. |  
| `TriggerWordsPresence(words_list=['dress', 'gown'])` | Checks for the presence of any of the specified words, as determined by the user. (Boolean).  |  
| `RegExp(reg_exp=r'.*\?.*', display_name="Questions")`| Checks for match with a defined regular expression. (Boolean).  |  

**Note**: you must import specific `nltk` components to use all available descriptors:

```python
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('vader_lexicon')
```

# Descriptors in text-specific metrics

Several Metrics and Presets are specifically created to generate Descriptors from raw text data. For example, `TextDescriptorsDriftMetric()` or `TextDescriptorsCorrelationMetric()`. 

## Default
To generate the Report using Descriptors, select the relevant Metrics or Presets and apply them to a text column. You must specify the text column in the column mapping.

**Example 1**. To combine several text-related Metrics in a single Report:

```python
text_specific_metrics_report = Report(metrics=[
    TextDescriptorsDriftMetric(column_name="Review_Text"),
    TextDescriptorsDistribution(column_name="Review_Text"),
    TextDescriptorsCorrelationMetric(column_name="Review_Text"),
])
```

**Example 2**. To generate a text-related Preset:

```python
text_overview_report = Report(metrics=[
    TextOverviewPreset(column_name="Review_Text")
])
```

In these cases, the defaults will apply:
* 3 default Descriptors will be calculated.
* If data drift is evaluated, the default drift detection methods will apply. The defaults are the same as for tabular drift detection.
* If correlations are calculated, they will include all numerical columns in the dataset and all text Descriptors. 

## Descriptors parameters 
To customize the text-related Metrics or use non-default descriptors (e.g., `TriggerWordsPresence()` that requires specifying the list of words), you should use the `descriptors` parameter. Pass it to the chosen Metric or Preset. 

**Example 1**. Here is how you specify which Descriptors to include in a specific Metric, the titles for the corresponding Descriptor columns (they will appear in visualizations), and the list of trigger words to track:    

```python
report = Report(metrics=[
    TextDescriptorsDriftMetric("Review_Text", descriptors={
        "Review Text Length" : TextLength(),
        "Reviews about Dress" : TriggerWordsPresence(words_list=['dress', 'gown']),
        "Review about Blouses" : TriggerWordsPresence(words_list=['blouse', 'shirt'])
    }),
    TextDescriptorsCorrelationMetric(column_name="Title", descriptors={
        "Title OOV" : OOV(),
        "Title Non Letter %" : NonLetterCharacterPercentage(),
        "Title Length" : TextLength()
    })
])
```

**Example 2**. Here is how to do this for a Preset:

```python
text_overview_report = Report(metrics=[
    TextOverviewPreset(column_name="Review_Text", descriptors={
        "Review Text OOV" : OOV(),
        "Review Text Non Letter %" : NonLetterCharacterPercentage(),
        "Review Text Length" : TextLength(),
        "Reviews about Dress" : TriggerWordsPresence(words_list=['dress', 'gown']),
        "Review about Blouses" : TriggerWordsPresence(words_list=['blouse', 'shirt'])
    })
])
```

## "Lemmatize" parameter

The `TriggerWordsPresence()` Descriptor has `lemmatize` parameter. The default is `True`. When you specify the Trigger Words, it will also search for the variant and inflected forms of this word.

You can override the default and set it as `False.` In this case, it will only search for exact matches.

```python
report = Report(metrics=[
    TextDescriptorsDriftMetric("Review_Text", descriptors={
        "Reviews about Dress" : TriggerWordsPresence(words_list=['dress', 'gown'], lemmatize='False'),
        "Review about Blouses" : TriggerWordsPresence(words_list=['blouse', 'shirt'])
    })
])
```

## Descriptors as “virtual columns”

You can also use Descriptors as if they exist as additional columns in the dataset and refer to them in relevant tabular Metrics and Tests. 

You should use a specific syntax to refer to the “virtual” Descriptor columns.  

**Example 1**. Descriptors in column-level Metrics:

```python
table_column_metrics_report = Report(metrics=[
    ColumnSummaryMetric(column_name = TextLength().for_column("Review_Text")),
    ColumnDriftMetric(column_name = TextLength().for_column("Review_Text")),
    ColumnCorrelationsMetric(column_name = TextLength().for_column("Review_Text")),
    ColumnDistributionMetric(column_name = TextLength().for_column("Review_Text")),
    ColumnValueRangeMetric(column_name = TextLength().for_column("Review_Text"), left=0, right=20)
    
])
```

For example, when you call `ColumnDriftMetric()` for the "virtual" column `TextLength().for_column("Review_Text")`, you will evaluate statistical distribution drift in the length of texts that appear in the “Review_Text” column.

**Example 2**. Descriptors in column-level Tests:

```python
table_column_test_suite = TestSuite(tests=[
    TestColumnDrift(column_name = TextLength().for_column("Review_Text")),
    TestValueRange(column_name = TextLength().for_column("Review_Text")),
    TestNumberOfOutRangeValues(column_name = TextLength().for_column("Review_Text")),
    TestShareOfOutRangeValues(column_name = TextLength().for_column("Review_Text")),
    TestMeanInNSigmas(column_name = TextLength().for_column("Review_Text")),
    TestColumnValueMin(column_name = TextLength().for_column("Review_Text")),
    TestColumnValueMax(column_name = TextLength().for_column("Review_Text")),
    TestColumnValueMean(column_name = TextLength().for_column("Review_Text")),
    TestColumnValueMedian(column_name = TextLength().for_column("Review_Text")),
    TestColumnValueStd(column_name = TextLength().for_column("Review_Text")),
    TestColumnQuantile(column_name = TextLength().for_column("Review_Text"), quantile=0.25),
    
])
```

For example, when you call `TestValueRange()` for the “virtual” column `TextLength().for_column("Review_Text")` , you will evaluate whether the length of texts in the column “Review_Text” stays within the specific range. If you do not specify the range manually, Evidently will infer the range from the reference dataset, and apply +/-10% heuristic to generate the test conditions. 

{% hint style="info" %}
**Test conditions.** Refer to the [All tests](../reference/all-tests.md) table to see the default conditions for individual Tests, and [How to set test conditions](../tests-and-reports/custom-test-suite.md)  to learn how to specify conditions manually.
{% endhint %}

**Example 3**. Descriptors in dataset-level Metrics:

```python
classification_report = Report(metrics=[
    ClassificationQualityByFeatureTable(columns=["Age", "Review_Text"], descriptors = {
        "Review_Text":{
        "Text Length" : TextLength(),
        "Reviews about Dress" : TriggerWordsPresence(words_list=['dress', 'gown']),
        "Review about Blouses" : TriggerWordsPresence(words_list=['blouse', 'shirt'])
    }})
```

In this case, you will generate the Classification Quality By Feature Metric, which will plot the model performance against virtual features like “whether the reviews contained the word blouse or shirt”). 

**Note**: For dataset-level metrics, you currently cannot exclude Descriptors. All default Descriptors will be included. 


## Display name parameter

You can also specify a custom display name for the Metrics. This is useful when you have a lengthy Regular Expression or list of Trigger Words when the default title of the metric can become very long.

```python
table_column_metrics_report = Report(metrics=[
    ColumnSummaryMetric(column_name = RegExp(reg_exp=r'.*\?.*', display_name="Questions").for_column("Review_Text")),
    ColumnDriftMetric(column_name = SentenceCount(display_name="SentenceCount").for_column("Review_Text")),
    ColumnCorrelationsMetric(column_name = WordCount(display_name="WordCount").for_column("Review_Text")),
    ColumnDistributionMetric(column_name = Sentiment(display_name="Sentiment").for_column("Review_Text")),
    ColumnValueRangeMetric(column_name = TextLength(display_name="TextLength").for_column("Review_Text"), left=0, right=20)
])

table_column_metrics_report.run(reference_data=reviews_ref, current_data=reviews_cur, column_mapping=column_mapping)
table_column_metrics_report
```

