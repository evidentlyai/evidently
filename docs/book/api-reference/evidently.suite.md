# evidently.suite package

## Submodules


### _class_ Context(execution_graph: Optional[ExecutionGraph], metrics: list, tests: list, metric_results: dict, test_results: dict, state: State, renderers: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))
Bases: `object`

Pipeline execution context tracks pipeline execution and lifecycle

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; execution_graph _: Optional[ExecutionGraph]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric_results _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metrics _: list_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; renderers _: [RenderersDefinitions](evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; state _: State_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; test_results _: dict_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; tests _: list_ 

#### Methods: 

### _class_ Display(options: Optional[list] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; options_provider _: [OptionsProvider](evidently.options.md#evidently.options.OptionsProvider)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; json()

##### &nbsp;&nbsp;&nbsp;&nbsp; save_html(filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE)

##### &nbsp;&nbsp;&nbsp;&nbsp; save_json(filename)

##### &nbsp;&nbsp;&nbsp;&nbsp; show(mode='auto')

### _exception_ ExecutionError()
Bases: `Exception`


### _class_ State(name: str)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#### Methods: 

### _class_ States()
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; Calculated _ = State(name='Calculated')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Init _ = State(name='Init')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Tested _ = State(name='Tested')_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; Verified _ = State(name='Verified')_ 

#### Methods: 

### _class_ Suite()
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

### _class_ ExecutionGraph()
Bases: `object`

#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_metric_execution_iterator()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_test_execution_iterator()

### _class_ SimpleExecutionGraph(metrics: List[[Metric](evidently.metrics.md#evidently.metrics.base_metric.Metric)], tests: List[[Test](evidently.tests.md#evidently.tests.base_test.Test)])
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
