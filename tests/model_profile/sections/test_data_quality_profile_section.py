from datetime import datetime

import pytest

import numpy as np
import pandas as pd

from evidently.analyzers.utils import ColumnMapping
from evidently.model_profile.sections.data_quality_profile_section import DataQualityProfileSection

from .helpers import calculate_section_results
from .helpers import check_profile_section_result_common_part
from .helpers import check_section_without_calculation_results


def test_no_calculation_results() -> None:
    check_section_without_calculation_results(DataQualityProfileSection, "data_quality")


@pytest.mark.parametrize(
    "reference_data, current_data, expected_metrics",
    (
        (
            pd.DataFrame(
                {
                    "target": [1, 2, 3, 4],
                    "numerical_feature": [0.5, 0.0, 4.8, 2.1],
                    "categorical_feature": [1, 1, 0, 1],
                }
            ),
            None,
            {
                "reference": {
                    "categorical_feature": {
                        "count": 4,
                        "feature_type": "cat",
                        "missing_count": 0,
                        "missing_percentage": 0.0,
                        "most_common_value": 1,
                        "most_common_value_percentage": 75,
                        "unique_count": 2,
                        "unique_percentage": 50,
                    },
                    "numerical_feature": {
                        "count": 4,
                        "feature_type": "num",
                        "infinite_count": 0,
                        "infinite_percentage": 0.0,
                        "max": 4.8,
                        "mean": 1.85,
                        "min": 0.0,
                        "missing_count": 0,
                        "missing_percentage": 0.0,
                        "most_common_value": 2.1,
                        "most_common_value_percentage": 25,
                        "percentile_25": 0.38,
                        "percentile_50": 1.3,
                        "percentile_75": 2.78,
                        "std": 2.16,
                        "unique_count": 4,
                        "unique_percentage": 100,
                    },
                    "target": {
                        "count": 4,
                        "feature_type": "num",
                        "infinite_count": 0,
                        "infinite_percentage": 0.0,
                        "max": 4,
                        "mean": 2.5,
                        "min": 1,
                        "missing_count": 0,
                        "missing_percentage": 0.0,
                        "most_common_value": 4,
                        "most_common_value_percentage": 25,
                        "percentile_25": 1.75,
                        "percentile_50": 2.5,
                        "percentile_75": 3.25,
                        "std": 1.29,
                        "unique_count": 4,
                        "unique_percentage": 100,
                    },
                }
            },
        ),
        (
            pd.DataFrame(
                {
                    "target": [np.nan, 2, 3, 3],
                    "numerical_feature": [np.nan, 0.0, 1, 0.5],
                    "categorical_feature": [1, np.nan, 0, 1],
                    "datetime_feature": [
                        datetime(year=2123, month=12, day=12),
                        datetime(year=2123, month=12, day=12),
                        datetime(year=2123, month=12, day=14),
                        np.nan,
                    ],
                }
            ),
            pd.DataFrame(
                {
                    "target": [2, 2, 2, np.nan],
                    "numerical_feature": [0, 0.0, 213123.123123, 0.5],
                    "categorical_feature": [1, 0, 0, 1],
                    "datetime_feature": [
                        datetime(year=2123, month=12, day=12),
                        datetime(year=2123, month=12, day=12),
                        datetime(year=2123, month=12, day=14),
                        datetime(year=2123, month=12, day=14),
                    ],
                }
            ),
            {
                "current": {
                    "categorical_feature": {
                        "count": 4,
                        "feature_type": "cat",
                        "missing_count": 0,
                        "missing_percentage": 0.0,
                        "most_common_value": 1,
                        "most_common_value_percentage": 50,
                        "unique_count": 2,
                        "unique_percentage": 50,
                        "new_in_current_values_count": 0,
                        "unused_in_current_values_count": 1,
                    },
                    "datetime_feature": {
                        "count": 4,
                        "feature_type": "datetime",
                        "max": "2123-12-14 00:00:00",
                        "min": "2123-12-12 00:00:00",
                        "missing_count": 0,
                        "missing_percentage": 0.0,
                        "most_common_value": "2123-12-12 00:00:00",
                        "most_common_value_percentage": 50,
                        "unique_count": 2,
                        "unique_percentage": 50,
                    },
                    "numerical_feature": {
                        "count": 4,
                        "feature_type": "num",
                        "infinite_count": 0,
                        "infinite_percentage": 0.0,
                        "max": 213123.12,
                        "mean": 53280.91,
                        "min": 0.0,
                        "missing_count": 0,
                        "missing_percentage": 0.0,
                        "most_common_value": 0.0,
                        "most_common_value_percentage": 50,
                        "percentile_25": 0.0,
                        "percentile_50": 0.25,
                        "percentile_75": 53281.16,
                        "std": 106561.48,
                        "unique_count": 3,
                        "unique_percentage": 75,
                    },
                    "target": {
                        "count": 3,
                        "feature_type": "num",
                        "infinite_count": 0,
                        "infinite_percentage": 0.0,
                        "max": 2.0,
                        "mean": 2.0,
                        "min": 2.0,
                        "missing_count": 1,
                        "missing_percentage": 25,
                        "most_common_value": 2.0,
                        "most_common_value_percentage": 75,
                        "percentile_25": 2.0,
                        "percentile_50": 2.0,
                        "percentile_75": 2.0,
                        "std": 0.0,
                        "unique_count": 1,
                        "unique_percentage": 25,
                    },
                },
                "reference": {
                    "categorical_feature": {
                        "count": 3,
                        "feature_type": "cat",
                        "missing_count": 1,
                        "missing_percentage": 25,
                        "most_common_value": 1.0,
                        "most_common_value_percentage": 50,
                        "unique_count": 2,
                        "unique_percentage": 50,
                    },
                    "datetime_feature": {
                        "count": 3,
                        "feature_type": "datetime",
                        "max": "2123-12-14 00:00:00",
                        "min": "2123-12-12 00:00:00",
                        "missing_count": 1,
                        "missing_percentage": 25,
                        "most_common_value": "2123-12-12 00:00:00",
                        "most_common_value_percentage": 50,
                        "unique_count": 2,
                        "unique_percentage": 50,
                    },
                    "numerical_feature": {
                        "count": 3,
                        "feature_type": "num",
                        "infinite_count": 0,
                        "infinite_percentage": 0.0,
                        "max": 1.0,
                        "mean": 0.5,
                        "min": 0.0,
                        "missing_count": 1,
                        "missing_percentage": 25,
                        "most_common_value": 0.5,
                        "most_common_value_percentage": 25,
                        "percentile_25": 0.25,
                        "percentile_50": 0.5,
                        "percentile_75": 0.75,
                        "std": 0.5,
                        "unique_count": 3,
                        "unique_percentage": 75,
                    },
                    "target": {
                        "count": 3,
                        "feature_type": "num",
                        "infinite_count": 0,
                        "infinite_percentage": 0.0,
                        "max": 3.0,
                        "mean": 2.67,
                        "min": 2.0,
                        "missing_count": 1,
                        "missing_percentage": 25,
                        "most_common_value": 3.0,
                        "most_common_value_percentage": 50,
                        "percentile_25": 2.5,
                        "percentile_50": 3.0,
                        "percentile_75": 3.0,
                        "std": 0.58,
                        "unique_count": 2,
                        "unique_percentage": 50,
                    },
                },
            },
        ),
    ),
)
def test_data_quality_profile_section_with_calculated_results(
    reference_data: pd.DataFrame, current_data: pd.DataFrame, expected_metrics: dict
):
    data_columns = ColumnMapping(
        numerical_features=["numerical_feature"],
        categorical_features=["categorical_feature"],
        target_names=["drift_target_result"],
        task="regression",
    )
    profile_section_result = calculate_section_results(
        DataQualityProfileSection, reference_data, current_data, data_columns
    )
    check_profile_section_result_common_part(profile_section_result, "data_quality")
    result_data = profile_section_result["data"]

    # check metrics
    assert "metrics" in result_data
    result_metrics: dict = result_data["metrics"]
    assert result_metrics == expected_metrics

@pytest.mark.parametrize(
    "kind, expected_corr_dict",
    [
        (
            "pearson",
            {
                'num_feature_1': {
                    'num_feature_2': 0.831246511091087,
                    'num_feature_3': 0.8703882797784892,
                    'num_feature_4': 1.0,
                    'target': 0.06286946134619315
                },
                'num_feature_2': {
                    'num_feature_1': 0.831246511091087,
                    'num_feature_3': 0.6387140179060972,
                    'num_feature_4': 1.0,
                    'target': -0.1354766133889617
                },
                'num_feature_3': {
                    'num_feature_1': 0.8703882797784892,
                    'num_feature_2': 0.6387140179060972,
                    'num_feature_4': np.nan,
                    'target': 0.1203858530857692
                },
                'num_feature_4': {
                    'num_feature_1': 1.0,
                    'num_feature_2': 1.0,
                    'num_feature_3': np.nan,
                    'target': 1.0
                },
                'target': {
                    'num_feature_1': 0.06286946134619315,
                    'num_feature_2': -0.1354766133889617,
                    'num_feature_3': 0.1203858530857692,
                    'num_feature_4': 1.0}
            }
        ),
        (
            "spearman",
            {
                'num_feature_1': {
                    'num_feature_2': 0.791470623690405,
                    'num_feature_3': 0.8703882797784891,
                    'num_feature_4': 1.0,
                    'target': 0.057788559639706465
                },
                'num_feature_2': {
                    'num_feature_1': 0.791470623690405,
                    'num_feature_3': 0.5991712703227052,
                    'num_feature_4': 1.0,
                    'target': -0.19500675222569575
                },
                'num_feature_3': {
                    'num_feature_1': 0.8703882797784891,
                    'num_feature_2': 0.5991712703227052,
                    'num_feature_4': np.nan,
                    'target': 0.11065666703449763
                },
                'num_feature_4': {
                    'num_feature_1': 1.0,
                    'num_feature_2': 1.0,
                    'num_feature_3': np.nan,
                    'target': 1.0
                },
                'target': {
                    'num_feature_1': 0.057788559639706465,
                    'num_feature_2': -0.19500675222569575,
                    'num_feature_3': 0.11065666703449763,
                    'num_feature_4': 1.0
                }
            }
        ),
        (
            "kendall",
            {
                'num_feature_1': {
                    'num_feature_2': 0.7360699299651778,
                    'num_feature_3': 0.7453559924999299,
                    'num_feature_4': 1.0,
                    'target': 0.0778498944161523
                },
                'num_feature_2': {
                    'num_feature_1': 0.7360699299651778,
                    'num_feature_3': 0.5246313898711125,
                    'num_feature_4': 1.0,
                    'target': -0.13430382733756338
                },
                'num_feature_3': {
                    'num_feature_1': 0.7453559924999299,
                    'num_feature_2': 0.5246313898711125,
                    'num_feature_4': np.nan,
                    'target': 0.1044465935734187
                },
                'num_feature_4': {
                    'num_feature_1': 1.0,
                    'num_feature_2': 1.0,
                    'num_feature_3': np.nan,
                    'target': 1.0
                },
                'target': {
                    'num_feature_1': 0.0778498944161523,
                    'num_feature_2': -0.13430382733756338,
                    'num_feature_3': 0.1044465935734187,
                    'num_feature_4': 1.0
                }
            }
        ),
        (
            'cramer_v',
            {
                'cat_feature_1': {
                    'cat_feature_2': 0.7211102550927979,
                    'cat_feature_3': 0.816496580927726,
                    'cat_feature_4': np.nan
                },
                'cat_feature_2': {
                    'cat_feature_1': 0.7211102550927979,
                    'cat_feature_3': 0.7071067811865476,
                    'cat_feature_4': 1.0
                },
                'cat_feature_3': {
                    'cat_feature_1': 0.816496580927726,
                    'cat_feature_2': 0.7071067811865476,
                    'cat_feature_4': np.nan
                },
                'cat_feature_4': {
                    'cat_feature_1': np.nan,
                    'cat_feature_2': 1.0,
                    'cat_feature_3': np.nan
                }
            }
        )
    ]
)
def test_data_quality_profile_section_correlations(kind: str, expected_corr_dict: dict) -> None:
    df = pd.DataFrame(
        {"num_feature_1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "num_feature_2": [0.1, 0.2, 0.3, 1, 0.5, 0.6, 0.7, 1, 0.9, 1],
        "num_feature_3": [1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
        "num_feature_4": [1, 2, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        "num_feature_constant": [1] * 10,
        "num_feature_empty": [np.nan] * 10,
        "cat_feature_1": ['a', 'a', 'a', 'a', 'a', 'b', 'b', 'b', 'b', 'b'],
        "cat_feature_2": ['c', 'd', 'c', 'f', 'c', 'g', 'c', 'h', 'c', 'j'],
        "cat_feature_3": [1, 1, 1, 1, 2, 2, 2, 2, 2, 2],
        "cat_feature_4": [1, 2, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        "cat_feature_constant": [1] * 10,
        "cat_feature_empty": [np.nan] * 10,
        "datetime_feature": [datetime(year=2123, month=12, day=12)] * 10,
        "target": [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
        }
    )
    column_mapping = ColumnMapping(
        target="target",
        numerical_features=["num_feature_1", "num_feature_2", "num_feature_3", "num_feature_4", "num_feature_constant", 
        "num_feature_empty"],
        categorical_features=["cat_feature_1", "cat_feature_2", "cat_feature_3", "cat_feature_4", 
        "cat_feature_constant", "cat_feature_empty"],
        datetime_features=["datetime_feature"],
        task="regression",
    )
    profile_section_result = calculate_section_results(
        DataQualityProfileSection, df, None, column_mapping
    )
    np.testing.assert_equal(profile_section_result['data']['correlations']['reference'][kind], expected_corr_dict)
