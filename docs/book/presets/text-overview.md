**TL;DR:** You can explore and compare text datasets.

* **Report**: for visual analysis or metrics export, use the `TextEvals`.

# Text Evals Report   

To visually explore the descriptive properties of text data, you can create a new Report object and generate `TextEvals` preset for the column containing the text data. It's best to define your own set of `descriptors` by passing them as a list to the `TextEvals` preset. For more details, see [how descriptors work](../tests-and-reports/text-descriptors.md).

If you don’t specify descriptors, the Preset will use default statistics.

## Code example

```python
text_overview_report = Report(metrics=[
    TextEvals(column_name="Review_Text")
])

text_overview_report.run(reference_data=ref, current_data=cur)
text_overview_report
```

Note that to calculate some text-related metrics, you may also need to also import additional libraries:

```
import nltk
nltk.download('words')
nltk.download('wordnet')
nltk.download('omw-1.4')
```

## Data Requirements

* You can pass **one or two** datasets. Evidently will compute descriptors both for the **current** production data and the **reference** data. If you pass a single dataset, there will be no comparison.
* To run this preset, you must have **text columns** in your dataset. Additional features and prediction/target are optional. Pass them if you want to analyze the correlations with text descriptors. 
* **Column mapping**. Specify the columns that contain text features in [column mapping](../input-data/column-mapping.md). 

## How it looks

The report includes 5 components. All plots are interactive.

**Aggregated visuals in plots.** Starting from v 0.3.2, all visuals in the Evidently Reports are aggregated by default. This helps decrease the load time and report size for larger datasets. If you work with smaller datasets or samples, you can pass an [option to generate plots with raw data](../customization/report-data-aggregation.md). You can choose whether you want it on not based on the size of your dataset.

### Text Descriptors Distribution

The report generates several features that describe different text properties and shows the distributions of these text descriptors. 

#### Text length

![](<../.gitbook/assets/reports/metric_text_descriptors_distribution_text_length-min.png>)

#### Non-letter characters

![](<../.gitbook/assets/reports/metric_text_descriptors_distribution_nlc-min.png>)

#### Out-of-vocabulary words

![](<../.gitbook/assets/reports/metric_text_descriptors_distribution_oov-min.png>)

#### Sentiment 

Shows the distribution of text sentiment (-1 negative to 1 positive).

#### Sentence Count

Shows the sentence count.

## Metrics output

You can also get the report output as a JSON or a Python dictionary.

## Report customization

* You can [choose your own descriptors](../tests-and-reports/text-descriptors.md).
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* You can create a different report or test suite from scratch, taking this one as an inspiration. 

# Examples

* Head to an [example how-to notebook](https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_run_calculations_over_text_data.ipynb) to see an example Text Overview preset and other metrics and tests for text data.

