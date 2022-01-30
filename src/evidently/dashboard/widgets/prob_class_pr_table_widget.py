#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer

from evidently.model.widget import BaseWidgetInfo, TabInfo
from evidently.dashboard.widgets.widget import Widget


class ProbClassPRTableWidget(Widget):
    def __init__(self, title: str, dataset: str = 'reference'):
        super().__init__(title)
        self.dataset = dataset  # reference or current

    def analyzers(self):
        return [ProbClassificationPerformanceAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        results = ProbClassificationPerformanceAnalyzer.get_results(analyzers_results)
        utility_columns = results.columns.utility_columns

        if utility_columns.target is None or utility_columns.prediction is None:
            if self.dataset == 'reference':
                raise ValueError(f"Widget [{self.title}] requires 'target' and 'prediction' columns")

            return None

        if self.dataset == 'reference':
            metrics = results.reference_metrics

            if metrics is None:
                raise ValueError(f"Widget [{self.title}] required 'reference' results from"
                                 f" {ProbClassificationPerformanceAnalyzer.__name__} but no data found")

        elif self.dataset == 'current':
            metrics = results.current_metrics

        else:
            raise ValueError(f"Widget [{self.title}] required 'current' or 'reference' dataset value")

        if metrics is None:
            return None

        if len(utility_columns.prediction) <= 2:
            if metrics.pr_table is None:
                raise ValueError(f"Widget [{self.title}] got no pr_table value")

            if not isinstance(metrics.pr_table, list):
                raise ValueError(f"Widget [{self.title}] got incorrect tyoe for pr_table value")

            pr_table_data: list = metrics.pr_table
            params_data = []

            for line in pr_table_data:
                count = line[1]
                prob = round(line[2], 2)
                top = round(line[0], 1)
                tp = line[3]
                fp = line[4]
                precision = round(line[5], 1)
                recall = round(line[6], 1)

                params_data.append({
                    'f1': float(top),
                    'f2': int(count),
                    'f3': float(prob),
                    'f4': int(tp),
                    'f5': int(fp),
                    'f6': float(precision),
                    'f7': float(recall)
                })

            widget_info = BaseWidgetInfo(
                title=self.title,
                type="big_table",
                size=1 if current_data is not None else 2,
                params={
                    "rowsPerPage": 21,
                    "columns": [
                        {
                            "title": "Top(%)",
                            "field": "f1",
                            "sort": "asc"
                        },
                        {
                            "title": "Count",
                            "field": "f2"
                        },
                        {
                            "title": "Prob",
                            "field": "f3",
                        },
                        {
                            "title": "TP",
                            "field": "f4"
                        },
                        {
                            "title": "FP",
                            "field": "f5"
                        },
                        {
                            "title": "Precision",
                            "field": "f6"
                        },
                        {
                            "title": "Recall",
                            "field": "f7"
                        }
                    ],
                    "data": params_data
                },
            )

        else:
            # create tables
            tabs = []

            for label in utility_columns.prediction:
                params_data = []

                if metrics.pr_table is None:
                    raise ValueError(f"Widget [{self.title}] got no pr_table value")

                if not isinstance(metrics.pr_table, dict):
                    raise ValueError(f"Widget [{self.title}] got incorrect type of pr_table value")

                pr_table_data_list = metrics.pr_table[label]

                for line in pr_table_data_list:
                    count = line[1]
                    prob = round(line[2], 2)
                    top = round(line[0], 1)
                    tp = line[3]
                    fp = line[4]
                    precision = round(line[5], 1)
                    recall = round(line[6], 1)

                    params_data.append({'f1': float(top),
                                        'f2': int(count),
                                        'f3': float(prob),
                                        'f4': int(tp),
                                        'f5': int(fp),
                                        'f6': float(precision),
                                        'f7': float(recall)})

                tabs.append(TabInfo(
                    id=label,
                    title=label,
                    widget=BaseWidgetInfo(
                        title="",
                        type="big_table",
                        size=2,  # if current_data is not None else 2,
                        params={
                            "rowsPerPage": 21,
                            "columns": [
                                {
                                    "title": "Top(%)",
                                    "field": "f1",
                                    "sort": "asc"
                                },
                                {
                                    "title": "Count",
                                    "field": "f2"
                                },
                                {
                                    "title": "Prob",
                                    "field": "f3"
                                },
                                {
                                    "title": "TP",
                                    "field": "f4"
                                },
                                {
                                    "title": "FP",
                                    "field": "f5"
                                },
                                {
                                    "title": "Precision",
                                    "field": "f6"
                                },
                                {
                                    "title": "Recall",
                                    "field": "f7"
                                }
                            ],
                            "data": params_data
                        },
                        additionalGraphs=[]
                    )
                ))

            widget_info = BaseWidgetInfo(
                type="tabs",
                title=self.title,
                size=1 if current_data is not None else 2,
                tabs=tabs
            )
        return widget_info
