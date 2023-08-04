from evidently2.core.calculation import CalculationResult


class Context:
    def __init__(self):
        self.results = Dict[CalculationKey, CalculationResult]