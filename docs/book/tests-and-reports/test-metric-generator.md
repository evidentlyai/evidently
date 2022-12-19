Sometimes you need to generate multiple column-level Tests or Metrics.

To simplify it, you can:
* Pass a list of parameters or columns to a chosen Test or Metric
* Use test/metric generator helper functions

# List comprehension 

You can pass a list of parameters/conditions or columns. It works the same for Tests and Metrics.

**Example 1**. Pass the list of quantile values to run multiple Tests for the same column. 

```python
suite = TestSuite(tests=[
   TestColumnQuantile(column_name="education-num", quantile=quantile) for quantile in [0.5, 0.9, 0.99]
])

suite.run(current_data=current_data, reference_data=reference_data)
suite
```

**Example 2**. Apply the same Test with a defined custom condition for all columns in the list: 

```python
suite = TestSuite(tests=[
   TestColumnValueMin(column_name=column_name, gt=0) for column_name in ["age", "fnlwgt", "education-num"]
])
 
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

# Column test generator

You can also use the `generate_column_tests` function to create multiple Tests.

**Example 1.** Generate the same Test for all the columns in the dataset. It will use defaults if you do not specify the test condition.

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfMissingValues)])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

You can also pass a custom Test condition:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfMissingValues, columns="all", parameters={"lt": 0.5})])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

**Example 2.**  You can generate Tests for different subsets of columns. Here is how you generate tests only for **numerical columns**:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnValueMin, columns="num")])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

Here is how you generate tests only for **categorical columns**:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfMissingValues, columns="cat", parameters={"lt": 0.1})])
suite.run(current_data=current_data, reference_data=refernce_data)
suite
```
 
You can also generate Tests with a certain condition for a **defined column list**:
 
```python
suite = TestSuite(tests=[generate_column_tests(TestColumnValueMin, columns=["age", "fnlwgt", "education-num"],
                                              parameters={"gt": 0})])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```
 
## Column parameter

You can use the parameter `columns` to define a list of columns to which you apply the tests. If it is a list, just use it as a list of the columns. If `columns` is a string, it can take the following values:
* `"all"` - apply tests/metrics for all columns, including target/prediction columns.
* `"num"` - for numerical features, as provided by column mapping or defined automatically
* `"cat"` - for categorical features, as provided by column mapping or defined automatically
* `"features"` - for all features, excluding the target/prediction columns.
* `"none"` -  the same as "all."

# Column metric generator

It works the same way for metrics. In this case, you should use `generate_column_metrics` function.

**Example 1**: To generate multiple metrics for all the columns in the list with a custom parameter.

```python
metric_generator_report = Report(
    metrics=[
        generate_column_metrics(
            ColumnValueRangeMetric,
            columns=['mean radius', 'mean texture', 'mean perimeter'],
            parameters={"left": 5, "right": 25}
        )
    ]
)
metric_generator_report.run(current_data=bcancer_ref, reference_data=bcancer_cur)
metric_generator_report
```
