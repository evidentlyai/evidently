from typing import Dict
from typing import Optional
from typing import Tuple

from evidently.calculations.stattests import PossibleStatTestType


def resolve_stattest_threshold(
    feature_name: str,
    feature_type: str,
    stattest: Optional[PossibleStatTestType],
    cat_stattest: Optional[PossibleStatTestType],
    num_stattest: Optional[PossibleStatTestType],
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]],
    stattest_threshold: Optional[float],
    cat_stattest_threshold: Optional[float],
    num_stattest_threshold: Optional[float],
    per_column_stattest_threshold: Optional[Dict[str, float]],
) -> Tuple[Optional[PossibleStatTestType], Optional[float]]:
    return (
        _calculate_stattest(
            feature_name,
            feature_type,
            stattest,
            cat_stattest,
            num_stattest,
            per_column_stattest,
        ),
        _calculate_threshold(
            feature_name,
            feature_type,
            stattest_threshold,
            cat_stattest_threshold,
            num_stattest_threshold,
            per_column_stattest_threshold,
        ),
    )


def _calculate_stattest(
    feature_name: str,
    feature_type: str,
    stattest: Optional[PossibleStatTestType] = None,
    cat_stattest: Optional[PossibleStatTestType] = None,
    num_stattest: Optional[PossibleStatTestType] = None,
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
) -> Optional[PossibleStatTestType]:
    func = None if stattest is None else stattest
    if feature_type == "cat":
        type_func = cat_stattest
    elif feature_type == "num":
        type_func = num_stattest
    else:
        raise ValueError(f"Unexpected feature type {feature_type}.")
    func = func if type_func is None else type_func
    if per_column_stattest is None:
        return func
    return per_column_stattest.get(feature_name, func)


def _calculate_threshold(
    feature_name: str,
    feature_type: str,
    stattest_threshold: Optional[float] = None,
    cat_stattest_threshold: Optional[float] = None,
    num_stattest_threshold: Optional[float] = None,
    per_column_stattest_threshold: Optional[Dict[str, float]] = None,
) -> Optional[float]:
    if per_column_stattest_threshold is not None:
        return per_column_stattest_threshold.get(feature_name)

    if cat_stattest_threshold is not None and feature_type == "cat":
        return cat_stattest_threshold

    if num_stattest_threshold is not None and feature_type == "num":
        return num_stattest_threshold

    if stattest_threshold is not None:
        return stattest_threshold
    return None
