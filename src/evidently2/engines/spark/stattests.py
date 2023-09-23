from scipy.stats import chisquare

from evidently2.calculations.stattests.chisquare import ChiSquare
from evidently2.engines.spark.basic import SparkCalculation


# class SparkChiSquare(SparkCalculation[ChiSquare]):
#     calculation_type = ChiSquare
#
#     @classmethod
#     def calculate(cls, self: ChiSquare, data):
#         exp = self.exp.get_result()
#         keys = set(data.keys()) | set(exp.keys())
#         return chisquare([data.get(k, 0) for k in keys], [exp.get(k, 0) for k in keys])[1]
