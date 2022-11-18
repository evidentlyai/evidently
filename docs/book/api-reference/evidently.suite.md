# evidently.suite package

## Submodules

## evidently.suite.base_suite module


### _class_ evidently.suite.base_suite.Context(execution_graph: Optional[ExecutionGraph], metrics: list, tests: list, metric_results: dict, test_results: dict, state: State, renderers: [RenderersDefinitions](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))
Bases: `object`

Pipeline execution context tracks pipeline execution and lifecycle


#### execution_graph(_: Optional[ExecutionGraph_ )

#### metric_results(_: dic_ )

#### metrics(_: lis_ )

#### renderers(_: [RenderersDefinitions](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions_ )

#### state(_: Stat_ )

#### test_results(_: dic_ )

#### tests(_: lis_ )

### _class_ evidently.suite.base_suite.Display(options: Optional[list] = None)
Bases: `object`


#### _abstract_ as_dict()

#### json()

#### options_provider(_: [OptionsProvider](api-reference/evidently.options.md#evidently.options.OptionsProvider_ )

#### save_html(filename: str, mode: Union[str, SaveMode] = SaveMode.SINGLE_FILE)

#### save_json(filename)

#### show(mode='auto')

### _exception_ evidently.suite.base_suite.ExecutionError()
Bases: `Exception`


### _class_ evidently.suite.base_suite.State(name: str)
Bases: `object`


#### name(_: st_ )

### _class_ evidently.suite.base_suite.States()
Bases: `object`


#### Calculated(_ = State(name='Calculated'_ )

#### Init(_ = State(name='Init'_ )

#### Tested(_ = State(name='Tested'_ )

#### Verified(_ = State(name='Verified'_ )

### _class_ evidently.suite.base_suite.Suite()
Bases: `object`


#### add_metric(metric: [Metric](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric))

#### add_test(test: [Test](api-reference/evidently.tests.md#evidently.tests.base_test.Test))

#### context(_: Contex_ )

#### run_calculate(data: [InputData](api-reference/evidently.metrics.md#evidently.metrics.base_metric.InputData))

#### run_checks()

#### verify()

### evidently.suite.base_suite.find_metric_renderer(obj, renderers: [RenderersDefinitions](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))

### evidently.suite.base_suite.find_test_renderer(obj, renderers: [RenderersDefinitions](api-reference/evidently.renderers.md#evidently.renderers.base_renderer.RenderersDefinitions))
## evidently.suite.execution_graph module


### _class_ evidently.suite.execution_graph.ExecutionGraph()
Bases: `object`


#### _abstract_ get_metric_execution_iterator()

#### _abstract_ get_test_execution_iterator()

### _class_ evidently.suite.execution_graph.SimpleExecutionGraph(metrics: List[[Metric](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)], tests: List[[Test](api-reference/evidently.tests.md#evidently.tests.base_test.Test)])
Bases: `ExecutionGraph`

Simple execution graph without any work with dependencies at all,

    assumes that metrics already in order for execution


#### get_metric_execution_iterator()

#### get_test_execution_iterator()

#### metrics(_: List[[Metric](api-reference/evidently.metrics.md#evidently.metrics.base_metric.Metric)_ )

#### tests(_: List[[Test](api-reference/evidently.tests.md#evidently.tests.base_test.Test)_ )
## Module contents
