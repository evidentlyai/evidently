from numbers import Number
from typing import List
from typing import Optional
from typing import Union

from evidently.v2.metrics.data_integrity_metrics import DataIntegrityMetrics

from .base_test import BaseCheckValueTest


class BaseIntegrityValueTest(BaseCheckValueTest):
    data_integrity_metric: DataIntegrityMetrics

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
        data_integrity_metric: Optional[DataIntegrityMetrics] = None
    ):
        super().__init__(eq=eq, gt=gt, gte=gte, is_in=is_in, lt=lt, lte=lte, not_eq=not_eq, not_in=not_in)

        if data_integrity_metric is None:
            self.data_integrity_metric = DataIntegrityMetrics()

        else:
            self.data_integrity_metric = data_integrity_metric


class TestNumberOfColumns(BaseIntegrityValueTest):
    name = "Test Number of Columns"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_columns
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of columns is {value}"


class TestNumberOfRows(BaseIntegrityValueTest):
    name = "Test Number of Rows"

    def calculate_value_for_test(self) -> Number:
        self.value = self.data_integrity_metric.get_result().number_of_rows
        return self.value

    def get_description(self, value: Number) -> str:
        return f"Number of rows is {value}"
