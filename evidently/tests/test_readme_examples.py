import json

import pytest
import pandas as pd
import numpy as np
from sklearn import datasets


from evidently import ColumnMapping
from evidently.dashboard import Dashboard
from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection, CatTargetDriftProfileSection, \
    RegressionPerformanceProfileSection, ClassificationPerformanceProfileSection, \
    ProbClassificationPerformanceProfileSection
from evidently.tabs import DataDriftTab, RegressionPerformanceTab, CatTargetDriftTab, ClassificationPerformanceTab, \
    ProbClassificationPerformanceTab


def _get_iris():
    # we do not use setUp method here, because of side effects in tests
    # side effect can be avoided by using fixtures from pytest :-)
    iris = datasets.load_iris()
    iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_frame['target'] = iris.target
    return iris, iris_frame


def _get_probabilistic_iris():
    iris = datasets.load_iris()
    iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
    random_probs = np.random.random((3, 150))
    random_probs = (random_probs / random_probs.sum(0))
    pred_df = pd.DataFrame(random_probs.T, columns=iris.target_names)
    iris_frame['target'] = iris.target_names[iris['target']]
    merged_reference = pd.concat([iris_frame, pred_df], axis=1)

    iris_column_mapping = ColumnMapping()
    iris_column_mapping.target = 'target'
    iris_column_mapping.prediction = iris.target_names.tolist()
    iris_column_mapping.numerical_features = iris.feature_names
    return merged_reference, iris_column_mapping


# TODO(fixme): Actually we would like to test html's output, but because
#  evidently/nbextension/static/index.js is missing
#  (and evidently/nbextension/static/index.js.LICENSE.txt is an actual text file)
#  saving an html report in the test itself fails.
#  A reasonable fallback is to use the private _json() method. Although, since it is never used anywhere else
#  it may be considered a bad testing practice to have methods only for testing purposes.
#  For now we stick to it until something better comes along.


@pytest.fixture
def iris():
    return datasets.load_iris()


@pytest.fixture
def iris_frame(iris):
    iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
    iris_frame['target'] = iris.target
    return iris_frame


@pytest.fixture
def iris_targets(iris):
    iris_targets = iris.target_names
    return iris_targets


###
# The following are extracted from the README.md file.
###
def test_data_drift_dashboard(iris_frame) -> None:
    # To generate the **Data Drift** report, run:
    iris_data_drift_report = Dashboard(tabs=[DataDriftTab()])
    iris_data_drift_report.calculate(iris_frame[:100], iris_frame[100:])
    actual = json.loads(iris_data_drift_report._json())
    # we leave the actual content test to other tests for widgets
    assert 'name' in actual
    assert len(actual['widgets']) == 1


def test_data_drift_categorical_target_drift_dashboard(iris_frame) -> None:
    # To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
    iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab(), CatTargetDriftTab()])
    iris_data_and_target_drift_report.calculate(iris_frame[:100], iris_frame[100:])
    actual = json.loads(iris_data_and_target_drift_report._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 3


def test_regression_performance_dashboard(iris_frame) -> None:
    # To generate the **Regression Model Performance** report, run:
    # FIXME: when prediction column is not present in the dataset
    #   ValueError: [Widget Regression Model Performance Report.] wi is None,
    #   no data available (forget to set it in widget?)
    iris_frame['prediction'] = iris_frame['target'][::-1]
    regression_model_performance = Dashboard(tabs=[RegressionPerformanceTab()])
    regression_model_performance.calculate(iris_frame[:100], iris_frame[100:])
    actual = json.loads(regression_model_performance._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 20


def test_regression_performance_single_frame_dashboard(iris_frame) -> None:
    # You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
    # FIXME: when prediction column is not present in the dataset
    #   ValueError: [Widget Regression Model Performance Report.] wi is None,
    #   no data available (forget to set it in widget?)
    iris_frame['prediction'] = iris_frame['target'][::-1]
    regression_single_model_performance = Dashboard(tabs=[RegressionPerformanceTab()])
    regression_single_model_performance.calculate(iris_frame, None)
    actual = json.loads(regression_single_model_performance._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 11


def test_classification_performance_dashboard(iris_frame) -> None:
    # To generate the **Classification Model Performance** report, run:
    # FIXME: when prediction column is not present in the dataset
    #  ValueError: [Widget Classification Model Performance Report.] wi is None,
    #  no data available (forget to set it in widget?)
    iris_frame['prediction'] = iris_frame['target'][::-1]
    classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab()])
    classification_performance_report.calculate(iris_frame[:100], iris_frame[100:])

    actual = json.loads(classification_performance_report._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 10


def test_probabilistic_classification_performance_dashboard(iris_frame, iris_targets) -> None:
    # For **Probabilistic Classification Model Performance** report, run:
    random_probs = np.random.random((3, 150))
    random_probs = (random_probs / random_probs.sum(0))
    pred_df = pd.DataFrame(random_probs.T, columns=iris_targets)
    iris_frame = pd.concat([iris_frame, pred_df], axis=1)
    iris_frame['target'] = iris_targets[iris_frame['target']]
    iris_column_mapping = ColumnMapping()
    iris_column_mapping.prediction = iris_targets
    classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab()])
    classification_performance_report.calculate(iris_frame, iris_frame, iris_column_mapping)

    actual = json.loads(classification_performance_report._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 20


def test_classification_performance_on_single_frame_dashboard(iris_frame) -> None:
    # You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
    iris_frame['prediction'] = iris_frame['target'][::-1]
    classification_single_frame_performance = Dashboard(tabs=[ClassificationPerformanceTab()])
    classification_single_frame_performance.calculate(iris_frame, None)
    actual = json.loads(classification_single_frame_performance._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 6


def test_probabilistic_classification_performance_on_single_frame_dashboard(iris_frame, iris_targets) -> None:
    # You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
    # FIXME: like above, when prediction column is not present in the dataset
    random_probs = np.random.random((3, 150))
    random_probs = (random_probs / random_probs.sum(0))
    pred_df = pd.DataFrame(random_probs.T, columns=iris_targets)
    iris_frame = pd.concat([iris_frame, pred_df], axis=1)
    iris_frame['target'] = iris_targets[iris_frame['target']]
    iris_column_mapping = ColumnMapping()
    iris_column_mapping.prediction = iris_targets
    prob_classification_single_frame_performance = Dashboard(tabs=[ProbClassificationPerformanceTab()])
    prob_classification_single_frame_performance.calculate(iris_frame, None, iris_column_mapping)
    actual = json.loads(prob_classification_single_frame_performance._json())
    assert 'name' in actual
    assert len(actual['widgets']) == 11


###
# The following are extracted from the README.md file.
###
def test_data_drift_profile() -> None:
    # To generate the **Data Drift** report, run:
    iris, iris_frame = _get_iris()
    iris_frame['prediction'] = iris.target[::-1]
    iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
    iris_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])

    actual = json.loads(iris_data_drift_profile.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['data_drift']['data']) == 6
    assert 'metrics' in actual['data_drift']['data']


def test_data_drift_categorical_target_drift_profile() -> None:
    # To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
    iris, iris_frame = _get_iris()
    iris_frame['prediction'] = iris.target[::-1]
    iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
    iris_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])
    iris_target_and_data_drift_profile = Profile(
        sections=[DataDriftProfileSection(), CatTargetDriftProfileSection()])
    iris_target_and_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])

    actual = json.loads(iris_target_and_data_drift_profile.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 3
    assert len(actual['data_drift']['data']) == 6
    assert len(actual['cat_target_drift']['data']) == 5
    assert actual['data_drift']['data'].get('metrics')


def test_regression_performance_profile() -> None:
    # To generate the **Regression Model Performance** report, run:
    iris, iris_frame = _get_iris()
    iris_frame['prediction'] = iris.target[::-1]
    iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
    iris_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])
    regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection()])
    regression_single_model_performance.calculate(iris_frame, None)

    actual = json.loads(regression_single_model_performance.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['regression_performance']['data']) == 5
    assert actual['regression_performance']['data'].get('metrics')


def test_regression_performance_single_frame_profile() -> None:
    # You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
    iris, iris_frame = _get_iris()
    iris_frame['prediction'] = iris.target[::-1]
    iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
    iris_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])
    regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection()])
    regression_single_model_performance.calculate(iris_frame, None)

    actual = json.loads(regression_single_model_performance.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['regression_performance']['data']) == 5
    assert actual['regression_performance']['data'].get('metrics')


def test_classification_performance_profile() -> None:
    # To generate the **Classification Model Performance** report, run:
    iris, iris_frame = _get_iris()
    iris_frame['prediction'] = iris.target[::-1]
    iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
    iris_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])
    classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection()])
    classification_performance_profile.calculate(iris_frame[:100], iris_frame[100:])

    actual = json.loads(classification_performance_profile.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['classification_performance']['data']) == 5
    assert actual['classification_performance']['data'].get('metrics')


def test_classification_performance_single_profile() -> None:
    iris, iris_frame = _get_iris()
    iris_frame['prediction'] = iris.target[::-1]
    iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
    iris_data_drift_profile.calculate(iris_frame[:100], iris_frame[100:])
    classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection()])
    classification_performance_profile.calculate(iris_frame[:100], None)

    actual = json.loads(classification_performance_profile.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['classification_performance']['data']) == 5
    assert actual['classification_performance']['data'].get('metrics')


def test_probabilistic_classification_performance_profile() -> None:
    # For **Probabilistic Classification Model Performance** report, run:
    merged_reference, column_mapping = _get_probabilistic_iris()

    iris_prob_classification_profile = Profile(sections=[ProbClassificationPerformanceProfileSection()])
    iris_prob_classification_profile.calculate(merged_reference, merged_reference, column_mapping)
    # FIXME: this does not work! why?
    # iris_prob_classification_profile.calculate(merged_reference[:100], merged_reference[100:].reset_index(drop=True),
    #                                            column_mapping = column_mapping)

    actual = json.loads(iris_prob_classification_profile.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['probabilistic_classification_performance']['data']) == 5
    assert len(actual['probabilistic_classification_performance']['data']['metrics']) == 2
    assert 'reference' in actual['probabilistic_classification_performance']['data']['metrics']
    assert 'current' in actual['probabilistic_classification_performance']['data']['metrics']


def test_probabilistic_classification_single_performance_profile() -> None:
    # For **Probabilistic Classification Model Performance** report, run:
    merged_reference, column_mapping = _get_probabilistic_iris()

    iris_prob_classification_profile = Profile(sections=[ProbClassificationPerformanceProfileSection()])
    iris_prob_classification_profile.calculate(merged_reference, None, column_mapping)
    # FIXME: this does not work! why?
    # iris_prob_classification_profile.calculate(merged_reference[:100], None,
    #                                            column_mapping = iris_column_mapping)

    actual = json.loads(iris_prob_classification_profile.json())
    # we leave the actual content test to other tests for widgets
    assert 'timestamp' in actual
    assert len(actual) == 2
    assert len(actual['probabilistic_classification_performance']['data']) == 5
    assert len(actual['probabilistic_classification_performance']['data']['metrics']) == 1
    assert 'reference' in actual['probabilistic_classification_performance']['data']['metrics']
