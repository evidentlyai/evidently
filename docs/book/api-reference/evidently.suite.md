# evidently.suite package

## Submodules


### _class _ Context(execution_graph: Optional[ExecutionGraph], metrics: list, tests: list, metric_results: dict, test_results: dict, state: State, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))
Bases: `object`

Pipeline execution context tracks pipeline execution and lifecycle


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

### _class _ Display(options: Optional[list] = None)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; json()

##### &nbsp;&nbsp;&nbsp;&nbsp; save_html(filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE)

##### &nbsp;&nbsp;&nbsp;&nbsp; save_json(filename)

##### &nbsp;&nbsp;&nbsp;&nbsp; show(mode='auto')

### _exception _ ExecutionError()
Bases: `Exception`


### _class _ State(name: str)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#### Methods: 

### _class _ States()
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; Calculated _ = State(name='Calculated')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Init _ = State(name='Init')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Tested _ = State(name='Tested')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Verified _ = State(name='Verified')_ 

#### Methods: 

### _class _ Suite()
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; context _: Context_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; add_metric(metric: [Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric))

##### &nbsp;&nbsp;&nbsp;&nbsp; add_test(test: [Test](evidently.tests.md#evidently.tests.base_test.Test))

##### &nbsp;&nbsp;&nbsp;&nbsp; run_calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

##### &nbsp;&nbsp;&nbsp;&nbsp; run_checks()

##### &nbsp;&nbsp;&nbsp;&nbsp; verify()

### find_metric_renderer(obj, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### find_test_renderer(obj, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### _class _ ExecutionGraph()
Bases: `object`


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_metric_execution_iterator()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_test_execution_iterator()

### _class _ SimpleExecutionGraph(metrics: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)], tests: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)])
Bases: `ExecutionGraph`

Simple execution graph without any work with dependencies at all,

    assumes that metrics already in order for execution


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics _: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; tests _: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_metric_execution_iterator()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_test_execution_iterator()
## Module contents
