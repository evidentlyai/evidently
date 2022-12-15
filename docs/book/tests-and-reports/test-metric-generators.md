# Tests generation 

There are several features that simplify generating multiple column-level tests. 

## List comprehension

You can pass a list of parameters or a list of columns. 

**Example 1**. Pass the list of multiple quantile values to test for the same column. 

```python
suite = TestSuite(tests=[
   TestColumnQuantile(column_name="education-num", quantile=quantile) for quantile in [0.5, 0.9, 0.99]
])

suite.run(current_data=current_data, reference_data=reference_data)
suite
```

**Example 2**. Apply the same test with a defined custom parameter for all columns in the list: 

```python
suite = TestSuite(tests=[
   TestColumnValueMin(column_name=column_name, gt=0) for column_name in ["age", "fnlwgt", "education-num"]
])
 
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

## Column test generator

You can also use the `generate_column_tests` function to create multiple tests.

By default, it generates tests with the default parameters for all the columns:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfMissingValues)])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

You can also pass the parameters:

```python
suite = TestSuite(tests=[generate_column_tests(TestColumnShareOfMissingValues, columns="all", parameters={"lt": 0.5})])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```

You can generate tests for different subsets of columns. Here is how you generate tests only for **numerical columns**:

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
 
You can also generate tests with defined parameters, for a custom defined column list:
 
```python
suite = TestSuite(tests=[generate_column_tests(TestColumnValueMin, columns=["age", "fnlwgt", "education-num"],
                                              parameters={"gt": 0})])
suite.run(current_data=current_data, reference_data=reference_data)
suite
```
 
### Column parameter

You can use the parameter `columns` to define a list of columns to which you apply the tests. If it is a list, just use it as a list of the columns. If `columns` is a string, it can take the following values:
* `"all"` - apply tests for all columns, including target/prediction columns.
* `"num"` - for numerical features, as provided by column mapping or defined automatically
* `"cat"` - for categorical features, as provided by column mapping or defined automatically
* `"features"` - for all features, excluding the target/prediction columns.
* `"none"` -  the same as "all."


