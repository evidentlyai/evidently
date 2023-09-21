from abc import ABC
from typing import ClassVar

import numpy as np

from evidently2.calculations.basic import CleanColumn
from evidently2.calculations.basic import CreateSet
from evidently2.calculations.basic import Div
from evidently2.calculations.basic import DropInf
from evidently2.calculations.basic import DropNA
from evidently2.calculations.basic import Histogram
from evidently2.calculations.basic import IsFinite
from evidently2.calculations.basic import LessThen
from evidently2.calculations.basic import Mask
from evidently2.calculations.basic import Mul
from evidently2.calculations.basic import MultDict
from evidently2.calculations.basic import NUnique
from evidently2.calculations.basic import Size
from evidently2.calculations.basic import UnionList
from evidently2.calculations.basic import Unique
from evidently2.calculations.basic import ValueCounts
from evidently2.core.calculation import CalculationEngine
from evidently2.core.calculation import CalculationImplementation
from evidently2.core.calculation import InputColumnData
from evidently2.core.spark import is_spark_data
from evidently.metric_results import Distribution


class PandasEngine(CalculationEngine):

    @classmethod
    def can_use_engine(cls, data) -> bool:
        # fixme
        return not is_spark_data(data)


class PandasCalculation(CalculationImplementation, ABC):
    engine: ClassVar = PandasEngine


class PandasInputColumnData(PandasCalculation[InputColumnData]):
    calculation_type: ClassVar = InputColumnData

    @classmethod
    def calculate(cls, self: InputColumnData, data):
        return data[self.column]


class PandasDropInf(PandasCalculation[DropInf]):
    calculation_type = DropInf

    @classmethod
    def calculate(cls, self: DropInf, data):
        return data[np.isfinite(data)]


class PandasCleanColumn(PandasCalculation[CleanColumn]):
    calculation_type = CleanColumn

    @classmethod
    def calculate(cls, calculation: CleanColumn, data):
        return data.replace([-np.inf, np.inf], np.nan).dropna()

    # @property
    # def empty(self):
    #     # todo: can we do this lazy?
    #     try:
    #         result = self.get_result()
    #         if is_spark_data(result):
    #             return result.rdd.isEmpty()
    #         return result.empty
    #     except NoInputError:
    #         return False


class PandasDropNA(PandasCalculation[DropNA]):
    calculation_type = DropNA

    @classmethod
    def calculate(cls, self: DropNA, data):
        return data.dropna()


class PandasUnique(PandasCalculation[Unique]):
    calculation_type = Unique

    @classmethod
    def calculate(cls, self: Unique, data):
        return data.unique()


class PandasCreateSet(PandasCalculation[CreateSet]):
    calculation_type = CreateSet

    @classmethod
    def calculate(cls, self: CreateSet, data):
        return set(data)


class PandasUnionList(PandasCalculation[UnionList]):
    calculation_type = UnionList

    @classmethod
    def calculate(cls, self: UnionList, data):
        return list(data | self.second.get_result())


class PandasSize(PandasCalculation[Size]):
    calculation_type = Size

    @classmethod
    def calculate(cls, self: Size, data):
        return data.shape[0]


class PandasDiv(PandasCalculation[Div]):
    calculation_type = Div

    @classmethod
    def calculate(cls, self: Div, data):
        return data / self.second.get_result()


class PandasValueCounts(PandasCalculation[ValueCounts]):
    calculation_type = ValueCounts

    @classmethod
    def calculate(cls, self: ValueCounts, data):
        return data.value_counts()


class PandasMul(PandasCalculation[Mul]):
    calculation_type = Mul

    @classmethod
    def calculate(cls, self: Mul, data):
        return data * self.second.get_result()


class PandasMultDict(PandasCalculation[MultDict]):
    calculation_type = MultDict

    @classmethod
    def calculate(cls, self: MultDict, data):
        m = self.mul.get_result()
        return {k: v * m for k, v in data.items()}


class PandasLessThen(PandasCalculation[LessThen]):
    calculation_type = LessThen

    @classmethod
    def calculate(cls, self: LessThen, data):
        return data < self.second.get_result()


class PandasNUnique(PandasCalculation[NUnique]):
    calculation_type = NUnique

    @classmethod
    def calculate(cls, self: NUnique, data):
        return data.nunique()


class PandasHistogram(PandasCalculation[Histogram]):
    calculation_type = Histogram

    @classmethod
    def calculate(cls, self: Histogram, data):
        y, x = [
            t.tolist()
            for t in np.histogram(
                data,
                bins=self.bins,
                density=self.density,
            )
        ]
        return Distribution(x=x, y=y)


class PandasMask(PandasCalculation[Mask]):
    calculation_type = Mask

    @classmethod
    def calculate(cls, self: Mask, data):
        return data[self.mask.get_result()]


class PandasIsFinite(PandasCalculation[IsFinite]):
    calculation_type = IsFinite

    @classmethod
    def calculate(cls, self: IsFinite, data):
        return np.isfinite(data)
