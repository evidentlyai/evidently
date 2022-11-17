# Table of Contents

* [evidently.utils](#evidently.utils)
* [evidently.utils.data\_operations](#evidently.utils.data_operations)
  * [DatasetColumns](#evidently.utils.data_operations.DatasetColumns)
    * [get\_all\_features\_list](#evidently.utils.data_operations.DatasetColumns.get_all_features_list)
    * [get\_all\_columns\_list](#evidently.utils.data_operations.DatasetColumns.get_all_columns_list)
    * [get\_features\_len](#evidently.utils.data_operations.DatasetColumns.get_features_len)
  * [recognize\_task](#evidently.utils.data_operations.recognize_task)
  * [recognize\_column\_type](#evidently.utils.data_operations.recognize_column_type)
* [evidently.utils.data\_preprocessing](#evidently.utils.data_preprocessing)
* [evidently.utils.generators](#evidently.utils.generators)
  * [BaseGenerator](#evidently.utils.generators.BaseGenerator)
  * [make\_generator\_by\_columns](#evidently.utils.generators.make_generator_by_columns)
* [evidently.utils.numpy\_encoder](#evidently.utils.numpy_encoder)
  * [NumpyEncoder](#evidently.utils.numpy_encoder.NumpyEncoder)
    * [default](#evidently.utils.numpy_encoder.NumpyEncoder.default)
* [evidently.utils.types](#evidently.utils.types)
  * [ApproxValue](#evidently.utils.types.ApproxValue)
* [evidently.utils.visualizations](#evidently.utils.visualizations)
  * [plot\_num\_feature\_in\_time](#evidently.utils.visualizations.plot_num_feature_in_time)
  * [plot\_time\_feature\_distr](#evidently.utils.visualizations.plot_time_feature_distr)
  * [plot\_cat\_feature\_in\_time](#evidently.utils.visualizations.plot_cat_feature_in_time)
  * [plot\_boxes](#evidently.utils.visualizations.plot_boxes)
  * [plot\_cat\_cat\_rel](#evidently.utils.visualizations.plot_cat_cat_rel)

<a id="evidently.utils"></a>

# evidently.utils

<a id="evidently.utils.data_operations"></a>

# evidently.utils.data\_operations

Methods for clean null or NaN values in a dataset

<a id="evidently.utils.data_operations.DatasetColumns"></a>

## DatasetColumns Objects

```python
@dataclass
class DatasetColumns()
```

<a id="evidently.utils.data_operations.DatasetColumns.get_all_features_list"></a>

#### get\_all\_features\_list

```python
def get_all_features_list(cat_before_num: bool = True,
                          include_datetime_feature: bool = False) -> List[str]
```

List all features names.

By default, returns cat features than num features and du not return other.

If you want to change the order - set  `cat_before_num` to False.

If you want to add date time columns - set `include_datetime_feature` to True.

<a id="evidently.utils.data_operations.DatasetColumns.get_all_columns_list"></a>

#### get\_all\_columns\_list

```python
def get_all_columns_list() -> List[str]
```

List all columns.

<a id="evidently.utils.data_operations.DatasetColumns.get_features_len"></a>

#### get\_features\_len

```python
def get_features_len(include_time_columns: bool = False) -> int
```

How mane feature do we have. It is useful for pagination in widgets.

By default, we sum category nad numeric features.

If you want to include date time columns - set `include_datetime_feature` to True.

<a id="evidently.utils.data_operations.recognize_task"></a>

#### recognize\_task

```python
def recognize_task(target_name: str, dataset: pd.DataFrame) -> str
```

Try to guess about the target type:
if the target has a numeric type and number of unique values > 5: task == ΓÇÿregressionΓÇÖ
in all other cases task == ΓÇÿclassificationΓÇÖ.

**Arguments**:

- `target_name` - name of target column.
- `dataset` - usually the data which you used in training.
  

**Returns**:

  Task parameter.

<a id="evidently.utils.data_operations.recognize_column_type"></a>

#### recognize\_column\_type

```python
def recognize_column_type(dataset: pd.DataFrame, column_name: str,
                          columns: DatasetColumns) -> str
```

Try to get the column type.

<a id="evidently.utils.data_preprocessing"></a>

# evidently.utils.data\_preprocessing

<a id="evidently.utils.generators"></a>

# evidently.utils.generators

<a id="evidently.utils.generators.BaseGenerator"></a>

## BaseGenerator Objects

```python
class BaseGenerator(Generic[TObject])
```

Base class for tests and metrics generator creation

To create a new generator:
    - inherit a class from the base class
    - implement `generate_tests` method and return a list of test objects from it

A Suite or a Report will call the method and add generated tests to its list instead of the generator object.

You can use `columns_info` parameter in `generate` for getting data structure meta info like columns list.

For example:
    if you want to create a test generator for 50, 90, 99 quantiles tests
    for all numeric columns with default condition, by reference quantiles

class TestQuantiles(BaseTestGenerator):
    def generate(self, columns_info: DatasetColumns) -> List[TestValueQuantile]:
        return [
            TestValueQuantile(column_name=name, quantile=quantile)
            for quantile in (0.5, 0.9, 0.99)
            for name in columns_info.num_feature_names
        ]

Do not forget set correct test type for `generate` return value

<a id="evidently.utils.generators.make_generator_by_columns"></a>

#### make\_generator\_by\_columns

```python
def make_generator_by_columns(
        base_class: Type,
        columns: Optional[Union[str, list]] = None,
        parameters: Optional[Dict] = None) -> BaseGenerator
```

Create a test generator for a columns list with a test class.

Base class is specified with `base_class` parameter.
If the test have no "column_name" parameter - TypeError will be raised.

Columns list can be defined with parameter `columns`.
If it is a list - just use it as a list of the columns.
If `columns` is a string, it can be one of values:
- "all" - make tests for all columns, including target/prediction columns
- "num" - for numeric features
- "cat" - for category features
- "features" - for all features, not target/prediction columns.
None value is the same as "all".
If `columns` is string, and it is not one of the values, ValueError will be raised.

`parameters` is used for specifying other parameters for each object, it is the same for all generated objects.

<a id="evidently.utils.numpy_encoder"></a>

# evidently.utils.numpy\_encoder

<a id="evidently.utils.numpy_encoder.NumpyEncoder"></a>

## NumpyEncoder Objects

```python
class NumpyEncoder(json.JSONEncoder)
```

Numpy and Pandas data types to JSON types encoder

<a id="evidently.utils.numpy_encoder.NumpyEncoder.default"></a>

#### default

```python
def default(o)
```

JSON converter calls the method when it cannot convert an object to a Python type
Convert the object to a Python type

If we cannot convert the object, leave the default `JSONEncoder` behaviour - raise a TypeError exception.

<a id="evidently.utils.types"></a>

# evidently.utils.types

Additional types, classes, dataclasses, etc.

<a id="evidently.utils.types.ApproxValue"></a>

## ApproxValue Objects

```python
class ApproxValue()
```

Class for approximate scalar value calculations

<a id="evidently.utils.visualizations"></a>

# evidently.utils.visualizations

<a id="evidently.utils.visualizations.plot_num_feature_in_time"></a>

#### plot\_num\_feature\_in\_time

```python
def plot_num_feature_in_time(curr_data: pd.DataFrame,
                             ref_data: Optional[pd.DataFrame],
                             feature_name: str, datetime_name: str, freq: str,
                             color_options: ColorOptions)
```

Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.

<a id="evidently.utils.visualizations.plot_time_feature_distr"></a>

#### plot\_time\_feature\_distr

```python
def plot_time_feature_distr(curr_data: pd.DataFrame,
                            ref_data: Optional[pd.DataFrame],
                            feature_name: str, color_options: ColorOptions)
```

Accepts current and reference data as pandas dataframes with two columns: feature_name, "number_of_items"

<a id="evidently.utils.visualizations.plot_cat_feature_in_time"></a>

#### plot\_cat\_feature\_in\_time

```python
def plot_cat_feature_in_time(curr_data: pd.DataFrame,
                             ref_data: Optional[pd.DataFrame],
                             feature_name: str, datetime_name: str, freq: str,
                             color_options: ColorOptions)
```

Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.

<a id="evidently.utils.visualizations.plot_boxes"></a>

#### plot\_boxes

```python
def plot_boxes(curr_for_plots: dict, ref_for_plots: Optional[dict],
               yaxis_title: str, xaxis_title: str,
               color_options: ColorOptions)
```

Accepts current and reference data as dicts with box parameters ("mins", "lowers", "uppers", "means", "maxs")
and name of boxes parameter - "values"

<a id="evidently.utils.visualizations.plot_cat_cat_rel"></a>

#### plot\_cat\_cat\_rel

```python
def plot_cat_cat_rel(curr: pd.DataFrame, ref: pd.DataFrame, target_name: str,
                     feature_name: str, color_options: ColorOptions)
```

Accepts current and reference data as pandas dataframes with two columns: feature_name and "count_objects".

