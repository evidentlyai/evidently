#!/usr/bin/env python
# coding: utf-8
import json
from typing import Optional, List

import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from evidently import ColumnMapping
from evidently.analyzers.data_profile_analyzer import DataProfileAnalyzer
from evidently.model.widget import BaseWidgetInfo, AlertStats, AdditionalGraphInfo
from evidently.dashboard.widgets.widget import Widget, GREY, RED, COLOR_DISCRETE_SEQUENCE


class DataProfileFeaturesWidget(Widget):
    period_prefix: str

    def analyzers(self):
        return [DataProfileAnalyzer]

    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping,
                  analyzers_results) -> Optional[BaseWidgetInfo]:
        self.period_prefix = ''
        data_profile_results = DataProfileAnalyzer.get_results(analyzers_results)
        columns = data_profile_results.columns.utility_columns
        target_column = columns.target

        if target_column is None:
            raise ValueError('target column should be present')

        all_features: List[str] = [target_column]

        target_type = data_profile_results.reference_features_stats[target_column]['feature_type']
        cat_feature_names = data_profile_results.columns.cat_feature_names
        date_column = columns.date

        if date_column is not None:
            all_features += [date_column]

        self._transform_cat_features(reference_data, current_data, cat_feature_names, target_column, target_type)
        # set params data
        params_data = []
        all_features += data_profile_results.columns.get_all_features_list(
            cat_before_num=True,
            include_datetime_feature=True,
        )

        for feature_name in all_features:
            feature_type = data_profile_results.reference_features_stats[feature_name]['feature_type']
            if feature_name == target_column:
                prefix = ', target'
            else:
                prefix = ''

            params_data.append(
                {
                    "details": {
                        "parts": self.assemble_parts(target_column, date_column, feature_name, feature_type),
                        "insights": []
                    },
                    "f1": feature_name + prefix,
                    "f2": feature_type,
                    "f3": ' ',  # data_profile_results.ref_features_stats[feature_name]['most common value'],
                    "f4": 'graph'
                }
            )

        # set additionalGraphs
        additional_graphs_data = []

        # additional graphs data
        for feature_name in all_features:
            feature_type = data_profile_results.reference_features_stats[feature_name]['feature_type']
            if date_column and feature_type != 'date':
                freq = self._choose_agg_period(date_column, reference_data, current_data)
                reference_data[date_column + '_period'] = reference_data[date_column].dt.to_period(freq=freq)
                if current_data is not None:
                    current_data[date_column + '_period'] = current_data[date_column].dt.to_period(freq=freq)
                    feature_in_time_figure = self._plot_feature_in_time_2_df(reference_data, current_data, date_column,
                                                                             feature_name, feature_type)
                else:
                    feature_in_time_figure = self._plot_feature_in_time_1_df(reference_data, date_column, feature_name,
                                                                             feature_type)

                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name or '' + '_in_time',
                        {
                            "title": "",
                            "size": 2,
                            "text": "",
                            "type": "big_graph",
                            "params":
                                {
                                    "data": feature_in_time_figure['data'],
                                    "layout": feature_in_time_figure['layout']
                                }
                        }
                    )
                )

            if target_column and feature_name != target_column and feature_name:
                if current_data is not None:
                    feature_and_target_figure = self._plot_feature_and_target_2_df(reference_data, current_data,
                                                                                   target_column, target_type,
                                                                                   feature_name, feature_type)
                else:
                    feature_and_target_figure = self._plot_feature_and_target_1_df(reference_data, target_column,
                                                                                   target_type, feature_name,
                                                                                   feature_type)
                additional_graphs_data.append(
                    AdditionalGraphInfo(
                        feature_name or '' + "_by_target",
                        {
                            "title": "",
                            "size": 2,
                            "text": "",
                            "type": "big_graph",
                            "params":
                                {
                                    "data": feature_and_target_figure['data'],
                                    "layout": feature_and_target_figure['layout']
                                }
                        }
                    )
                )

        return BaseWidgetInfo(
            title='data profile report',
            type="big_table",
            details="",
            alertStats=AlertStats(),
            alerts=[],
            alertsPosition="row",
            insights=[],
            size=2,
            params={
                "rowsPerPage": min(len(all_features), 10),
                "columns": [
                    {
                        "title": "Feature",
                        "field": "f1"
                    },
                    {
                        "title": "Type",
                        "field": "f2"
                    },
                    {
                        "title": "Characteristics",
                        "field": "f3"
                    },
                    {
                        "title": "Picture",
                        "field": "f4"
                    }
                ],
                "data": params_data
            },

            additionalGraphs=additional_graphs_data
        )

    def assemble_parts(self, target_column: str, date_column: Optional[str], feature_name: str, feature_type: str) -> List:
        parts = []
        if date_column and feature_type != 'date':
            parts.append({
                "title": feature_name + " in time",
                "id": feature_name + "_in_time",
                "type": "widget"
            })
        if target_column and feature_name != target_column:
            parts.append({
                "title": feature_name + " by target",
                "id": feature_name + "_by_target",
                "type": "widget"
            })
        return parts

    def _transform_df_to_time_mean_view(self, df: pd.DataFrame, date_column: str, feature_name: str):
        df = df.groupby(date_column + '_period')[feature_name].mean().reset_index()
        df[date_column] = df[date_column + '_period'].dt.to_timestamp()
        return df

    def _transform_df_to_time_count_view(self, df: pd.DataFrame, date_column: str, feature_name: str):
        df = df.groupby([date_column + '_period', feature_name]).size()
        df.name = 'num'
        df = df.reset_index()
        df[date_column] = df[date_column + '_period'].dt.to_timestamp()
        return df

    def _plot_feature_in_time_1_df(self, reference_data: pd.DataFrame, date_column: str, feature_name: str,
                                   feature_type: str) -> dict:
        tmp = reference_data[[date_column + '_period', feature_name]].copy()
        feature_in_time_figure = {}

        if feature_type == 'num':
            tmp = self._transform_df_to_time_mean_view(tmp, date_column, feature_name)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=tmp.sort_values(date_column)[date_column],
                                     y=tmp.sort_values(date_column)[feature_name],
                                     line=dict(color=RED, shape="spline")))
            fig.update_layout(yaxis_title='Mean ' + feature_name + ' per ' + self.period_prefix)
            feature_in_time_figure = json.loads(fig.to_json())

        elif feature_type == 'cat':
            tmp = self._transform_df_to_time_count_view(tmp, date_column, feature_name)

            fig = go.Figure()
            for i, val in enumerate(tmp[feature_name].unique()):
                fig.add_trace(go.Bar(
                    x=tmp.loc[tmp[feature_name] == val, date_column],
                    y=tmp.loc[tmp[feature_name] == val, 'num'],
                    name=str(val),
                    marker_color=COLOR_DISCRETE_SEQUENCE[i]))
            fig.update_traces(marker_line_width=0.01)
            fig.update_layout(barmode='stack', bargap=0, yaxis_title='count category values per ' + self.period_prefix)

            feature_in_time_figure = json.loads(fig.to_json())

        return feature_in_time_figure

    def _plot_feature_in_time_2_df(self, reference_data: pd.DataFrame, current_data: pd.DataFrame,
                                   date_column: str, feature_name: str, feature_type: str) -> dict:
        tmp_ref = reference_data[[date_column + '_period', feature_name]].copy()
        tmp_curr = current_data[[date_column + '_period', feature_name]].copy()
        feature_in_time_figure = {}

        if feature_type == 'num':
            tmp_ref = self._transform_df_to_time_mean_view(tmp_ref, date_column, feature_name)
            tmp_curr = self._transform_df_to_time_mean_view(tmp_curr, date_column, feature_name)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=tmp_ref.sort_values(date_column)[date_column],
                                     y=tmp_ref.sort_values(date_column)[feature_name],
                                     line=dict(color=GREY, shape="spline"), name='reference'))
            fig.add_trace(go.Scatter(x=tmp_curr.sort_values(date_column)[date_column],
                                     y=tmp_curr.sort_values(date_column)[feature_name],
                                     line=dict(color=RED, shape="spline"), name='current'))
            fig.update_layout(yaxis_title='Mean ' + feature_name + ' per ' + self.period_prefix)
            feature_in_time_figure = json.loads(fig.to_json())

        elif feature_type == 'cat':
            tmp_ref = self._transform_df_to_time_count_view(tmp_ref, date_column, feature_name)
            tmp_curr = self._transform_df_to_time_count_view(tmp_curr, date_column, feature_name)

            subplots_ratio = self._get_subplots_ratio(tmp_ref[date_column], tmp_curr[date_column])
            fig = make_subplots(rows=1, cols=2, shared_yaxes=True, subplot_titles=("reference", "current"),
                                column_widths=subplots_ratio, horizontal_spacing=0.03)

            for i, val in enumerate(tmp_ref[feature_name].unique()):
                fig.add_trace(go.Bar(
                    x=tmp_ref.loc[tmp_ref[feature_name] == val, date_column],
                    y=tmp_ref.loc[tmp_ref[feature_name] == val, 'num'],
                    name=str(val),
                    marker_color=COLOR_DISCRETE_SEQUENCE[i], opacity=0.6, showlegend=False), 1, 1)
                fig.add_trace(go.Bar(
                    x=tmp_curr.loc[tmp_curr[feature_name] == val, date_column],
                    y=tmp_curr.loc[tmp_curr[feature_name] == val, 'num'],
                    name=str(val),
                    marker_color=COLOR_DISCRETE_SEQUENCE[i]), 1, 2)
            fig.update_traces(marker_line_width=0.01)
            fig.update_layout(
                barmode='stack', bargap=0, yaxis_title='count category values per ' + self.period_prefix
            )
            feature_in_time_figure = json.loads(fig.to_json())

        return feature_in_time_figure

    def _get_subplots_ratio(self, s1: pd.Series, s2: pd.Series):
        d1 = (s1.max() - s1.min()).days
        d2 = (s2.max() - s2.min()).days
        ratio = np.round(d1 / (d1 + d2), 3)
        return ratio, 1 - ratio

    def _transform_df_count_values(self, df: pd.DataFrame, target_column: str, feature_name: Optional[str]):
        df = df.groupby([target_column, feature_name]).size()
        df.name = 'count_objects'
        df = df.reset_index()
        return df

    def _plot_feature_and_target_1_df(self, reference_data: pd.DataFrame, target_column: str, target_type: str,
                                      feature_name: Optional[str], feature_type: str) -> dict:
        tmp = reference_data[[target_column, feature_name]].copy()
        if feature_type == 'cat':
            if target_type == 'num':
                fig = px.strip(
                    tmp.sample(2000, random_state=0), x=feature_name, y=target_column,
                    color_discrete_sequence=COLOR_DISCRETE_SEQUENCE
                )
                fig.update_traces(marker=dict(size=2))
            else:
                tmp = self._transform_df_count_values(tmp, target_column, feature_name)
                fig = go.Figure()
                for i, val in enumerate(tmp[target_column].unique()):
                    trace = go.Bar(
                        x=tmp.loc[tmp[target_column] == val, feature_name],
                        y=tmp.loc[tmp[target_column] == val, 'count_objects'],
                        marker_color=COLOR_DISCRETE_SEQUENCE[i], name=str(val)
                    )
                    fig.add_trace(trace)
                fig.update_layout(yaxis_title='count')
        else:
            if target_type == 'num':
                fig = go.Figure()
                trace = go.Scatter(x=tmp.sample(2000, random_state=0)[feature_name],
                                   y=tmp.sample(2000, random_state=0)[target_column], mode='markers', marker_color=RED)
                fig.add_trace(trace)

                fig.update_layout(yaxis_title=target_column, xaxis_title=feature_name)

            else:
                fig = px.strip(tmp.sample(2000, random_state=0), x=target_column, y=feature_name,
                               color_discrete_sequence=COLOR_DISCRETE_SEQUENCE)
                fig.update_traces(marker=dict(size=2))
        feature_and_target_figure = json.loads(fig.to_json())
        return feature_and_target_figure

    def _plot_feature_and_target_2_df(self, reference_data: pd.DataFrame, current_data: pd.DataFrame,
                                      target_column: str, target_type: str, feature_name: str,
                                      feature_type: str) -> dict:
        tmp_ref = reference_data[[target_column, feature_name]].copy()
        tmp_curr = current_data[[target_column, feature_name]].copy()
        tmp_ref['df'] = 'reference'
        tmp_curr['df'] = 'current'
        if feature_type == 'cat':
            if target_type == 'num':
                tmp = (tmp_ref.loc[:, [feature_name, target_column, 'df']].sample(2000)
                       .append(tmp_curr.loc[:, [feature_name, target_column, 'df']].sample(2000)))
                fig = px.strip(tmp, x=feature_name, y=target_column, color='df', color_discrete_sequence=[GREY, RED])
                fig.update_traces(marker=dict(size=2))
                fig.update_layout(legend_title_text='')
            else:
                tmp_ref = self._transform_df_count_values(tmp_ref, target_column, feature_name)
                tmp_curr = self._transform_df_count_values(tmp_curr, target_column, feature_name)
                fig = make_subplots(rows=1, cols=2, shared_yaxes=True,
                                    subplot_titles=['reference', 'current'])

                for i, val in enumerate(tmp_ref[target_column].unique()):
                    trace = go.Bar(x=tmp_ref.loc[tmp_ref[target_column] == val, feature_name],
                                   y=tmp_ref.loc[tmp_ref[target_column] == val, 'count_objects'],
                                   marker_color=COLOR_DISCRETE_SEQUENCE[i], opacity=0.6, showlegend=False)
                    fig.append_trace(trace, 1, 1)
                for i, val in enumerate(tmp_curr[target_column].unique()):
                    trace = go.Bar(x=tmp_curr.loc[tmp_curr[target_column] == val, feature_name],
                                   y=tmp_curr.loc[tmp_curr[target_column] == val, 'count_objects'],
                                   marker_color=COLOR_DISCRETE_SEQUENCE[i], name=str(val))
                    fig.append_trace(trace, 1, 2)
                fig.update_layout(yaxis_title='count')
        else:
            if target_type == 'num':
                fig = make_subplots(rows=1, cols=2, shared_yaxes=True)
                trace = go.Scatter(x=tmp_ref.sample(2000, random_state=0)[feature_name],
                                   y=tmp_ref.sample(2000, random_state=0)[target_column], mode='markers',
                                   marker_color=GREY, name='reference')
                fig.append_trace(trace, 1, 1)
                trace = go.Scatter(x=tmp_curr.sample(2000, random_state=0)[feature_name],
                                   y=tmp_curr.sample(2000, random_state=0)[target_column], mode='markers',
                                   marker_color=RED, name="current")
                fig.append_trace(trace, 1, 2)
                fig.update_layout(yaxis_title=target_column)
                fig.update_xaxes(title_text=feature_name, row=1, col=1)
                fig.update_xaxes(title_text=feature_name, row=1, col=2)

            else:
                tmp = (tmp_ref.loc[:, [feature_name, target_column, 'df']].sample(2000)
                       .append(tmp_curr.loc[:, [feature_name, target_column, 'df']].sample(2000)))
                fig = px.strip(tmp, x=target_column, y=feature_name, color='df', color_discrete_sequence=[GREY, RED])
                fig.update_traces(marker=dict(size=2))
                fig.update_layout(legend_title_text='')
        feature_and_target_figure = json.loads(fig.to_json())
        return feature_and_target_figure

    def _transform_cat_features(self, reference_data: pd.DataFrame, current_data: Optional[pd.DataFrame],
                                cat_feature_names: List[str], target_column: Optional[str],
                                target_type: Optional[str]):
        if target_column and target_type == 'cat':
            cat_feature_names = cat_feature_names + [target_column]
        for feature_name in cat_feature_names:
            if reference_data[feature_name].nunique() > 6:
                cats = reference_data[feature_name].value_counts()[:5].index.astype(str)
                reference_data[feature_name] = reference_data[feature_name].apply(lambda x: x if x in cats else 'other')
                if current_data is not None:
                    current_data[feature_name] = current_data[feature_name].apply(lambda x: x if x in cats else 'other')

    def _choose_agg_period(self, date_column: str, reference_data: pd.DataFrame,
                           current_data: Optional[pd.DataFrame]) -> str:
        OPTIMAL_POINTS = 150
        prefix_dict = {'A': 'year', 'Q': 'quarter', 'M': 'month', 'W': 'week', 'D': 'day', 'H': 'hour'}
        datetime_feature = reference_data[date_column]
        if current_data is not None:
            datetime_feature = datetime_feature.append(current_data[date_column])
        days = (datetime_feature.max() - datetime_feature.min()).days
        time_points = pd.Series(index=['A', 'Q', 'M', 'W', 'D', 'H'],
                                data=[abs(OPTIMAL_POINTS - days / 365), abs(OPTIMAL_POINTS - days / 90),
                                      abs(OPTIMAL_POINTS - days / 30), abs(OPTIMAL_POINTS - days / 7),
                                      abs(OPTIMAL_POINTS - days), abs(OPTIMAL_POINTS - days * 24)])
        self.period_prefix = prefix_dict[time_points.idxmin()]
        return str(time_points.idxmin())
