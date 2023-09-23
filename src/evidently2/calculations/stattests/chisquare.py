from typing import Tuple

from evidently2.calculations.basic import Div, LessThen, MultDict, Size, ValueCounts
from evidently2.calculations.stattests.base import StatTest
from evidently2.core.calculation import Calculation, Constant
from scipy.stats import chisquare

class ChiSquare(Calculation):
    exp: Calculation


def _chi_stat_test(
    reference_data: Calculation, current_data: Calculation, feature_type: str, threshold: float
) -> Tuple[Calculation, Calculation]:
    # keys = get_unique_not_nan_values_list_from_series(current_data=current_data, reference_data=reference_data)
    # k_norm = current_data.shape[0] / reference_data.shape[0]
    k_norm = Div(input_data=Size(input_data=current_data), second=Size(input_data=reference_data))
    ref_feature_dict = ValueCounts(input_data=reference_data)
    current_feature_dict = ValueCounts(input_data=current_data)
    f_exp = MultDict(input_data=ref_feature_dict, mul=k_norm)
    p_value = ChiSquare(input_data=current_feature_dict, exp=f_exp)
    # return p_value, p_value < threshold
    return p_value, LessThen(input_data=p_value, second=Constant(value=threshold))


chi_stat_test = StatTest(
    name="chisquare", display_name="chi-square p_value", func=_chi_stat_test, allowed_feature_types=["cat"]
)