#!/usr/bin/env python
# coding: utf-8
from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo
from evidently.utils.data_operations import process_columns


class ClassTargetNameWidget(Widget):
    def analyzers(self):
        return []

    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        columns = process_columns(reference_data, column_mapping)

        if (
            columns.utility_columns.target is None
            or columns.utility_columns.prediction is None
        ):
            raise ValueError(
                f"Widget [{self.title}] requires 'target' and 'prediction' columns"
            )

        return BaseWidgetInfo(
            title=self.title,
            type="counter",
            size=2,
            params={
                "counters": [
                    {
                        "value": "",
                        "label": f"Classification Model Performance Report. Target:'{columns.utility_columns.target}'",
                    }
                ]
            },
        )
