# evidently.tests package

Available tests for TestSuite reports.
Tests grouped into modules.
For detailed information see module documentation.

## Submodules

## <a name="module-evidently.tests.base_test"></a>base_test module


### class BaseCheckValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseConditionsTest`

Base class for all tests with checking a value condition

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class BaseConditionsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `Test`, `ABC`

Base class for all tests with a condition

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

### class GroupData(id: str, title: str, description: str, sort_index: int = 0, severity: Optional[str] = None)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; description : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; id : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; severity : Optional[str]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; sort_index : int  = 0 

##### &nbsp;&nbsp;&nbsp;&nbsp; title : str 

### class GroupTypeData(id: str, title: str, values: List[evidently.tests.base_test.GroupData] = <factory>)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; id : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; title : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : List[GroupData] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; add_value(data: GroupData)

### class GroupingTypes()
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; ByClass  = GroupTypeData(id='by_class', title='By class', values=[]) 

##### &nbsp;&nbsp;&nbsp;&nbsp; ByFeature  = GroupTypeData(id='by_feature', title='By feature', values=[GroupData(id='no group', title='Dataset-level tests', description='Some tests cannot be grouped by feature', sort_index=0, severity=None)]) 

##### &nbsp;&nbsp;&nbsp;&nbsp; TestGroup  = GroupTypeData(id='test_group', title='By test group', values=[GroupData(id='no group', title='Ungrouped', description='Some tests don’t belong to any group under the selected condition', sort_index=0, severity=None), GroupData(id='classification', title='Classification', description='', sort_index=0, severity=None), GroupData(id='data_drift', title='Data Drift', description='', sort_index=0, severity=None), GroupData(id='data_integrity', title='Data Integrity', description='', sort_index=0, severity=None), GroupData(id='data_quality', title='Data Quality', description='', sort_index=0, severity=None), GroupData(id='regression', title='Regression', description='', sort_index=0, severity=None)]) 

##### &nbsp;&nbsp;&nbsp;&nbsp; TestType  = GroupTypeData(id='test_type', title='By test type', values=[]) 

### class Test()
Bases: `object`

all fields in test class with type that is subclass of Metric would be used as dependencies of test.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; context  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  check()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_result()

##### &nbsp;&nbsp;&nbsp;&nbsp; set_context(context)

### class TestResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; ERROR  = 'ERROR' 

##### &nbsp;&nbsp;&nbsp;&nbsp; FAIL  = 'FAIL' 

##### &nbsp;&nbsp;&nbsp;&nbsp; SKIPPED  = 'SKIPPED' 

##### &nbsp;&nbsp;&nbsp;&nbsp; SUCCESS  = 'SUCCESS' 

##### &nbsp;&nbsp;&nbsp;&nbsp; WARNING  = 'WARNING' 

##### &nbsp;&nbsp;&nbsp;&nbsp; description : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups : Dict[str, str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; status : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; is_passed()

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_error(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_fail(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_success(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_warning(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; set_status(status: str, description: Optional[str] = None)

### class TestValueCondition(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `object`

Class for processing a value conditions - should it be less, greater than, equals and so on.

An object of the class stores specified conditions and can be used for checking a value by them.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; eq : Optional[Union[float, int]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; gt : Optional[Union[float, int]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; gte : Optional[Union[float, int]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; is_in : Optional[List[Union[float, int, str, bool]]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; lt : Optional[Union[float, int]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; lte : Optional[Union[float, int]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; not_eq : Optional[Union[float, int]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; not_in : Optional[List[Union[float, int, str, bool]]]  = None 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; check_value(value: Union[float, int])

##### &nbsp;&nbsp;&nbsp;&nbsp; has_condition()
Checks if we have a condition in the object and returns True in this case.
If we have no conditions - returns False.

### generate_column_tests(test_class: Type[Test], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Function for generating tests for columns

## <a name="module-evidently.tests.classification_performance_tests"></a>classification_performance_tests module


### class ByClassClassificationTest(label: str, probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; by_class_metric : [ClassificationQualityByClass](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass) 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'classification' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  get_value(result: dict)

### class SimpleClassificationTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'classification' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; abstract  get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class SimpleClassificationTestTopK(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

### class TestAccuracyScore(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Accuracy Score' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestAccuracyScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestAccuracyScore)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestAccuracyScore)

### class TestF1ByClass(label: str, probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'F1 Score by Class' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: dict)

### class TestF1ByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1ByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestF1ByClass)

### class TestF1Score(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'F1 Score' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestF1ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestF1Score)

### class TestFNR(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'False Negative Rate' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestFNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestFNR)

### class TestFPR(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'False Positive Rate' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestFPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestFPR)

### class TestLogLoss(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Logarithmic Loss' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestLogLossRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestLogLoss)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestLogLoss)

### class TestPrecisionByClass(label: str, probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Precision Score by Class' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: dict)

### class TestPrecisionByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestPrecisionByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestPrecisionByClass)

### class TestPrecisionScore(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Precision Score' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestPrecisionScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestPrecisionScore)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestPrecisionScore)

### class TestRecallByClass(label: str, probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Recall Score by Class' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: dict)

### class TestRecallByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestRecallByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestRecallByClass)

### class TestRecallScore(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Recall Score' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestRecallScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestRecallScore)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestRecallScore)

### class TestRocAuc(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'ROC AUC Score' 

##### &nbsp;&nbsp;&nbsp;&nbsp; roc_curve : [ClassificationRocCurve](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestRocAucRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestRocAuc)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestRocAuc)

### class TestTNR(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'True Negative Rate' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestTNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestTNR)

### class TestTPR(probas_threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix : [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix) 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; k : Optional[Union[float, int]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'True Positive Rate' 

##### &nbsp;&nbsp;&nbsp;&nbsp; probas_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### class TestTPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestTPR)
## <a name="module-evidently.tests.data_drift_tests"></a>data_drift_tests module


### class BaseDataDriftMetricsTest(columns: Optional[List[str]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_drift' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestAllFeaturesValueDrift(columns: Optional[List[str]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for numeric and category features

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestColumnDrift(column_name: str, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, stattest_threshold: Optional[float] = None)
Bases: `Test`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_drift' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnDriftMetric](evidently.metrics.data_drift.md#evidently.metrics.data_drift.column_drift_metric.ColumnDriftMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Drift per Column' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestColumnDriftRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnDrift)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnDrift)

### class TestCustomFeaturesValueDrift(features: List[str], stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for specified features

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; cat_stattest_threshold : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; features : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; num_stattest_threshold : Optional[float]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest : Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; per_column_stattest_threshold : Optional[Dict[str, float]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest : Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]  = None 

##### &nbsp;&nbsp;&nbsp;&nbsp; stattest_threshold : Optional[float]  = None 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestDataDriftResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, features: Dict[str, Tuple[str, float, float]] = <factory>)
Bases: `TestResult`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; features : Dict[str, Tuple[str, float, float]] 

### class TestNumberOfDriftedColumns(columns: Optional[List[str]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `BaseDataDriftMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Drifted Features' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfDriftedColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDriftedColumns)

### class TestShareOfDriftedColumns(columns: Optional[List[str]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_column_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, stattest_threshold: Optional[float] = None, cat_stattest_threshold: Optional[float] = None, num_stattest_threshold: Optional[float] = None, per_column_stattest_threshold: Optional[Dict[str, float]] = None)
Bases: `BaseDataDriftMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Share of Drifted Columns' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestShareOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestShareOfDriftedColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfDriftedColumns)
## <a name="module-evidently.tests.data_integrity_tests"></a>data_integrity_tests module


### class BaseIntegrityByColumnsConditionTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_integrity_metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class BaseIntegrityColumnMissingValuesTest(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

### class BaseIntegrityMissingValuesValuesTest(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

### class BaseIntegrityOneColumnTest(column_name: str)
Bases: `Test`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class BaseIntegrityValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

### class BaseTestMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

Common class for tests of missing values.
Some tests have the same details visualizations.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; MISSING_VALUES_NAMING_MAPPING  = {None: 'Pandas nulls (None, NAN, etc.)', '': '"" (empty string)', inf: 'Numpy "inf" value', -inf: 'Numpy "-inf" value'} 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_table_with_missing_values_and_percents_by_column(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), metric_result: [DatasetMissingValuesMetricResult](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult), name: str)
Get a table with missing values number and percents

##### &nbsp;&nbsp;&nbsp;&nbsp; get_table_with_number_of_missing_values_by_one_missing_value(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), current_missing_values: dict, reference_missing_values: Optional[dict], name: str)

### class TestAllColumnsShareOfMissingValues(columns: Optional[List[str]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestColumnAllConstantValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only one unique value in a column

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'All Constant Values in a Column' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestColumnAllConstantValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnAllConstantValues)

### class TestColumnAllUniqueValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only uniques values in a column

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'All Unique Values in a Column' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestColumnAllUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnAllUniqueValues)

### class TestColumnNumberOfDifferentMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of differently encoded missing values in one column.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Different Types of Missing Values in a Column' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnNumberOfDifferentMissingValues)

### class TestColumnNumberOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of missing values in one column.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Number of Missing Values in a Column' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnNumberOfMissingValues)

### class TestColumnRegExp(column_name: str, reg_exp: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnRegExpMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'RegExp Match' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class TestColumnRegExpRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnRegExp)

### class TestColumnShareOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a share of missing values in one column.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Share of Missing Values in a Column' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnShareOfMissingValues)

### class TestColumnsType(columns_type: Optional[dict] = None)
Bases: `Test`

This test compares columns type against the specified ones or a reference dataframe


##### &nbsp;&nbsp;&nbsp;&nbsp; class Result name: str, description: str, status: str, groups: Dict[str, str] = <factory>, columns_types: Dict[str, Tuple[str, str]] = <factory>
Bases: `TestResult`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns_types : Dict[str, Tuple[str, str]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

##### &nbsp;&nbsp;&nbsp;&nbsp; columns_type : Optional[dict] 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_integrity' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Column Types' 

### class TestColumnsTypeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnsType)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnsType)

### class TestNumberOfColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of all columns in the data, including utility columns (id/index, datetime, target, predictions)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Columns' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfColumns)

### class TestNumberOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of columns with a missing value.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Number of Columns With Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfColumnsWithMissingValues)

### class TestNumberOfConstantColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained only one unique value

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Constant Columns' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfConstantColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfConstantColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfConstantColumns)

### class TestNumberOfDifferentMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of different encoded missing values.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Different Types of Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDifferentMissingValues)

### class TestNumberOfDuplicatedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many columns have duplicates in the dataset

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Duplicate Columns' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfDuplicatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDuplicatedColumns)

### class TestNumberOfDuplicatedRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many rows have duplicates in the dataset

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Duplicate Rows' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfDuplicatedRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDuplicatedRows)

### class TestNumberOfEmptyColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained all NAN values

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Empty Columns' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfEmptyColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfEmptyColumns)

### class TestNumberOfEmptyRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows contained all NAN values

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Empty Rows' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of missing values.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Number of Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfMissingValues)

### class TestNumberOfRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows in the data

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Rows' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfRows)

### class TestNumberOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of rows with a missing value.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Number Of Rows With Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfRowsWithMissingValues)

### class TestShareOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of columns with a missing value.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Share of Columns With Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestShareOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfColumnsWithMissingValues)

### class TestShareOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of missing values.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Share of Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfMissingValues)

### class TestShareOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of rows with a missing value.

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'The Share of Rows With Missing Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestShareOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfRowsWithMissingValues)
## <a name="module-evidently.tests.data_quality_tests"></a>data_quality_tests module


### class BaseDataQualityCorrelationsMetricsValueTest(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; method : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric) 

### class BaseDataQualityMetricsValueTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

### class BaseDataQualityValueListMetricsTest(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : Optional[list] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class BaseDataQualityValueRangeMetricsTest(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; left : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; right : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class BaseFeatureDataQualityMetricsTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityMetricsValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class TestAllColumnsMostCommonValueShare(columns: Optional[List[str]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates most common value share tests for each column in the dataset

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestCatColumnsOutOfListValues(columns: Optional[List[str]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create share of out of list values tests for category columns

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestColumnQuantile(column_name: str, quantile: float, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnQuantileMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Quantile Value' 

##### &nbsp;&nbsp;&nbsp;&nbsp; quantile : float 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### class TestColumnQuantileRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnQuantile)

### class TestColumnValueMax(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Max Value' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnValueMaxRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMax)

### class TestColumnValueMean(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Mean Value' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnValueMeanRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMean)

### class TestColumnValueMedian(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Median Value' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnValueMedianRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMedian)

### class TestColumnValueMin(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Min Value' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnValueMinRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMin)

### class TestColumnValueStd(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Standard Deviation (SD)' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestColumnValueStdRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueStd)

### class TestConflictPrediction()
Bases: `Test`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : ConflictPredictionMetric 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Test number of conflicts in prediction' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestConflictTarget()
Bases: `Test`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : ConflictTargetMetric 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Test number of conflicts in target' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestCorrelationChanges(corr_diff: float = 0.25, method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; corr_diff : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Change in Correlation' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestCorrelationChangesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestCorrelationChanges)

### class TestHighlyCorrelatedColumns(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; method : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Highly Correlated Columns' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestHighlyCorrelatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestHighlyCorrelatedColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestHighlyCorrelatedColumns)

### class TestMeanInNSigmas(column_name: str, n_sigmas: int = 2)
Bases: `Test`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; n_sigmas : int 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Mean Value Stability' 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestMeanInNSigmasRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestMeanInNSigmas)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestMeanInNSigmas)

### class TestMostCommonValueShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Share of the Most Common Value' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestMostCommonValueShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestMostCommonValueShare)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestMostCommonValueShare)

### class TestNumColumnsMeanInNSigmas(columns: Optional[List[str]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create tests of mean for all numeric columns

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestNumColumnsOutOfRangeValues(columns: Optional[List[str]] = None)
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates share of out of range values tests for all numeric columns

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns : Optional[List[str]] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### class TestNumberOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number Out-of-List Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : Optional[list] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfOutListValues)

### class TestNumberOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; left : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Out-of-Range Values ' 

##### &nbsp;&nbsp;&nbsp;&nbsp; right : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfOutRangeValues)

### class TestNumberOfUniqueValues(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Number of Unique Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestNumberOfUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfUniqueValues)

### class TestPredictionFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; method : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Correlation between Prediction and Features' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestPredictionFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestTargetFeaturesCorrelations)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestPredictionFeaturesCorrelations)

### class TestShareOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Share of Out-of-List Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : Optional[list] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestShareOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestShareOfOutListValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfOutListValues)

### class TestShareOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; left : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Share of Out-of-Range Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; right : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestShareOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestShareOfOutRangeValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfOutRangeValues)

### class TestTargetFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; method : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Correlation between Target and Features' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestTargetFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestTargetFeaturesCorrelations)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestTargetFeaturesCorrelations)

### class TestTargetPredictionCorrelation(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; method : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Correlation between Target and Prediction' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestUniqueValuesShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Share of Unique Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestUniqueValuesShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestUniqueValuesShare)

### class TestValueList(column_name: str, values: Optional[list] = None)
Bases: `Test`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Out-of-List Values' 

##### &nbsp;&nbsp;&nbsp;&nbsp; values : Optional[list] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestValueListRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueList)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueList)

### class TestValueRange(column_name: str, left: Optional[float] = None, right: Optional[float] = None)
Bases: `Test`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'data_quality' 

##### &nbsp;&nbsp;&nbsp;&nbsp; left : Optional[float] 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Value Range' 

##### &nbsp;&nbsp;&nbsp;&nbsp; right : Optional[float] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### class TestValueRangeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueRange)
## <a name="module-evidently.tests.regression_performance_tests"></a>regression_performance_tests module


### class BaseRegressionPerformanceMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; group : str  = 'regression' 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

### class TestValueAbsMaxError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Max Absolute Error' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestValueAbsMaxErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueAbsMaxError)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueAbsMaxError)

### class TestValueMAE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Mean Absolute Error (MAE)' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestValueMAERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueMAE)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueMAE)

### class TestValueMAPE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Mean Absolute Percentage Error (MAPE)' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestValueMAPERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueMAPE)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueMAPE)

### class TestValueMeanError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Mean Error (ME)' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestValueMeanErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueMeanError)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueMeanError)

### class TestValueR2Score(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'R2 Score' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestValueR2ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueR2Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueAbsMaxError)

### class TestValueRMSE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition : TestValueCondition 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric : [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric : [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric) 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str  = 'Root Mean Square Error (RMSE)' 

##### &nbsp;&nbsp;&nbsp;&nbsp; value : Union[float, int] 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### class TestValueRMSERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options : [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions) 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueRMSE)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueRMSE)
## <a name="module-evidently.tests.utils"></a>utils module


### approx(value, relative=None, absolute=None)
Get approximate value for checking a value is equal to other within some tolerance


### dataframes_to_table(current: DataFrame, reference: Optional[DataFrame], columns: List[str], table_id: str, sort_by: str = 'curr', na_position: str = 'first', asc: bool = False)

### plot_boxes(\*, curr_for_plots: dict, ref_for_plots: Optional[dict], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_check(fig, condition, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_conf_mtrx(curr_mtrx, ref_mtrx)

### plot_correlations(current_correlations, reference_correlations)

### plot_dicts_to_table(dict_curr: dict, dict_ref: Optional[dict], columns: list, id_prfx: str, sort_by: str = 'curr', asc: bool = False)

### plot_metric_value(fig, metric_val: float, metric_name: str)

### plot_rates(\*, curr_rate_plots_data: dict, ref_rate_plots_data: Optional[dict] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_roc_auc(\*, curr_roc_curve: dict, ref_roc_curve: Optional[dict], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### plot_value_counts_tables(feature_name, values, curr_df, ref_df, id_prfx)

### plot_value_counts_tables_ref_curr(feature_name, curr_df, ref_df, id_prfx)

### regression_perf_plot(\*, val_for_plot: Dict[str, Series], hist_for_plot: Dict[str, Series], name: str, curr_metric: float, ref_metric: Optional[float] = None, is_ref_data: bool = False, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
