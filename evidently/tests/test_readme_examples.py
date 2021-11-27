import json
from tempfile import TemporaryDirectory
from unittest.mock import patch, MagicMock

import pandas as pd
from sklearn import datasets
from unittest import TestCase

from evidently.dashboard import Dashboard
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
        iris_data_drift_report = Dashboard(tabs=[DataDriftTab])
        iris_data_drift_report.calculate(self.iris_frame[:100], self.iris_frame[100:])
        actual = json.loads(iris_data_drift_report._json())
        # we leave the actual content test to other tests for widgets
        self.assertTrue('name' in actual)
        self.assertTrue(len(actual['widgets']) == 1)

    def test_data_drift_categorical_target_drift_dashboard(self):
        # To generate the **Data Drift** and the **Categorical Target Drift** reports, run:
        iris_data_and_target_drift_report = Dashboard(tabs=[DataDriftTab, CatTargetDriftTab])
        iris_data_and_target_drift_report.calculate(self.iris_frame[:100], self.iris_frame[100:])
        actual = json.loads(iris_data_and_target_drift_report._json())
        self.assertTrue('name' in actual)
        self.assertTrue(len(actual['widgets']) == 3)

    def test_regression_performance_dashboard(self):
        # To generate the **Regression Model Performance** report, run:
        regression_model_performance = Dashboard(tabs=[RegressionPerformanceTab])
        regression_model_performance.calculate(self.iris_frame[:100], self.iris_frame[100:])
        # FIXME:
        #   ValueError: [Widget Regression Model Performance Report.] self.wi is None,
        #   no data available (forget to set it in widget?)
        # actual = json.loads(regression_model_performance._json())
        # self.assertTrue('name' in actual)

    def test_regression_performance_single_frame_dashboard(self):
        # You can also generate a **Regression Model Performance** for a single `DataFrame`. In this case, run:
        regression_single_model_performance = Dashboard(tabs=[RegressionPerformanceTab])
        regression_single_model_performance.calculate(self.iris_frame[:100], None)
        # FIXME:
        #   ValueError: [Widget Regression Model Performance Report.] self.wi is None,
        #   no data available (forget to set it in widget?)
        # actual = json.loads(regression_single_model_performance._json())
        # self.assertTrue('name' in actual)


    def test_classification_performance_dashboard(self):
        # To generate the **Classification Model Performance** report, run:
        classification_performance_report = Dashboard(tabs=[ClassificationPerformanceTab])
        classification_performance_report.calculate(self.iris_frame[:100], self.iris_frame[100:])
        # FIXME:
        #  ValueError: [Widget Classification Model Performance Report.] self.wi is None,
        #  no data available (forget to set it in widget?)
        # actual = json.loads(classification_performance_report._json())
        # self.assertTrue('name' in actual)

    def test_probabilistic_classification_performance_dashboard(self):
        # For **Probabilistic Classification Model Performance** report, run:
        classification_performance_report = Dashboard(tabs=[ProbClassificationPerformanceTab])
        classification_performance_report.calculate(self.iris_frame[:100], self.iris_frame[100:])
        # FIXME:
        #  ValueError: [Widget Probabilistic Classification Model Performance Report.] self.wi is None,
        #  no data available (forget to set it in widget?)
        # actual = json.loads(classification_performance_report._json())
        # self.assertTrue('name' in actual)

    def test_classification_performance_single_frame_dashboard(self):
        # You can also generate either of the **Classification** reports for a single `DataFrame`. In this case, run:
        # FIXME:
        #   unless something change with the upper tests, this will fail anyways.

        classification_single_model_performance = Dashboard(tabs=[ClassificationPerformanceTab])
        classification_single_model_performance.calculate(self.iris_frame[:100], None)
        # with open('data/dashboards/classification_single_model_performance_test_data.json', 'w+') as f:
        #     json.dump(json.loads(classification_single_model_performance._json('test')), f, indent=2)
        prob_classification_single_model_performance = Dashboard(tabs=[ProbClassificationPerformanceTab])
        prob_classification_single_model_performance.calculate(self.iris_frame[:100], None)
        # with open('data/dashboards/classification_single_model_performance_test_data.json', 'w+') as f:
        #     json.dump(json.loads(classification_single_model_performance._json('test')), f, indent=2)
