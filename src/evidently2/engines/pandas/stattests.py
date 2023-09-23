from scipy.stats import chisquare, wasserstein_distance

from evidently2.calculations.stattests.chisquare import ChiSquare
from evidently2.calculations.stattests.wasserstein import Wasserstein
from evidently2.core.calculation import Calc
from evidently2.engines.pandas.basic import PandasCalculation


class PandasChiSquare(PandasCalculation[ChiSquare]):
    calculation_type = ChiSquare

    @classmethod
    def calculate(cls, self: ChiSquare, data):
        exp = self.exp.get_result()
        keys = set(data.keys()) | set(exp.keys())
        return chisquare([data.get(k, 0) for k in keys], [exp.get(k, 0) for k in keys])[1]


class PandasWasserstein(PandasCalculation[Wasserstein]):
    calculation_type = Wasserstein

    @classmethod
    def calculate(cls, self: Wasserstein, data):
        return wasserstein_distance(self.input_data.get_result(), self.current.get_result())
