**TL;DR:** You can monitor and analyze the performance of a recommender system. 

* **Report**: for visual analysis or metrics export, use the `RecsysPreset`.
* **Test Suite**: for pipeline checks, use the `RecsysTestPreset`.

# Recommendation Quality Report

If you want to visually explore the model performance, create a new Report object and include the `RecsysPreset`.

## Code example

```python
report = Report(metrics=[
    RecsysPreset(k=5),
])
column_mapping = ColumnMapping(recommendations_type='rank', target='rating', prediction='rank', item_id='title', user_id='user_id')
report.run(
    reference_data=reference,
    current_data=current,
    column_mapping=column_mapping,
    additional_data={'current_train_data': train_data}
  )
report
```
Check the [How-to example](https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_run_recsys_metrics.ipynb) for an end-to-end example on a sample dataset. 

## How it works

![](../.gitbook/assets/reports/metric_popularity_bias-min.png)

The **Recommender System Performance** report evaluates the quality of a recommender system. It can also compare the performance against the past, or the performance of an alternative model.

* Works for a **single model** or helps compare the **two**.
* Displays 10+ plots related to the **predictive quality**, **ranking quality** and recommendation **diversity**.
* Helps explore recommendation bias and examples of recommendations.

Check the [All Metrics Table](../reference/all-metrics.md) for a complete list of metrics and parameters. Check the [Ranking Metrics Guide](../reference/ranking-metrics.md) for an explanation of each metric.

## Data Requirements

* To run this report, you need to have both **target** (true relevance) and **prediction** (rank or score) columns available. Additional **training data** and **input features** are required for some of the metrics.
* To generate a comparative report, you will need **two** datasets. The **reference** dataset serves as a benchmark, e.g. past model performance or a performance of a different model. Evidently analyzes the change by comparing the **current** production data to the **reference** data.
* You can also run this report for a **single** dataset, with no comparison performed. 
* You must perform **column mapping** to map the data inputs correctly.

Check the [Column Mapping](../input-data/column-mapping.md) guide and instructions on using [Additional Data](../input-data/recsys_data.md) in recommendations. 

## Report customization

* You can pass `user_bias_columns` columns or `item_bias_columns` you want to evaluate for bias.
* You can pass `display_features` you want to display in the recommendation cases table.
* You can pass `user_ids: List` to specify which users you want to display in the recommendation cases table.
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* If you want to exclude some metrics, you can create a custom report by combining the chosen metrics. See the complete list [here](../reference/all-metrics.md)

Check the [All Metrics Table](../reference/all-metrics.md) for a complete list of metrics and parameters. 

# Recommender System Test Suite

If you want to run recommender system performance checks as part of a pipeline, you can create a Test Suite and include the `RecsysTestPreset`.

## Code example

```python

tests = TestSuite(tests=[
    RecsysTestPreset(k=5)
])

column_mapping = ColumnMapping(recommendations_type='rank', target='rating', prediction='rank', item_id='title', user_id='user_id')
tests.run(
    reference_data=reference,
    current_data=current,
    column_mapping=column_mapping,
    additional_data={'current_train_data': train_data}
  )
tests
```

## How it works

You can use the `RecsysTestPreset` to evaluate the quality of a recommender or ranking system, when you have the ground truth data (relevance scores).

* It compares **ranking quality metrics** against the defined expectation. 
* For Evidently to **generate the test conditions automatically**, you should pass the reference dataset (e.g., performance during the previous period). You can also set the performance expectations manually by passing custom test conditions. 

Head here to the [All tests](../reference/all-tests.md) table to see the composition of each preset and default parameters. 

## Test Suite customization

* You can set custom test conditions.
* If you want to exclude some tests or add additional ones, you can create a custom test suite by combining the chosen tests. See the complete list [here](../reference/all-tests.md).
