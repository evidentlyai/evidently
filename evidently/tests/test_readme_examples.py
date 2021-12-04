import json

import pandas as pd
from sklearn import datasets
from unittest import TestCase

from evidently.dashboard import Dashboard
from evidently.model_profile import Profile
from evidently.profile_sections import DataDriftProfileSection, CatTargetDriftProfileSection, \
    RegressionPerformanceProfileSection, ClassificationPerformanceProfileSection, \
    ProbClassificationPerformanceProfileSection
from evidently.tabs import DataDriftTab, RegressionPerformanceTab, CatTargetDriftTab, ClassificationPerformanceTab, \
    ProbClassificationPerformanceTab


class TestDashboards(TestCase):
    # TODO(fixme): Actually we would like to test html's output, but because
    #  evidently/nbextension/static/index.js is missing
    #  (and evidently/nbextension/static/index.js.LICENSE.txt is an actual text file)
    #  saving an html report in the test itself fails.
    #  A reasonable fallback is to use the private _json() method. Although, since it is never used anywhere else
    #  it may be considered a bad testing practice to have methods only for testing purposes.
    #  For now we stick to it, however, until something better comes along.

    def setUp(self) -> None:
        iris = datasets.load_iris()
        self.iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
        self.iris_frame['target'] = iris.target

    ###
    # The following are extracted from the README.md file.
    ###
    def test_data_drift_dashboard(self):
        # To generate the **Data Drift** report, run:
        iris_data_drift_report = Dashboard(tabs=[DataDriftTab()])
        iris_data_drift_report.calculate(self.iris_frame[:100], self.iris_frame[100:])
        actual = json.loads(iris_data_drift_report._json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('name' in actual)
        self.assertTrue(len(actual['widgets']) == 1)

    def test_data_drift_categorical_target_drift_dashboard(self):
        # To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
        iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab(), CatTargetDriftTab()])
        iris_data_and_target_drift_report.calculate(self.iris_frame[:100], self.iris_frame[100:])
        actual = json.loads(iris_data_and_target_drift_report._json())
        self.assertTrue('name' in actual)
        self.assertTrue(len(actual['widgets']) == 3)

    def test_regression_performance_dashboard(self):
        # To generate the **Regression Model Performance** report, run:
        # FIXME: when prediction column is not present in the dataset
        #   ValueError: [Widget Regression Model Performance Report.] self.wi is None,
        #   no data available (forget to set it in widget?)
        self.iris_frame['prediction'] = self.iris_frame['target'][::-1]
        regression_model_performance = Dashboard(tabs=[RegressionPerformanceTab()])
        regression_model_performance.calculate(self.iris_frame[:100], self.iris_frame[100:])
        actual = json.loads(regression_model_performance._json())
        self.assertTrue('name' in actual)
        self.assertEqual(len(actual['widgets']), 20)

    def test_regression_performance_single_frame_dashboard(self):
        # You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
        # FIXME: when prediction column is not present in the dataset
        #   ValueError: [Widget Regression Model Performance Report.] self.wi is None,
        #   no data available (forget to set it in widget?)
        self.iris_frame['prediction'] = self.iris_frame['target'][::-1]
        regression_single_model_performance = Dashboard(tabs=[RegressionPerformanceTab()])
        regression_single_model_performance.calculate(self.iris_frame, None)
        actual = json.loads(regression_single_model_performance._json())
        self.assertTrue('name' in actual)
        self.assertEqual(len(actual['widgets']), 12)

    def test_classification_performance_dashboard(self):
        # To generate the **Classification Model Performance** report, run:
        # FIXME: when prediction column is not present in the dataset
        #  ValueError: [Widget Classification Model Performance Report.] self.wi is None,
        #  no data available (forget to set it in widget?)
        self.iris_frame['prediction'] = self.iris_frame['target'][::-1]
        classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab()])
        classification_performance_report.calculate(self.iris_frame[:100], self.iris_frame[100:])

        actual = json.loads(classification_performance_report._json())
        self.assertTrue('name' in actual)
        self.assertEqual(len(actual['widgets']), 10)

    def test_probabilistic_classification_performance_dashboard(self):
        # For **Probabilistic Classification Model Performance** report, run:
        # FIXME: when prediction column is not present in the dataset
        #  ValueError: [Widget Probabilistic Classification Model Performance Report.] self.wi is None,
        #  no data available (forget to set it in widget?)
        self.iris_frame['prediction'] = self.iris_frame['target'][::-1]
        classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab()])
        classification_performance_report.calculate(self.iris_frame[:100], self.iris_frame[100:])

        actual = json.loads(classification_performance_report._json())
        self.assertTrue('name' in actual)
        self.assertEqual(len(actual['widgets']), 10)

    def test_classification_performance_single_frame_dashboard(self):
        # You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
        # FIXME: like above, when prediction column is not present in the dataset
        self.iris_frame['prediction'] = self.iris_frame['target'][::-1]
        classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab()])
        classification_single_model_performance.calculate(self.iris_frame, None)
        actual = json.loads(classification_single_model_performance._json())
        self.assertTrue('name' in actual)
        self.assertEqual(len(actual['widgets']), 9)
        prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab()])
        prob_classification_single_model_performance.calculate(self.iris_frame, None)
        actual = json.loads(prob_classification_single_model_performance._json())
        self.assertTrue('name' in actual)
        self.assertEqual(len(actual['widgets']), 10)


class TestProfiles(TestCase):

    def setUp(self) -> None:
        iris = datasets.load_iris()
        self.iris_frame = pd.DataFrame(iris.data, columns=iris.feature_names)
        self.iris_frame['target'] = iris.target
        self.iris_frame['prediction'] = iris.target[::-1]

    ###
    # The following are extracted from the README.md file.
    ###
    def test_data_drift_profile(self):
        # To generate the **Data Drift** report, run:
        iris_data_drift_profile = Profile(sections=[DataDriftProfileSection()])
        iris_data_drift_profile.calculate(self.iris_frame[:100], self.iris_frame[100:])

        actual = json.loads(iris_data_drift_profile.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertEqual(len(actual), 2)
        self.assertEqual(len(actual['data_drift']['data']), 6)
        self.assertTrue('metrics' in actual['data_drift']['data'])

    def test_data_drift_categorical_target_drift_profile(self):
        # To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
        iris_target_and_data_drift_profile = Profile(sections=[DataDriftProfileSection(), CatTargetDriftProfileSection()])
        iris_target_and_data_drift_profile.calculate(self.iris_frame[:100], self.iris_frame[100:])

        actual = json.loads(iris_target_and_data_drift_profile.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertTrue(len(actual) == 3)
        self.assertEqual(len(actual['data_drift']['data']), 6)
        self.assertEqual(len(actual['cat_target_drift']['data']), 5)
        self.assertTrue(actual['data_drift']['data'].get('metrics'))

    def test_regression_performance_profile(self):
        # To generate the **Regression Model Performance** report, run:
        regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection()])
        regression_single_model_performance.calculate(self.iris_frame, None)

        actual = json.loads(regression_single_model_performance.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertTrue(len(actual) == 2)
        self.assertTrue(len(actual['regression_performance']['data']) == 5)
        self.assertTrue(actual['regression_performance']['data'].get('metrics'))

    def test_regression_performance_single_frame_profile(self):
        # You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
        regression_single_model_performance = Profile(sections=[RegressionPerformanceProfileSection()])
        regression_single_model_performance.calculate(self.iris_frame, None)

        actual = json.loads(regression_single_model_performance.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertTrue(len(actual) == 2)
        self.assertTrue(len(actual['regression_performance']['data']) == 5)
        self.assertTrue(actual['regression_performance']['data'].get('metrics'))

    def test_classification_performance_profile(self):
        # To generate the **Classification Model Performance** report, run:
        # FIXME: come up with good example because iris does not cut it
        #  unless there is a bug (that we will discover by writing tests)
        classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection()])
        classification_performance_profile.calculate(self.iris_frame[:100], self.iris_frame[100:])

        actual = json.loads(classification_performance_profile.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertTrue(len(actual) == 2)
        self.assertTrue(len(actual['classification_performance']['data']) == 5)
        self.assertTrue(actual['classification_performance']['data'].get('metrics'))

    def test_classification_performance_single_profile(self):
        # FIXME: come up with good example because iris does not cut it
        #  unless there is a bug (that we will discover by writing tests)
        classification_performance_profile = Profile(sections=[ClassificationPerformanceProfileSection()])
        classification_performance_profile.calculate(self.iris_frame[:100], None)

        actual = json.loads(classification_performance_profile.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertTrue(len(actual) == 2)
        self.assertTrue(len(actual['classification_performance']['data']) == 5)
        self.assertTrue(actual['classification_performance']['data'].get('metrics'))

    def test_probabilistic_classification_performance_profile(self):
        # For **Probabilistic Classification Model Performance** report, run:
        classification_performance_profile = Profile(sections=[ProbClassificationPerformanceProfileSection()])
        classification_performance_profile.calculate(self.iris_frame[:100], self.iris_frame[100:])
        actual = json.loads(classification_performance_profile.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertEqual(len(actual), 2)
        self.assertEqual(len(actual['classification_performance']['data']), 5)
        self.assertTrue(actual['classification_performance']['data'].get('metrics'))

    def test_probabilistic_classification_single_performance_profile(self):
        # For **Probabilistic Classification Model Performance** report, run:
        classification_performance_profile = Profile(sections=[ProbClassificationPerformanceProfileSection()])
        classification_performance_profile.calculate(self.iris_frame[:100], None)
        actual = json.loads(classification_performance_profile.json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('timestamp' in actual)
        self.assertTrue(len(actual) == 2)
        self.assertTrue(len(actual['classification_performance']['data']) == 5)
        self.assertTrue(actual['classification_performance']['data'].get('metrics'))
