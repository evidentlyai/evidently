---
description: How to add custom text descriptors.
---

You can implement custom row-level evaluations for text data that you will later use just like any other descriptor across Metrics and Tests. You can implement descriptors that use a single column or two columns.

# Code example

Refer to a How-to example:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_use_llm_judge_template.ipynb" %}

# Custom descriptors

Imports: 

```python
from evidently.descriptors import CustomColumnEval, CustomPairColumnEval
```

## Single column descriptor 

You can create a custom descriptor that will take a single column from your dataset and run a certain evaluation for each row.

**Implement your evaluation as a Python function**. It will take a pandas Series as input and return a transformed Series. 

Here, the `is_empty_string_callable` function takes a column of strings and returns an "EMPTY" or "NON EMPTY" outcome for each.

```python
def is_empty_string_callable(val1):
    return pd.Series(["EMPTY" if val == "" else "NON EMPTY" for val in val1], index=val1.index)
```

**Create a custom descriptor**. Create an example of `CustomColumnEval` class to wrap the evaluation logic into an object that you can later use to process specific dataset input.

```python
empty_string = CustomColumnEval(
    func=is_empty_string_callable,
    feature_type="cat",
    display_name="Empty response"
)
```

Where:
* `func: Callable[[pd.Series], pd.Series]` is a function that returns a transformed pandas Series.
* `display_name: str` is the new descriptor's name that will appear in Reports and Test Suites.
* `feature_type` is the type of descriptor that the function returns (`cat` for categorical, `num` for numerical)

**Apply the new descriptor**. To create a Report with a new Descriptor, pass it as a `column_name` to the `ColumnSummaryMetric`. This will compute the new descriptor for all rows in the specified column and summarize its distribution:

```python
report = Report(metrics=[
    ColumnSummaryMetric(column_name=empty_string.on("response")),
])
```

Run the Report on your `df` dataframe as usual:

```python
report.run(reference_data=None, 
           current_data=df)
```

## Double column descriptor

You can create a custom descriptor that will take two columns from your dataset and will run a certain evaluation for each row. (For example, for pairwise evaluators).

**Implement your evaluation as a Python function**. Here, the `exact_match_callable` function takes two columns and checks whether each pair of values is the same, returning "MATCH" if they are equal and "MISMATCH" if they are not.

```python
def exact_match_callable(val1, val2):
    return pd.Series(["MATCH" if val else "MISMATCH" for val in val1 == val2])
```

**Create a custom descriptor**. Create an example of the `CustomPairColumnEval` class to wrap the evaluation logic into an object that you can later use to process two named columns in a dataset.

```python
exact_match =  CustomPairColumnEval(
    func=exact_match_callable,
    first_column="response",
    second_column="question",
    feature_type="cat",
    display_name="Exact match between response and question"
)
```

Where:

* `func: Callable[[pd.Series, pd.Series], pd.Series]` is a function that returns a transformed pandas Series after evaluating two columns.
* `first_column: str` is the name of the first column to be passed into the function.
* `second_column: str` is the name of the second column to be passed into the function.
* `display_name: str` is the new descriptor's name that will appear in Reports and Test Suites.
* `feature_type` is the type of descriptor that the function returns (`cat` for categorical, `num` for numerical).

**Apply the new descriptor**. To create a Report with a new Descriptor, pass it as a `column_name` to the ColumnSummaryMetric. This will compute the new descriptor for all rows in the dataset and summarize its distribution:

```python
report = Report(metrics=[
    ColumnSummaryMetric(column_name=exact_match.as_column())
])
```

Run the Report on your `df` dataframe as usual:

```python
report.run(reference_data=None, 
           current_data=df)
```
