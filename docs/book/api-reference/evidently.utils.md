# evidently.utils package

## Submodules

Methods for clean null or NaN values in a dataset


### _class_ DatasetColumns(utility_columns: DatasetUtilityColumns, target_type: Optional[str], num_feature_names: List[str], cat_feature_names: List[str], datetime_feature_names: List[str], target_names: Optional[List[str]], task: Optional[str])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_feature_names _: List[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime_feature_names _: List[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_feature_names _: List[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_names _: Optional[List[str]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_type _: Optional[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; task _: Optional[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; utility_columns _: DatasetUtilityColumns_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_all_columns_list()
List all columns.

##### &nbsp;&nbsp;&nbsp;&nbsp; get_all_features_list(cat_before_num: bool = True, include_datetime_feature: bool = False)
List all features names.
By default, returns cat features than num features and du not return other.
If you want to change the order - set  cat_before_num to False.
If you want to add date time columns - set include_datetime_feature to True.

##### &nbsp;&nbsp;&nbsp;&nbsp; get_features_len(include_time_columns: bool = False)
How mane feature do we have. It is useful for pagination in widgets.
By default, we sum category nad numeric features.
If you want to include date time columns - set include_datetime_feature to True.

### _class_ DatasetUtilityColumns(date: Optional[str], id_column: Optional[str], target: Optional[str], prediction: Union[str, Sequence[str], NoneType])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; date _: Optional[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; id_column _: Optional[str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction _: Optional[Union[str, Sequence[str]]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target _: Optional[str]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

### process_columns(dataset: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### recognize_column_type(dataset: DataFrame, column_name: str, columns: DatasetColumns)
Try to get the column type.


### recognize_task(target_name: str, dataset: DataFrame)
Try to guess about the target type:
if the target has a numeric type and number of unique values > 5: task == ‘regression’
in all other cases task == ‘classification’.


* **Parameters**

    - **target_name** – name of target column.

    - **dataset** – usually the data which you used in training.



* **Returns**

    Task parameter.



### replace_infinity_values_to_nan(dataframe: DataFrame)

### _class_ ColumnDefinition(column_name: str, column_type: ColumnType)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_type _: ColumnType_ 

#### Methods: 

### _class_ ColumnPresenceState(value)
Bases: `Enum`

An enumeration.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; Missing _ = 2_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Partially _ = 1_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Present _ = 0_ 

#### Methods: 

### _class_ ColumnType(value)
Bases: `Enum`

An enumeration.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; Categorical _ = 'cat'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Datetime _ = 'datetime'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Numerical _ = 'num'_ 

#### Methods: 

### _class_ DataDefinition(columns: List[ColumnDefinition], target: Optional[ColumnDefinition], prediction_columns: Optional[PredictionColumns], id_column: Optional[ColumnDefinition], datetime_column: Optional[ColumnDefinition], task: Optional[str], classification_labels: Optional[Sequence[str]])
Bases: `object`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; classification_labels()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_columns(filter_def: str = 'all')

##### &nbsp;&nbsp;&nbsp;&nbsp; get_datetime_column()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_id_column()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_prediction_columns()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_target_column()

##### &nbsp;&nbsp;&nbsp;&nbsp; task()

### _class_ PredictionColumns(predicted_values: Optional[ColumnDefinition] = None, prediction_probas: Optional[List[ColumnDefinition]] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; predicted_values _: Optional[ColumnDefinition]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction_probas _: Optional[List[ColumnDefinition]]_ _ = None_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_columns_list()

### create_data_definition(reference_data: Optional[DataFrame], current_data: DataFrame, mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### _class_ BaseGenerator()
Bases: `Generic`[`TObject`]

Base class for tests and metrics generator creation

To create a new generator:

    - inherit a class from the base class

    - implement generate_tests method and return a list of test objects from it

A Suite or a Report will call the method and add generated tests to its list instead of the generator object.

You can use columns_info parameter in generate for getting data structure meta info like columns list.

For example:

    if you want to create a test generator for 50, 90, 99 quantiles tests
    for all numeric columns with default condition, by reference quantiles

```python
>>> class TestQuantiles(BaseTestGenerator):
...    def generate(self, columns_info: DatasetColumns) -> List[TestValueQuantile]:
...        return [
...            TestValueQuantile(column_name=name, quantile=quantile)
...            for quantile in (0.5, 0.9, 0.99)
...            for name in columns_info.num_feature_names
...        ]
```

Do not forget set correct test type for generate return value

#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ generate(columns_info: DatasetColumns)

### make_generator_by_columns(base_class: Type, columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Create a test generator for a columns list with a test class.

Base class is specified with base_class parameter.
If the test have no “column_name” parameter - TypeError will be raised.

Columns list can be defined with parameter columns.
If it is a list - just use it as a list of the columns.
If columns is a string, it can be one of values:
- “all” - make tests for all columns, including target/prediction columns
- “num” - for numeric features
- “cat” - for category features
- “features” - for all features, not target/prediction columns.
None value is the same as “all”.
If columns is string, and it is not one of the values, ValueError will be raised.

parameters is used for specifying other parameters for each object, it is the same for all generated objects.


### _class_ NumpyEncoder(\*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)
Bases: `JSONEncoder`

Numpy and Pandas data types to JSON types encoder


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; default(o)
JSON converter calls the method when it cannot convert an object to a Python type
Convert the object to a Python type
If we cannot convert the object, leave the default JSONEncoder behaviour - raise a TypeError exception.
Additional types, classes, dataclasses, etc.


### _class_ ApproxValue(value: Union[float, int], relative: Optional[Union[float, int]] = None, absolute: Optional[Union[float, int]] = None)
Bases: `object`

Class for approximate scalar value calculations

##### &nbsp;&nbsp;&nbsp;&nbsp; _property_ tolerance _: Union[float, int]_ 
#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; DEFAULT_ABSOLUTE _ = 1e-12_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; DEFAULT_RELATIVE _ = 1e-06_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

### _class_ Distribution(x: Union[<built-in function array>, list], y: Union[<built-in function array>, list])
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; x _: Union[array, list]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; y _: Union[array, list]_ 

#### Methods: 

### get_distribution_for_category_column(column: Series, normalize: bool = False)

### get_distribution_for_column(\*, column_type: str, current: Series, reference: Optional[Series] = None)

### get_distribution_for_numerical_column(column: Series, bins: Optional[Union[list, array]] = None)

### make_hist_df(hist: Tuple[array, array])

### make_hist_for_cat_plot(curr: Series, ref: Optional[Series] = None, normalize: bool = False, dropna=False)

### make_hist_for_num_plot(curr: Series, ref: Optional[Series] = None)

### plot_boxes(curr_for_plots: dict, ref_for_plots: Optional[dict], yaxis_title: str, xaxis_title: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as dicts with box parameters (“mins”, “lowers”, “uppers”, “means”, “maxs”)
and name of boxes parameter - “values”


### plot_cat_cat_rel(curr: DataFrame, ref: DataFrame, target_name: str, feature_name: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: feature_name and “count_objects”.


### plot_cat_feature_in_time(curr_data: DataFrame, ref_data: Optional[DataFrame], feature_name: str, datetime_name: str, freq: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.


### plot_conf_mtrx(curr_mtrx, ref_mtrx)

### plot_distr(\*, hist_curr, hist_ref=None, orientation='v', color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_distr_subplots(\*, hist_curr, hist_ref=None, xaxis_name: str = '', yaxis_name: str = '', same_color: bool = False, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_distr_with_log_button(curr_data: DataFrame, curr_data_log: DataFrame, ref_data: Optional[DataFrame], ref_data_log: Optional[DataFrame], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_error_bias_colored_scatter(curr_scatter_data: Dict[str, Dict[str, Series]], ref_scatter_data: Optional[Dict[str, Dict[str, Series]]], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_line_in_time(\*, curr: Dict[str, Series], ref: Optional[Dict[str, Series]], x_name: str, y_name: str, xaxis_name: str = '', yaxis_name: str = '', color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_num_feature_in_time(curr_data: DataFrame, ref_data: Optional[DataFrame], feature_name: str, datetime_name: str, freq: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.


### plot_num_num_rel(curr: Dict[str, list], ref: Optional[Dict[str, list]], target_name: str, column_name: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_pred_actual_time(\*, curr: Dict[str, Series], ref: Optional[Dict[str, Series]], x_name: str = 'x', xaxis_name: str = '', yaxis_name: str = '', color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_scatter(\*, curr: Dict[str, Union[list, Series]], ref: Optional[Dict[str, list]], x: str, y: str, xaxis_name: Optional[str] = None, yaxis_name: Optional[str] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_scatter_for_data_drift(curr_y: list, curr_x: list, y0: float, y1: float, y_name: str, x_name: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_time_feature_distr(curr_data: DataFrame, ref_data: Optional[DataFrame], feature_name: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: feature_name, “number_of_items”

## Module contents
