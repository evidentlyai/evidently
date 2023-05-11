import builtins
import dataclasses
import json
import uuid
from collections import defaultdict
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import pandas as pd
from pydantic import BaseModel
from pydantic import parse_obj_as
from pydantic.utils import import_string
from typing_extensions import get_args

from evidently import ColumnMapping
from evidently.base_metric import InputData
from evidently.base_metric import Metric
from evidently.base_metric import MetricResult
from evidently.core import IncludeOptions
from evidently.metric_preset.metric_preset import MetricPreset
from evidently.metric_results import DatasetColumns
from evidently.model.dashboard import DashboardInfo
from evidently.model.widget import AdditionalGraphInfo
from evidently.options.base import AnyOptions
from evidently.renderers.base_renderer import DetailsInfo
from evidently.suite.base_suite import Display
from evidently.suite.base_suite import Suite
from evidently.suite.base_suite import find_metric_renderer
from evidently.utils import NumpyEncoder
from evidently.utils.data_operations import process_columns
from evidently.utils.data_preprocessing import create_data_definition
from evidently.utils.generators import BaseGenerator


class Report(Display):
    _inner_suite: Suite
    _columns_info: DatasetColumns
    _first_level_metrics: List[Union[Metric]]
    metrics: List[Union[Metric, MetricPreset, BaseGenerator]]

    def __init__(self, metrics: List[Union[Metric, MetricPreset, BaseGenerator]], options: AnyOptions = None):
        super().__init__(options)
        # just save all metrics and metric presets
        self.metrics = metrics
        self._inner_suite = Suite(self.options)
        self._first_level_metrics = []

    def run(
        self,
        *,
        reference_data: Optional[pd.DataFrame],
        current_data: pd.DataFrame,
        column_mapping: Optional[ColumnMapping] = None,
        agg_data: bool = False,
    ) -> None:
        if column_mapping is None:
            column_mapping = ColumnMapping()

        if current_data is None:
            raise ValueError("Current dataset should be present")

        self._columns_info = process_columns(current_data, column_mapping)

        self._inner_suite.verify()

        data_definition = create_data_definition(reference_data, current_data, column_mapping)
        data = InputData(reference_data, current_data, None, None, column_mapping, data_definition)

        # get each item from metrics/presets and add to metrics list
        # do it in one loop because we want to save metrics and presets order
        for item in self.metrics:
            # if the item is a metric generator, then we need to generate metrics and add them to the report
            if isinstance(item, BaseGenerator):
                for metric in item.generate(columns_info=self._columns_info):
                    if isinstance(metric, Metric):
                        self._first_level_metrics.append(metric)
                        self._inner_suite.add_metric(metric)

                    else:
                        # if generated item is not a metric, raise an error
                        raise ValueError(f"Incorrect metric type in generator {item}")

            elif isinstance(item, MetricPreset):
                metrics = []

                for metric_item in item.generate_metrics(data=data, columns=self._columns_info):
                    if isinstance(metric_item, BaseGenerator):
                        metrics.extend(metric_item.generate(columns_info=self._columns_info))

                    else:
                        metrics.append(metric_item)

                for metric in metrics:
                    self._first_level_metrics.append(metric)
                    self._inner_suite.add_metric(metric)

            elif isinstance(item, Metric):
                self._first_level_metrics.append(item)
                self._inner_suite.add_metric(item)

            else:
                raise ValueError("Incorrect item instead of a metric or metric preset was passed to Report")

        data_definition = create_data_definition(reference_data, current_data, column_mapping)
        curr_add, ref_add = self._inner_suite.create_additional_features(current_data, reference_data, data_definition)
        data = InputData(
            reference_data,
            current_data,
            ref_add,
            curr_add,
            column_mapping,
            data_definition,
        )
        if agg_data:
            self._inner_suite.context.options.agg_data = True
        self._inner_suite.run_calculate(data)

    def as_dict(  # type: ignore[override]
        self,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        metrics = []
        include = include or {}
        exclude = exclude or {}
        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metric_id = metric.get_id()
            metrics.append(
                {
                    "metric": metric_id,
                    "result": renderer.render_json(
                        metric,
                        include_render=include_render,
                        include=include.get(metric_id),
                        exclude=exclude.get(metric_id),
                    ),
                }
            )

        return {
            "metrics": metrics,
        }

    def as_pandas(self, group: str = None) -> Union[Dict[str, pd.DataFrame], pd.DataFrame]:
        metrics = defaultdict(list)

        for metric in self._first_level_metrics:
            renderer = find_metric_renderer(type(metric), self._inner_suite.context.renderers)
            metric_id = metric.get_id()
            if group is not None and metric_id != group:
                continue
            metrics[metric_id].append(renderer.render_pandas(metric))

        result = {cls: pd.concat(val) for cls, val in metrics.items()}
        if group is None and len(result) == 1:
            return next(iter(result.values()))
        if group is None:
            return result
        if group not in result:
            raise ValueError(f"Metric group {group} not found in this report")
        return result[group]

    def _build_dashboard_info(self):
        metrics_results = []
        additional_graphs = []

        color_options = self.options.color_options

        for test in self._first_level_metrics:
            renderer = find_metric_renderer(type(test), self._inner_suite.context.renderers)
            # set the color scheme from the report for each render
            renderer.color_options = color_options
            html_info = renderer.render_html(test)

            for info_item in html_info:
                for additional_graph in info_item.get_additional_graphs():
                    if isinstance(additional_graph, AdditionalGraphInfo):
                        additional_graphs.append(DetailsInfo("", additional_graph.params, additional_graph.id))

                    else:
                        additional_graphs.append(DetailsInfo("", additional_graph, additional_graph.id))

            metrics_results.extend(html_info)

        return (
            "evidently_dashboard_" + str(uuid.uuid4()).replace("-", ""),
            DashboardInfo("Report", widgets=[result for result in metrics_results]),
            {
                f"{item.id}": dataclasses.asdict(item.info) if dataclasses.is_dataclass(item.info) else item.info
                for item in additional_graphs
            },
        )

    def save_profile(self, path):
        payload = _ReportPayload(
            metrics=[
                (_MetricPayload.from_metric(m), res["result"])
                for m, res in zip(self._first_level_metrics, self.as_dict(include_render=True)["metrics"])
            ]
        )

        with open(path, "w") as f:
            json.dump(payload.dict(), f, indent=2, cls=NumpyEncoder)

    @classmethod
    def load_profile(cls, path):
        with open(path, "r") as f:
            payload = parse_obj_as(_ReportPayload, json.load(f))

        report = payload.load

        return report


class _MetricPayload(BaseModel):
    cls: str
    params: Dict[str, Tuple[str, Any]]

    @classmethod
    def from_metric(cls, metric: Metric):
        parameters = {
            name: (f"{value.__class__.__module__}.{value.__class__.__name__}", value)
            for name, value in metric.__dict__.items()
            if name not in ["context"]
        }
        parameters = {
            name: (t, p if not isinstance(p, Metric) else _MetricPayload.from_metric(p))
            for name, (t, p) in parameters.items()
        }
        return _MetricPayload(cls=f"{metric.__class__.__module__}.{metric.__class__.__name__}", params=parameters)

    def to_metric(self) -> Metric:
        metric_cls = import_string(self.cls)
        cls = metric_cls()
        for name, (type_name, value) in self.params.items():
            type_ = smart_import_string(type_name)
            if isinstance(type_, type) and issubclass(type_, Metric):
                value = _MetricPayload(**value).to_metric()
            elif isinstance(type_, type) and issubclass(type_, BaseModel):
                value = type_(**value)
            else:
                try:
                    value = type_(value) if type_ is not None else None
                except TypeError:
                    raise
            cls.__dict__[name] = value
        return cls


def smart_import_string(dotted_path):
    if dotted_path.startswith("builtins."):
        dotted_path = dotted_path[len("builtins.") :]
        if dotted_path == "NoneType":
            return None
        return getattr(builtins, dotted_path)
    return import_string(dotted_path)


class _ReportPayload(BaseModel):
    metrics: List[Tuple[_MetricPayload, Dict]]

    @property
    def load(self):
        metrics = []
        results = []
        for mp, result in self.metrics:
            metric = mp.to_metric()
            metrics.append(metric)
            result_type = get_args(metric.__class__.__orig_bases__[0])[0]
            assert issubclass(result_type, MetricResult)
            results.append(parse_obj_as(result_type, result))

        report = Report(metrics=metrics)
        report._first_level_metrics = metrics
        context = report._inner_suite.context
        for metric, result in zip(metrics, results):
            metric.set_context(context)
            context.metrics.append(metric)
            context.metric_results[metric] = result
        return report
