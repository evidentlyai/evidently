from collections import Counter
from pprint import pprint
from typing import Dict
from typing import List
from typing import Optional

from evidently import ColumnMapping
from evidently2.core.calculation import Context
from evidently2.core.calculation import DataType
from evidently2.core.calculation import InputData
from evidently2.core.calculation import Profile
from evidently2.core.calculation import ProfileCalculations
from evidently2.core.calculation import get_calculation_uses
from evidently2.core.calculation import partial_calculations
from evidently2.core.metric import BaseMetric
from evidently2.core.metric import MetricResultCalculation
from evidently.base_metric import MetricResult
from evidently.pydantic_utils import EvidentlyBaseModel
from evidently.utils.data_preprocessing import create_data_definition


class Suite:
    pass


class Report(EvidentlyBaseModel):
    class Config:
        underscore_attrs_are_private = True

    metrics: List[BaseMetric]
    # todo: move to suite, keeping it here for speed
    _ctx: Context = Context()
    _metric_results: Dict[BaseMetric, MetricResult] = {}

    def _prepare_input_data(
        self,
        current_data: Optional[DataType],
        reference_data: Optional[DataType],
        column_mapping: Optional[ColumnMapping],
    ):
        cur_data, ref_data = (current_data, reference_data) if current_data is not None else (reference_data, None)
        data_definition = create_data_definition(ref_data, cur_data, column_mapping or ColumnMapping())
        data = InputData(current_data=current_data, reference_data=reference_data, data_definition=data_definition)
        return data

    def run(
        self, current_data: DataType, reference_data: Optional[DataType], column_mapping: Optional[ColumnMapping] = None
    ):
        data = self._prepare_input_data(current_data, reference_data, column_mapping)
        with Context.use(self._ctx):
            metric_calculations: Dict[BaseMetric, MetricResultCalculation] = {}
            calculation_counter = Counter()
            for m in self.metrics:
                metric_calculations[m] = m.get_calculation(data)
                calculation_counter.update(get_calculation_uses(metric_calculations[m]))

            # pprint(calculation_counter)
            for calc, count in calculation_counter.items():
                if count < 2:
                    calc.disable_cache()
            for m, calc in metric_calculations.items():
                self._metric_results[m] = calc.get_result()

    def create_reference_profile(
        self, reference_data: DataType, column_mapping: Optional[ColumnMapping] = None
    ) -> Profile:
        data = self._prepare_input_data(None, reference_data, column_mapping)
        cache = ProfileCalculations(calculations=[], results=[])
        metric_calculations = []
        with Context.use(self._ctx) as ctx:
            for m in self.metrics:
                result_calculation = m.get_calculation(data)
                metric_calculations.append(result_calculation)
                _, deps = partial_calculations(result_calculation)
                cache = cache.merge(ctx.get_profile_cache(list(deps)))

        return Profile(cache=cache, metrics=self.metrics, metric_calculations=metric_calculations)

    def as_dict(self):
        return {
            "metrics": [
                {"id": metric.__class__.__name__, "result": self._metric_results[metric].dict()}
                for metric in self.metrics
            ]
        }
