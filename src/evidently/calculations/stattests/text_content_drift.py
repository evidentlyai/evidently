from typing import Tuple

import pandas as pd

from evidently.calculations.stattests.registry import StatTest
from evidently.calculations.stattests.registry import register_stattest
from evidently.utils.data_drift_utils import calculate_text_drift_score


def _text_content_drift(
    reference_data: pd.Series, current_data: pd.Series, feature_type: str, threshold: float
) -> Tuple[float, bool]:
    return calculate_text_drift_score(reference_data, current_data, p_value=threshold)


text_content_drift_stat_test = StatTest(
    name="text_content_drift",
    display_name="Text content drift",
    func=_text_content_drift,
    allowed_feature_types=["text"],
    default_threshold=0.05,
)

register_stattest(text_content_drift_stat_test)
