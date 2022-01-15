import json
from typing import Optional

import pandas as pd
import numpy as np

import plotly.figure_factory as ff

from evidently.model.widget import BaseWidgetInfo
from evidently.dashboard.widgets.widget import Widget


class TargetDistributionWidget(Widget):
    def __init__(self, title: str):
        super().__init__(title)

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        
        hist_data = [reference_data[column_mapping.target], current_data[column_mapping.target]]
        group_labels = ['reference', 'production']
        colors = ['#333F44', '#37AA9C'] 

        fig = ff.create_distplot(hist_data, group_labels, colors=colors, show_hist=False, show_rug=False)

        fig.update_layout(
            xaxis_title="Value", 
            yaxis_title="Share",
            xaxis=dict(
                showticklabels=True
            ),
            yaxis=dict(
                showticklabels=True
            ),
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )

        target_dist_json = json.loads(fig.to_json())

        return BaseWidgetInfo(
            title=self.title,
            type="big_graph",
            size=1,
            params={
                "data": target_dist_json['data'],
                "layout": target_dist_json['layout']
            },
        )

