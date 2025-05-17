import dataclasses
from typing import List

from evidently.core.metric_types import render_widgets
from evidently.legacy.model.widget import BaseWidgetInfo


@dataclasses.dataclass
class PresetResult:
    widget: List[BaseWidgetInfo]

    def _repr_html_(self):
        return render_widgets(self.widget, as_iframe=True)
