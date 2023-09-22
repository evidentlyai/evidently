import pandas as pd

from evidently2.core.calculation import Calculation
from evidently2.core.calculation import NoInputError
from evidently2.core.calculation import _CalculationBase
from evidently.metric_results import Distribution


class DropInf(Calculation):
    pass


class CleanColumn(Calculation[pd.Series, pd.Series]):
    pass


class DropNA(Calculation):
    pass


class Unique(Calculation):
    pass


class CreateSet(Calculation):
    pass


class UnionList(Calculation):
    second: Calculation


class Size(Calculation):
    pass


class Div(Calculation):
    second: Calculation


class ValueCounts(Calculation):
    pass


class Mul(Calculation):
    second: Calculation


class MultDict(Calculation):
    mul: Calculation


class LessThen(Calculation):
    second: _CalculationBase


class NUnique(Calculation):
    pass


class Histogram(Calculation[pd.Series, Distribution]):
    bins: int
    density: bool

    def __init__(self, input_data: _CalculationBase, bins: int, density: bool):
        super().__init__(input_data=input_data, bins=bins, density=density)


class Mask(Calculation[pd.Series, pd.Series]):
    mask: Calculation


class IsFinite(Calculation[pd.Series, pd.Series]):
    def __init__(self, input_data: _CalculationBase):
        super().__init__(input_data=input_data)


class IsEmpty(Calculation):
    def __bool__(self):
        try:
            return self.get_result()
        except NoInputError:
            return False
