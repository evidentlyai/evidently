# evidently.tests package

## Submodules


### _class_ BaseCheckValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

### _class_ BaseConditionsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `Test`, `ABC`

Base class for all tests with a condition


#### condition(_: TestValueConditio_ )

### _class_ GroupData(id: str, title: str, description: str, sort_index: int = 0, severity: Optional[str] = None)
Bases: `object`


#### description(_: st_ )

#### id(_: st_ )

#### severity(_: Optional[str_ _ = Non_ )

#### sort_index(_: in_ _ = _ )

#### title(_: st_ )

### _class_ GroupTypeData(id: str, title: str, values: List[evidently.tests.base_test.GroupData] = <factory>)
Bases: `object`


#### add_value(data: GroupData)

#### id(_: st_ )

#### title(_: st_ )

#### values(_: List[GroupData_ )

### _class_ GroupingTypes()
Bases: `object`


#### ByClass(_ = GroupTypeData(id='by_class', title='By class', values=[]_ )

#### ByFeature(_ = GroupTypeData(id='by_feature', title='By feature', values=[GroupData(id='no group', title='Dataset-level tests', description='Some tests cannot be grouped by feature', sort_index=0, severity=None)]_ )

#### TestGroup(_ = GroupTypeData(id='test_group', title='By test group', values=[GroupData(id='no group', title='Ungrouped', description='Some tests don’t belong to any group under the selected condition', sort_index=0, severity=None), GroupData(id='classification', title='Classification', description='', sort_index=0, severity=None), GroupData(id='data_drift', title='Data Drift', description='', sort_index=0, severity=None), GroupData(id='data_integrity', title='Data Integrity', description='', sort_index=0, severity=None), GroupData(id='data_quality', title='Data Quality', description='', sort_index=0, severity=None), GroupData(id='regression', title='Regression', description='', sort_index=0, severity=None)]_ )

#### TestType(_ = GroupTypeData(id='test_type', title='By test type', values=[]_ )

### _class_ Test()
Bases: `object`

all fields in test class with type that is subclass of Metric would be used as dependencies of test.


#### _abstract_ check()

#### context(_ = Non_ )

#### get_result()

#### group(_: st_ )

#### name(_: st_ )

#### set_context(context)

### _class_ TestResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>)
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

### _class_ TestValueCondition(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

### generate_column_tests(test_class: Type[Test], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Function for generating tests for columns


### _class_ ByClassClassificationTest(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### by_class_metric(_: [ClassificationQualityByClass](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass_ )

#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_condition()

#### _abstract_ get_value(result: dict)

#### group(_: st_ _ = 'classification_ )

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

### _class_ SimpleClassificationTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_condition()

#### _abstract_ get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### group(_: st_ _ = 'classification_ )

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ )

### _class_ SimpleClassificationTestTopK(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`, `ABC`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_condition()

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

### _class_ TestAccuracyScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'Accuracy Score_ )

#### value(_: Union[float, int_ )

### _class_ TestAccuracyScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestAccuracyScore)

#### render_json(obj: TestAccuracyScore)

### _class_ TestF1ByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: dict)

#### name(_: st_ _ = 'F1 Score by Class_ )

### _class_ TestF1ByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1ByClass)

#### render_json(obj: TestF1ByClass)

### _class_ TestF1Score(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'F1 Score_ )

#### value(_: Union[float, int_ )

### _class_ TestF1ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestF1Score)

### _class_ TestFNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'False Negative Rate_ )

#### value(_: Union[float, int_ )

### _class_ TestFNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestFNR)

### _class_ TestFPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'False Positive Rate_ )

#### value(_: Union[float, int_ )

### _class_ TestFPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestFPR)

### _class_ TestLogLoss(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'Logarithmic Loss_ )

#### value(_: Union[float, int_ )

### _class_ TestLogLossRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestLogLoss)

#### render_json(obj: TestLogLoss)

### _class_ TestPrecisionByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: dict)

#### name(_: st_ _ = 'Precision Score by Class_ )

### _class_ TestPrecisionByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestPrecisionByClass)

#### render_json(obj: TestPrecisionByClass)

### _class_ TestPrecisionScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'Precision Score_ )

#### value(_: Union[float, int_ )

### _class_ TestPrecisionScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestPrecisionScore)

#### render_json(obj: TestPrecisionScore)

### _class_ TestRecallByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: dict)

#### name(_: st_ _ = 'Recall Score by Class_ )

### _class_ TestRecallByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestRecallByClass)

#### render_json(obj: TestRecallByClass)

### _class_ TestRecallScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'Recall Score_ )

#### value(_: Union[float, int_ )

### _class_ TestRecallScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestRecallScore)

#### render_json(obj: TestRecallScore)

### _class_ TestRocAuc(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### name(_: st_ _ = 'ROC AUC Score_ )

#### roc_curve(_: [ClassificationRocCurve](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve_ )

### _class_ TestRocAucRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestRocAuc)

#### render_json(obj: TestRocAuc)

### _class_ TestTNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'True Negative Rate_ )

#### value(_: Union[float, int_ )

### _class_ TestTNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestTNR)

### _class_ TestTPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### condition(_: TestValueConditio_ )

#### conf_matrix(_: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix_ )

#### dummy_metric(_: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric_ )

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

#### metric(_: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric_ )

#### name(_: st_ _ = 'True Positive Rate_ )

#### value(_: Union[float, int_ )

### _class_ TestTPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestF1Score)

#### render_json(obj: TestTPR)

### _class_ BaseDataDriftMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### check()

#### group(_: st_ _ = 'data_drift_ )

#### metric(_: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

### _class_ TestAllFeaturesValueDrift()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for numeric and category features


#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestColumnValueDrift(column_name: str, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `Test`


#### check()

#### column_name(_: st_ )

#### group(_: st_ _ = 'data_drift_ )

#### metric(_: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

#### name(_: st_ _ = 'Drift per Column_ )

### _class_ TestColumnValueDriftRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueDrift)

#### render_json(obj: TestColumnValueDrift)

### _class_ TestCustomFeaturesValueDrift(features: List[str])
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for specified features


#### features(_: List[str_ )

#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestDataDriftResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, features: Dict[str, Tuple[str, float, float]] = <factory>)
Bases: `TestResult`


#### features(_: Dict[str, Tuple[str, float, float]_ )

### _class_ TestNumberOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
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


#### metric(_: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

#### name(_: st_ _ = 'Number of Drifted Features_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfDriftedColumns)

#### render_json(obj: TestNumberOfDriftedColumns)

### _class_ TestShareOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
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


#### metric(_: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable_ )

#### name(_: st_ _ = 'Share of Drifted Columns_ )

#### value(_: Union[float, int_ )

### _class_ TestShareOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestShareOfDriftedColumns)

#### render_json(obj: TestShareOfDriftedColumns)

### _class_ BaseIntegrityByColumnsConditionTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column_name(_: st_ )

#### data_integrity_metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### group(_: st_ _ = 'data_integrity_ )

#### groups()

### _class_ BaseIntegrityColumnMissingValuesTest(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column_name(_: st_ )

#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

### _class_ BaseIntegrityMissingValuesValuesTest(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

### _class_ BaseIntegrityOneColumnTest(column_name: str)
Bases: `Test`, `ABC`


#### column_name(_: st_ )

#### group(_: st_ _ = 'data_integrity_ )

#### groups()

#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

### _class_ BaseIntegrityValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

### _class_ BaseTestMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

Common class for tests of missing values.
Some tests have the same details visualizations.


#### MISSING_VALUES_NAMING_MAPPING(_ = {None: 'Pandas nulls (None, NAN, etc.)', '': '"" (empty string)', inf: 'Numpy "inf" value', -inf: 'Numpy "-inf" value'_ )

#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### get_table_with_missing_values_and_percents_by_column(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), metric_result: [DatasetMissingValuesMetricResult](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult), name: str)
Get a table with missing values number and percents


#### get_table_with_number_of_missing_values_by_one_missing_value(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), current_missing_values: dict, reference_missing_values: Optional[dict], name: str)

### _class_ TestAllColumnsShareOfMissingValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)


#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestColumnAllConstantValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only one unique value in a column


#### check()

#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'All Constant Values in a Column_ )

### _class_ TestColumnAllConstantValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnAllConstantValues)

### _class_ TestColumnAllUniqueValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only uniques values in a column


#### check()

#### column_name(_: st_ )

#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'All Unique Values in a Column_ )

### _class_ TestColumnAllUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnAllUniqueValues)

### _class_ TestColumnNumberOfDifferentMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'Different Types of Missing Values in a Column_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset


#### render_json(obj: TestColumnNumberOfDifferentMissingValues)

### _class_ TestColumnNumberOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number of Missing Values in a Column_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestColumnNumberOfMissingValues)

### _class_ TestColumnShareOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Share of Missing Values in a Column_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestColumnShareOfMissingValues)

### _class_ TestColumnValueRegExp(column_name: str, reg_exp: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [ColumnRegExpMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric_ )

#### name(_: st_ _ = 'RegExp Match_ )

### _class_ TestColumnValueRegExpRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueRegExp)

### _class_ TestColumnsType(columns_type: Optional[dict] = None)
Bases: `Test`

This test compares columns type against the specified ones or a reference dataframe


#### _class_ Result(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, columns_types: Dict[str, Tuple[str, str]] = <factory>)
Bases: `TestResult`


#### columns_types(_: Dict[str, Tuple[str, str]_ )

#### check()

#### columns_type(_: Optional[dict_ )

#### group(_: st_ _ = 'data_integrity_ )

#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Column Types_ )

### _class_ TestColumnsTypeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnsType)

#### render_json(obj: TestColumnsType)

### _class_ TestNumberOfColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Columns_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfColumns)

#### render_json(obj: TestNumberOfColumns)

### _class_ TestNumberOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number of Columns With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestNumberOfColumnsWithMissingValues)

### _class_ TestNumberOfConstantColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Constant Columns_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfConstantColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfConstantColumns)

#### render_json(obj: TestNumberOfConstantColumns)

### _class_ TestNumberOfDifferentMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'Different Types of Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset


#### render_json(obj: TestNumberOfDifferentMissingValues)

### _class_ TestNumberOfDuplicatedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Duplicate Columns_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfDuplicatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfDuplicatedColumns)

### _class_ TestNumberOfDuplicatedRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Duplicate Rows_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfDuplicatedRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfDuplicatedRows)

### _class_ TestNumberOfEmptyColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Empty Columns_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfEmptyColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfEmptyColumns)

### _class_ TestNumberOfEmptyRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Empty Rows_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number of Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestNumberOfMissingValues)

### _class_ TestNumberOfRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric_ )

#### name(_: st_ _ = 'Number of Rows_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfRows)

### _class_ TestNumberOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Number Of Rows With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestNumberOfRowsWithMissingValues)

### _class_ TestShareOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Share of Columns With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestShareOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestShareOfColumnsWithMissingValues)

### _class_ TestShareOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'Share of Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfMissingValues)

#### render_json(obj: TestShareOfMissingValues)

### _class_ TestShareOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric_ )

#### name(_: st_ _ = 'The Share of Rows With Missing Values_ )

#### value(_: Union[float, int_ )

### _class_ TestShareOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_json(obj: TestShareOfRowsWithMissingValues)

### _class_ BaseDataQualityCorrelationsMetricsValueTest(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_quality_ )

#### method(_: st_ )

#### metric(_: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

### _class_ BaseDataQualityMetricsValueTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

### _class_ BaseDataQualityValueListMetricsTest(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column_name(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### groups()

#### metric(_: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### values(_: Optional[list_ )

### _class_ BaseDataQualityValueRangeMetricsTest(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### column(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### groups()

#### left(_: Optional[float_ )

#### metric(_: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### right(_: Optional[float_ )

### _class_ BaseFeatureDataQualityMetricsTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityMetricsValueTest`, `ABC`


#### check()

#### column_name(_: st_ )

#### groups()

### _class_ TestAllColumnsMostCommonValueShare()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates most common value share tests for each column in the dataset


#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestCatColumnsOutOfListValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create share of out of list values tests for category columns


#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestColumnValueMax(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Max Value_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnValueMaxRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMax)

### _class_ TestColumnValueMean(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Mean Value_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnValueMeanRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMean)

### _class_ TestColumnValueMedian(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Median Value_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnValueMedianRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMedian)

### _class_ TestColumnValueMin(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Min Value_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnValueMinRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueMin)

### _class_ TestColumnValueStd(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Standard Deviation (SD)_ )

#### value(_: Union[float, int_ )

### _class_ TestColumnValueStdRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestColumnValueStd)

### _class_ TestConflictPrediction()
Bases: `Test`


#### check()

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [DataQualityStabilityMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric_ )

#### name(_: st_ _ = 'Test number of conflicts in prediction_ )

### _class_ TestConflictTarget()
Bases: `Test`


#### check()

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [DataQualityStabilityMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric_ )

#### name(_: st_ _ = 'Test number of conflicts in target_ )

### _class_ TestCorrelationChanges(corr_diff: float = 0.25, method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Change in Correlation_ )

### _class_ TestCorrelationChangesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestCorrelationChanges)

### _class_ TestHighlyCorrelatedColumns(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Highly Correlated Columns_ )

#### value(_: Union[float, int_ )

### _class_ TestHighlyCorrelatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestHighlyCorrelatedColumns)

#### render_json(obj: TestHighlyCorrelatedColumns)

### _class_ TestMeanInNSigmas(column_name: str, n_sigmas: int = 2)
Bases: `Test`


#### check()

#### column_name(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### n_sigmas(_: in_ )

#### name(_: st_ _ = 'Mean Value Stability_ )

### _class_ TestMeanInNSigmasRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestMeanInNSigmas)

#### render_json(obj: TestMeanInNSigmas)

### _class_ TestMostCommonValueShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Share of the Most Common Value_ )

#### value(_: Union[float, int_ )

### _class_ TestMostCommonValueShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestMostCommonValueShare)

#### render_json(obj: TestMostCommonValueShare)

### _class_ TestNumColumnsMeanInNSigmas()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create tests of mean for all numeric columns


#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestNumColumnsOutOfRangeValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates share of out of range values tests for all numeric columns


#### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class_ TestNumberOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### name(_: st_ _ = 'Number Out-of-List Values_ )

#### value(_: Union[float, int_ )

#### values(_: Optional[list_ )

### _class_ TestNumberOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfOutListValues)

### _class_ TestNumberOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### name(_: st_ _ = 'Number of Out-of-Range Values _ )

#### right(_: Optional[float_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfOutRangeValues)

### _class_ TestNumberOfUniqueValues(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Number of Unique Values_ )

#### value(_: Union[float, int_ )

### _class_ TestNumberOfUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestNumberOfUniqueValues)

### _class_ TestPredictionFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Correlation between Prediction and Features_ )

#### value(_: Union[float, int_ )

### _class_ TestPredictionFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestTargetFeaturesCorrelations)

#### render_json(obj: TestPredictionFeaturesCorrelations)

### _class_ TestShareOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### name(_: st_ _ = 'Share of Out-of-List Values_ )

#### value(_: Union[float, int_ )

#### values(_: Optional[list_ )

### _class_ TestShareOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestShareOfOutListValues)

#### render_json(obj: TestShareOfOutListValues)

### _class_ TestShareOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### name(_: st_ _ = 'Share of Out-of-Range Values_ )

#### right(_: Optional[float_ )

#### value(_: Union[float, int_ )

### _class_ TestShareOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestShareOfOutRangeValues)

#### render_json(obj: TestShareOfOutRangeValues)

### _class_ TestTargetFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Correlation between Target and Features_ )

#### value(_: Union[float, int_ )

### _class_ TestTargetFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestTargetFeaturesCorrelations)

#### render_json(obj: TestTargetFeaturesCorrelations)

### _class_ TestTargetPredictionCorrelation(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric_ )

#### name(_: st_ _ = 'Correlation between Target and Prediction_ )

#### value(_: Union[float, int_ )

### _class_ TestUniqueValuesShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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


#### metric(_: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric_ )

#### name(_: st_ _ = 'Share of Unique Values_ )

#### value(_: Union[float, int_ )

### _class_ TestUniqueValuesShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestUniqueValuesShare)

### _class_ TestValueList(column_name: str, values: Optional[list] = None)
Bases: `Test`


#### check()

#### column_name(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### metric(_: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric_ )

#### name(_: st_ _ = 'Out-of-List Values_ )

#### values(_: Optional[list_ )

### _class_ TestValueListRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueList)

#### render_json(obj: TestValueList)

### _class_ TestValueQuantile(column_name: str, quantile: float, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
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

#### metric(_: [ColumnQuantileMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric_ )

#### name(_: st_ _ = 'Quantile Value_ )

#### quantile(_: floa_ )

### _class_ TestValueQuantileRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueQuantile)

### _class_ TestValueRange(column_name: str, left: Optional[float] = None, right: Optional[float] = None)
Bases: `Test`


#### check()

#### column(_: st_ )

#### group(_: st_ _ = 'data_quality_ )

#### left(_: Optional[float_ )

#### metric(_: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric_ )

#### name(_: st_ _ = 'Value Range_ )

#### right(_: Optional[float_ )

### _class_ TestValueRangeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueRange)

### _class_ BaseRegressionPerformanceMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### group(_: st_ _ = 'regression_ )

#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

### _class_ TestValueAbsMaxError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Max Absolute Error_ )

#### value(_: Union[float, int_ )

### _class_ TestValueAbsMaxErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueAbsMaxError)

#### render_json(obj: TestValueAbsMaxError)

### _class_ TestValueMAE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Mean Absolute Error (MAE)_ )

#### value(_: Union[float, int_ )

### _class_ TestValueMAERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueMAE)

#### render_json(obj: TestValueMAE)

### _class_ TestValueMAPE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Mean Absolute Percentage Error (MAPE)_ )

#### value(_: Union[float, int_ )

### _class_ TestValueMAPERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueMAPE)

#### render_json(obj: TestValueMAPE)

### _class_ TestValueMeanError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Mean Error (ME)_ )

#### value(_: Union[float, int_ )

### _class_ TestValueMeanErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueMeanError)

#### render_json(obj: TestValueMeanError)

### _class_ TestValueR2Score(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'R2 Score_ )

#### value(_: Union[float, int_ )

### _class_ TestValueR2ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueR2Score)

#### render_json(obj: TestValueAbsMaxError)

### _class_ TestValueRMSE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### calculate_value_for_test()
Method for getting the checking value.

Define it in a child class


#### condition(_: TestValueConditio_ )

#### dummy_metric(_: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric_ )

#### get_condition()

#### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.

Define it in a child class


#### metric(_: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric_ )

#### name(_: st_ _ = 'Root Mean Square Error (RMSE)_ )

#### value(_: Union[float, int_ )

### _class_ TestValueRMSERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### color_options(_: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions_ )

#### render_html(obj: TestValueRMSE)

#### render_json(obj: TestValueRMSE)

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
## Module contents
