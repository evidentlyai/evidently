from unittest import TestCase
from evidently.analyzers.stattests import chisquare_stattest
from pandas import DataFrame


class TestChiSquare(TestCase):

    def test_simple_calculation(self):
        df1 = DataFrame({
            'a': ['a'] * 5 + ['b'] * 5
        })
        df2 = DataFrame({
            'a': ['a'] * 5 + ['b'] * 5
        })
        self.assertEqual(chisquare_stattest.chi_stat_test(df1['a'], df2['a']), 1.)
