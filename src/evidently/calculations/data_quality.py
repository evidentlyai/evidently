"""Methods for overall dataset quality calculations - rows count, a specific values count, etc."""
from typing import Optional, Dict, Union

import pandas as pd
from dataclasses import dataclass, fields


def get_rows_count(dataset: pd.DataFrame):
    """Count quantity of rows in  a dataset"""
    return dataset.shape[0]


@dataclass
class FeatureQualityStats:
    """Class for all features data quality metrics store.

    A type of the feature is stored in `feature_type` field.
    Concrete stat kit depends on the feature type. Is a metric is not applicable - leave `None` value for it.

    Metrics for all feature types:
        - feature type - cat for category, num for numeric, datetime for datetime features
        - count - quantity of a meaningful values (do not take into account NaN values)
        - missing_count - quantity of meaningless (NaN) values
        - missing_percentage - the percentage of the missed values
        - unique_count - quantity of unique values
        - unique_percentage - the percentage of the unique values
        - max - maximum value (not applicable for category features)
        - min - minimum value (not applicable for category features)
        - most_common_value - the most common value in the feature values
        - most_common_value_percentage - the percentage of the most common value
        - most_common_not_null_value - if `most_common_value` equals NaN - the next most common value. Otherwise - None
        - most_common_not_null_value_percentage - the percentage of `most_common_not_null_value` if it is defined.
            If `most_common_not_null_value` is not defined, equals None too.

    Metrics for numeric features only:
        - infinite_count - quantity infinite values (for numeric features only)
        - infinite_percentage - the percentage of infinite values (for numeric features only)
        - percentile_25 - 25% percentile for meaningful values
        - percentile_50 - 50% percentile for meaningful values
        - percentile_75 - 75% percentile for meaningful values
        - mean - the sum of the meaningful values divided by the number of the meaningful values
        - std - standard deviation of the values

    Metrics for category features only:
        - new_in_current_values_count - quantity of new values in the current dataset after the reference
            Defined for reference dataset only.
        - new_in_current_values_count - quantity of values in the reference dataset that not presented in the current
            Defined for reference dataset only.
    """

    # feature type - cat for category, num for numeric, datetime for datetime features
    feature_type: str
    # quantity on
    count: int = 0
    infinite_count: Optional[int] = None
    infinite_percentage: Optional[float] = None
    missing_count: Optional[int] = None
    missing_percentage: Optional[float] = None
    unique_count: Optional[int] = None
    unique_percentage: Optional[float] = None
    percentile_25: Optional[float] = None
    percentile_50: Optional[float] = None
    percentile_75: Optional[float] = None
    max: Optional[Union[int, float, bool, str]] = None
    min: Optional[Union[int, float, bool, str]] = None
    mean: Optional[float] = None
    most_common_value: Optional[Union[int, float, bool, str]] = None
    most_common_value_percentage: Optional[float] = None
    std: Optional[float] = None
    most_common_not_null_value: Optional[Union[int, float, bool, str]] = None
    most_common_not_null_value_percentage: Optional[float] = None
    new_in_current_values_count: Optional[int] = None
    unused_in_current_values_count: Optional[int] = None

    def is_datetime(self):
        """Checks that the object store stats for a datetime feature"""
        return self.feature_type == "datetime"

    def is_numeric(self):
        """Checks that the object store stats for a numeric feature"""
        return self.feature_type == "num"

    def is_category(self):
        """Checks that the object store stats for a category feature"""
        return self.feature_type == "cat"

    def as_dict(self):
        return {field.name: getattr(self, field.name) for field in fields(FeatureQualityStats)}

    def __eq__(self, other):
        for field in fields(FeatureQualityStats):
            other_field_value = getattr(other, field.name)
            self_field_value = getattr(self, field.name)

            if pd.isnull(other_field_value) and pd.isnull(self_field_value):
                continue

            if not other_field_value == self_field_value:
                return False

        return True


@dataclass
class DataQualityStats:
    num_features_stats: Optional[Dict[str, FeatureQualityStats]] = None
    cat_features_stats: Optional[Dict[str, FeatureQualityStats]] = None
    datetime_features_stats: Optional[Dict[str, FeatureQualityStats]] = None
    target_stats: Optional[Dict[str, FeatureQualityStats]] = None
    prediction_stats: Optional[Dict[str, FeatureQualityStats]] = None

    def get_all_features(self) -> Dict[str, FeatureQualityStats]:
        result = {}

        for features in (
            self.target_stats,
            self.prediction_stats,
            self.datetime_features_stats,
            self.cat_features_stats,
            self.num_features_stats,
        ):
            if features is not None:
                result.update(features)

        return result

    def __getitem__(self, item) -> FeatureQualityStats:
        for features in (
            self.target_stats,
            self.prediction_stats,
            self.datetime_features_stats,
            self.cat_features_stats,
            self.num_features_stats,
        ):
            if features is not None and item in features:
                return features[item]

        raise KeyError(item)
