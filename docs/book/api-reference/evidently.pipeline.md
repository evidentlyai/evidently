# evidently.pipeline package

## Submodules


### _class_ ColumnMapping(target: Optional[str] = 'target', prediction: Union[str, int, Sequence[str], Sequence[int], NoneType] = 'prediction', datetime: Optional[str] = 'datetime', id: Optional[str] = None, numerical_features: Optional[List[str]] = None, categorical_features: Optional[List[str]] = None, datetime_features: Optional[List[str]] = None, target_names: Optional[List[str]] = None, task: Optional[str] = None, pos_label: Union[str, int, NoneType] = 1)
Bases: `object`

#### Attributes: 

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

##### &nbsp;&nbsp;&nbsp;&nbsp; is_classification_task()

##### &nbsp;&nbsp;&nbsp;&nbsp; is_regression_task()

### _class_ TaskType()
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; CLASSIFICATION_TASK _: str_ _ = 'classification'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; REGRESSION_TASK _: str_ _ = 'regression'_ 

#### Methods: 

### _class_ Pipeline(stages: Sequence[PipelineStage], options: list)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; analyzers_results _: Dict[Type[Analyzer], object]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; stages _: Sequence[PipelineStage]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; execute(reference_data: DataFrame, current_data: Optional[DataFrame] = None, column_mapping: Optional[ColumnMapping] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; get_analyzers()

### _class_ PipelineStage()
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; add_analyzer(analyzer_type: Type[Analyzer])

##### &nbsp;&nbsp;&nbsp;&nbsp; analyzers()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: ColumnMapping, analyzers_results: Dict[Type[Analyzer], Any])
## Module contents
