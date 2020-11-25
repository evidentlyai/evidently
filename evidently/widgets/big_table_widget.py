#!/usr/bin/env python
# coding: utf-8

import pandas as pd

from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.widgets.widget import Widget


class BigTableWidget(Widget):
    def __init__(self, title: str):
        super().__init__()
        self.title = title

    def calculate(self, reference_data: pd.DataFrame, production_data: pd.DataFrame, column_mapping):
        ## need to fill self.widget_info / self.additional_graph with same structure
        pass

    def get_info(self) -> BaseWidgetInfo:
        return BaseWidgetInfo(
            title=self.title,
            type="big_table",
            details="",
            alertStats=AlertStats(),
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=2,
            params={
                "columns": [
                    {
                        "title": "Feature",
                        "field": "f1"
                    },
                    {
                        "title": "Data drift",
                        "field": "f2"
                    },
                    {
                        "title": "Distribution",
                        "field": "f3",
                        "type": "histogram",
                        "options": {
                            "xField": "x",
                            "yField": "y"
                        }
                    },
                    {
                        "title": "Distribution shift (similarity test at 95% confidence level)",
                        "field": "f4"
                    },
                    {
                        "title": "Alerts",
                        "field": "f5"
                    }
                ],
                "data": [
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "season_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "season_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "season",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1000.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0
                            ],
                            "y": [
                                3.5,
                                3.6,
                                3.7,
                                3.8,
                                3.9,
                                4.0,
                                4.1,
                                4.2,
                                4.3,
                                4.4,
                                4.5
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "holiday_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "holiday_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "holiday",
                        "f2": "Not Detected",
                        "f3": {
                            "x": [
                                976.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                24.0
                            ],
                            "y": [
                                0.0,
                                0.1,
                                0.2,
                                0.30000000000000004,
                                0.4,
                                0.5,
                                0.6000000000000001,
                                0.7000000000000001,
                                0.8,
                                0.9,
                                1.0
                            ]
                        },
                        "f4": "Not rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "workingday_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "workingday_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "workingday",
                        "f2": "Not Detected",
                        "f3": {
                            "x": [
                                312.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                688.0
                            ],
                            "y": [
                                0.0,
                                0.1,
                                0.2,
                                0.30000000000000004,
                                0.4,
                                0.5,
                                0.6000000000000001,
                                0.7000000000000001,
                                0.8,
                                0.9,
                                1.0
                            ]
                        },
                        "f4": "Not rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "weather_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "weather_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "weather",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                566.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                382.0,
                                0.0,
                                0.0,
                                0.0,
                                52.0
                            ],
                            "y": [
                                1.0,
                                1.2,
                                1.4,
                                1.6,
                                1.8,
                                2.0,
                                2.2,
                                2.4000000000000004,
                                2.6,
                                2.8,
                                3.0
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "temp_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "temp_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "temp",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                7.0,
                                55.0,
                                197.0,
                                182.0,
                                307.0,
                                93.0,
                                73.0,
                                46.0,
                                32.0,
                                8.0
                            ],
                            "y": [
                                6.56,
                                8.61,
                                10.66,
                                12.709999999999999,
                                14.759999999999998,
                                16.81,
                                18.86,
                                20.909999999999997,
                                22.959999999999997,
                                25.009999999999998,
                                27.06
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "atemp_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "atemp_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "atemp",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                12.0,
                                84.0,
                                193.0,
                                237.0,
                                132.0,
                                183.0,
                                73.0,
                                61.0,
                                8.0,
                                17.0
                            ],
                            "y": [
                                9.09,
                                11.286999999999999,
                                13.484,
                                15.681000000000001,
                                17.878,
                                20.075,
                                22.272,
                                24.469,
                                26.666,
                                28.863,
                                31.06
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "humidity_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "humidity_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "humidity",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                7.0,
                                5.0,
                                59.0,
                                144.0,
                                188.0,
                                180.0,
                                80.0,
                                149.0,
                                105.0,
                                83.0
                            ],
                            "y": [
                                16.0,
                                24.4,
                                32.8,
                                41.2,
                                49.6,
                                58.0,
                                66.4,
                                74.80000000000001,
                                83.2,
                                91.60000000000001,
                                100.0
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "windspeed_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "windspeed_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "windspeed",
                        "f2": "Not Detected",
                        "f3": {
                            "x": [
                                117.0,
                                193.0,
                                201.0,
                                271.0,
                                112.0,
                                57.0,
                                39.0,
                                9.0,
                                0.0,
                                1.0
                            ],
                            "y": [
                                0.0,
                                4.30006,
                                8.60012,
                                12.90018,
                                17.20024,
                                21.500300000000003,
                                25.80036,
                                30.10042,
                                34.40048,
                                38.700540000000004,
                                43.0006
                            ]
                        },
                        "f4": "Not rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "month_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "month_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "month",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                89.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                455.0,
                                0.0,
                                0.0,
                                0.0,
                                456.0
                            ],
                            "y": [
                                10.0,
                                10.2,
                                10.4,
                                10.6,
                                10.8,
                                11.0,
                                11.2,
                                11.4,
                                11.6,
                                11.8,
                                12.0
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "hour_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "hour_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "hour",
                        "f2": "Not Detected",
                        "f3": {
                            "x": [
                                123.0,
                                81.0,
                                82.0,
                                126.0,
                                84.0,
                                84.0,
                                126.0,
                                84.0,
                                84.0,
                                126.0
                            ],
                            "y": [
                                0.0,
                                2.3,
                                4.6,
                                6.8999999999999995,
                                9.2,
                                11.5,
                                13.799999999999999,
                                16.099999999999998,
                                18.4,
                                20.7,
                                23.0
                            ]
                        },
                        "f4": "Not rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "year_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "year_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "year",
                        "f2": "Detected",
                        "f3": {
                            "x": [
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0,
                                1000.0,
                                0.0,
                                0.0,
                                0.0,
                                0.0
                            ],
                            "y": [
                                2011.5,
                                2011.6,
                                2011.7,
                                2011.8,
                                2011.9,
                                2012.0,
                                2012.1,
                                2012.2,
                                2012.3,
                                2012.4,
                                2012.5
                            ]
                        },
                        "f4": "Rejected",
                        "f5": " "
                    },
                    {
                        "details": {
                            "parts": [
                                {
                                    "title": "Data drift",
                                    "id": "week_day_drift"
                                },
                                {
                                    "title": "Data distribution",
                                    "id": "week_day_distr"
                                }
                            ],
                            "insights": []
                        },
                        "f1": "week_day",
                        "f2": "Not Detected",
                        "f3": {
                            "x": [
                                144.0,
                                137.0,
                                0.0,
                                144.0,
                                0.0,
                                143.0,
                                144.0,
                                0.0,
                                144.0,
                                144.0
                            ],
                            "y": [
                                1.0,
                                1.6,
                                2.2,
                                2.8,
                                3.4,
                                4.0,
                                4.6,
                                5.2,
                                5.8,
                                6.3999999999999995,
                                7.0
                            ]
                        },
                        "f4": "Not rejected",
                        "f5": " "
                    }
                ]
            },
            additionalGraphs=[AdditionalGraphInfo("holiday_drift", {"data": [
                {"marker": {"color": "#4d4d4d", "size": 6}, "mode": "markers", "name": "Production", "type": "scatter",
                 "x": ["2012-10-16", "2012-10-17", "2012-10-18", "2012-10-19", "2012-11-01", "2012-11-02", "2012-11-03",
                       "2012-11-04", "2012-11-05", "2012-11-06", "2012-11-07", "2012-11-08", "2012-11-09", "2012-11-10",
                       "2012-11-11", "2012-11-12", "2012-11-13", "2012-11-14", "2012-11-15", "2012-11-16", "2012-11-17",
                       "2012-11-18", "2012-11-19", "2012-12-01", "2012-12-02", "2012-12-03", "2012-12-04", "2012-12-05",
                       "2012-12-06", "2012-12-07", "2012-12-08", "2012-12-09", "2012-12-10", "2012-12-11", "2012-12-12",
                       "2012-12-13", "2012-12-14", "2012-12-15", "2012-12-16", "2012-12-17", "2012-12-18",
                       "2012-12-19"],
                 "y": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}], "layout": {
                "legend": {"orientation": "h", "x": 1, "xanchor": "right", "y": 1.02, "yanchor": "bottom"}, "shapes": [
                    {"fillcolor": "LightGreen", "layer": "below", "line": {"width": 0}, "opacity": 0.5, "type": "rect",
                     "x0": 0, "x1": 1, "xref": "paper", "y0": -0.13886233657597655, "y1": 0.19692424230124458,
                     "yref": "y"},
                    {"line": {"color": "Green", "width": 3}, "name": "Reference", "type": "line", "x0": 0, "x1": 1,
                     "xref": "paper", "y0": 0.02903095286263403, "y1": 0.02903095286263403, "yref": "y"}],
                "showlegend": True, "template": {"data": {"bar": [
                    {"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"},
                     "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "barpolar": [
                    {"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "carpet": [{
                    "aaxis": {
                        "endlinecolor": "#2a3f5f",
                        "gridcolor": "white",
                        "linecolor": "white",
                        "minorgridcolor": "white",
                        "startlinecolor": "#2a3f5f"},
                    "baxis": {
                        "endlinecolor": "#2a3f5f",
                        "gridcolor": "white",
                        "linecolor": "white",
                        "minorgridcolor": "white",
                        "startlinecolor": "#2a3f5f"},
                    "type": "carpet"}],
                    "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""},
                                    "type": "choropleth"}], "contour": [
                        {"colorbar": {"outlinewidth": 0, "ticks": ""},
                         "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"],
                                        [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"],
                                        [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"],
                                        [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"],
                                        [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}],
                    "contourcarpet": [
                        {"colorbar": {"outlinewidth": 0, "ticks": ""},
                         "type": "contourcarpet"}], "heatmap": [
                        {"colorbar": {"outlinewidth": 0, "ticks": ""},
                         "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"],
                                        [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"],
                                        [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"],
                                        [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"],
                                        [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}],
                    "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""},
                                   "colorscale": [[0.0, "#0d0887"],
                                                  [0.1111111111111111, "#46039f"],
                                                  [0.2222222222222222, "#7201a8"],
                                                  [0.3333333333333333, "#9c179e"],
                                                  [0.4444444444444444, "#bd3786"],
                                                  [0.5555555555555556, "#d8576b"],
                                                  [0.6666666666666666, "#ed7953"],
                                                  [0.7777777777777778, "#fb9f3a"],
                                                  [0.8888888888888888, "#fdca26"],
                                                  [1.0, "#f0f921"]],
                                   "type": "heatmapgl"}], "histogram": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}],
                    "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""},
                                     "colorscale": [[0.0, "#0d0887"],
                                                    [0.1111111111111111,
                                                     "#46039f"],
                                                    [0.2222222222222222,
                                                     "#7201a8"],
                                                    [0.3333333333333333,
                                                     "#9c179e"],
                                                    [0.4444444444444444,
                                                     "#bd3786"],
                                                    [0.5555555555555556,
                                                     "#d8576b"],
                                                    [0.6666666666666666,
                                                     "#ed7953"],
                                                    [0.7777777777777778,
                                                     "#fb9f3a"],
                                                    [0.8888888888888888,
                                                     "#fdca26"],
                                                    [1.0, "#f0f921"]],
                                     "type": "histogram2d"}],
                    "histogram2dcontour": [
                        {"colorbar": {"outlinewidth": 0, "ticks": ""},
                         "colorscale": [[0.0, "#0d0887"],
                                        [0.1111111111111111, "#46039f"],
                                        [0.2222222222222222, "#7201a8"],
                                        [0.3333333333333333, "#9c179e"],
                                        [0.4444444444444444, "#bd3786"],
                                        [0.5555555555555556, "#d8576b"],
                                        [0.6666666666666666, "#ed7953"],
                                        [0.7777777777777778, "#fb9f3a"],
                                        [0.8888888888888888, "#fdca26"],
                                        [1.0, "#f0f921"]],
                         "type": "histogram2dcontour"}], "mesh3d": [
                        {"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [
                        {"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}],
                    "pie": [{"automargin": True, "type": "pie"}], "scatter": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatter3d": [
                        {"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                         "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}],
                    "scattercarpet": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                         "type": "scattercarpet"}], "scattergeo": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}],
                    "scattergl": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                         "type": "scattergl"}], "scattermapbox": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}],
                    "scatterpolar": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                         "type": "scatterpolar"}], "scatterpolargl": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}],
                    "scatterternary": [
                        {"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}},
                         "type": "scatterternary"}], "surface": [
                        {"colorbar": {"outlinewidth": 0, "ticks": ""},
                         "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"],
                                        [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"],
                                        [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"],
                                        [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"],
                                        [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}],
                    "table": [{"cells": {"fill": {"color": "#EBF0F8"},
                                         "line": {"color": "white"}},
                               "header": {"fill": {"color": "#C8D4E3"},
                                          "line": {"color": "white"}},
                               "type": "table"}]}, "layout": {
                    "annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1},
                    "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {
                        "diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"],
                                      [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"],
                                      [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]],
                        "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"],
                                       [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"],
                                       [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"],
                                       [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"],
                                       [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]],
                        "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"],
                                            [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"],
                                            [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"],
                                            [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"],
                                            [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]},
                    "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880",
                                 "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"},
                    "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": True,
                            "showland": True, "subunitcolor": "white"}, "hoverlabel": {"align": "left"},
                    "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white",
                    "plot_bgcolor": "#E5ECF6",
                    "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""},
                              "bgcolor": "#E5ECF6",
                              "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {
                        "xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2,
                                  "linecolor": "white", "showbackground": True, "ticks": "", "zerolinecolor": "white"},
                        "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2,
                                  "linecolor": "white", "showbackground": True, "ticks": "", "zerolinecolor": "white"},
                        "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2,
                                  "linecolor": "white", "showbackground": True, "ticks": "", "zerolinecolor": "white"}},
                    "shapedefaults": {"line": {"color": "#2a3f5f"}},
                    "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""},
                                "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""},
                                "bgcolor": "#E5ECF6",
                                "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}},
                    "title": {"x": 0.05},
                    "xaxis": {"automargin": True, "gridcolor": "white", "linecolor": "white", "ticks": "",
                              "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2},
                    "yaxis": {"automargin": True, "gridcolor": "white", "linecolor": "white", "ticks": "",
                              "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}},
                "xaxis": {"title": {"text": "Timestamp"}}, "yaxis": {"title": {"text": "holiday"}}}}
                                                  )],
        )
