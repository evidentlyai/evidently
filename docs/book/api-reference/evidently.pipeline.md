# evidently.pipeline package

## Submodules

## evidently.pipeline.column_mapping module


### _class_ evidently.pipeline.column_mapping.ColumnMapping(target: Optional[str] = 'target', prediction: Union[str, int, Sequence[str], Sequence[int], NoneType] = 'prediction', datetime: Optional[str] = 'datetime', id: Optional[str] = None, numerical_features: Optional[List[str]] = None, categorical_features: Optional[List[str]] = None, datetime_features: Optional[List[str]] = None, target_names: Optional[List[str]] = None, task: Optional[str] = None, pos_label: Union[str, int, NoneType] = 1)
Bases: `object`


#### categorical_features(_: Optional[List[str]_ _ = Non_ )

#### datetime(_: Optional[str_ _ = 'datetime_ )

#### datetime_features(_: Optional[List[str]_ _ = Non_ )

#### id(_: Optional[str_ _ = Non_ )

#### is_classification_task()

#### is_regression_task()

#### numerical_features(_: Optional[List[str]_ _ = Non_ )

#### pos_label(_: Optional[Union[str, int]_ _ = _ )

#### prediction(_: Optional[Union[str, int, Sequence[str], Sequence[int]]_ _ = 'prediction_ )

#### target(_: Optional[str_ _ = 'target_ )

#### target_names(_: Optional[List[str]_ _ = Non_ )

#### task(_: Optional[str_ _ = Non_ )

### _class_ evidently.pipeline.column_mapping.TaskType()
Bases: `object`


#### CLASSIFICATION_TASK(_: st_ _ = 'classification_ )

#### REGRESSION_TASK(_: st_ _ = 'regression_ )
## evidently.pipeline.pipeline module


### _class_ evidently.pipeline.pipeline.Pipeline(stages: Sequence[PipelineStage], options: list)
Bases: `object`


#### analyzers_results(_: Dict[Type[Analyzer], object_ )

#### execute(reference_data: DataFrame, current_data: Optional[DataFrame] = None, column_mapping: Optional[ColumnMapping] = None)

#### get_analyzers()

#### options_provider(_: [OptionsProvider](api-reference/evidently.options.md#evidently.options.OptionsProvider_ )

#### stages(_: Sequence[PipelineStage_ )
## evidently.pipeline.stage module


### _class_ evidently.pipeline.stage.PipelineStage()
Bases: `object`


#### add_analyzer(analyzer_type: Type[Analyzer])

#### analyzers()

#### _abstract_ calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: ColumnMapping, analyzers_results: Dict[Type[Analyzer], Any])

#### options_provider(_: [OptionsProvider](api-reference/evidently.options.md#evidently.options.OptionsProvider_ )
## Module contents
