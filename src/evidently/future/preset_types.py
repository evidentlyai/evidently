import dataclasses
from typing import List

from evidently.future.metric_types import render_widgets
from evidently.model.widget import BaseWidgetInfo


@dataclasses.dataclass
class PresetResult:
    widget: List[BaseWidgetInfo]

    def _repr_html_(self):
        return render_widgets(self.widget)
