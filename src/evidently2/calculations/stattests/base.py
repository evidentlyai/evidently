import dataclasses
from typing import Callable, List, Optional, Tuple

from evidently2.calculations.basic import NUnique, Size
from evidently2.core.calculation import Calculation


@dataclasses.dataclass
class StatTestResult:
    drift_score: Calculation
    drifted: Calculation
    actual_threshold: float


StatTestFuncType = Callable[[Calculation, Calculation, str, float], Tuple[Calculation, Calculation]]


@dataclasses.dataclass
class StatTest:
    name: str
    display_name: str
    func: StatTestFuncType
    allowed_feature_types: List[str]
    default_threshold: float = 0.05

    def __call__(
        self, reference_data: Calculation, current_data: Calculation, feature_type: str, threshold: Optional[float]
    ) -> StatTestResult:
        actual_threshold = self.default_threshold if threshold is None else threshold
        p = self.func(reference_data, current_data, feature_type, actual_threshold)
        drift_score, drifted = p
        return StatTestResult(drift_score=drift_score, drifted=drifted, actual_threshold=actual_threshold)

    def __hash__(self):
        # hash by name, so stattests with same name would be the same.
        return hash(self.name)


def _get_default_stattest(reference_data: Calculation, feature_type: str) -> StatTest:
    from evidently2.calculations.stattests.chisquare import chi_stat_test
    z_stat_test = ks_stat_test = jensenshannon_stat_test = chi_stat_test


    # todo: we can make this lazy too
    n_values = NUnique(input_data=reference_data).get_result()
    size = Size(input_data=reference_data).get_result()
    if size <= 1000:
        if n_values <= 5:

            return chi_stat_test if n_values > 2 else z_stat_test
        elif n_values > 5:
            return ks_stat_test
    elif size > 1000:
        if n_values <= 5:
            return jensenshannon_stat_test
        elif n_values > 5:
            from evidently2.calculations.stattests.wasserstein import wasserstein_stat_test
            return wasserstein_stat_test

    raise ValueError(f"Unexpected feature_type {feature_type}")


def get_stattest(reference_data: Calculation, feature_type: str, stattest_func: Optional[str]) -> StatTest:
    if stattest_func is None:
        return _get_default_stattest(reference_data, feature_type)

    ...
    if stattest_func == "wasserstein":
        from evidently2.calculations.stattests.wasserstein import wasserstein_stat_test
        return wasserstein_stat_test