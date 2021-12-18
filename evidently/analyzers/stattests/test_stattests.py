from pandas import DataFrame
from pytest import approx

from evidently.analyzers.stattests import chisquare_stattest


def test_simple_calculation() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5
    })
    assert chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name']) == 1.


def test_simple_calculation_2() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 8 + ['b'] * 3
    })
    result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
    assert result == approx(0.11690, abs=1e-5)


def test_simple_calculation_3() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
    })
    assert chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name']) == 1.


def test_simple_calculation_4() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 8 + ['b'] * 3 + ['c'] * 5
    })
    result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
    assert result == approx(0.29253, abs=1e-5)


def test_current_data_contains_one_class_less() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5 + ['c'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 8 + ['b'] * 3
    })
    result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
    assert result == 0.


def test_reference_data_contains_one_class_less() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 8 + ['b'] * 3 + ['c'] * 5
    })
    result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
    assert result == approx(0.024, abs=1e-3)


def test_data_with_single_class() -> None:
    reference = DataFrame({
        'column_name': ['a'] * 5 + ['b'] * 5
    })
    current = DataFrame({
        'column_name': ['a'] * 8 + ['b'] * 3 + ['c'] * 5
    })
    result = chisquare_stattest.chi_stat_test(reference['column_name'], current['column_name'])
    assert result == approx(0.024, abs=1e-3)
