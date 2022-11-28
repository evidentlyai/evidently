# evidently.pipeline package

## Submodules

## <a name="module-evidently.pipeline.column_mapping"></a>column_mapping module


### class ColumnMapping(target: Optional[str] = 'target', prediction: Union[str, int, Sequence[str], Sequence[int], NoneType] = 'prediction', datetime: Optional[str] = 'datetime', id: Optional[str] = None, numerical_features: Optional[List[str]] = None, categorical_features: Optional[List[str]] = None, datetime_features: Optional[List[str]] = None, target_names: Optional[List[str]] = None, task: Optional[str] = None, pos_label: Union[str, int, NoneType] = 1)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; categorical_features : Optional[List[str]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime : Optional[str]  = 'datetime' 

##### &nbsp;&nbsp;&nbsp;&nbsp; datetime_features : Optional[List[str]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; id : Optional[str]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; numerical_features : Optional[List[str]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; pos_label : Optional[Union[str, int]]  = 1 

##### &nbsp;&nbsp;&nbsp;&nbsp; prediction : Optional[Union[str, int, Sequence[str], Sequence[int]]]  = 'prediction' 

##### &nbsp;&nbsp;&nbsp;&nbsp; target : Optional[str]  = 'target' 

##### &nbsp;&nbsp;&nbsp;&nbsp; target_names : Optional[List[str]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; task : Optional[str]  = None 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; is_classification_task()

##### &nbsp;&nbsp;&nbsp;&nbsp; is_regression_task()

### class TaskType()
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; CLASSIFICATION_TASK : str  = 'classification' 

##### &nbsp;&nbsp;&nbsp;&nbsp; REGRESSION_TASK : str  = 'regression' 
## <a name="module-evidently.pipeline.pipeline"></a>pipeline module


### class Pipeline(stages: Sequence[PipelineStage], options: list)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; analyzers_results : Dict[Type[Analyzer], object] 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider : [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider) 

##### &nbsp;&nbsp;&nbsp;&nbsp; stages : Sequence[PipelineStage] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; execute(reference_data: DataFrame, current_data: Optional[DataFrame] = None, column_mapping: Optional[ColumnMapping] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; get_analyzers()
## <a name="module-evidently.pipeline.stage"></a>stage module


### class PipelineStage()
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider : [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; add_analyzer(analyzer_type: Type[Analyzer])

##### &nbsp;&nbsp;&nbsp;&nbsp; analyzers()

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  calculate(reference_data: DataFrame, current_data: DataFrame, column_mapping: ColumnMapping, analyzers_results: Dict[Type[Analyzer], Any])
