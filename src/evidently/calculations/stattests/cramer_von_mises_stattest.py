from typing import Tuple

import pandas as pd
from scipy import stats

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest


def _cramer_von_mises(
    reference_data: pd.Series,
    current_data: pd.Series,
    feature_type: str,
    threshold: float,
) -> Tuple[float, bool]:
    """Run the two-sample Cramer-Von-mises test of two samples.
    Args:
        reference_data: reference data
        current_data: current data
        feature_type: feature type
        threshold: level of significance
    Returns:
        p_value: p-value
        test_result: whether the drift is detected
    """
    res = stats.cramervonmises_2samp(reference_data, current_data)
    return res.pvalue, res.pvalue <= threshold


cramer_von_mises = StatTest(
    name="cramer_von_mises",
    display_name="cramer_von_mises",
    func=_cramer_von_mises,
    allowed_feature_types=["num"],
)

register_stattest(cramer_von_mises)
