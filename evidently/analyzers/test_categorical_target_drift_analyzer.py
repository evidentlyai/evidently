from unittest import TestCase
from pandas import DataFrame

from evidently import ColumnMapping
from evidently.analyzers.cat_target_drift_analyzer import CatTargetDriftAnalyzer


class TestCatTargetDriftAnalyzer(TestCase):

    def _assert_result_structure(self, result):
        self.assertTrue('utility_columns' in result)
        self.assertTrue('cat_feature_names' in result)
        self.assertTrue('num_feature_names' in result)
        self.assertTrue('target_names' in result)
        self.assertTrue('metrics' in result)
        self.assertEqual(result['metrics']['target_type'], 'cat')

    def test_different_target_column_name(self):
        df1 = DataFrame({
            'another_target': ['a'] * 10 + ['b'] * 10
        })
        df2 = DataFrame({
            'another_target': ['a'] * 10 + ['b'] * 10
        })
        analyzer = CatTargetDriftAnalyzer()

        result = analyzer.calculate(df1, df2, ColumnMapping(target='another_target'))
        self._assert_result_structure(result)
        self.assertEqual(result['metrics']['target_name'], 'another_target')

    def test_basic_structure_no_drift(self):
        df1 = DataFrame({
            'target': ['a'] * 10 + ['b'] * 10
        })
        df2 = DataFrame({
            'target': ['a'] * 10 + ['b'] * 10
        })
        analyzer = CatTargetDriftAnalyzer()

        result = analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertAlmostEqual(result['metrics']['target_drift'], 1)
        self.assertEqual(result['metrics']['target_name'], 'target')

    def test_small_sample_size(self):
        df1 = DataFrame({
            'target': ['a', 'b']
        })
        df2 = DataFrame({
            'target': ['b']
        })
        analyzer = CatTargetDriftAnalyzer()

        result = analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.386, 2)
        self.assertEqual(result['metrics']['target_name'], 'target')

    def test_different_labels_1(self):
        df1 = DataFrame({
            'target': ['a', 'b']
        })
        df2 = DataFrame({
            'target': ['c']
        })
        analyzer = CatTargetDriftAnalyzer()

        # FIXME: RuntimeWarning: divide by zero encountered in true_divide
        result = analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertAlmostEqual(result['metrics']['target_drift'], 0., 2)
        self.assertEqual(result['metrics']['target_name'], 'target')

    def test_different_labels_2(self):
        df1 = DataFrame({
            'target': ['c'] * 10
        })
        df2 = DataFrame({
            'target': ['a', 'b'] * 10
        })
        analyzer = CatTargetDriftAnalyzer()

        # FIXME: RuntimeWarning: divide by zero encountered in true_divide
        result = analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertAlmostEqual(result['metrics']['target_drift'], 0., 2)
        self.assertEqual(result['metrics']['target_name'], 'target')

    def test_computation_of_categories_as_numbers(self):
        df1 = DataFrame({
            'target': [0, 1] * 10
        })
        df2 = DataFrame({
            'target': [1] * 5
        })
        analyzer = CatTargetDriftAnalyzer()

        # FIXME: RuntimeWarning: divide by zero encountered in true_divide
        result = analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertAlmostEqual(result['metrics']['target_drift'], 0.04122, 3)
        self.assertEqual(result['metrics']['target_name'], 'target')
        print(result)

    def test_computing_of_target_and_prediction(self):
        df1 = DataFrame({
            'target': ['a', 'b'] * 10,
            'prediction': ['b', 'c'] * 10
        })
        df2 = DataFrame({
            'target': ['b', 'c'] * 5,
            'prediction': ['a', 'b'] * 5
        })
        analyzer = CatTargetDriftAnalyzer()
        result = analyzer.calculate(df1, df2, ColumnMapping())
        self._assert_result_structure(result)
        self.assertAlmostEqual(result['metrics']['target_drift'], 0., 3)
        self.assertEqual(result['metrics']['prediction_name'], 'prediction')
        self.assertEqual(result['metrics']['prediction_type'], 'cat')
