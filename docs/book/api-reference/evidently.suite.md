# evidently.suite package

## Submodules


### _class _ Context(execution_graph: Optional[ExecutionGraph], metrics: list, tests: list, metric_results: dict, test_results: dict, state: State, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))
Bases: `object`

Pipeline execution context tracks pipeline execution and lifecycle


#### execution_graph _: Optional[ExecutionGraph]_ 

#### metric_results _: dict_ 

#### metrics _: list_ 

#### renderers _: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions)_ 

#### state _: State_ 

#### test_results _: dict_ 

#### tests _: list_ 

### _class _ Display(options: Optional[list] = None)
Bases: `object`


#### _abstract _ as_dict()

#### json()

#### options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### save_html(filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE)

#### save_json(filename)

#### show(mode='auto')

### _exception _ ExecutionError()
Bases: `Exception`


### _class _ State(name: str)
Bases: `object`


#### name _: str_ 

### _class _ States()
Bases: `object`


#### Calculated _ = State(name='Calculated')_ 

#### Init _ = State(name='Init')_ 

#### Tested _ = State(name='Tested')_ 

#### Verified _ = State(name='Verified')_ 

### _class _ Suite()
Bases: `object`


#### add_metric(metric: [Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric))

#### add_test(test: [Test](evidently.tests.md#evidently.tests.base_test.Test))

#### context _: Context_ 

#### run_calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### run_checks()

#### verify()

### find_metric_renderer(obj, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### find_test_renderer(obj, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### _class _ ExecutionGraph()
Bases: `object`


#### _abstract _ get_metric_execution_iterator()

#### _abstract _ get_test_execution_iterator()

### _class _ SimpleExecutionGraph(metrics: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)], tests: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)])
Bases: `ExecutionGraph`

Simple execution graph without any work with dependencies at all,

    assumes that metrics already in order for execution


#### get_metric_execution_iterator()

#### get_test_execution_iterator()

#### metrics _: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)]_ 

#### tests _: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)]_ 
## Module contents
