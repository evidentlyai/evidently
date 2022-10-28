from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import Alert
from evidently.model.widget import AlertStats
from evidently.model.widget import BaseWidgetInfo
from evidently.model.widget import Insight
from evidently.model.widget import TriggeredAlertStats


class PercentWidget(Widget):
    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        return BaseWidgetInfo(
            type="percent",
            title="Example Percent Widget",
            size=1,
            details="Some additional information",
            alertsPosition="row",
            alertStats=AlertStats(
                active=4,
                triggered=TriggeredAlertStats(
                    last_24h=3,
                    period=1,
                ),
            ),
            alerts=[
                Alert(
                    value=5,
                    state="warning",
                    text="short text",
                    longText="some long description of alert",
                )
            ],
            params={"value": 40, "maxValue": 134, "details": "Some information"},
            insights=[
                Insight("Info insight", "info", "Example insight information"),
                Insight("Warning insight", "warning", "Example insight information"),
                Insight("Error insight", "error", "Example insight information"),
                Insight("Success insight", "success", "Example insight information"),
            ],
        )

    def analyzers(self):
        return []
