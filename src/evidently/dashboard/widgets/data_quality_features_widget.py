#!/usr/bin/env python
# coding: utf-8
import json
from typing import List
from typing import Optional
from typing import Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzer
from evidently.analyzers.data_quality_analyzer import DataQualityAnalyzerResults
from evidently.calculations.data_quality import FeatureQualityStats
from evidently.dashboard.widgets.widget import Widget
from evidently.model.widget import AdditionalGraphInfo
from evidently.model.widget import BaseWidgetInfo
from evidently.options import ColorOptions


class DataQualityFeaturesWidget(Widget):
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
        color_options = self.options_provider.get(ColorOptions)
        self.period_prefix = ""
        is_current_data = current_data is not None
        data_quality_results = DataQualityAnalyzer.get_results(analyzers_results)
        columns = data_quality_results.columns.utility_columns
        target_column = columns.target
        target_type: Optional[str]

        if target_column:
            target_type = data_quality_results.reference_features_stats[target_column].feature_type

        else:
            target_type = None

        cat_feature_names = data_quality_results.columns.cat_feature_names
        date_column = columns.date
        self._transform_cat_features(reference_data, current_data, cat_feature_names, target_column, target_type)

        all_features = data_quality_results.columns.get_all_features_list(
            cat_before_num=True, include_datetime_feature=True
        )
        if date_column:
            all_features = [date_column] + all_features
        if target_column:
            all_features = [target_column] + all_features

        if is_current_data:
            metrics_values_headers = ["reference", "current"]

        else:
            metrics_values_headers = [""]

        widgets_list = []
        for feature_name in all_features:
            additional_graphs = []
            feature_type = data_quality_results.reference_features_stats[feature_name].feature_type
            fig_main_distr = self._plot_main_distr_figure(
                reference_data, current_data, feature_name, feature_type, color_options
            )
            parts = self.assemble_parts(target_column, date_column, feature_name, feature_type)
            # additional_graphs = []
            if date_column and feature_type != "datetime":
                freq = self._choose_agg_period(date_column, reference_data, current_data)
                reference_data[date_column + "_period"] = reference_data[date_column].dt.to_period(freq=freq)
                if current_data is not None:
                    current_data[date_column + "_period"] = current_data[date_column].dt.to_period(freq=freq)
                    feature_in_time_figure = self._plot_feature_in_time_2_df(
                        reference_data, current_data, date_column, feature_name, feature_type, color_options
                    )
                else:
                    feature_in_time_figure = self._plot_feature_in_time_1_df(
                        reference_data, date_column, feature_name, feature_type, color_options
                    )
                additional_graphs.append(
                    AdditionalGraphInfo(
                        feature_name + "_in_time",
                        {
                            "data": feature_in_time_figure["data"],
                            "layout": feature_in_time_figure["layout"],
                        },
                    )
                )

            if target_column and feature_name != target_column:
                if current_data is not None:
                    feature_and_target_figure = self._plot_feature_and_target_2_df(
                        reference_data,
                        current_data,
                        target_column,
                        target_type,
                        feature_name,
                        feature_type,
                        color_options,
                    )
                else:
                    feature_and_target_figure = self._plot_feature_and_target_1_df(
                        reference_data, target_column, target_type, feature_name, feature_type, color_options
                    )
                additional_graphs.append(
                    AdditionalGraphInfo(
                        feature_name + "_by_target",
                        {
                            "data": feature_and_target_figure["data"],
                            "layout": feature_and_target_figure["layout"],
                        },
                    )
                )

            wi = BaseWidgetInfo(
                type="rich_data",
                title="",
                size=2,
                params={
                    "header": feature_name,
                    "description": feature_type,
                    "metricsValuesHeaders": metrics_values_headers,
                    "metrics": self._metrics_for_table(feature_name, data_quality_results, is_current_data),
                    "graph": {"data": fig_main_distr["data"], "layout": fig_main_distr["layout"]},
                    "details": {"parts": parts, "insights": []},
                },
                additionalGraphs=additional_graphs,
            )

            widgets_list.append(wi)

        return BaseWidgetInfo(title="", size=2, type="list", widgets=widgets_list, pageSize=10)

    @staticmethod
    def _get_stats_with_names(
        stats_list: List[Tuple[str, str, Optional[str]]],
        reference_stats: FeatureQualityStats,
        current_stats: Optional[FeatureQualityStats],
    ) -> List[dict]:
        def get_values_as_string(stats_dict, field_name, field_percentage_name) -> str:
            field_value = stats_dict[field_name]

            if field_value is None:
                field_value = ""

            if field_percentage_name is None:
                return str(field_value)

            else:
                return f"{field_value} ({stats_dict[field_percentage_name]}%)"

        result = []
        reference_stats_dict = reference_stats.as_dict()

        if current_stats is None:
            current_stats_dict = None

        else:
            current_stats_dict = current_stats.as_dict()

        for stat_label, stat_field, stat_field_percentage in stats_list:
            values = [get_values_as_string(reference_stats_dict, stat_field, stat_field_percentage)]

            if current_stats_dict is not None:
                values.append(get_values_as_string(current_stats_dict, stat_field, stat_field_percentage))

            result.append(
                {
                    "label": stat_label,
                    "values": values,
                }
            )
        return result

    def _metrics_for_table(
        self, feature_name: str, data_quality_results: DataQualityAnalyzerResults, is_current_data: bool
    ):
        reference_stats = data_quality_results.reference_features_stats[feature_name]

        current_stats: Optional[FeatureQualityStats] = None

        if data_quality_results.current_features_stats is not None and is_current_data:
            current_stats = data_quality_results.current_features_stats[feature_name]

        metrics = []
        if reference_stats.is_category():
            # mapping for category stats: (field in analyser results name, label in widget table name)
            cat_features = [
                ("count", "count", None),
                ("unique", "unique_count", "unique_percentage"),
                ("most common", "most_common_value", "most_common_value_percentage"),
                ("missing", "missing_count", "missing_percentage"),
            ]

            if current_stats:
                cat_features.append(("new categories", "new_in_current_values_count", None))
                cat_features.append(("missing categories", "unused_in_current_values_count", None))

            metrics.extend(self._get_stats_with_names(cat_features, reference_stats, current_stats))

        elif reference_stats.is_numeric():
            # mapping for category stats: (label, field_name_for_main_value, field_name_for_percentage)
            num_features = [
                ("count", "count", None),
                ("mean", "mean", None),
                ("std", "std", None),
                ("min", "min", None),
                ("25%", "percentile_25", None),
                ("50%", "percentile_50", None),
                ("75%", "percentile_75", None),
                ("max", "max", None),
                ("unique", "unique_count", "unique_percentage"),
                ("most common", "most_common_value", "most_common_value_percentage"),
                ("missing", "missing_count", "missing_percentage"),
                ("infinite", "infinite_count", "infinite_percentage"),
            ]
            metrics.extend(self._get_stats_with_names(num_features, reference_stats, current_stats))

        elif reference_stats.is_datetime():
            # mapping for category stats: (field in analyser results name, label in widget table name)
            datetime_features = [
                ("count", "count", None),
                ("unique", "unique_count", "unique_percentage"),
                ("most common", "most_common_value", "most_common_value_percentage"),
                ("missing", "missing_count", "missing_percentage"),
                ("first", "min", None),
                ("last", "max", None),
            ]
            metrics.extend(self._get_stats_with_names(datetime_features, reference_stats, current_stats))

        return metrics

    def _plot_main_distr_figure(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        feature_name: str,
        feature_type: str,
        color_options: ColorOptions,
    ) -> dict:
        if feature_type == "num":
            if current_data is None:
                trace1 = go.Histogram(x=reference_data[feature_name], marker_color=color_options.primary_color)
                trace2 = go.Histogram(
                    x=np.log10(reference_data.loc[reference_data[feature_name] > 0, feature_name]),
                    marker_color=color_options.primary_color,
                    visible=False,
                )
                data = [trace1, trace2]
                updatemenus = [
                    dict(
                        type="buttons",
                        direction="right",
                        x=1.0,
                        yanchor="top",
                        buttons=list(
                            [
                                dict(label="Linear Scale", method="update", args=[{"visible": [True, False]}]),
                                dict(label="Log Scale", method="update", args=[{"visible": [False, True]}]),
                            ]
                        ),
                    )
                ]

            else:
                trace1 = go.Histogram(
                    x=reference_data[feature_name],
                    marker_color=color_options.get_reference_data_color(),
                    name="reference",
                )
                trace2 = go.Histogram(
                    x=np.log10(reference_data.loc[reference_data[feature_name] > 0, feature_name]),
                    marker_color=color_options.get_reference_data_color(),
                    visible=False,
                    name="reference",
                )
                trace3 = go.Histogram(
                    x=current_data[feature_name], marker_color=color_options.get_current_data_color(), name="current"
                )
                trace4 = go.Histogram(
                    x=np.log10(current_data.loc[current_data[feature_name] > 0, feature_name]),
                    marker_color=color_options.get_current_data_color(),
                    visible=False,
                    name="current",
                )
                data = [trace1, trace2, trace3, trace4]

                updatemenus = [
                    dict(
                        type="buttons",
                        direction="right",
                        x=1.0,
                        yanchor="top",
                        buttons=list(
                            [
                                dict(
                                    label="Linear Scale",
                                    method="update",
                                    args=[{"visible": [True, False, True, False]}],
                                ),
                                dict(
                                    label="Log Scale", method="update", args=[{"visible": [False, True, False, True]}]
                                ),
                            ]
                        ),
                    )
                ]
            layout = dict(updatemenus=updatemenus)

            fig = go.Figure(data=data, layout=layout)

        elif feature_type == "cat":
            fig = go.Figure()
            cats = list(reference_data[feature_name].value_counts().index.astype(str))
            if "other" in cats:
                cats.remove("other")
                cats = cats + ["other"]
            if current_data is None:
                fig.add_trace(go.Histogram(x=reference_data[feature_name], marker_color=color_options.primary_color))
            else:
                fig.add_trace(
                    go.Histogram(
                        x=reference_data[feature_name],
                        marker_color=color_options.get_reference_data_color(),
                        name="reference",
                    )
                )
                fig.add_trace(
                    go.Histogram(
                        x=current_data[feature_name],
                        marker_color=color_options.get_current_data_color(),
                        name="current",
                    )
                )
            fig.update_xaxes(categoryorder="array", categoryarray=cats)

        elif feature_type == "datetime":
            freq = self._choose_agg_period(feature_name, reference_data, current_data)
            tmp_ref = reference_data[feature_name].dt.to_period(freq=freq)
            tmp_ref = tmp_ref.value_counts().reset_index()
            tmp_ref.columns = [feature_name, "number_of_items"]
            tmp_ref[feature_name] = tmp_ref[feature_name].dt.to_timestamp()
            fig = go.Figure()
            if current_data is None:
                fig.add_trace(
                    go.Scatter(
                        x=tmp_ref.sort_values(feature_name)[feature_name],
                        y=tmp_ref.sort_values(feature_name)["number_of_items"],
                        line=dict(color=color_options.primary_color, shape="spline"),
                    )
                )
            else:
                tmp_curr = current_data[feature_name].dt.to_period(freq=freq)
                tmp_curr = tmp_curr.value_counts().reset_index()
                tmp_curr.columns = [feature_name, "number_of_items"]
                tmp_curr[feature_name] = tmp_curr[feature_name].dt.to_timestamp()

                max_ref_date = tmp_ref[feature_name].max()
                min_curr_date = tmp_curr[feature_name].min()
                if max_ref_date == min_curr_date:
                    if (
                        tmp_curr.loc[tmp_curr[feature_name] == min_curr_date, "number_of_items"].iloc[0]
                        > tmp_ref.loc[tmp_ref[feature_name] == max_ref_date, "number_of_items"].iloc[0]
                    ):
                        tmp_curr.loc[tmp_curr[feature_name] == min_curr_date, "number_of_items"] = (
                            tmp_curr.loc[tmp_curr[feature_name] == min_curr_date, "number_of_items"]
                            + tmp_ref.loc[tmp_ref[feature_name] == max_ref_date, "number_of_items"]
                        )
                        tmp_ref = tmp_ref[tmp_ref[feature_name] != max_ref_date]
                    else:
                        tmp_ref.loc[tmp_ref[feature_name] == max_ref_date, "number_of_items"] = (
                            tmp_ref.loc[tmp_ref[feature_name] == max_ref_date, "number_of_items"]
                            + tmp_curr.loc[tmp_curr[feature_name] == min_curr_date, "number_of_items"]
                        )
                        tmp_curr = tmp_curr[tmp_curr[feature_name] != min_curr_date]

                fig.add_trace(
                    go.Scatter(
                        x=tmp_ref.sort_values(feature_name)[feature_name],
                        y=tmp_ref.sort_values(feature_name)["number_of_items"],
                        line=dict(color=color_options.get_reference_data_color(), shape="spline"),
                        name="reference",
                    )
                )
                fig.add_trace(
                    go.Scatter(
                        x=tmp_curr.sort_values(feature_name)[feature_name],
                        y=tmp_curr.sort_values(feature_name)["number_of_items"],
                        line=dict(color=color_options.get_current_data_color(), shape="spline"),
                        name="current",
                    )
                )
        else:
            return {}

        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        fig_main_distr = json.loads(fig.to_json())
        return fig_main_distr

    @staticmethod
    def assemble_parts(
        target_column: Optional[str], date_column: Optional[str], feature_name: str, feature_type: str
    ) -> List:
        parts = []
        if date_column and feature_type != "datetime":
            parts.append({"title": feature_name + " in time", "id": feature_name + "_in_time"})
        if target_column and feature_name != target_column:
            parts.append({"title": feature_name + " by target", "id": feature_name + "_by_target"})
        return parts

    @staticmethod
    def _transform_df_to_time_mean_view(df: pd.DataFrame, date_column: str, feature_name: str):
        df = df.groupby(date_column + "_period")[feature_name].mean().reset_index()
        df[date_column] = df[date_column + "_period"].dt.to_timestamp()
        return df

    @staticmethod
    def _transform_df_to_time_count_view(df: pd.DataFrame, date_column: str, feature_name: str):
        df = df.groupby([date_column + "_period", feature_name]).size()
        df.name = "num"
        df = df.reset_index()
        df[date_column] = df[date_column + "_period"].dt.to_timestamp()
        return df

    def _plot_feature_in_time_1_df(
        self,
        reference_data: pd.DataFrame,
        date_column: str,
        feature_name: str,
        feature_type: str,
        color_options: ColorOptions,
    ) -> dict:
        tmp = reference_data[[date_column + "_period", feature_name]].copy()
        feature_in_time_figure = {}

        if feature_type == "num":
            tmp = self._transform_df_to_time_mean_view(tmp, date_column, feature_name)

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=tmp.sort_values(date_column)[date_column],
                    y=tmp.sort_values(date_column)[feature_name],
                    line=dict(color=color_options.primary_color, shape="spline"),
                )
            )
            fig.update_layout(yaxis_title="Mean " + feature_name + " per " + self.period_prefix)
            feature_in_time_figure = json.loads(fig.to_json())

        elif feature_type == "cat":
            tmp = self._transform_df_to_time_count_view(tmp, date_column, feature_name)

            fig = go.Figure()
            for i, val in enumerate(tmp[feature_name].unique()):
                fig.add_trace(
                    go.Bar(
                        x=tmp.loc[tmp[feature_name] == val, date_column],
                        y=tmp.loc[tmp[feature_name] == val, "num"],
                        name=str(val),
                        marker_color=color_options.color_sequence[i],
                    )
                )
            fig.update_traces(marker_line_width=0.01)
            fig.update_layout(barmode="stack", bargap=0, yaxis_title="count category values per " + self.period_prefix)

            feature_in_time_figure = json.loads(fig.to_json())

        return feature_in_time_figure

    def _plot_feature_in_time_2_df(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        date_column: str,
        feature_name: str,
        feature_type: str,
        color_options: ColorOptions,
    ) -> dict:
        tmp_ref = reference_data[[date_column + "_period", feature_name]].copy()
        tmp_curr = current_data[[date_column + "_period", feature_name]].copy()
        feature_in_time_figure = {}

        if feature_type == "num":
            tmp_ref = self._transform_df_to_time_mean_view(tmp_ref, date_column, feature_name)
            tmp_curr = self._transform_df_to_time_mean_view(tmp_curr, date_column, feature_name)

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=tmp_ref.sort_values(date_column)[date_column],
                    y=tmp_ref.sort_values(date_column)[feature_name],
                    line=dict(color=color_options.get_reference_data_color(), shape="spline"),
                    name="reference",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=tmp_curr.sort_values(date_column)[date_column],
                    y=tmp_curr.sort_values(date_column)[feature_name],
                    line=dict(color=color_options.get_current_data_color(), shape="spline"),
                    name="current",
                )
            )
            fig.update_layout(yaxis_title="Mean " + feature_name + " per " + self.period_prefix)
            feature_in_time_figure = json.loads(fig.to_json())

        elif feature_type == "cat":
            tmp_ref = self._transform_df_to_time_count_view(tmp_ref, date_column, feature_name)
            tmp_curr = self._transform_df_to_time_count_view(tmp_curr, date_column, feature_name)

            fig = go.Figure()
            for i, val in enumerate(tmp_ref[feature_name].unique()):
                fig.add_trace(
                    go.Bar(
                        x=tmp_ref.loc[tmp_ref[feature_name] == val, date_column],
                        y=tmp_ref.loc[tmp_ref[feature_name] == val, "num"],
                        name=str(val),
                        marker_color=color_options.color_sequence[i],
                        opacity=0.6,
                    )
                )
                fig.add_trace(
                    go.Bar(
                        x=tmp_curr.loc[tmp_curr[feature_name] == val, date_column],
                        y=tmp_curr.loc[tmp_curr[feature_name] == val, "num"],
                        name=str(val),
                        marker_color=color_options.color_sequence[i],
                        showlegend=False,
                    )
                )
            fig.update_traces(marker_line_width=0.01)
            fig.update_layout(
                barmode="stack",
                bargap=0,
                yaxis_title="count category values per " + self.period_prefix,
                title="reference/current",
            )
            feature_in_time_figure = json.loads(fig.to_json())

        return feature_in_time_figure

    @staticmethod
    def _get_subplots_ratio(s1: pd.Series, s2: pd.Series):
        d1 = (s1.max() - s1.min()).days
        d2 = (s2.max() - s2.min()).days
        ratio = np.round(d1 / (d1 + d2), 3)
        return ratio, 1 - ratio

    @staticmethod
    def _transform_df_count_values(df: pd.DataFrame, target_column: str, feature_name: Optional[str]):
        df = df.groupby([target_column, feature_name]).size()
        df.name = "count_objects"
        df = df.reset_index()
        return df

    def _plot_feature_and_target_1_df(
        self,
        reference_data: pd.DataFrame,
        target_column: str,
        target_type: Optional[str],
        feature_name: Optional[str],
        feature_type: str,
        color_options: ColorOptions,
    ) -> dict:
        tmp = reference_data[[target_column, feature_name]].copy()
        if feature_type == "cat":
            if target_type == "num":
                fig = go.Figure()
                trace = go.Box(x=tmp[feature_name], y=tmp[target_column], marker_color=color_options.primary_color)
                fig.add_trace(trace)
                fig.update_layout(yaxis_title=target_column, xaxis_title=feature_name)
                fig.update_traces(marker_size=3)
            else:
                tmp = self._transform_df_count_values(tmp, target_column, feature_name)
                fig = go.Figure()
                for i, val in enumerate(tmp[target_column].unique()):
                    trace = go.Bar(
                        x=tmp.loc[tmp[target_column] == val, feature_name],
                        y=tmp.loc[tmp[target_column] == val, "count_objects"],
                        marker_color=color_options.color_sequence[i],
                        name=str(val),
                    )
                    fig.add_trace(trace)
                fig.update_layout(yaxis_title="count")
        else:
            if target_type == "num":
                fig = go.Figure()
                trace = go.Scatter(
                    x=tmp.sample(min(2000, len(tmp)), random_state=0)[feature_name],
                    y=tmp.sample(min(2000, len(tmp)), random_state=0)[target_column],
                    mode="markers",
                    marker_color=color_options.primary_color,
                )
                fig.add_trace(trace)

                fig.update_layout(
                    yaxis_title=target_column, xaxis_title=feature_name, legend={"itemsizing": "constant"}
                )
                fig.update_traces(marker_size=4)

            else:
                fig = go.Figure()
                trace = go.Box(y=tmp[feature_name], x=tmp[target_column], marker_color=color_options.primary_color)
                fig.add_trace(trace)
                fig.update_layout(yaxis_title=feature_name, xaxis_title=target_column)
                fig.update_traces(marker_size=3)
        feature_and_target_figure = json.loads(fig.to_json())
        return feature_and_target_figure

    def _plot_feature_and_target_2_df(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame,
        target_column: str,
        target_type: Optional[str],
        feature_name: str,
        feature_type: str,
        color_options: ColorOptions,
    ) -> dict:
        tmp_ref = reference_data[[target_column, feature_name]].copy()
        tmp_curr = current_data[[target_column, feature_name]].copy()
        tmp_ref["df"] = "reference"
        tmp_curr["df"] = "current"
        if feature_type == "cat":
            if target_type == "num":
                fig = go.Figure()
                trace1 = go.Box(
                    x=tmp_ref[feature_name],
                    y=tmp_ref[target_column],
                    marker_color=color_options.get_reference_data_color(),
                    name="reference",
                )
                fig.add_trace(trace1)
                trace2 = go.Box(
                    x=tmp_curr[feature_name],
                    y=tmp_curr[target_column],
                    marker_color=color_options.get_current_data_color(),
                    name="current",
                )
                fig.add_trace(trace2)

                fig.update_layout(yaxis_title=target_column, xaxis_title=feature_name, boxmode="group")
                fig.update_traces(marker_size=3)
            else:
                tmp_ref = self._transform_df_count_values(tmp_ref, target_column, feature_name)
                tmp_curr = self._transform_df_count_values(tmp_curr, target_column, feature_name)
                fig = make_subplots(rows=1, cols=2, shared_yaxes=True, subplot_titles=["reference", "current"])

                for i, val in enumerate(tmp_ref[target_column].unique()):
                    trace = go.Bar(
                        x=tmp_ref.loc[tmp_ref[target_column] == val, feature_name],
                        y=tmp_ref.loc[tmp_ref[target_column] == val, "count_objects"],
                        marker_color=color_options.color_sequence[i],
                        opacity=0.6,
                        showlegend=False,
                    )
                    fig.add_trace(trace, 1, 1)
                for i, val in enumerate(tmp_curr[target_column].unique()):
                    trace = go.Bar(
                        x=tmp_curr.loc[tmp_curr[target_column] == val, feature_name],
                        y=tmp_curr.loc[tmp_curr[target_column] == val, "count_objects"],
                        marker_color=color_options.color_sequence[i],
                        name=str(val),
                    )
                    fig.add_trace(trace, 1, 2)
                fig.update_layout(yaxis_title="count")
        else:
            if target_type == "num":
                fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
                trace = go.Scatter(
                    x=tmp_ref.sample(min(2000, len(tmp_ref)), random_state=0)[feature_name],
                    y=tmp_ref.sample(min(2000, len(tmp_ref)), random_state=0)[target_column],
                    mode="markers",
                    marker_color=color_options.get_reference_data_color(),
                    name="reference",
                )
                fig.add_trace(trace, 1, 1)
                trace = go.Scatter(
                    x=tmp_curr.sample(min(2000, len(tmp_curr)), random_state=0)[feature_name],
                    y=tmp_curr.sample(min(2000, len(tmp_curr)), random_state=0)[target_column],
                    mode="markers",
                    marker_color=color_options.get_current_data_color(),
                    name="current",
                )
                fig.add_trace(trace, 1, 2)
                fig.update_layout(yaxis_title=target_column, legend={"itemsizing": "constant"})
                fig.update_xaxes(title_text=feature_name, row=1, col=1)
                fig.update_xaxes(title_text=feature_name, row=1, col=2)
                fig.update_traces(marker_size=4)

            else:
                fig = go.Figure()
                trace1 = go.Box(
                    x=tmp_ref[target_column],
                    y=tmp_ref[feature_name],
                    marker_color=color_options.get_reference_data_color(),
                    name="reference",
                )
                fig.add_trace(trace1)
                trace2 = go.Box(
                    x=tmp_curr[target_column],
                    y=tmp_curr[feature_name],
                    marker_color=color_options.get_current_data_color(),
                    name="current",
                )
                fig.add_trace(trace2)
                fig.update_layout(yaxis_title=feature_name, xaxis_title=target_column, boxmode="group")
                fig.update_traces(marker_size=3)

        feature_and_target_figure = json.loads(fig.to_json())
        return feature_and_target_figure

    @staticmethod
    def _transform_cat_features(
        reference_data: pd.DataFrame,
        current_data: Optional[pd.DataFrame],
        cat_feature_names: List[str],
        target_column: Optional[str],
        target_type: Optional[str],
    ):
        if target_column and target_type == "cat":
            cat_feature_names = cat_feature_names + [target_column]
        for feature_name in cat_feature_names:
            if reference_data[feature_name].nunique() > 6:
                cats = reference_data[feature_name].value_counts().iloc[:5].index.astype(str)
                reference_data[feature_name] = reference_data[feature_name].apply(
                    lambda x: x if str(x) in cats else "other"
                )
                if current_data is not None:
                    current_data[feature_name] = current_data[feature_name].apply(
                        lambda x: x if str(x) in cats else "other"
                    )

    def _choose_agg_period(
        self, date_column: str, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame]
    ) -> str:
        optimal_points = 150
        prefix_dict = {"A": "year", "Q": "quarter", "M": "month", "W": "week", "D": "day", "H": "hour"}
        datetime_feature = reference_data[date_column]
        if current_data is not None:
            datetime_feature = datetime_feature.append(current_data[date_column])
        days = (datetime_feature.max() - datetime_feature.min()).days
        time_points = pd.Series(
            index=["A", "Q", "M", "W", "D", "H"],
            data=[
                abs(optimal_points - days / 365),
                abs(optimal_points - days / 90),
                abs(optimal_points - days / 30),
                abs(optimal_points - days / 7),
                abs(optimal_points - days),
                abs(optimal_points - days * 24),
            ],
        )
        self.period_prefix = prefix_dict[time_points.idxmin()]
        return str(time_points.idxmin())
