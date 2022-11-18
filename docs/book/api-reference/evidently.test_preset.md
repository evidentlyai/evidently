# evidently.test_preset package

## Submodules


### _class _ BinaryClassificationTestPreset(prediction_type: str, threshold: float = 0.5)
Bases: `TestPreset`


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

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics _: List[Union[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric), [MetricPreset](evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset), [BaseGenerator](evidently.utils.md#evidently.utils.generators.BaseGenerator)]]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; execution_graph _: Optional[ExecutionGraph]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric_results _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics _: list_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; renderers _: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; state _: State_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; test_results _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; tests _: list_ 

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

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; run(\*, reference_data: Optional[DataFrame], current_data: DataFrame, column_mapping: Optional[[ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ BinaryClassificationTopKTestPreset(k: Union[float, int])
Bases: `TestPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ MulticlassClassificationTestPreset(prediction_type: str)
Bases: `TestPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataDriftTestPreset()
Bases: `TestPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataQualityTestPreset()
Bases: `TestPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ DataStabilityTestPreset()
Bases: `TestPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ NoTargetPerformanceTestPreset(columns: Optional[List[str]] = None)
Bases: `TestPreset`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns _: List[str]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ RegressionTestPreset()
Bases: `TestPreset`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestPreset()
Bases: `object`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))
## Module contents
