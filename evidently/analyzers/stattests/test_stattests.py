from unittest import TestCase
from evidently.analyzers.stattests import chisquare_stattest
from pandas import DataFrame


class TestChiSquare(TestCase):

    def test_simple_calculation(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5
        })
        self.assertAlmostEqual(chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name']), 1.)

    def test_simple_calculation_2(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 8 + ['b'] * 3
        })
        result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
        self.assertAlmostEqual(result, 0.11690, 3)

    def test_simple_calculation_3(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
        })
        self.assertAlmostEqual(chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name']), 1.)

    def test_simple_calculation_4(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 8 + ['b'] * 3 + ['c'] * 5
        })
        result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
        self.assertAlmostEqual(result, 0.29253, 3)

    def test_current_data_contains_one_class_less(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 8 + ['b'] * 3
        })
        result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
        self.assertAlmostEqual(result, 0.)

    def test_reference_data_contains_one_class_less(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 8 + ['b'] * 3 + ['c'] * 5
        })
        result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
        self.assertAlmostEqual(result, 0.024, 3)

    def test_data_with_single_class(self):
        reference = DataFrame({
            'column_name': ['a'] * 5 + ['b'] * 5
        })
        current = DataFrame({
            'column_name': ['a'] * 8 + ['b'] * 3 + ['c'] * 5
        })
        result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
        self.assertAlmostEqual(result, 0.024, 3)
