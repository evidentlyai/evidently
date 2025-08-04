import pandas as pd
from scipy.stats import epps_singleton_2samp
from evidently.calculations.stattests.registry import StatTest, register_stattest


def _epps_singleton_stat_test(reference_data: pd.Series, current_data: pd.Series,
                               feature_type: str, threshold: float):
    reference_data = reference_data.dropna()
    current_data = current_data.dropna()

    stat, p_value = epps_singleton_2samp(reference_data, current_data)
    return float(p_value), p_value < threshold


epps_singleton_test = StatTest(
    name="epps_singleton",
    display_name="Epps‑Singleton Test",
    func=_epps_singleton_stat_test,
    allowed_feature_types=["num"],
)

register_stattest(epps_singleton_test)
