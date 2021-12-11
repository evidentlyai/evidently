from unittest import TestCase

import numpy as np
from pandas import DataFrame

from evidently import ColumnMapping
from evidently.analyzers.num_target_drift_analyzer import NumTargetDriftAnalyzer
from evidently.options import DataDriftOptions, OptionsProvider


class TestCatTargetDriftAnalyzer(TestCase):

    def setUp(self):
        options_provider: OptionsProvider = OptionsProvider()
        options_provider.add(DataDriftOptions(confidence=0.5))
        self.analyzer = NumTargetDriftAnalyzer()
        self.analyzer.options_provider = options_provider

    def _assert_result_structure(self, result):
        self.assertTrue('utility_columns' in result)
        self.assertTrue('cat_feature_names' in result)
        self.assertTrue('num_feature_names' in result)
        self.assertTrue('target_names' in result)
        self.assertTrue('metrics' in result)

    def test_raises_error_when_target_non_numeric(self):
        df1 = DataFrame({
            'another_target': ['a'] * 10 + ['b'] * 10
        })
        df2 = DataFrame({
            'another_target': ['a'] * 10 + ['b'] * 10
        })

        with self.assertRaises(ValueError):
            self.analyzer.calculate(df1, df2, ColumnMapping(target='another_target'))

    def test_different_target_column_name(self):
        df1 = DataFrame({
            'another_target': range(20)
        })
        df2 = DataFrame({
            'another_target': range(20)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping(target='another_target'))
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'another_target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertEqual(result['metrics']['target_drift'], 1)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'another_target': 1.0})
        self.assertEqual(correlations['current'], {'another_target': 1.0})

    def test_different_prediction_column_name(self):
        df1 = DataFrame({
            'another_prediction': range(20)
        })
        df2 = DataFrame({
            'another_prediction': range(20)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping(prediction='another_prediction'))
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['prediction_name'], 'another_prediction')
        self.assertEqual(result['metrics']['prediction_type'], 'num')
        self.assertEqual(result['metrics']['prediction_drift'], 1)
        correlations = result['metrics']['prediction_correlations']
        self.assertEqual(correlations['reference'], {'another_prediction': 1.0})
        self.assertEqual(correlations['current'], {'another_prediction': 1.0})

    def test_basic_structure_no_drift(self):
        df1 = DataFrame({
            'target': range(20)
        })
        df2 = DataFrame({
            'target': range(20)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertEqual(result['metrics']['target_drift'], 1)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertEqual(correlations['current'], {'target': 1.0})

    def test_basic_structure_no_drift_2(self):
        df1 = DataFrame({
            'target': range(20)
        })
        df2 = DataFrame({
            'target': range(19, -1, -1)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        # because of ks test, target's distribution is the same, hence no drift
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertEqual(result['metrics']['target_drift'], 1)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertEqual(correlations['current'], {'target': 1.0})

    def test_basic_structure_drift(self):
        df1 = DataFrame({
            'target': range(20)
        })
        df2 = DataFrame({
            'target': range(10, 30)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.01229, 3)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertEqual(correlations['current'], {'target': 1.0})

    def test_small_sample_size_1(self):
        df1 = DataFrame({
            'target': [0]
        })
        df2 = DataFrame({
            'target': [10]
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 1, 3)
        correlations = result['metrics']['target_correlations']
        self.assertTrue(np.isnan(correlations['reference']['target']))
        self.assertTrue(np.isnan(correlations['current']['target']))

    def test_small_sample_size_2(self):
        df1 = DataFrame({
            'target': [0]
        })
        df2 = DataFrame({
            'target': range(10)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.3636, 3)
        correlations = result['metrics']['target_correlations']
        self.assertTrue(np.isnan(correlations['reference']['target']))
        self.assertEqual(correlations['current'], {'target': 1.0})

    def test_small_sample_size_3(self):
        df1 = DataFrame({
            'target': range(10)
        })
        df2 = DataFrame({
            'target': [10]
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.1818, 3)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertTrue(np.isnan(correlations['current']['target']))

    def test_computing_of_target_and_prediction(self):
        df1 = DataFrame({
            'target': range(10),
            'prediction': range(1, 11)
        })
        df2 = DataFrame({
            'target': range(5, 15),
            'prediction': range(2, 12)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertEqual(result['metrics']['prediction_name'], 'prediction')
        self.assertEqual(result['metrics']['prediction_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.16782, 3)
        self.assertAlmostEqual(result['metrics']['prediction_drift'], 1, 3)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertEqual(correlations['current'], {'target': 1.0})
        correlations = result['metrics']['prediction_correlations']
        self.assertEqual(correlations['reference'], {'prediction': 1.0})
        self.assertEqual(correlations['current'], {'prediction': 1.0})

    def test_computing_of_only_prediction(self):
        df1 = DataFrame({
            'prediction': range(1, 11)
        })
        df2 = DataFrame({
            'prediction': range(3, 13)
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['prediction_name'], 'prediction')
        self.assertEqual(result['metrics']['prediction_type'], 'num')
        self.assertAlmostEqual(result['metrics']['prediction_drift'], 0.99445, 3)
        correlations = result['metrics']['prediction_correlations']
        self.assertEqual(correlations['reference'], {'prediction': 1.0})
        self.assertEqual(correlations['current'], {'prediction': 1.0})

    def test_computing_with_nans(self):
        df1 = DataFrame({
            'target': list(range(20)) + [np.nan, np.inf]
        })
        df2 = DataFrame({
            'target': [np.nan, np.inf] + list(range(10, 30))
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.02004, 3)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertEqual(correlations['current'], {'target': 1.0})

    def test_computing_uses_a_custom_function(self):
        df1 = DataFrame({
            'target': range(20)
        })
        df2 = DataFrame({
            'target': range(10)
        })

        options = DataDriftOptions(num_target_stattest_func=lambda x, y: np.pi)
        self.analyzer.options_provider.add(options)
        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], np.pi, 4)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'target': 1.0})
        self.assertEqual(correlations['current'], {'target': 1.0})

    def test_computing_of_correlations_between_columns(self):
        df1 = DataFrame({
            'target': range(20),
            'num_1': range(0, -20, -1),
            'num_2': range(10, -10, -1),
            'cat_1': ['a'] * 20
        })
        df2 = DataFrame({
            'target': range(10),
            'num_1': range(0, -10, -1),
            'num_2': range(10, 0, -1),
            'cat_1': ['b'] * 10
        })

        result = self.analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'target')
        self.assertEqual(result['metrics']['target_type'], 'num')
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.06228, 4)
        correlations = result['metrics']['target_correlations']
        self.assertEqual(correlations['reference'], {'num_1': -1.0, 'num_2': -1.0, 'target': 1.0})
        self.assertEqual(correlations['current'], {'num_1': -1.0, 'num_2': -1.0, 'target': 1.0})

    def test_computing_of_correlations_between_columns_fails_for_second_data_when_columns_missing(self):
        df1 = DataFrame({
            'target': range(20),
            'num_1': range(0, -20, -1),
            'num_2': range(10, -10, -1),
            'cat_1': ['a'] * 20
        })
        df2 = DataFrame({
            'target': range(10)
        })

        self.analyzer.calculate(df1, df2, ColumnMapping())

    def test_computing_of_correlations_between_columns_fails_for_second_data_when_columns_missing_2(self):
        df1 = DataFrame({
            'prediction': range(20),
            'num_1': range(0, -20, -1),
            'num_2': range(10, -10, -1),
            'cat_1': ['a'] * 20
        })
        df2 = DataFrame({
            'prediction': range(10),
            'num_1': range(0, -10, -1),
        })

        self.analyzer.calculate(df1, df2, ColumnMapping())
