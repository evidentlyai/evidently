# evidently.pipeline package

## Submodules


### _class _ ColumnMapping(target: Optional[str] = 'target', prediction: Union[str, int, Sequence[str], Sequence[int], NoneType] = 'prediction', datetime: Optional[str] = 'datetime', id: Optional[str] = None, numerical_features: Optional[List[str]] = None, categorical_features: Optional[List[str]] = None, datetime_features: Optional[List[str]] = None, target_names: Optional[List[str]] = None, task: Optional[str] = None, pos_label: Union[str, int, NoneType] = 1)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; exception _: BaseException_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; different_missing_values _: Dict[Any, int]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_sequence _: Sequence[str]_ _ = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; current_data_color _: Optional[str]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; fill_color _: str_ _ = 'LightGreen'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; heatmap _: str_ _ = 'RdBu_r'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; majority_color _: str_ _ = '#1acc98'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; non_visible_color _: str_ _ = 'white'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; overestimation_color _: str_ _ = '#ee5540'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; primary_color _: str_ _ = '#ed0400'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; reference_data_color _: Optional[str]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; secondary_color _: str_ _ = '#4d4d4d'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; underestimation_color _: str_ _ = '#6574f7'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; vertical_lines _: str_ _ = 'green'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; zero_line_color _: str_ _ = 'green'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; categorical_features _: Optional[List[str]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime _: Optional[str]_ _ = 'datetime'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime_features _: Optional[List[str]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; id _: Optional[str]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; numerical_features _: Optional[List[str]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; pos_label _: Optional[Union[str, int]]_ _ = 1_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction _: Optional[Union[str, int, Sequence[str], Sequence[int]]]_ _ = 'prediction'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target _: Optional[str]_ _ = 'target'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_names _: Optional[List[str]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; task _: Optional[str]_ _ = None_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; get_current_data_color()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_reference_data_color()

##### &nbsp;&nbsp;&nbsp;&nbsp; is_classification_task()

##### &nbsp;&nbsp;&nbsp;&nbsp; is_regression_task()

### _class _ TaskType()
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; CLASSIFICATION_TASK _: str_ _ = 'classification'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; REGRESSION_TASK _: str_ _ = 'regression'_ 

#### Methods: 

### _class _ Pipeline(stages: Sequence[PipelineStage], options: list)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; analyzers_results _: Dict[Type[Analyzer], object]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; stages _: Sequence[PipelineStage]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; execute(reference_data: DataFrame, current_data: Optional[DataFrame] = None, column_mapping: Optional[ColumnMapping] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; get_analyzers()

### _class _ PipelineStage()
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; add_analyzer(analyzer_type: Type[Analyzer])

##### &nbsp;&nbsp;&nbsp;&nbsp; analyzers()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: ColumnMapping, analyzers_results: Dict[Type[Analyzer], Any])
## Module contents
