from typing import Tuple

import pandas as pd
from scipy.stats import ttest_ind

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest

from scipy.stats import ttest_ind


def _two_sample_t_test(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    """Run the two-sample t test of two samples. Alternative: two-sided
        Args:
            reference_data: reference data
            current_data: current data
            feature_type: feature type
            threshold: level of significance
        Returns:
            p_value: two-tailed p-value
            test_result: whether the drift is detected
        """
    p_value = ttest_ind(reference_data, current_data)[1]
    return p_value, p_value < threshold


two_sample_t_test = StatTest(
    name="two sample t",
    display_name="Two-Sample-T-test p_value",
    func=_two_sample_t_test,
    allowed_feature_types=["num"],
)

register_stattest(two_sample_t_test)
