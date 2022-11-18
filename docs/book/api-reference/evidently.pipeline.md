# evidently.pipeline package

## Submodules


### _class _ ColumnMapping(target: Optional[str] = 'target', prediction: Union[str, int, Sequence[str], Sequence[int], NoneType] = 'prediction', datetime: Optional[str] = 'datetime', id: Optional[str] = None, numerical_features: Optional[List[str]] = None, categorical_features: Optional[List[str]] = None, datetime_features: Optional[List[str]] = None, target_names: Optional[List[str]] = None, task: Optional[str] = None, pos_label: Union[str, int, NoneType] = 1)
Bases: `object`


#### Attributes: 

##### labels _: Sequence[Union[str, int]]_ 

##### values _: list_ 

##### exception _: BaseException_ 

##### column_name _: str_ 

##### options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

##### different_missing_values _: Dict[Any, int]_ 

##### number_of_different_missing_values _: int_ 

##### number_of_missing_values _: int_ 

##### number_of_rows _: int_ 

##### share_of_missing_values _: float_ 

##### column_name _: str_ 

##### color_sequence _: Sequence[str]_ _ = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4')_ 

##### current_data_color _: Optional[str]_ _ = None_ 

##### fill_color _: str_ _ = 'LightGreen'_ 

##### heatmap _: str_ _ = 'RdBu_r'_ 

##### majority_color _: str_ _ = '#1acc98'_ 

##### non_visible_color _: str_ _ = 'white'_ 

##### overestimation_color _: str_ _ = '#ee5540'_ 

##### primary_color _: str_ _ = '#ed0400'_ 

##### reference_data_color _: Optional[str]_ _ = None_ 

##### secondary_color _: str_ _ = '#4d4d4d'_ 

##### underestimation_color _: str_ _ = '#6574f7'_ 

##### vertical_lines _: str_ _ = 'green'_ 

##### zero_line_color _: str_ _ = 'green'_ 

##### categorical_features _: Optional[List[str]]_ _ = None_ 

##### datetime _: Optional[str]_ _ = 'datetime'_ 

##### datetime_features _: Optional[List[str]]_ _ = None_ 

##### id _: Optional[str]_ _ = None_ 

##### numerical_features _: Optional[List[str]]_ _ = None_ 

##### pos_label _: Optional[Union[str, int]]_ _ = 1_ 

##### prediction _: Optional[Union[str, int, Sequence[str], Sequence[int]]]_ _ = 'prediction'_ 

##### target _: Optional[str]_ _ = 'target'_ 

##### target_names _: Optional[List[str]]_ _ = None_ 

##### task _: Optional[str]_ _ = None_ 

#### Methods: 

##### generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

##### get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### get_current_data_color()

##### get_reference_data_color()

##### is_classification_task()

##### is_regression_task()

### _class _ TaskType()
Bases: `object`


#### Attributes: 

##### CLASSIFICATION_TASK _: str_ _ = 'classification'_ 

##### REGRESSION_TASK _: str_ _ = 'regression'_ 

#### Methods: 

### _class _ Pipeline(stages: Sequence[PipelineStage], options: list)
Bases: `object`


#### Attributes: 

##### analyzers_results _: Dict[Type[Analyzer], object]_ 

##### options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

##### stages _: Sequence[PipelineStage]_ 

#### Methods: 

##### execute(reference_data: DataFrame, current_data: Optional[DataFrame] = None, column_mapping: Optional[ColumnMapping] = None)

##### get_analyzers()

### _class _ PipelineStage()
Bases: `object`


#### Attributes: 

##### options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### Methods: 

##### add_analyzer(analyzer_type: Type[Analyzer])

##### analyzers()

##### _abstract _ calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: ColumnMapping, analyzers_results: Dict[Type[Analyzer], Any])
## Module contents
