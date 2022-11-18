# evidently.utils package

## Submodules

## evidently.utils.data_operations module

Methods for clean null or NaN values in a dataset


### _class_ evidently.utils.data_operations.DatasetColumns(utility_columns: evidently.utils.data_operations.DatasetUtilityColumns, target_type: Optional[str], num_feature_names: List[str], cat_feature_names: List[str], datetime_feature_names: List[str], target_names: Optional[List[str]], task: Optional[str])
Bases: `object`


#### as_dict()

#### cat_feature_names(_: List[str_ )

#### datetime_feature_names(_: List[str_ )

#### get_all_columns_list()
List all columns.


#### get_all_features_list(cat_before_num: bool = True, include_datetime_feature: bool = False)
List all features names.

By default, returns cat features than num features and du not return other.

If you want to change the order - set  cat_before_num to False.

If you want to add date time columns - set include_datetime_feature to True.


#### get_features_len(include_time_columns: bool = False)
How mane feature do we have. It is useful for pagination in widgets.

By default, we sum category nad numeric features.

If you want to include date time columns - set include_datetime_feature to True.


#### num_feature_names(_: List[str_ )

#### target_names(_: Optional[List[str]_ )

#### target_type(_: Optional[str_ )

#### task(_: Optional[str_ )

#### utility_columns(_: DatasetUtilityColumn_ )

### _class_ evidently.utils.data_operations.DatasetUtilityColumns(date: Optional[str], id_column: Optional[str], target: Optional[str], prediction: Union[str, Sequence[str], NoneType])
Bases: `object`


#### as_dict()

#### date(_: Optional[str_ )

#### id_column(_: Optional[str_ )

#### prediction(_: Optional[Union[str, Sequence[str]]_ )

#### target(_: Optional[str_ )

### evidently.utils.data_operations.process_columns(dataset: DataFrame, column_mapping: [ColumnMapping](api-reference/evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

### evidently.utils.data_operations.recognize_column_type(dataset: DataFrame, column_name: str, columns: DatasetColumns)
Try to get the column type.


### evidently.utils.data_operations.recognize_task(target_name: str, dataset: DataFrame)
Try to guess about the target type:
if the target has a numeric type and number of unique values > 5: task == ‘regression’
in all other cases task == ‘classification’.


* **Parameters**

    - **target_name** – name of target column.

    - **dataset** – usually the data which you used in training.



* **Returns**

    Task parameter.



### evidently.utils.data_operations.replace_infinity_values_to_nan(dataframe: DataFrame)
## evidently.utils.generators module


### _class_ evidently.utils.generators.BaseGenerator()
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

class TestQuantiles(BaseTestGenerator):

    def generate(self, columns_info: DatasetColumns) -> List[TestValueQuantile]:

        return [

            TestValueQuantile(column_name=name, quantile=quantile)
            for quantile in (0.5, 0.9, 0.99)
            for name in columns_info.num_feature_names

        ]

Do not forget set correct test type for generate return value


#### _abstract_ generate(columns_info: DatasetColumns)

### evidently.utils.generators.make_generator_by_columns(base_class: Type, columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
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

## evidently.utils.numpy_encoder module


### _class_ evidently.utils.numpy_encoder.NumpyEncoder(\*, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, sort_keys=False, indent=None, separators=None, default=None)
Bases: `JSONEncoder`

Numpy and Pandas data types to JSON types encoder


#### default(o)
JSON converter calls the method when it cannot convert an object to a Python type
Convert the object to a Python type

If we cannot convert the object, leave the default JSONEncoder behaviour - raise a TypeError exception.

## evidently.utils.types module

Additional types, classes, dataclasses, etc.


### _class_ evidently.utils.types.ApproxValue(value: Union[float, int], relative: Optional[Union[float, int]] = None, absolute: Optional[Union[float, int]] = None)
Bases: `object`

Class for approximate scalar value calculations


#### DEFAULT_ABSOLUTE(_ = 1e-1_ )

#### DEFAULT_RELATIVE(_ = 1e-0_ )

#### as_dict()

#### _property_ tolerance(_: Union[float, int_ )

#### value(_: Union[float, int_ )
## evidently.utils.visualizations module


### _class_ evidently.utils.visualizations.Distribution(x: Union[<built-in function array>, list], y: Union[<built-in function array>, list])
Bases: `object`


#### x(_: Union[array, list_ )

#### y(_: Union[array, list_ )

### evidently.utils.visualizations.get_distribution_for_category_column(column: Series, normalize: bool = False)

### evidently.utils.visualizations.get_distribution_for_column(\*, column_type: str, current: Series, reference: Optional[Series] = None)

### evidently.utils.visualizations.get_distribution_for_numerical_column(column: Series, bins: Optional[Union[list, array]] = None)

### evidently.utils.visualizations.make_hist_df(hist: Tuple[array, array])

### evidently.utils.visualizations.make_hist_for_cat_plot(curr: Series, ref: Optional[Series] = None, normalize: bool = False, dropna=False)

### evidently.utils.visualizations.make_hist_for_num_plot(curr: Series, ref: Optional[Series] = None)

### evidently.utils.visualizations.plot_boxes(curr_for_plots: dict, ref_for_plots: Optional[dict], yaxis_title: str, xaxis_title: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as dicts with box parameters (“mins”, “lowers”, “uppers”, “means”, “maxs”)
and name of boxes parameter - “values”


### evidently.utils.visualizations.plot_cat_cat_rel(curr: DataFrame, ref: DataFrame, target_name: str, feature_name: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: feature_name and “count_objects”.


### evidently.utils.visualizations.plot_cat_feature_in_time(curr_data: DataFrame, ref_data: Optional[DataFrame], feature_name: str, datetime_name: str, freq: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.


### evidently.utils.visualizations.plot_conf_mtrx(curr_mtrx, ref_mtrx)

### evidently.utils.visualizations.plot_distr(\*, hist_curr, hist_ref=None, orientation='v', color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_distr_subplots(\*, hist_curr, hist_ref=None, xaxis_name: str = '', yaxis_name: str = '', same_color: bool = False, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_distr_with_log_button(curr_data: DataFrame, curr_data_log: DataFrame, ref_data: Optional[DataFrame], ref_data_log: Optional[DataFrame], color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_error_bias_colored_scatter(curr_scatter_data: Dict[str, Dict[str, Series]], ref_scatter_data: Optional[Dict[str, Dict[str, Series]]], color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_line_in_time(\*, curr: Dict[str, Series], ref: Optional[Dict[str, Series]], x_name: str, y_name: str, xaxis_name: str = '', yaxis_name: str = '', color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_num_feature_in_time(curr_data: DataFrame, ref_data: Optional[DataFrame], feature_name: str, datetime_name: str, freq: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: datetime_name and feature_name.


### evidently.utils.visualizations.plot_num_num_rel(curr: Dict[str, list], ref: Optional[Dict[str, list]], target_name: str, column_name: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_pred_actual_time(\*, curr: Dict[str, Series], ref: Optional[Dict[str, Series]], x_name: str = 'x', xaxis_name: str = '', yaxis_name: str = '', color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_scatter(\*, curr: Dict[str, Union[list, Series]], ref: Optional[Dict[str, list]], x: str, y: str, xaxis_name: Optional[str] = None, yaxis_name: Optional[str] = None, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_scatter_for_data_drift(curr_y: list, curr_x: list, y0: float, y1: float, y_name: str, x_name: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.utils.visualizations.plot_time_feature_distr(curr_data: DataFrame, ref_data: Optional[DataFrame], feature_name: str, color_options: [ColorOptions](api-reference/evidently.options.md#evidently.options.color_scheme.ColorOptions))
Accepts current and reference data as pandas dataframes with two columns: feature_name, “number_of_items”

## Module contents
