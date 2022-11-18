# evidently.tests package

## Submodules


### _class _ BaseCheckValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseConditionsTest`

Base class for all tests with checking a value condition


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

##### value _: Union[float, int]_ 

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

##### generate_tests(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

##### as_dict()

##### run(\*, reference_data: Optional[DataFrame], current_data: DataFrame, column_mapping: Optional[[ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)] = None)

##### _abstract _ calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### check()

##### get_condition()

##### _abstract _ get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### groups()

### _class _ BaseConditionsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `Test`, `ABC`

Base class for all tests with a condition


#### Attributes: 

##### condition _: TestValueCondition_ 

#### Methods: 

### _class _ GroupData(id: str, title: str, description: str, sort_index: int = 0, severity: Optional[str] = None)
Bases: `object`


#### Attributes: 

##### description _: str_ 

##### id _: str_ 

##### severity _: Optional[str]_ _ = None_ 

##### sort_index _: int_ _ = 0_ 

##### title _: str_ 

#### Methods: 

### _class _ GroupTypeData(id: str, title: str, values: List[evidently.tests.base_test.GroupData] = <factory>)
Bases: `object`


#### Attributes: 

##### id _: str_ 

##### title _: str_ 

##### values _: List[GroupData]_ 

#### Methods: 

##### add_value(data: GroupData)

### _class _ GroupingTypes()
Bases: `object`


#### Attributes: 

##### ByClass _ = GroupTypeData(id='by_class', title='By class', values=[])_ 

##### ByFeature _ = GroupTypeData(id='by_feature', title='By feature', values=[GroupData(id='no group', title='Dataset-level tests', description='Some tests cannot be grouped by feature', sort_index=0, severity=None)])_ 

##### TestGroup _ = GroupTypeData(id='test_group', title='By test group', values=[GroupData(id='no group', title='Ungrouped', description='Some tests don’t belong to any group under the selected condition', sort_index=0, severity=None), GroupData(id='classification', title='Classification', description='', sort_index=0, severity=None), GroupData(id='data_drift', title='Data Drift', description='', sort_index=0, severity=None), GroupData(id='data_integrity', title='Data Integrity', description='', sort_index=0, severity=None), GroupData(id='data_quality', title='Data Quality', description='', sort_index=0, severity=None), GroupData(id='regression', title='Regression', description='', sort_index=0, severity=None)])_ 

##### TestType _ = GroupTypeData(id='test_type', title='By test type', values=[])_ 

#### Methods: 

### _class _ Test()
Bases: `object`

all fields in test class with type that is subclass of Metric would be used as dependencies of test.


#### Attributes: 

##### context _ = None_ 

##### group _: str_ 

##### name _: str_ 

#### Methods: 

##### _abstract _ check()

##### get_result()

##### set_context(context)

### _class _ TestResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>)
Bases: `object`


#### Attributes: 

##### ERROR _ = 'ERROR'_ 

##### FAIL _ = 'FAIL'_ 

##### SKIPPED _ = 'SKIPPED'_ 

##### SUCCESS _ = 'SUCCESS'_ 

##### WARNING _ = 'WARNING'_ 

##### description _: str_ 

##### groups _: Dict[str, str]_ 

##### name _: str_ 

##### status _: str_ 

#### Methods: 

##### is_passed()

##### mark_as_error(description: Optional[str] = None)

##### mark_as_fail(description: Optional[str] = None)

##### mark_as_success(description: Optional[str] = None)

##### mark_as_warning(description: Optional[str] = None)

##### set_status(status: str, description: Optional[str] = None)

### _class _ TestValueCondition(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `object`

Class for processing a value conditions - should it be less, greater than, equals and so on.

An object of the class stores specified conditions and can be used for checking a value by them.


#### Attributes: 

##### eq _: Optional[Union[float, int]]_ _ = None_ 

##### gt _: Optional[Union[float, int]]_ _ = None_ 

##### gte _: Optional[Union[float, int]]_ _ = None_ 

##### is_in _: Optional[List[Union[float, int, str, bool]]]_ _ = None_ 

##### lt _: Optional[Union[float, int]]_ _ = None_ 

##### lte _: Optional[Union[float, int]]_ _ = None_ 

##### not_eq _: Optional[Union[float, int]]_ _ = None_ 

##### not_in _: Optional[List[Union[float, int, str, bool]]]_ _ = None_ 

#### Methods: 

##### as_dict()

##### check_value(value: Union[float, int])

##### has_condition()
Checks if we have a condition in the object and returns True in this case.
If we have no conditions - returns False.

### generate_column_tests(test_class: Type[Test], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Function for generating tests for columns


### _class _ ByClassClassificationTest(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### by_class_metric _: [ClassificationQualityByClass](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass)_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### group _: str_ _ = 'classification'_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### _abstract _ get_value(result: dict)

### _class _ SimpleClassificationTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### Attributes: 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### group _: str_ _ = 'classification'_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### _abstract _ get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ SimpleClassificationTestTopK(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`, `ABC`


#### Attributes: 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

### _class _ TestAccuracyScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'Accuracy Score'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestAccuracyScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestAccuracyScore)

##### render_json(obj: TestAccuracyScore)

### _class _ TestF1ByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### Attributes: 

##### name _: str_ _ = 'F1 Score by Class'_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: dict)

### _class _ TestF1ByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestF1ByClass)

##### render_json(obj: TestF1ByClass)

### _class _ TestF1Score(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'F1 Score'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestF1ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestF1Score)

##### render_json(obj: TestF1Score)

### _class _ TestFNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'False Negative Rate'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestFNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestF1Score)

##### render_json(obj: TestFNR)

### _class _ TestFPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'False Positive Rate'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestFPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestF1Score)

##### render_json(obj: TestFPR)

### _class _ TestLogLoss(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'Logarithmic Loss'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestLogLossRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestLogLoss)

##### render_json(obj: TestLogLoss)

### _class _ TestPrecisionByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### Attributes: 

##### name _: str_ _ = 'Precision Score by Class'_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: dict)

### _class _ TestPrecisionByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestPrecisionByClass)

##### render_json(obj: TestPrecisionByClass)

### _class _ TestPrecisionScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'Precision Score'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestPrecisionScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestPrecisionScore)

##### render_json(obj: TestPrecisionScore)

### _class _ TestRecallByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### Attributes: 

##### name _: str_ _ = 'Recall Score by Class'_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: dict)

### _class _ TestRecallByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestRecallByClass)

##### render_json(obj: TestRecallByClass)

### _class _ TestRecallScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'Recall Score'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestRecallScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestRecallScore)

##### render_json(obj: TestRecallScore)

### _class _ TestRocAuc(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### Attributes: 

##### name _: str_ _ = 'ROC AUC Score'_ 

##### roc_curve _: [ClassificationRocCurve](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve)_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestRocAucRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestRocAuc)

##### render_json(obj: TestRocAuc)

### _class _ TestTNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'True Negative Rate'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestTNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestF1Score)

##### render_json(obj: TestTNR)

### _class _ TestTPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### name _: str_ _ = 'True Positive Rate'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestTPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestF1Score)

##### render_json(obj: TestTPR)

### _class _ BaseDataDriftMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### group _: str_ _ = 'data_drift'_ 

##### metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

#### Methods: 

##### check()

### _class _ TestAllFeaturesValueDrift()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for numeric and category features


#### Attributes: 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestColumnValueDrift(column_name: str, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `Test`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_drift'_ 

##### metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

##### name _: str_ _ = 'Drift per Column'_ 

#### Methods: 

##### check()

### _class _ TestColumnValueDriftRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueDrift)

##### render_json(obj: TestColumnValueDrift)

### _class _ TestCustomFeaturesValueDrift(features: List[str])
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for specified features


#### Attributes: 

##### features _: List[str]_ 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestDataDriftResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, features: Dict[str, Tuple[str, float, float]] = <factory>)
Bases: `TestResult`


#### Attributes: 

##### features _: Dict[str, Tuple[str, float, float]]_ 

#### Methods: 

### _class _ TestNumberOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseDataDriftMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

##### name _: str_ _ = 'Number of Drifted Features'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfDriftedColumns)

##### render_json(obj: TestNumberOfDriftedColumns)

### _class _ TestShareOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseDataDriftMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

##### name _: str_ _ = 'Share of Drifted Columns'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestShareOfDriftedColumns)

##### render_json(obj: TestShareOfDriftedColumns)

### _class _ BaseIntegrityByColumnsConditionTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### column_name _: str_ 

##### data_integrity_metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### group _: str_ _ = 'data_integrity'_ 

#### Methods: 

##### groups()

### _class _ BaseIntegrityColumnMissingValuesTest(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_integrity'_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

#### Methods: 

### _class _ BaseIntegrityMissingValuesValuesTest(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### group _: str_ _ = 'data_integrity'_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

#### Methods: 

### _class _ BaseIntegrityOneColumnTest(column_name: str)
Bases: `Test`, `ABC`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_integrity'_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

#### Methods: 

##### groups()

### _class _ BaseIntegrityValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### group _: str_ _ = 'data_integrity'_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

#### Methods: 

### _class _ BaseTestMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

Common class for tests of missing values.
Some tests have the same details visualizations.


#### Attributes: 

##### MISSING_VALUES_NAMING_MAPPING _ = {None: 'Pandas nulls (None, NAN, etc.)', '': '"" (empty string)', inf: 'Numpy "inf" value', -inf: 'Numpy "-inf" value'}_ 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### get_table_with_missing_values_and_percents_by_column(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), metric_result: [DatasetMissingValuesMetricResult](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult), name: str)
Get a table with missing values number and percents

##### get_table_with_number_of_missing_values_by_one_missing_value(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), current_missing_values: dict, reference_missing_values: Optional[dict], name: str)

### _class _ TestAllColumnsShareOfMissingValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)


#### Attributes: 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestColumnAllConstantValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only one unique value in a column


#### Attributes: 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'All Constant Values in a Column'_ 

#### Methods: 

##### check()

### _class _ TestColumnAllConstantValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnAllConstantValues)

### _class _ TestColumnAllUniqueValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only uniques values in a column


#### Attributes: 

##### column_name _: str_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'All Unique Values in a Column'_ 

#### Methods: 

##### check()

### _class _ TestColumnAllUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnAllUniqueValues)

### _class _ TestColumnNumberOfDifferentMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of differently encoded missing values in one column.


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'Different Types of Missing Values in a Column'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset

##### render_json(obj: TestColumnNumberOfDifferentMissingValues)

### _class _ TestColumnNumberOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of missing values in one column.


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Number of Missing Values in a Column'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestColumnNumberOfMissingValues)

### _class _ TestColumnShareOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a share of missing values in one column.


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Share of Missing Values in a Column'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestColumnShareOfMissingValues)

### _class _ TestColumnValueRegExp(column_name: str, reg_exp: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_integrity'_ 

##### metric _: [ColumnRegExpMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric)_ 

##### name _: str_ _ = 'RegExp Match'_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### groups()

### _class _ TestColumnValueRegExpRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueRegExp)

### _class _ TestColumnsType(columns_type: Optional[dict] = None)
Bases: `Test`

This test compares columns type against the specified ones or a reference dataframe


##### _class _ Result name: str, description: str, status: str, groups: Dict[str, str] = <factory>, columns_types: Dict[str, Tuple[str, str]] = <factory>
Bases: `TestResult`


#### Attributes: 

##### columns_types _: Dict[str, Tuple[str, str]]_ 

#### Methods: 

##### check()

##### columns_type _: Optional[dict]_ 

##### group _: str_ _ = 'data_integrity'_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Column Types'_ 

#### Attributes: 

#### Methods: 

### _class _ TestColumnsTypeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnsType)

##### render_json(obj: TestColumnsType)

### _class _ TestNumberOfColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of all columns in the data, including utility columns (id/index, datetime, target, predictions)


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Columns'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfColumns)

##### render_json(obj: TestNumberOfColumns)

### _class _ TestNumberOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of columns with a missing value.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Number of Columns With Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfMissingValues)

##### render_json(obj: TestNumberOfColumnsWithMissingValues)

### _class _ TestNumberOfConstantColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained only one unique value


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Constant Columns'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfConstantColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfConstantColumns)

##### render_json(obj: TestNumberOfConstantColumns)

### _class _ TestNumberOfDifferentMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of different encoded missing values.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'Different Types of Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset

##### render_json(obj: TestNumberOfDifferentMissingValues)

### _class _ TestNumberOfDuplicatedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many columns have duplicates in the dataset


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Duplicate Columns'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDuplicatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestNumberOfDuplicatedColumns)

### _class _ TestNumberOfDuplicatedRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many rows have duplicates in the dataset


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Duplicate Rows'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDuplicatedRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestNumberOfDuplicatedRows)

### _class _ TestNumberOfEmptyColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained all NAN values


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Empty Columns'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfEmptyColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfEmptyColumns)

### _class _ TestNumberOfEmptyRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows contained all NAN values


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Empty Rows'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of missing values.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Number of Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfMissingValues)

##### render_json(obj: TestNumberOfMissingValues)

### _class _ TestNumberOfRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows in the data


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### name _: str_ _ = 'Number of Rows'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestNumberOfRows)

### _class _ TestNumberOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of rows with a missing value.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Number Of Rows With Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestNumberOfRowsWithMissingValues)

### _class _ TestShareOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of columns with a missing value.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Share of Columns With Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfMissingValues)

##### render_json(obj: TestShareOfColumnsWithMissingValues)

### _class _ TestShareOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of missing values.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'Share of Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfMissingValues)

##### render_json(obj: TestShareOfMissingValues)

### _class _ TestShareOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of rows with a missing value.


#### Attributes: 

##### condition _: TestValueCondition_ 

##### metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### name _: str_ _ = 'The Share of Rows With Missing Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_json(obj: TestShareOfRowsWithMissingValues)

### _class _ BaseDataQualityCorrelationsMetricsValueTest(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### group _: str_ _ = 'data_quality'_ 

##### method _: str_ 

##### metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

#### Methods: 

### _class _ BaseDataQualityMetricsValueTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

#### Methods: 

### _class _ BaseDataQualityValueListMetricsTest(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### values _: Optional[list]_ 

#### Methods: 

##### groups()

### _class _ BaseDataQualityValueRangeMetricsTest(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### column _: str_ 

##### group _: str_ _ = 'data_quality'_ 

##### left _: Optional[float]_ 

##### metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### right _: Optional[float]_ 

#### Methods: 

##### groups()

### _class _ BaseFeatureDataQualityMetricsTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityMetricsValueTest`, `ABC`


#### Attributes: 

##### column_name _: str_ 

#### Methods: 

##### check()

##### groups()

### _class _ TestAllColumnsMostCommonValueShare()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates most common value share tests for each column in the dataset


#### Attributes: 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestCatColumnsOutOfListValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create share of out of list values tests for category columns


#### Attributes: 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestColumnValueMax(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Max Value'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMaxRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueMax)

### _class _ TestColumnValueMean(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Mean Value'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMeanRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueMean)

### _class _ TestColumnValueMedian(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Median Value'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMedianRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueMedian)

### _class _ TestColumnValueMin(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Min Value'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMinRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueMin)

### _class _ TestColumnValueStd(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Standard Deviation (SD)'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueStdRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestColumnValueStd)

### _class _ TestConflictPrediction()
Bases: `Test`


#### Attributes: 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [DataQualityStabilityMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric)_ 

##### name _: str_ _ = 'Test number of conflicts in prediction'_ 

#### Methods: 

##### check()

### _class _ TestConflictTarget()
Bases: `Test`


#### Attributes: 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [DataQualityStabilityMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric)_ 

##### name _: str_ _ = 'Test number of conflicts in target'_ 

#### Methods: 

##### check()

### _class _ TestCorrelationChanges(corr_diff: float = 0.25, method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### corr_diff _: float_ 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### name _: str_ _ = 'Change in Correlation'_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestCorrelationChangesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestCorrelationChanges)

### _class _ TestHighlyCorrelatedColumns(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### method _: str_ 

##### metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### name _: str_ _ = 'Highly Correlated Columns'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestHighlyCorrelatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestHighlyCorrelatedColumns)

##### render_json(obj: TestHighlyCorrelatedColumns)

### _class _ TestMeanInNSigmas(column_name: str, n_sigmas: int = 2)
Bases: `Test`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### n_sigmas _: int_ 

##### name _: str_ _ = 'Mean Value Stability'_ 

#### Methods: 

##### check()

### _class _ TestMeanInNSigmasRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestMeanInNSigmas)

##### render_json(obj: TestMeanInNSigmas)

### _class _ TestMostCommonValueShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Share of the Most Common Value'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestMostCommonValueShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestMostCommonValueShare)

##### render_json(obj: TestMostCommonValueShare)

### _class _ TestNumColumnsMeanInNSigmas()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create tests of mean for all numeric columns


#### Attributes: 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestNumColumnsOutOfRangeValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates share of out of range values tests for all numeric columns


#### Attributes: 

#### Methods: 

##### generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestNumberOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### name _: str_ _ = 'Number Out-of-List Values'_ 

##### value _: Union[float, int]_ 

##### values _: Optional[list]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfOutListValues)

### _class _ TestNumberOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`


#### Attributes: 

##### column _: str_ 

##### condition _: TestValueCondition_ 

##### left _: Optional[float]_ 

##### metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### name _: str_ _ = 'Number of Out-of-Range Values '_ 

##### right _: Optional[float]_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfOutRangeValues)

### _class _ TestNumberOfUniqueValues(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Number of Unique Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestNumberOfUniqueValues)

### _class _ TestPredictionFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### method _: str_ 

##### metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### name _: str_ _ = 'Correlation between Prediction and Features'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestPredictionFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestTargetFeaturesCorrelations)

##### render_json(obj: TestPredictionFeaturesCorrelations)

### _class _ TestShareOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### name _: str_ _ = 'Share of Out-of-List Values'_ 

##### value _: Union[float, int]_ 

##### values _: Optional[list]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestShareOfOutListValues)

##### render_json(obj: TestShareOfOutListValues)

### _class _ TestShareOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`


#### Attributes: 

##### column _: str_ 

##### condition _: TestValueCondition_ 

##### left _: Optional[float]_ 

##### metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### name _: str_ _ = 'Share of Out-of-Range Values'_ 

##### right _: Optional[float]_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestShareOfOutRangeValues)

##### render_json(obj: TestShareOfOutRangeValues)

### _class _ TestTargetFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### method _: str_ 

##### metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### name _: str_ _ = 'Correlation between Target and Features'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestTargetFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestTargetFeaturesCorrelations)

##### render_json(obj: TestTargetFeaturesCorrelations)

### _class _ TestTargetPredictionCorrelation(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### method _: str_ 

##### metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### name _: str_ _ = 'Correlation between Target and Prediction'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestUniqueValuesShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### column_name _: str_ 

##### condition _: TestValueCondition_ 

##### metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### name _: str_ _ = 'Share of Unique Values'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestUniqueValuesShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestUniqueValuesShare)

### _class _ TestValueList(column_name: str, values: Optional[list] = None)
Bases: `Test`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### name _: str_ _ = 'Out-of-List Values'_ 

##### values _: Optional[list]_ 

#### Methods: 

##### check()

### _class _ TestValueListRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueList)

##### render_json(obj: TestValueList)

### _class _ TestValueQuantile(column_name: str, quantile: float, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### Attributes: 

##### column_name _: str_ 

##### group _: str_ _ = 'data_quality'_ 

##### metric _: [ColumnQuantileMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric)_ 

##### name _: str_ _ = 'Quantile Value'_ 

##### quantile _: float_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### groups()

### _class _ TestValueQuantileRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueQuantile)

### _class _ TestValueRange(column_name: str, left: Optional[float] = None, right: Optional[float] = None)
Bases: `Test`


#### Attributes: 

##### column _: str_ 

##### group _: str_ _ = 'data_quality'_ 

##### left _: Optional[float]_ 

##### metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### name _: str_ _ = 'Value Range'_ 

##### right _: Optional[float]_ 

#### Methods: 

##### check()

### _class _ TestValueRangeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueRange)

### _class _ BaseRegressionPerformanceMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### group _: str_ _ = 'regression'_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

#### Methods: 

### _class _ TestValueAbsMaxError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### name _: str_ _ = 'Max Absolute Error'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueAbsMaxErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueAbsMaxError)

##### render_json(obj: TestValueAbsMaxError)

### _class _ TestValueMAE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### name _: str_ _ = 'Mean Absolute Error (MAE)'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueMAERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueMAE)

##### render_json(obj: TestValueMAE)

### _class _ TestValueMAPE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### name _: str_ _ = 'Mean Absolute Percentage Error (MAPE)'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueMAPERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueMAPE)

##### render_json(obj: TestValueMAPE)

### _class _ TestValueMeanError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### name _: str_ _ = 'Mean Error (ME)'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueMeanErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueMeanError)

##### render_json(obj: TestValueMeanError)

### _class _ TestValueR2Score(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### name _: str_ _ = 'R2 Score'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueR2ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueR2Score)

##### render_json(obj: TestValueAbsMaxError)

### _class _ TestValueRMSE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### condition _: TestValueCondition_ 

##### dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### name _: str_ _ = 'Root Mean Square Error (RMSE)'_ 

##### value _: Union[float, int]_ 

#### Methods: 

##### calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### get_condition()

##### get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueRMSERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### render_html(obj: TestValueRMSE)

##### render_json(obj: TestValueRMSE)

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
