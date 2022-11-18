# evidently.tests package

## Submodules

## evidently.tests.base_test module


### _class_ evidently.tests.base_test.BaseCheckValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseConditionsTest`

Base class for all tests with checking a value condition


#### _abstract_ calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### check()

#### get_condition()

#### _abstract_ get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### groups()

#### value(_: Union[float, int_ )

### _class_ evidently.tests.base_test.BaseConditionsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `Test`, `ABC`

Base class for all tests with a condition


#### condition(_: TestValueConditio_ )

### _class_ evidently.tests.base_test.GroupData(id: str, title: str, description: str, sort_index: int = 0, severity: Optional[str] = None)
Bases: `object`


#### description(_: st_ )

#### id(_: st_ )

#### severity(_: Optional[str_ _ = Non_ )

#### sort_index(_: in_ _ = _ )

#### title(_: st_ )

### _class_ evidently.tests.base_test.GroupTypeData(id: str, title: str, values: List[evidently.tests.base_test.GroupData] = <factory>)
Bases: `object`


#### add_value(data: GroupData)

#### id(_: st_ )

#### title(_: st_ )

#### values(_: List[GroupData_ )

### _class_ evidently.tests.base_test.GroupingTypes()
Bases: `object`


#### ByClass(_ = GroupTypeData(id='by_class', title='By class', values=[]_ )

#### ByFeature(_ = GroupTypeData(id='by_feature', title='By feature', values=[GroupData(id='no group', title='Dataset-level tests', description='Some tests cannot be grouped by feature', sort_index=0, severity=None)]_ )

#### TestGroup(_ = GroupTypeData(id='test_group', title='By test group', values=[GroupData(id='no group', title='Ungrouped', description='Some tests don’t belong to any group under the selected condition', sort_index=0, severity=None), GroupData(id='classification', title='Classification', description='', sort_index=0, severity=None), GroupData(id='data_drift', title='Data Drift', description='', sort_index=0, severity=None), GroupData(id='data_integrity', title='Data Integrity', description='', sort_index=0, severity=None), GroupData(id='data_quality', title='Data Quality', description='', sort_index=0, severity=None), GroupData(id='regression', title='Regression', description='', sort_index=0, severity=None)]_ )

#### TestType(_ = GroupTypeData(id='test_type', title='By test type', values=[]_ )

### _class_ evidently.tests.base_test.Test()
Bases: `object`

all fields in test class with type that is subclass of Metric would be used as dependencies of test.


#### _abstract_ check()

#### context(_ = Non_ )

#### get_result()

#### group(_: st_ )

#### name(_: st_ )

#### set_context(context)

### _class_ evidently.tests.base_test.TestResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>)
Bases: `object`


#### ERROR(_ = 'ERROR_ )

#### FAIL(_ = 'FAIL_ )

#### SKIPPED(_ = 'SKIPPED_ )

#### SUCCESS(_ = 'SUCCESS_ )

#### WARNING(_ = 'WARNING_ )

#### description(_: st_ )

#### groups(_: Dict[str, str_ )

#### is_passed()

#### mark_as_error(description: Optional[str] = None)

#### mark_as_fail(description: Optional[str] = None)

#### mark_as_success(description: Optional[str] = None)

#### mark_as_warning(description: Optional[str] = None)

#### name(_: st_ )

#### set_status(status: str, description: Optional[str] = None)

#### status(_: st_ )

### _class_ evidently.tests.base_test.TestValueCondition(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `object`

Class for processing a value conditions - should it be less, greater than, equals and so on.

An object of the class stores specified conditions and can be used for checking a value by them.


#### as_dict()

#### check_value(value: Union[float, int])

#### eq(_: Optional[Union[float, int]_ _ = Non_ )

#### gt(_: Optional[Union[float, int]_ _ = Non_ )

#### gte(_: Optional[Union[float, int]_ _ = Non_ )

#### has_condition()
Checks if we have a condition in the object and returns True in this case.

If we have no conditions - returns False.


#### is_in(_: Optional[List[Union[float, int, str, bool]]_ _ = Non_ )

#### lt(_: Optional[Union[float, int]_ _ = Non_ )

#### lte(_: Optional[Union[float, int]_ _ = Non_ )

#### not_eq(_: Optional[Union[float, int]_ _ = Non_ )

#### not_in(_: Optional[List[Union[float, int, str, bool]]_ _ = Non_ )

### evidently.tests.base_test.generate_column_tests(test_class: Type[Test], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Function for generating tests for columns

## evidently.tests.classification_performance_tests module


### _class_ evidently.tests.classification_performance_tests.ByClassClassificationTest(label: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`, `ABC`


#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ )

### _class_ evidently.tests.classification_performance_tests.SimpleClassificationTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### get_condition()

#### _abstract_ get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### group(_: st_ _ = 'classification_ )

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ )

### _class_ evidently.tests.classification_performance_tests.SimpleClassificationTestTopK(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`, `ABC`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestAccuracyScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'Accuracy Score_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestAccuracyScoreRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestAccuracyScore)

#### render_json(obj: TestAccuracyScore)

### _class_ evidently.tests.classification_performance_tests.TestF1ByClass(label: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### name(_: st_ _ = 'F1 Score by Class_ )

### _class_ evidently.tests.classification_performance_tests.TestF1ByClassRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1ByClass)

#### render_json(obj: TestF1ByClass)

### _class_ evidently.tests.classification_performance_tests.TestF1Score(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'F1 Score_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestF1ScoreRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestF1Score)

### _class_ evidently.tests.classification_performance_tests.TestFNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'False Negative Rate_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestFNRRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestFNR)

### _class_ evidently.tests.classification_performance_tests.TestFPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'False Positive Rate_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestFPRRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestFPR)

### _class_ evidently.tests.classification_performance_tests.TestLogLoss(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'Logarithmic Loss_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestLogLossRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestLogLoss)

#### render_json(obj: TestLogLoss)

### _class_ evidently.tests.classification_performance_tests.TestPrecisionByClass(label: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### name(_: st_ _ = 'Precision Score by Class_ )

### _class_ evidently.tests.classification_performance_tests.TestPrecisionByClassRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestPrecisionByClass)

#### render_json(obj: TestPrecisionByClass)

### _class_ evidently.tests.classification_performance_tests.TestPrecisionScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'Precision Score_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestPrecisionScoreRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestPrecisionScore)

#### render_json(obj: TestPrecisionScore)

### _class_ evidently.tests.classification_performance_tests.TestRecallByClass(label: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### name(_: st_ _ = 'Recall Score by Class_ )

### _class_ evidently.tests.classification_performance_tests.TestRecallByClassRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestRecallByClass)

#### render_json(obj: TestRecallByClass)

### _class_ evidently.tests.classification_performance_tests.TestRecallScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'Recall Score_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestRecallScoreRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestRecallScore)

#### render_json(obj: TestRecallScore)

### _class_ evidently.tests.classification_performance_tests.TestRocAuc(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'ROC AUC Score_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestRocAucRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestRocAuc)

#### render_json(obj: TestRocAuc)

### _class_ evidently.tests.classification_performance_tests.TestTNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'True Negative Rate_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestTNRRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestTNR)

### _class_ evidently.tests.classification_performance_tests.TestTPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationPerformanceMetrics](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.DatasetClassificationPerformanceMetrics))

#### metric(_: [Metric](./evidently.metrics.md#evidently.metrics.base_metric.Metric)[[ClassificationPerformanceResults](./evidently.metrics.md#evidently.metrics.classification_performance_metrics.ClassificationPerformanceResults)_ )

#### name(_: st_ _ = 'True Positive Rate_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.classification_performance_tests.TestTPRRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestTPR)
## evidently.tests.data_drift_tests module


### _class_ evidently.tests.data_drift_tests.BaseDataDriftMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### check()

#### group(_: st_ _ = 'data_drift_ )

#### metric(_: [DataDriftTable](./evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

### _class_ evidently.tests.data_drift_tests.TestAllFeaturesValueDrift()
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for numeric and category features


#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_drift_tests.TestColumnValueDrift(column_name: str, options: Optional[[DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `Test`


#### check()

#### column_name(_: st_ )

#### group(_: st_ _ = 'data_drift_ )

#### metric(_: [DataDriftTable](./evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

#### name(_: st_ _ = 'Drift per Column_ )

### _class_ evidently.tests.data_drift_tests.TestColumnValueDriftRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueDrift)

#### render_json(obj: TestColumnValueDrift)

### _class_ evidently.tests.data_drift_tests.TestCustomFeaturesValueDrift(features: List[str])
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for specified features


#### features(_: List[str_ )

#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_drift_tests.TestDataDriftResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, features: Dict[str, Tuple[str, float, float]] = <factory>)
Bases: `TestResult`


#### features(_: Dict[str, Tuple[str, float, float]_ )

### _class_ evidently.tests.data_drift_tests.TestNumberOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseDataDriftMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DataDriftTable](./evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

#### name(_: st_ _ = 'Number of Drifted Features_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_drift_tests.TestNumberOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfDriftedColumns)

#### render_json(obj: TestNumberOfDriftedColumns)

### _class_ evidently.tests.data_drift_tests.TestShareOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](./evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseDataDriftMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DataDriftTable](./evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

#### name(_: st_ _ = 'Share of Drifted Columns_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_drift_tests.TestShareOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestShareOfDriftedColumns)

#### render_json(obj: TestShareOfDriftedColumns)
## evidently.tests.data_integrity_tests module


### _class_ evidently.tests.data_integrity_tests.BaseIntegrityByColumnsConditionTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column_name(_: st_ )

#### data_integrity_metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### group(_: st_ _ = 'data_integrity_ )

#### groups()

### _class_ evidently.tests.data_integrity_tests.BaseIntegrityColumnMissingValuesTest(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column_name(_: st_ )

#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

### _class_ evidently.tests.data_integrity_tests.BaseIntegrityMissingValuesValuesTest(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

### _class_ evidently.tests.data_integrity_tests.BaseIntegrityOneColumnTest(column_name: str)
Bases: `Test`, `ABC`


#### column_name(_: st_ )

#### group(_: st_ _ = 'data_integrity_ )

#### groups()

#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

### _class_ evidently.tests.data_integrity_tests.BaseIntegrityValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

### _class_ evidently.tests.data_integrity_tests.BaseTestMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

Common class for tests of missing values.
Some tests have the same details visualizations.


#### MISSING_VALUES_NAMING_MAPPING(_ = {None: 'Pandas nulls (None, NAN, etc.)', '': '"" (empty string)', inf: 'Numpy "inf" value', -inf: 'Numpy "-inf" value'_ )

#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### get_table_with_missing_values_and_percents_by_column(info: [TestHtmlInfo](./evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), metric_result: [DatasetMissingValuesMetricResult](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult), name: str)
Get a table with missing values number and percents


#### get_table_with_number_of_missing_values_by_one_missing_value(info: [TestHtmlInfo](./evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), current_missing_values: dict, reference_missing_values: Optional[dict], name: str)

### _class_ evidently.tests.data_integrity_tests.TestAllColumnsShareOfMissingValues()
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)


#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_integrity_tests.TestColumnAllConstantValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only one unique value in a column


#### check()

#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'All Constant Values in a Column_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnAllConstantValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnAllConstantValues)

### _class_ evidently.tests.data_integrity_tests.TestColumnAllUniqueValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only uniques values in a column


#### check()

#### column_name(_: st_ )

#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'All Unique Values in a Column_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnAllUniqueValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnAllUniqueValues)

### _class_ evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of differently encoded missing values in one column.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'Different Types of Missing Values in a Column_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset


#### render_json(obj: TestColumnNumberOfDifferentMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of missing values in one column.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number of Missing Values in a Column_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestColumnNumberOfMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestColumnShareOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a share of missing values in one column.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Share of Missing Values in a Column_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestColumnShareOfMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestColumnValueRegExp(column_name: str, reg_exp: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### group(_: st_ _ = 'data_integrity_ )

#### groups()

#### metric(_: [ColumnRegExpMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric_ )

#### name(_: st_ _ = 'RegExp Match_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnValueRegExpRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueRegExp)

### _class_ evidently.tests.data_integrity_tests.TestColumnsType(columns_type: Optional[dict] = None)
Bases: `Test`

This test compares columns type against the specified ones or a reference dataframe


#### _class_ Result(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, columns_types: Dict[str, Tuple[str, str]] = <factory>)
Bases: `TestResult`


#### columns_types(_: Dict[str, Tuple[str, str]_ )

#### check()

#### columns_type(_: Optional[dict_ )

#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Column Types_ )

### _class_ evidently.tests.data_integrity_tests.TestColumnsTypeRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnsType)

#### render_json(obj: TestColumnsType)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of all columns in the data, including utility columns (id/index, datetime, target, predictions)


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Columns_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfColumns)

#### render_json(obj: TestNumberOfColumns)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of columns with a missing value.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number of Columns With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestNumberOfColumnsWithMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfConstantColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained only one unique value


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Constant Columns_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfConstantColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfConstantColumns)

#### render_json(obj: TestNumberOfConstantColumns)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of different encoded missing values.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'Different Types of Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset


#### render_json(obj: TestNumberOfDifferentMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many columns have duplicates in the dataset


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Duplicate Columns_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfDuplicatedColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfDuplicatedColumns)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many rows have duplicates in the dataset


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Duplicate Rows_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfDuplicatedRowsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfDuplicatedRows)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfEmptyColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained all NAN values


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Empty Columns_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfEmptyColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfEmptyColumns)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfEmptyRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows contained all NAN values


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Empty Rows_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of missing values.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number of Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestNumberOfMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows in the data


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Rows_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfRowsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfRows)

### _class_ evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of rows with a missing value.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number Of Rows With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestNumberOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfRowsWithMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of columns with a missing value.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Share of Columns With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestShareOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestShareOfColumnsWithMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestShareOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of missing values.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'Share of Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestShareOfMissingValues)

### _class_ evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of rows with a missing value.


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [DatasetMissingValuesMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Share of Rows With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_integrity_tests.TestShareOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestShareOfRowsWithMissingValues)
## evidently.tests.data_quality_tests module


### _class_ evidently.tests.data_quality_tests.BaseDataQualityCorrelationsMetricsValueTest(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_quality_ )

#### method(_: st_ )

#### metric(_: [DatasetCorrelationsMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

### _class_ evidently.tests.data_quality_tests.BaseDataQualityMetricsValueTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

### _class_ evidently.tests.data_quality_tests.BaseDataQualityValueListMetricsTest(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column_name(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### groups()

#### metric(_: [ColumnValueListMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### values(_: Optional[list_ )

### _class_ evidently.tests.data_quality_tests.BaseDataQualityValueRangeMetricsTest(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### groups()

#### left(_: Optional[float_ )

#### metric(_: [ColumnValueRangeMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### right(_: Optional[float_ )

### _class_ evidently.tests.data_quality_tests.BaseFeatureDataQualityMetricsTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityMetricsValueTest`, `ABC`


#### check()

#### column_name(_: st_ )

#### groups()

### _class_ evidently.tests.data_quality_tests.TestAllColumnsMostCommonValueShare()
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates most common value share tests for each column in the dataset


#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_quality_tests.TestCatColumnsOutOfListValues()
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create share of out of list values tests for category columns


#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_quality_tests.TestColumnValueMax(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Max Value_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestColumnValueMaxRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMax)

### _class_ evidently.tests.data_quality_tests.TestColumnValueMean(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Mean Value_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestColumnValueMeanRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMean)

### _class_ evidently.tests.data_quality_tests.TestColumnValueMedian(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Median Value_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestColumnValueMedianRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMedian)

### _class_ evidently.tests.data_quality_tests.TestColumnValueMin(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Min Value_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestColumnValueMinRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMin)

### _class_ evidently.tests.data_quality_tests.TestColumnValueStd(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Standard Deviation (SD)_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestColumnValueStdRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueStd)

### _class_ evidently.tests.data_quality_tests.TestConflictPrediction()
Bases: `Test`


#### check()

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [DataQualityStabilityMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric_ )

#### name(_: st_ _ = 'Test number of conflicts in prediction_ )

### _class_ evidently.tests.data_quality_tests.TestConflictTarget()
Bases: `Test`


#### check()

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [DataQualityStabilityMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric_ )

#### name(_: st_ _ = 'Test number of conflicts in target_ )

### _class_ evidently.tests.data_quality_tests.TestCorrelationChanges(corr_diff: float = 0.25, method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### corr_diff(_: floa_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [DatasetCorrelationsMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Change in Correlation_ )

### _class_ evidently.tests.data_quality_tests.TestCorrelationChangesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestCorrelationChanges)

### _class_ evidently.tests.data_quality_tests.TestHighlyCorrelatedColumns(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### method(_: st_ )

#### metric(_: [DatasetCorrelationsMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Highly Correlated Columns_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestHighlyCorrelatedColumnsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestHighlyCorrelatedColumns)

#### render_json(obj: TestHighlyCorrelatedColumns)

### _class_ evidently.tests.data_quality_tests.TestMeanInNSigmas(column_name: str, n_sigmas: int = 2)
Bases: `Test`


#### check()

#### column_name(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### n_sigmas(_: in_ )

#### name(_: st_ _ = 'Mean Value Stability_ )

### _class_ evidently.tests.data_quality_tests.TestMeanInNSigmasRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestMeanInNSigmas)

#### render_json(obj: TestMeanInNSigmas)

### _class_ evidently.tests.data_quality_tests.TestMostCommonValueShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Share of the Most Common Value_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestMostCommonValueShareRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestMostCommonValueShare)

#### render_json(obj: TestMostCommonValueShare)

### _class_ evidently.tests.data_quality_tests.TestNumColumnsMeanInNSigmas()
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create tests of mean for all numeric columns


#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_quality_tests.TestNumColumnsOutOfRangeValues()
Bases: [`BaseGenerator`](./evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates share of out of range values tests for all numeric columns


#### generate(columns_info: [DatasetColumns](./evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ evidently.tests.data_quality_tests.TestNumberOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnValueListMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### name(_: st_ _ = 'Number Out-of-List Values_ )

#### value(_: Union[float, int_ )

#### values(_: Optional[list_ )

### _class_ evidently.tests.data_quality_tests.TestNumberOfOutListValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfOutListValues)

### _class_ evidently.tests.data_quality_tests.TestNumberOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### left(_: Optional[float_ )

#### metric(_: [ColumnValueRangeMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### name(_: st_ _ = 'Number of Out-of-Range Values _ )

#### right(_: Optional[float_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestNumberOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfOutRangeValues)

### _class_ evidently.tests.data_quality_tests.TestNumberOfUniqueValues(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Number of Unique Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestNumberOfUniqueValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfUniqueValues)

### _class_ evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### method(_: st_ )

#### metric(_: [DatasetCorrelationsMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Correlation between Prediction and Features_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestPredictionFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestTargetFeaturesCorrelations)

#### render_json(obj: TestPredictionFeaturesCorrelations)

### _class_ evidently.tests.data_quality_tests.TestShareOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnValueListMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### name(_: st_ _ = 'Share of Out-of-List Values_ )

#### value(_: Union[float, int_ )

#### values(_: Optional[list_ )

### _class_ evidently.tests.data_quality_tests.TestShareOfOutListValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestShareOfOutListValues)

#### render_json(obj: TestShareOfOutListValues)

### _class_ evidently.tests.data_quality_tests.TestShareOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### left(_: Optional[float_ )

#### metric(_: [ColumnValueRangeMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### name(_: st_ _ = 'Share of Out-of-Range Values_ )

#### right(_: Optional[float_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestShareOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestShareOfOutRangeValues)

#### render_json(obj: TestShareOfOutRangeValues)

### _class_ evidently.tests.data_quality_tests.TestTargetFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### method(_: st_ )

#### metric(_: [DatasetCorrelationsMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Correlation between Target and Features_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestTargetFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestTargetFeaturesCorrelations)

#### render_json(obj: TestTargetFeaturesCorrelations)

### _class_ evidently.tests.data_quality_tests.TestTargetPredictionCorrelation(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### method(_: st_ )

#### metric(_: [DatasetCorrelationsMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Correlation between Target and Prediction_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestUniqueValuesShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [ColumnSummaryMetric](./evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Share of Unique Values_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.data_quality_tests.TestUniqueValuesShareRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestUniqueValuesShare)

### _class_ evidently.tests.data_quality_tests.TestValueList(column_name: str, values: Optional[list] = None)
Bases: `Test`


#### check()

#### column_name(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [ColumnValueListMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### name(_: st_ _ = 'Out-of-List Values_ )

#### values(_: Optional[list_ )

### _class_ evidently.tests.data_quality_tests.TestValueListRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueList)

#### render_json(obj: TestValueList)

### _class_ evidently.tests.data_quality_tests.TestValueQuantile(column_name: str, quantile: float, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### column_name(_: st_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### group(_: st_ _ = 'data_quality_ )

#### groups()

#### metric(_: [ColumnQuantileMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric_ )

#### name(_: st_ _ = 'Quantile Value_ )

#### quantile(_: floa_ )

### _class_ evidently.tests.data_quality_tests.TestValueQuantileRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueQuantile)

### _class_ evidently.tests.data_quality_tests.TestValueRange(column_name: str, left: Optional[float] = None, right: Optional[float] = None)
Bases: `Test`


#### check()

#### column(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### left(_: Optional[float_ )

#### metric(_: [ColumnValueRangeMetric](./evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### name(_: st_ _ = 'Value Range_ )

#### right(_: Optional[float_ )

### _class_ evidently.tests.data_quality_tests.TestValueRangeRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueRange)
## evidently.tests.regression_performance_tests module


### _class_ evidently.tests.regression_performance_tests.BaseRegressionPerformanceMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'regression_ )

#### metric(_: [RegressionQualityMetric](./evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

### _class_ evidently.tests.regression_performance_tests.TestValueAbsMaxError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](./evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Max Absolute Error_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.regression_performance_tests.TestValueAbsMaxErrorRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueAbsMaxError)

#### render_json(obj: TestValueAbsMaxError)

### _class_ evidently.tests.regression_performance_tests.TestValueMAE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](./evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Mean Absolute Error (MAE)_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.regression_performance_tests.TestValueMAERenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueMAE)

#### render_json(obj: TestValueMAE)

### _class_ evidently.tests.regression_performance_tests.TestValueMAPE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](./evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Mean Absolute Percentage Error (MAPE)_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.regression_performance_tests.TestValueMAPERenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueMAPE)

#### render_json(obj: TestValueMAPE)

### _class_ evidently.tests.regression_performance_tests.TestValueMeanError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](./evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Mean Error (ME)_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.regression_performance_tests.TestValueMeanErrorRenderer(color_options: Optional[[ColorOptions](./evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](./evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueMeanError)

#### render_json(obj: TestValueMeanError)

### _class_ evidently.tests.regression_performance_tests.TestValueR2Score(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'R2 Score_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.regression_performance_tests.TestValueR2ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueR2Score)

#### render_json(obj: TestValueAbsMaxError)

### _class_ evidently.tests.regression_performance_tests.TestValueRMSE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Root Mean Square Error (RMSE)_ )

#### value(_: Union[float, int_ )

### _class_ evidently.tests.regression_performance_tests.TestValueRMSERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueRMSE)

#### render_json(obj: TestValueRMSE)
## evidently.tests.utils module


### evidently.tests.utils.approx(value, relative=None, absolute=None)
Get approximate value for checking a value is equal to other within some tolerance


### evidently.tests.utils.dataframes_to_table(current: DataFrame, reference: Optional[DataFrame], columns: List[str], table_id: str, sort_by: str = 'curr', na_position: str = 'first', asc: bool = False)

### evidently.tests.utils.plot_boxes(\*, curr_for_plots: dict, ref_for_plots: Optional[dict], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.tests.utils.plot_check(fig, condition, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.tests.utils.plot_conf_mtrx(curr_mtrx, ref_mtrx)

### evidently.tests.utils.plot_correlations(current_correlations, reference_correlations)

### evidently.tests.utils.plot_dicts_to_table(dict_curr: dict, dict_ref: Optional[dict], columns: list, id_prfx: str, sort_by: str = 'curr', asc: bool = False)

### evidently.tests.utils.plot_metric_value(fig, metric_val: float, metric_name: str)

### evidently.tests.utils.plot_rates(\*, curr_rate_plots_data: dict, ref_rate_plots_data: Optional[dict] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.tests.utils.plot_roc_auc(\*, curr_roc_curve: dict, ref_roc_curve: Optional[dict], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### evidently.tests.utils.plot_value_counts_tables(feature_name, values, curr_df, ref_df, id_prfx)

### evidently.tests.utils.plot_value_counts_tables_ref_curr(feature_name, curr_df, ref_df, id_prfx)

### evidently.tests.utils.regression_perf_plot(\*, val_for_plot: Dict[str, Series], hist_for_plot: Dict[str, Series], name: str, curr_metric: float, ref_metric: Optional[float] = None, is_ref_data: bool = False, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
## Module contents
