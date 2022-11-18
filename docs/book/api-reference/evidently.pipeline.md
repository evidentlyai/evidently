# evidently.pipeline package

## Submodules


### _class _ ColumnMapping(target: Optional[str] = 'target', prediction: Union[str, int, Sequence[str], Sequence[int], NoneType] = 'prediction', datetime: Optional[str] = 'datetime', id: Optional[str] = None, numerical_features: Optional[List[str]] = None, categorical_features: Optional[List[str]] = None, datetime_features: Optional[List[str]] = None, target_names: Optional[List[str]] = None, task: Optional[str] = None, pos_label: Union[str, int, NoneType] = 1)
Bases: `object`


#### categorical_features _: Optional[List[str]]_ _ = None_ 

#### datetime _: Optional[str]_ _ = 'datetime'_ 

#### datetime_features _: Optional[List[str]]_ _ = None_ 

#### id _: Optional[str]_ _ = None_ 

#### is_classification_task()

#### is_regression_task()

#### numerical_features _: Optional[List[str]]_ _ = None_ 

#### pos_label _: Optional[Union[str, int]]_ _ = 1_ 

#### prediction _: Optional[Union[str, int, Sequence[str], Sequence[int]]]_ _ = 'prediction'_ 

#### target _: Optional[str]_ _ = 'target'_ 

#### target_names _: Optional[List[str]]_ _ = None_ 

#### task _: Optional[str]_ _ = None_ 

### _class _ TaskType()
Bases: `object`


#### CLASSIFICATION_TASK _: str_ _ = 'classification'_ 

#### REGRESSION_TASK _: str_ _ = 'regression'_ 

### _class _ Pipeline(stages: Sequence[PipelineStage], options: list)
Bases: `object`


#### analyzers_results _: Dict[Type[Analyzer], object]_ 

#### execute(reference_data: DataFrame, current_data: Optional[DataFrame] = None, column_mapping: Optional[ColumnMapping] = None)

#### get_analyzers()

#### options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### stages _: Sequence[PipelineStage]_ 

### _class _ PipelineStage()
Bases: `object`


#### add_analyzer(analyzer_type: Type[Analyzer])

#### analyzers()

#### _abstract _ calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: ColumnMapping, analyzers_results: Dict[Type[Analyzer], Any])

#### options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 
## Module contents
