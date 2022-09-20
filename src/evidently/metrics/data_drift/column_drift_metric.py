from typing import Dict
from typing import List
from typing import Optional

import dataclasses
import pandas as pd

from evidently.calculations.data_drift import calculate_data_drift
from evidently.calculations.stattests import PossibleStatTestType
from evidently.metrics.base_metric import InputData
from evidently.metrics.base_metric import Metric
from evidently.metrics.utils import make_hist_for_cat_plot
from evidently.metrics.utils import make_hist_for_num_plot
from evidently.model.widget import WidgetType
from evidently.model.widget import BaseWidgetInfo
from evidently.options import DataDriftOptions
from evidently.options.data_drift import DEFAULT_NBINSX
from evidently.renderers.base_renderer import MetricHtmlInfo
from evidently.renderers.base_renderer import MetricRenderer
from evidently.renderers.base_renderer import default_renderer
from evidently.utils.types import Numeric


@dataclasses.dataclass
class ColumnDriftMetricResults:
    column_name: str
    column_type: str
    stattest_name: str
    threshold: Optional[float]
    drift_value: Numeric
    drift_detected: bool
    distr_for_plots: Dict[str, pd.DataFrame]


class ColumnDriftMetric(Metric[ColumnDriftMetricResults]):
    """Calculate drift metric for a column"""

    column_name: str
    column_type: str
    stattest: Optional[PossibleStatTestType]
    threshold: Optional[Numeric]
    nbinsx: Numeric
    xbins: Optional[Dict[str, int]]
    options: Optional[DataDriftOptions]

    def __init__(
        self,
        column_name: str,
        column_type: str,
        stattest: Optional[PossibleStatTestType] = None,
        threshold: Optional[Numeric] = None,
        nbinsx: Numeric = DEFAULT_NBINSX,
        xbins: Optional[Dict[str, int]] = None,
        options: Optional[DataDriftOptions] = None,
    ):
        self.column_name = column_name
        self.column_type = column_type
        self.stattest = stattest
        self.threshold = threshold
        self.nbinsx = nbinsx
        self.xbins = xbins
        self.options = options

    def calculate(self, data: InputData) -> ColumnDriftMetricResults:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        if self.column_name not in data.current_data:
            raise ValueError(f"Cannot find column {self.column_name} in current dataset")

        if self.column_name not in data.reference_data:
            raise ValueError(f"Cannot find column {self.column_name} in reference dataset")

        if self.column_type not in ("cat", "num"):
            raise ValueError(f"Incorrect column type {self.column_type}")

        drift_result = calculate_data_drift(
            current_data=data.current_data,
            reference_data=data.reference_data,
            column_name=self.column_name,
            stattest=self.stattest,
            threshold=self.threshold,
            feature_type=self.column_type,
        )

        if self.column_type == "cat":
            distr_for_plots = make_hist_for_num_plot(
                data.current_data[self.column_name], data.reference_data[self.column_name]
            )

        else:
            distr_for_plots = make_hist_for_cat_plot(
                data.current_data[self.column_name], data.reference_data[self.column_name]
            )

        return ColumnDriftMetricResults(
            column_name=self.column_name,
            column_type=self.column_type,
            stattest_name=drift_result.stattest_name,
            threshold=drift_result.threshold,
            drift_value=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            distr_for_plots=distr_for_plots,
        )


@default_renderer(wrap_type=ColumnDriftMetric)
class ColumnDriftMetricRenderer(MetricRenderer):
    def render_html(self, obj: ColumnDriftMetric) -> List[MetricHtmlInfo]:
        result = obj.get_result()
        return [
            MetricHtmlInfo(
                "column_data_drift_title",
                BaseWidgetInfo(
                    type=WidgetType.COUNTER.value,
                    title="",
                    size=2,
                    params={"counters": [{"value": "", "label": f"Column Data Drift: {result.drift_detected}"}]},
                ),
                details=[],
            )
        ]

    def render_json(self, obj: ColumnDriftMetric) -> dict:
        result = dataclasses.asdict(obj.get_result())
        # remove distribution data with pandas dataframes
        result.pop("distr_for_plots", None)
        return result
