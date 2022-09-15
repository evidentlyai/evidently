from typing import Optional

import pandas as pd

from evidently import ColumnMapping
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import BaseWidgetInfo


class TextWidget(Widget):
    def calculate(
        self,
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        column_mapping: ColumnMapping,
        analyzers_results,
    ) -> Optional[BaseWidgetInfo]:
        return BaseWidgetInfo(
            title="Some title",
            type="text",
            size=2,
            params={
                "text": """
# Some header
Hello, world!

## Sub header
- point 1
- point 2
- point 3
                """
            },
        )

    def analyzers(self):
        return []
