# evidently.tests package

## Submodules


### _class _ BaseCheckValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseConditionsTest`

Base class for all tests with checking a value condition


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

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

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

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; run(\*, reference_data: Optional[DataFrame], current_data: DataFrame, column_mapping: Optional[[ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping)] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### _class _ BaseConditionsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `Test`, `ABC`

Base class for all tests with a condition


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

#### Methods: 

### _class _ GroupData(id: str, title: str, description: str, sort_index: int = 0, severity: Optional[str] = None)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; description _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; id _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; severity _: Optional[str]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; sort_index _: int_ _ = 0_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

#### Methods: 

### _class _ GroupTypeData(id: str, title: str, values: List[evidently.tests.base_test.GroupData] = <factory>)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; id _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: List[GroupData]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; add_value(data: GroupData)

### _class _ GroupingTypes()
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; ByClass _ = GroupTypeData(id='by_class', title='By class', values=[])_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; ByFeature _ = GroupTypeData(id='by_feature', title='By feature', values=[GroupData(id='no group', title='Dataset-level tests', description='Some tests cannot be grouped by feature', sort_index=0, severity=None)])_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; TestGroup _ = GroupTypeData(id='test_group', title='By test group', values=[GroupData(id='no group', title='Ungrouped', description='Some tests don’t belong to any group under the selected condition', sort_index=0, severity=None), GroupData(id='classification', title='Classification', description='', sort_index=0, severity=None), GroupData(id='data_drift', title='Data Drift', description='', sort_index=0, severity=None), GroupData(id='data_integrity', title='Data Integrity', description='', sort_index=0, severity=None), GroupData(id='data_quality', title='Data Quality', description='', sort_index=0, severity=None), GroupData(id='regression', title='Regression', description='', sort_index=0, severity=None)])_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; TestType _ = GroupTypeData(id='test_type', title='By test type', values=[])_ 

#### Methods: 

### _class _ Test()
Bases: `object`

all fields in test class with type that is subclass of Metric would be used as dependencies of test.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; context _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ check()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_result()

##### &nbsp;&nbsp;&nbsp;&nbsp; set_context(context)

### _class _ TestResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>)
Bases: `object`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; ERROR _ = 'ERROR'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; FAIL _ = 'FAIL'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; SKIPPED _ = 'SKIPPED'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; SUCCESS _ = 'SUCCESS'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; WARNING _ = 'WARNING'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; description _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups _: Dict[str, str]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; status _: str_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; is_passed()

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_error(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_fail(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_success(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; mark_as_warning(description: Optional[str] = None)

##### &nbsp;&nbsp;&nbsp;&nbsp; set_status(status: str, description: Optional[str] = None)

### _class _ TestValueCondition(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `object`

Class for processing a value conditions - should it be less, greater than, equals and so on.

An object of the class stores specified conditions and can be used for checking a value by them.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; eq _: Optional[Union[float, int]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; gt _: Optional[Union[float, int]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; gte _: Optional[Union[float, int]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; is_in _: Optional[List[Union[float, int, str, bool]]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; lt _: Optional[Union[float, int]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; lte _: Optional[Union[float, int]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; not_eq _: Optional[Union[float, int]]_ _ = None_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; not_in _: Optional[List[Union[float, int, str, bool]]]_ _ = None_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; as_dict()

##### &nbsp;&nbsp;&nbsp;&nbsp; check_value(value: Union[float, int])

##### &nbsp;&nbsp;&nbsp;&nbsp; has_condition()
Checks if we have a condition in the object and returns True in this case.
If we have no conditions - returns False.

### generate_column_tests(test_class: Type[Test], columns: Optional[Union[str, list]] = None, parameters: Optional[Dict] = None)
Function for generating tests for columns


### _class _ ByClassClassificationTest(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; by_class_metric _: [ClassificationQualityByClass](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.quality_by_class_metric.ClassificationQualityByClass)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'classification'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_value(result: dict)

### _class _ SimpleClassificationTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'classification'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; _abstract _ get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ SimpleClassificationTestTopK(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

### _class _ TestAccuracyScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Accuracy Score'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestAccuracyScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestAccuracyScore)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestAccuracyScore)

### _class _ TestF1ByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'F1 Score by Class'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: dict)

### _class _ TestF1ByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1ByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestF1ByClass)

### _class _ TestF1Score(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'F1 Score'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestF1ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestF1Score)

### _class _ TestFNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'False Negative Rate'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestFNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestFNR)

### _class _ TestFPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'False Positive Rate'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestFPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestFPR)

### _class _ TestLogLoss(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Logarithmic Loss'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestLogLossRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestLogLoss)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestLogLoss)

### _class _ TestPrecisionByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Precision Score by Class'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: dict)

### _class _ TestPrecisionByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestPrecisionByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestPrecisionByClass)

### _class _ TestPrecisionScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Precision Score'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestPrecisionScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestPrecisionScore)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestPrecisionScore)

### _class _ TestRecallByClass(label: str, threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `ByClassClassificationTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Recall Score by Class'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: dict)

### _class _ TestRecallByClassRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestRecallByClass)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestRecallByClass)

### _class _ TestRecallScore(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Recall Score'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestRecallScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestRecallScore)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestRecallScore)

### _class _ TestRocAuc(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'ROC AUC Score'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; roc_curve _: [ClassificationRocCurve](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.roc_curve_metric.ClassificationRocCurve)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestRocAucRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestRocAuc)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestRocAuc)

### _class _ TestTNR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'True Negative Rate'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestTNRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestTNR)

### _class _ TestTPR(threshold: Optional[float] = None, k: Optional[Union[float, int]] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `SimpleClassificationTestTopK`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; conf_matrix _: [ClassificationConfusionMatrix](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.confusion_matrix_metric.ClassificationConfusionMatrix)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [ClassificationDummyMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_dummy_metric.ClassificationDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ClassificationQualityMetric](evidently.metrics.classification_performance.md#evidently.metrics.classification_performance.classification_quality_metric.ClassificationQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'True Positive Rate'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_value(result: [DatasetClassificationQuality](evidently.calculations.md#evidently.calculations.classification_performance.DatasetClassificationQuality))

### _class _ TestTPRRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestF1Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestTPR)

### _class _ BaseDataDriftMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_drift'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestAllFeaturesValueDrift()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for numeric and category features


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestColumnValueDrift(column_name: str, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `Test`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_drift'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Drift per Column'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestColumnValueDriftRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueDrift)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnValueDrift)

### _class _ TestCustomFeaturesValueDrift(features: List[str])
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create value drift tests for specified features


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; features _: List[str]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestDataDriftResult(name: str, description: str, status: str, groups: Dict[str, str] = <factory>, features: Dict[str, Tuple[str, float, float]] = <factory>)
Bases: `TestResult`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; features _: Dict[str, Tuple[str, float, float]]_ 

#### Methods: 

### _class _ TestNumberOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseDataDriftMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Drifted Features'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfDriftedColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDriftedColumns)

### _class _ TestShareOfDriftedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None, options: Optional[[DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)] = None)
Bases: `BaseDataDriftMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DataDriftTable](evidently.metrics.data_drift.md#evidently.metrics.data_drift.data_drift_table.DataDriftTable)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Share of Drifted Columns'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfDriftedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestShareOfDriftedColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfDriftedColumns)

### _class _ BaseIntegrityByColumnsConditionTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; data_integrity_metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### _class _ BaseIntegrityColumnMissingValuesTest(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

#### Methods: 

### _class _ BaseIntegrityMissingValuesValuesTest(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

#### Methods: 

### _class _ BaseIntegrityOneColumnTest(column_name: str)
Bases: `Test`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### _class _ BaseIntegrityValueTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

#### Methods: 

### _class _ BaseTestMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)

Common class for tests of missing values.
Some tests have the same details visualizations.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; MISSING_VALUES_NAMING_MAPPING _ = {None: 'Pandas nulls (None, NAN, etc.)', '': '"" (empty string)', inf: 'Numpy "inf" value', -inf: 'Numpy "-inf" value'}_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; get_table_with_missing_values_and_percents_by_column(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), metric_result: [DatasetMissingValuesMetricResult](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetricResult), name: str)
Get a table with missing values number and percents

##### &nbsp;&nbsp;&nbsp;&nbsp; get_table_with_number_of_missing_values_by_one_missing_value(info: [TestHtmlInfo](evidently.renderers.md#evidently.renderers.base_renderer.TestHtmlInfo), current_missing_values: dict, reference_missing_values: Optional[dict], name: str)

### _class _ TestAllColumnsShareOfMissingValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestColumnAllConstantValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only one unique value in a column


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'All Constant Values in a Column'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestColumnAllConstantValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnAllConstantValues)

### _class _ TestColumnAllUniqueValues(column_name: str)
Bases: `BaseIntegrityOneColumnTest`

Test that there is only uniques values in a column


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'All Unique Values in a Column'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestColumnAllUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnAllUniqueValues)

### _class _ TestColumnNumberOfDifferentMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of differently encoded missing values in one column.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Different Types of Missing Values in a Column'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnNumberOfDifferentMissingValues)

### _class _ TestColumnNumberOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a number of missing values in one column.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Number of Missing Values in a Column'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnNumberOfMissingValues)

### _class _ TestColumnShareOfMissingValues(column_name: str, missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityColumnMissingValuesTest`

Check a share of missing values in one column.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Share of Missing Values in a Column'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnShareOfMissingValues)

### _class _ TestColumnValueRegExp(column_name: str, reg_exp: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnRegExpMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_regexp_metric.ColumnRegExpMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'RegExp Match'_ 

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

### _class _ TestColumnValueRegExpRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueRegExp)

### _class _ TestColumnsType(columns_type: Optional[dict] = None)
Bases: `Test`

This test compares columns type against the specified ones or a reference dataframe


##### &nbsp;&nbsp;&nbsp;&nbsp; _class _ Result name: str, description: str, status: str, groups: Dict[str, str] = <factory>, columns_types: Dict[str, Tuple[str, str]] = <factory>
Bases: `TestResult`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; columns_types _: Dict[str, Tuple[str, str]]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

##### &nbsp;&nbsp;&nbsp;&nbsp; columns_type _: Optional[dict]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_integrity'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Column Types'_ 

#### Attributes: 

#### Methods: 

### _class _ TestColumnsTypeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnsType)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestColumnsType)

### _class _ TestNumberOfColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of all columns in the data, including utility columns (id/index, datetime, target, predictions)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Columns'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfColumns)

### _class _ TestNumberOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of columns with a missing value.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Number of Columns With Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfColumnsWithMissingValues)

### _class _ TestNumberOfConstantColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained only one unique value


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Constant Columns'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfConstantColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfConstantColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfConstantColumns)

### _class _ TestNumberOfDifferentMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of different encoded missing values.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Different Types of Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDifferentMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfDifferentMissingValues)
Get a table with a missing value and number of the value in the dataset

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDifferentMissingValues)

### _class _ TestNumberOfDuplicatedColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many columns have duplicates in the dataset


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Duplicate Columns'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDuplicatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDuplicatedColumns)

### _class _ TestNumberOfDuplicatedRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

How many rows have duplicates in the dataset


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Duplicate Rows'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfDuplicatedRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfDuplicatedRows)

### _class _ TestNumberOfEmptyColumns(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of columns contained all NAN values


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Empty Columns'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfEmptyColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfEmptyColumns)

### _class _ TestNumberOfEmptyRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows contained all NAN values


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Empty Rows'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of missing values.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Number of Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfMissingValues)

### _class _ TestNumberOfRows(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityValueTest`

Number of rows in the data


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_summary_metric.DatasetSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Rows'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfRowsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfRows)

### _class _ TestNumberOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a number of rows with a missing value.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Number Of Rows With Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestNumberOfRowsWithMissingValues)

### _class _ TestShareOfColumnsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of columns with a missing value.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Share of Columns With Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfColumnsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfColumnsWithMissingValues)

### _class _ TestShareOfMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of missing values.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Share of Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfMissingValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfMissingValues)

### _class _ TestShareOfRowsWithMissingValues(missing_values: Optional[list] = None, replace: bool = True, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseIntegrityMissingValuesValuesTest`

Check a share of rows with a missing value.


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetMissingValuesMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.dataset_missing_values_metric.DatasetMissingValuesMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'The Share of Rows With Missing Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfRowsWithMissingValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseTestMissingValuesRenderer`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfRowsWithMissingValues)

### _class _ BaseDataQualityCorrelationsMetricsValueTest(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; method _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

#### Methods: 

### _class _ BaseDataQualityMetricsValueTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

#### Methods: 

### _class _ BaseDataQualityValueListMetricsTest(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: Optional[list]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### _class _ BaseDataQualityValueRangeMetricsTest(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; left _: Optional[float]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; right _: Optional[float]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### _class _ BaseFeatureDataQualityMetricsTest(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityMetricsValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

##### &nbsp;&nbsp;&nbsp;&nbsp; groups()

### _class _ TestAllColumnsMostCommonValueShare()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates most common value share tests for each column in the dataset


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestCatColumnsOutOfListValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create share of out of list values tests for category columns


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestColumnValueMax(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Max Value'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMaxRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMax)

### _class _ TestColumnValueMean(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Mean Value'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMeanRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMean)

### _class _ TestColumnValueMedian(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Median Value'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMedianRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMedian)

### _class _ TestColumnValueMin(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Min Value'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueMinRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueMin)

### _class _ TestColumnValueStd(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Standard Deviation (SD)'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestColumnValueStdRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestColumnValueStd)

### _class _ TestConflictPrediction()
Bases: `Test`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DataQualityStabilityMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Test number of conflicts in prediction'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestConflictTarget()
Bases: `Test`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DataQualityStabilityMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.stability_metric.DataQualityStabilityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Test number of conflicts in target'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestCorrelationChanges(corr_diff: float = 0.25, method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; corr_diff _: float_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Change in Correlation'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestCorrelationChangesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestCorrelationChanges)

### _class _ TestHighlyCorrelatedColumns(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; method _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Highly Correlated Columns'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestHighlyCorrelatedColumnsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestHighlyCorrelatedColumns)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestHighlyCorrelatedColumns)

### _class _ TestMeanInNSigmas(column_name: str, n_sigmas: int = 2)
Bases: `Test`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; n_sigmas _: int_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Mean Value Stability'_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestMeanInNSigmasRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestMeanInNSigmas)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestMeanInNSigmas)

### _class _ TestMostCommonValueShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Share of the Most Common Value'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestMostCommonValueShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestMostCommonValueShare)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestMostCommonValueShare)

### _class _ TestNumColumnsMeanInNSigmas()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Create tests of mean for all numeric columns


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestNumColumnsOutOfRangeValues()
Bases: [`BaseGenerator`](evidently.utils.md#evidently.utils.generators.BaseGenerator)

Creates share of out of range values tests for all numeric columns


#### Attributes: 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; generate(columns_info: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

### _class _ TestNumberOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number Out-of-List Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: Optional[list]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfOutListValues)

### _class _ TestNumberOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; left _: Optional[float]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Out-of-Range Values '_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; right _: Optional[float]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfOutRangeValues)

### _class _ TestNumberOfUniqueValues(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Number of Unique Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestNumberOfUniqueValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestNumberOfUniqueValues)

### _class _ TestPredictionFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; method _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Correlation between Prediction and Features'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestPredictionFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestTargetFeaturesCorrelations)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestPredictionFeaturesCorrelations)

### _class _ TestShareOfOutListValues(column_name: str, values: Optional[list] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueListMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Share of Out-of-List Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: Optional[list]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfOutListValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestShareOfOutListValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfOutListValues)

### _class _ TestShareOfOutRangeValues(column_name: str, left: Optional[float] = None, right: Optional[float] = None, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityValueRangeMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; left _: Optional[float]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Share of Out-of-Range Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; right _: Optional[float]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestShareOfOutRangeValuesRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestShareOfOutRangeValues)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestShareOfOutRangeValues)

### _class _ TestTargetFeaturesCorrelations(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; method _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Correlation between Target and Features'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestTargetFeaturesCorrelationsRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestTargetFeaturesCorrelations)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestTargetFeaturesCorrelations)

### _class _ TestTargetPredictionCorrelation(method: str = 'pearson', eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseDataQualityCorrelationsMetricsValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; method _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [DatasetCorrelationsMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.dataset_correlations_metric.DatasetCorrelationsMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Correlation between Target and Prediction'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestUniqueValuesShare(column_name: str, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseFeatureDataQualityMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnSummaryMetric](evidently.metrics.data_integrity.md#evidently.metrics.data_integrity.column_summary_metric.ColumnSummaryMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Share of Unique Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestUniqueValuesShareRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestUniqueValuesShare)

### _class _ TestValueList(column_name: str, values: Optional[list] = None)
Bases: `Test`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueListMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_list_metric.ColumnValueListMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Out-of-List Values'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; values _: Optional[list]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestValueListRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueList)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueList)

### _class _ TestValueQuantile(column_name: str, quantile: float, eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnQuantileMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_quantile_metric.ColumnQuantileMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Quantile Value'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; quantile _: float_ 

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

### _class _ TestValueQuantileRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueQuantile)

### _class _ TestValueRange(column_name: str, left: Optional[float] = None, right: Optional[float] = None)
Bases: `Test`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; column _: str_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'data_quality'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; left _: Optional[float]_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [ColumnValueRangeMetric](evidently.metrics.data_quality.md#evidently.metrics.data_quality.column_value_range_metric.ColumnValueRangeMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Value Range'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; right _: Optional[float]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; check()

### _class _ TestValueRangeRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueRange)

### _class _ BaseRegressionPerformanceMetricsTest(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseCheckValueTest`, `ABC`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; group _: str_ _ = 'regression'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

#### Methods: 

### _class _ TestValueAbsMaxError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Max Absolute Error'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueAbsMaxErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueAbsMaxError)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueAbsMaxError)

### _class _ TestValueMAE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Mean Absolute Error (MAE)'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueMAERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueMAE)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueMAE)

### _class _ TestValueMAPE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Mean Absolute Percentage Error (MAPE)'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueMAPERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueMAPE)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueMAPE)

### _class _ TestValueMeanError(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Mean Error (ME)'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueMeanErrorRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueMeanError)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueMeanError)

### _class _ TestValueR2Score(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'R2 Score'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueR2ScoreRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueR2Score)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueAbsMaxError)

### _class _ TestValueRMSE(eq: Optional[Union[float, int]] = None, gt: Optional[Union[float, int]] = None, gte: Optional[Union[float, int]] = None, is_in: Optional[List[Union[float, int, str, bool]]] = None, lt: Optional[Union[float, int]] = None, lte: Optional[Union[float, int]] = None, not_eq: Optional[Union[float, int]] = None, not_in: Optional[List[Union[float, int, str, bool]]] = None)
Bases: `BaseRegressionPerformanceMetricsTest`


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; condition _: TestValueCondition_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; dummy_metric _: [RegressionDummyMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_dummy_metric.RegressionDummyMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; metric _: [RegressionQualityMetric](evidently.metrics.regression_performance.md#evidently.metrics.regression_performance.regression_quality.RegressionQualityMetric)_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; name _: str_ _ = 'Root Mean Square Error (RMSE)'_ 

##### &nbsp;&nbsp;&nbsp;&nbsp; value _: Union[float, int]_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; calculate_value_for_test()
Method for getting the checking value.
Define it in a child class

##### &nbsp;&nbsp;&nbsp;&nbsp; get_condition()

##### &nbsp;&nbsp;&nbsp;&nbsp; get_description(value: Union[float, int])
Method for getting a description that we can use.
The description can use the checked value.
Define it in a child class

### _class _ TestValueRMSERenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: [`TestRenderer`](evidently.renderers.md#evidently.renderers.base_renderer.TestRenderer)


#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

##### &nbsp;&nbsp;&nbsp;&nbsp; render_html(obj: TestValueRMSE)

##### &nbsp;&nbsp;&nbsp;&nbsp; render_json(obj: TestValueRMSE)

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
