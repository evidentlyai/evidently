from numbers import Number
from typing import List
from typing import Optional
from typing import Union

from evidently.v2.metrics import RegressionPerformanceMetrics
from evidently.v2.tests.base_test import BaseCheckValueTest


class BaseRegressionPerformanceMetricsTest(BaseCheckValueTest):
    metric: RegressionPerformanceMetrics
    feature_name: str

    def __init__(
        self,
        eq: Optional[Number] = None,
        gt: Optional[Number] = None,
        gte: Optional[Number] = None,
        is_in: Optional[List[Union[Number, str, bool]]] = None,
        lt: Optional[Number] = None,
        lte: Optional[Number] = None,
        not_eq: Optional[Number] = None,
        not_in: Optional[List[Union[Number, str, bool]]] = None,
        metric: Optional[RegressionPerformanceMetrics] = None
    ):
        if metric is not None:
            self.metric = metric

        else:
            self.metric = RegressionPerformanceMetrics()

        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)


class TestValueMAE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_abs_error

    def get_description(self, value: Number) -> str:
        return f"MAE value is {value}"


class TestValueMAPE(BaseRegressionPerformanceMetricsTest):
    name = "Test MAPE"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_abs_perc_error

    def get_description(self, value: Number) -> str:
        return f"MAPE value is {value}"


class TestValueMeanError(BaseRegressionPerformanceMetricsTest):
    name = "Test mean error"

    def calculate_value_for_test(self) -> Number:
        return self.metric.get_result().mean_error

    def get_description(self, value: Number) -> str:
        return f"Mean error value is {value}"
