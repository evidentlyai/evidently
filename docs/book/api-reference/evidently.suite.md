# evidently.suite package

## Submodules


### _class _ Context(execution_graph: Optional[ExecutionGraph], metrics: list, tests: list, metric_results: dict, test_results: dict, state: State, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))
Bases: `object`

Pipeline execution context tracks pipeline execution and lifecycle


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

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

##### metrics _: List[Union[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric), [MetricPreset](evidently.metric_preset.md#evidently.metric_preset.metric_preset.MetricPreset), [BaseGenerator](evidently.utils.md#evidently.utils.generators.BaseGenerator)]]_ 

##### execution_graph _: Optional[ExecutionGraph]_ 

##### metric_results _: dict_ 

##### metrics _: list_ 

##### renderers _: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions)_ 

##### state _: State_ 

##### test_results _: dict_ 

##### tests _: list_ 

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

##### as_dict()

##### run(\*, reference_data: Optional[DataFrame], current_data: DataFrame, column_mapping: Optional[[ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)] = None)

### _class _ Display(options: Optional[list] = None)
Bases: `object`


#### Attributes: 

##### options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### Methods: 

##### _abstract _ as_dict()

##### json()

##### save_html(filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE)

##### save_json(filename)

##### show(mode='auto')

### _exception _ ExecutionError()
Bases: `Exception`


### _class _ State(name: str)
Bases: `object`


#### Attributes: 

##### name _: str_ 

#### Methods: 

### _class _ States()
Bases: `object`


#### Attributes: 

##### Calculated _ = State(name='Calculated')_ 

##### Init _ = State(name='Init')_ 

##### Tested _ = State(name='Tested')_ 

##### Verified _ = State(name='Verified')_ 

#### Methods: 

### _class _ Suite()
Bases: `object`


#### Attributes: 

##### context _: Context_ 

#### Methods: 

##### add_metric(metric: [Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric))

##### add_test(test: [Test](evidently.tests.md#evidently.tests.base_test.Test))

##### run_calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### run_checks()

##### verify()

### find_metric_renderer(obj, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### find_test_renderer(obj, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### _class _ ExecutionGraph()
Bases: `object`


#### Attributes: 

#### Methods: 

##### _abstract _ get_metric_execution_iterator()

##### _abstract _ get_test_execution_iterator()

### _class _ SimpleExecutionGraph(metrics: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)], tests: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)])
Bases: `ExecutionGraph`

Simple execution graph without any work with dependencies at all,

    assumes that metrics already in order for execution


#### Attributes: 

##### metrics _: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)]_ 

##### tests _: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)]_ 

#### Methods: 

##### get_metric_execution_iterator()

##### get_test_execution_iterator()
## Module contents
