#!/usr/bin/env python
# coding: utf-8
import json
from typing import List
from typing import Optional
from typing import Tuple
import pandas as pd
import numpy as np

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzerResults
from evidently.analyzers.data_quality_analyzer import FeatureQualityStats
from evidently.model.widget import BaseWidgetInfo, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget, GREY, RED, COLOR_DISCRETE_SEQUENCE


class DataQualityCorrelationsWidget(Widget):
    period_prefix: str

    def analyzers(self):
        return [DataQualityAnalyzer]

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:

        data_quality_results = DataQualityAnalyzer.get_results(analyzers_results)
        is_current_data = current_data is not None
        reference_correlations = data_quality_results.reference_correlations
        if is_current_data:
            current_correlations = data_quality_results.current_correlations
        else:
            current_correlations = None

        additional_graphs = []
        for kind in ['pearson', 'spearman', 'kendall', 'cramer_v']:
            correlation_figure = self._plot_correlation_figure(kind, reference_correlations, current_correlations)
            additional_graphs.append(
                        AdditionalGraphInfo(
                            kind,
                            {
                                "data": correlation_figure["data"],
                                "layout": correlation_figure["layout"],
                            },
                        )
                    )

        wi = BaseWidgetInfo(
                type="expandable_list",
                title="",
                size=2,
                params={
                    "header": "Correlations",
                    "description": "",
                    "metricsValuesHeaders": [],
                    "metrics": [],
                    "graph": {},
                    "details": {},
                },
                # additionalGraphs=additional_graphs
            )
        return BaseWidgetInfo(title="", size=2, type="group", widgets=[wi], additionalGraphs=additional_graphs)

    def _plot_correlation_figure(self, kind: str, reference_correlations: dict,
    current_correlations: Optional[dict]) -> dict:
        if current_correlations is not None:
            cols = 2
            subplot_titles=["reference", "current"]
        else:
            cols = 1
            subplot_titles=[""]
        columns = reference_correlations[kind].columns
        fig = make_subplots(rows=1, cols=cols, subplot_titles=subplot_titles)
        trace = go.Heatmap(
                   z=reference_correlations[kind].corr(),
                   x=columns,
                   y=columns,
                   colorscale='RdBu')
        fig.append_trace(trace, 1, 1)
        if current_correlations is not None:
            trace = go.Heatmap(
                   z=current_correlations[kind].corr(),
                   x=columns,
                   y=columns,
                   colorscale='RdBu')
            fig.append_trace(trace, 1, 2)
        correlation_figure = json.loads(fig.to_json())
        return correlation_figure