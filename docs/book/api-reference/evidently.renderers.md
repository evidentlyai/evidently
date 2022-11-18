# evidently.renderers package

## Submodules


### _class _ BaseRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `object`

Base class for all renderers


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; exception _: BaseException_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; options _: [DataDriftOptions](evidently.options.md#evidently.options.data_drift.DataDriftOptions)_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; different_missing_values _: Dict[Any, int]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_different_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_missing_values _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; number_of_rows _: int_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; share_of_missing_values _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; column_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_sequence _: Sequence[str]_ _ = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4')_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; current_data_color _: Optional[str]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; fill_color _: str_ _ = 'LightGreen'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; heatmap _: str_ _ = 'RdBu_r'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; majority_color _: str_ _ = '#1acc98'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; non_visible_color _: str_ _ = 'white'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; overestimation_color _: str_ _ = '#ee5540'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; primary_color _: str_ _ = '#ed0400'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; reference_data_color _: Optional[str]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; secondary_color _: str_ _ = '#4d4d4d'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; underestimation_color _: str_ _ = '#6574f7'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; vertical_lines _: str_ _ = 'green'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; zero_line_color _: str_ _ = 'green'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; categorical_features _: Optional[List[str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; datetime _: Optional[str]_ _ = 'datetime'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; datetime_features _: Optional[List[str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; id _: Optional[str]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; numerical_features _: Optional[List[str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; pos_label _: Optional[Union[str, int]]_ _ = 1_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; prediction _: Optional[Union[str, int, Sequence[str], Sequence[int]]]_ _ = 'prediction'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target _: Optional[str]_ _ = 'target'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; target_names _: Optional[List[str]]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; task _: Optional[str]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; generate_metrics(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData), columns: [DatasetColumns](evidently.utils.md#evidently.utils.data_operations.DatasetColumns))

#####&nbsp;&nbsp;&nbsp;&nbsp; get_target_prediction_data(data: DataFrame, column_mapping: [ColumnMapping](evidently.pipeline.md#evidently.pipeline.column_mapping.ColumnMapping))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; calculate(data: [InputData](evidently.metrics.md#evidently.metrics.base_metric.InputData))

#####&nbsp;&nbsp;&nbsp;&nbsp; get_current_data_color()

#####&nbsp;&nbsp;&nbsp;&nbsp; get_reference_data_color()

#####&nbsp;&nbsp;&nbsp;&nbsp; is_classification_task()

#####&nbsp;&nbsp;&nbsp;&nbsp; is_regression_task()

### _class _ DetailsInfo(title: str, info: evidently.model.widget.BaseWidgetInfo, id: str = <factory>)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; id _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; info _: BaseWidgetInfo_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

#### Methods: 

### _class _ MetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseRenderer`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj)

### _class _ RenderersDefinitions(typed_renderers: dict = <factory>, default_html_test_renderer: Optional[evidently.renderers.base_renderer.TestRenderer] = None, default_html_metric_renderer: Optional[evidently.renderers.base_renderer.MetricRenderer] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; default_html_metric_renderer _: Optional[MetricRenderer]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; default_html_test_renderer _: Optional[TestRenderer]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; typed_renderers _: dict_ 

#### Methods: 

### _class _ TestHtmlInfo(name: str, description: str, status: str, details: List[DetailsInfo], groups: Dict[str, str])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; description _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; details _: List[DetailsInfo]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; groups _: Dict[str, str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; status _: str_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; with_details(title: str, info: BaseWidgetInfo)

### _class _ TestRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseRenderer`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; html_description(obj)

#####&nbsp;&nbsp;&nbsp;&nbsp; json_description(obj)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_html(obj)

#####&nbsp;&nbsp;&nbsp;&nbsp; render_json(obj)

### default_renderer(wrap_type)

### _class _ ColumnDefinition(title: str, field_name: str, type: evidently.renderers.html_widgets.ColumnType = <ColumnType.STRING: 'string'>, sort: Optional[evidently.renderers.html_widgets.SortDirection] = None, options: Optional[dict] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; field_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; options _: Optional[dict]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; sort _: Optional[SortDirection]_ _ = None_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; type _: ColumnType_ _ = 'string'_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; as_dict()

### _class _ ColumnType(value)
Bases: `Enum`

An enumeration.


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; HISTOGRAM _ = 'histogram'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; LINE _ = 'line'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; SCATTER _ = 'scatter'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; STRING _ = 'string'_ 

#### Methods: 

### _class _ CounterData(label: str, value: str)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; label _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; value _: str_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; _static _ float(label: str, value: float, precision: int)
create CounterData for float value with given precision.

* **Parameters**

- **label** – counter label
- **value** – float value of counter
- **precision** – decimal precision


#####&nbsp;&nbsp;&nbsp;&nbsp; _static _ int(label: str, value: int)
create CounterData for int value.

* **Parameters**

- **label** – counter label
- **value** – int value


#####&nbsp;&nbsp;&nbsp;&nbsp; _static _ string(label: str, value: str)
create CounterData for string value with given precision.

* **Parameters**

- **label** – counter label
- **value** – string value of counter


### _class _ DetailsPartInfo(title: str, info: Union[BaseWidgetInfo, PlotlyGraphInfo])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; info _: Union[BaseWidgetInfo, PlotlyGraphInfo]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

#### Methods: 

### _class _ GraphData(title: str, data: dict, layout: dict)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; data _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; layout _: dict_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; _static _ figure(title: str, figure: Figure)
create GraphData from plotly figure itself
:param title: title of graph
:param figure: plotly figure for getting data from

### _class _ HeatmapData(name: str, matrix: pandas.core.frame.DataFrame)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; matrix _: DataFrame_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#### Methods: 

### _class _ HistogramData(name: str, x: list, y: List[Union[int, float]])
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; x _: list_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; y _: List[Union[int, float]]_ 

#### Methods: 

### _class _ RichTableDataRow(fields: dict, details: Optional[RowDetails] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; details _: Optional[RowDetails]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; fields _: dict_ 

#### Methods: 

### _class _ RowDetails(parts: Optional[List[DetailsPartInfo]] = None)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; parts _: List[DetailsPartInfo]_ 

#### Methods: 

#####&nbsp;&nbsp;&nbsp;&nbsp; with_part(title: str, info: Union[BaseWidgetInfo, PlotlyGraphInfo])

### _class _ SortDirection(value)
Bases: `Enum`

An enumeration.


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; ASC _ = 'asc'_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; DESC _ = 'desc'_ 

#### Methods: 

### _class _ TabData(title: str, widget: evidently.model.widget.BaseWidgetInfo)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; title _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; widget _: BaseWidgetInfo_ 

#### Methods: 

### _class _ WidgetSize(value)
Bases: `Enum`

An enumeration.


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; FULL _ = 2_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; HALF _ = 1_ 

#### Methods: 

### counter(\*, counters: List[CounterData], title: str = '', size: WidgetSize = WidgetSize.FULL)
generate widget with given counters


* **Parameters**

    - **title** – widget title

    - **counters** – list of counters in widget

    - **size** – widget size


### Example

```python
>>> display_counters = [CounterData("value1", "some value"), CounterData.float("float", 0.111, 2)]
>>> widget_info = counter(counters=display_counters, title="counters example")
```


### get_class_separation_plot_data(current_plot: DataFrame, reference_plot: Optional[DataFrame], target_name: str, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### get_heatmaps_widget(\*, title: str = '', primary_data: HeatmapData, secondary_data: Optional[HeatmapData] = None, size: WidgetSize = WidgetSize.FULL, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
Create a widget with heatmap(s)


### get_histogram_figure(\*, primary_hist: HistogramData, secondary_hist: Optional[HistogramData] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions), orientation: str = 'v')

### get_histogram_figure_with_quantile(\*, current: HistogramData, reference: Optional[HistogramData] = None, current_quantile: float, reference_quantile: Optional[float] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions), orientation: str = 'v')

### get_histogram_figure_with_range(\*, primary_hist: HistogramData, secondary_hist: Optional[HistogramData] = None, left: Union[float, int], right: Union[float, int], orientation: str = 'v', color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### get_histogram_for_distribution(\*, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)] = None, title: str = '', xaxis_title: Optional[str] = None, yaxis_title: Optional[str] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### get_pr_rec_plot_data(current_pr_curve: dict, reference_pr_curve: Optional[dict], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### get_roc_auc_tab_data(curr_roc_curve: dict, ref_roc_curve: Optional[dict], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))

### header_text(\*, label: str, title: str = '', size: WidgetSize = WidgetSize.FULL)
generate widget with some text as header


* **Parameters**

    - **label** – text to display

    - **title** – widget title

    - **size** – widget size



### histogram(\*, title: str, primary_hist: HistogramData, secondary_hist: Optional[HistogramData] = None, color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions), orientation: str = 'v', size: WidgetSize = WidgetSize.FULL, xaxis_title: Optional[str] = None, yaxis_title: Optional[str] = None)
generate widget with one or two histogram


* **Parameters**

    - **title** – widget title

    - **primary_hist** – first histogram to show in widget

    - **secondary_hist** – optional second histogram to show in widget

    - **orientation** – bars orientation in histograms

    - **color_options** – color options to use for widgets

    - **size** – widget size

    - **xaxis_title** – title for x-axis

    - **yaxis_title** – title for y-axis


### Example

```python
>>> ref_hist = HistogramData("Histogram 1", x=["a", "b", "c"], y=[1, 2, 3])
>>> curr_hist = HistogramData("Histogram 2", x=["a", "b", "c"], y=[3, 2 ,1])
>>> widget_info = histogram(
>>>     title="Histogram example",
>>>     primary_hist=ref_hist,
>>>     secondary_hist=curr_hist,
>>>     color_options=color_options
>>> )
```


### plotly_data(\*, title: str, data: dict, layout: dict, size: WidgetSize = WidgetSize.FULL)
generate plotly plot with given data and layout (can be generated from plotly).


* **Parameters**

    - **title** – widget title

    - **data** – plotly figure data

    - **layout** – plotly figure layout

    - **size** – widget size


### Example

```python
>>> figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
>>> f_dict = figure.to_plotly_json()
>>> widget_info = plotly_data(title="Some plot title", data=f_dict["data"], layout=f_dict["layout"])
```


### plotly_figure(\*, title: str, figure: Figure, size: WidgetSize = WidgetSize.FULL)
generate plotly plot based on given plotly figure object.


* **Parameters**

    - **title** – title of widget

    - **figure** – plotly figure which should be rendered as widget

    - **size** – size of widget, default to WidgetSize.FULL


### Example

```python
>>> bar_figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
>>> widget_info = plotly_figure(title="Bar plot widget", figure=bar_figure, size=WidgetSize.FULL)
```


### plotly_graph(\*, graph_data: GraphData, size: WidgetSize = WidgetSize.FULL)
generate plotly plot with given GraphData object.


* **Parameters**

    - **graph_data** – plot data for widget

    - **size** – size of widget to render


### Example

```python
>>> figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
>>> f_dict = figure.to_plotly_json()
>>> bar_graph_data = GraphData(title="Some plot title", data=f_dict["data"], layout=f_dict["layout"])
>>> widget_info = plotly_graph(graph_data=bar_graph_data, size=WidgetSize.FULL)
```


### plotly_graph_tabs(\*, title: str, figures: List[GraphData], size: WidgetSize = WidgetSize.FULL)
generate Tab widget with multiple graphs


* **Parameters**

    - **title** – widget title

    - **figures** – list of graphs with tab titles

    - **size** – widget size


### Example

```python
>>> bar_figure = go.Figure(go.Bar(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
>>> line_figure = go.Figure(go.Line(name="Bar plot", x=[1, 2, 3, 4], y=[10, 11, 20, 11]))
>>> widget_info = plotly_graph_tabs(
...     title="Tabbed widget",
...     figures=[GraphData.figure("Bar", bar_figure), GraphData.figure("Line", line_figure)],
... )
```


### rich_table_data(\*, title: str = '', size: WidgetSize = WidgetSize.FULL, rows_per_page: int = 10, columns: List[ColumnDefinition], data: List[RichTableDataRow])
generate widget with rich table: with additional column types and details for rows


* **Parameters**

    - **title** – widget title

    - **size** – widget size

    - **rows_per_page** – maximum number per page to show

    - **columns** – list of columns in table

    - **data** – list of dicts with data (key-value pairs, keys is according to ColumnDefinition.field_name)


### Example

```python
>>> columns_def = [
...     ColumnDefinition("Column A", "field_1"),
...     ColumnDefinition("Column B", "field_2", ColumnType.HISTOGRAM,
...                      options={"xField": "x", "yField": "y", "color": "#ed0400"}),
...     ColumnDefinition("Column C", "field_3", sort=SortDirection.ASC),
... ]
>>> in_table_data = [
...     RichTableDataRow(fields=dict(field_1="a", field_2=dict(x=[1, 2, 3], y=[10, 11, 3]), field_3="2")),
...     RichTableDataRow(
...         fields=dict(field_1="b", field_2=dict(x=[1, 2, 3], y=[10, 11, 3]), field_3="1"),
...         details=RowDetails()
...             .with_part("Some details", counter(counters=[CounterData("counter 1", "value")])
...         )
...     )
... ]
>>> widget_info = rich_table_data(title="Rich table", rows_per_page=10, columns=columns_def, data=in_table_data)
```


### table_data(\*, column_names: Iterable[str], data: Iterable[Iterable], title: str = '', size: WidgetSize = WidgetSize.FULL)
generate simple table with given columns and data


* **Parameters**

    - **column_names** – list of column names in display order

    - **data** – list of data rows (lists of object to show in table in order of columns), object will be converted to str

    - **title** – widget title

    - **size** – widget size


### Example

```python
>>> columns = ["Column A", "Column B"]
>>> in_table_data = [[1, 2], [3, 4]]
>>> widget_info = table_data(column_names=columns, data=in_table_data, title="Table")
```


### widget_tabs(\*, title: str = '', size: WidgetSize = WidgetSize.FULL, tabs: List[TabData])
generate widget with tabs which can contain any other widget.


* **Parameters**

    - **title** – widget title

    - **size** – widget size

    - **tabs** – list of TabData with widgets to include


### Example

```python
>>> columns = ["Column A", "Column B"]
>>> in_table_data = [[1, 2], [3, 4]]
>>> tab_data = [
...     TabData("Counters", counter(counters=[CounterData("counter", "value")], title="Counter")),
...     TabData("Table", table_data(column_names=columns, data=in_table_data, title="Table")),
... ]
>>> widget_info = widget_tabs(title="Tabs", tabs=tab_data)
```


### widget_tabs_for_more_than_one(\*, title: str = '', size: WidgetSize = WidgetSize.FULL, tabs: List[TabData])
Draw tabs widget only if there is more than one tab, otherwise just draw one widget


### determine_template(mode: str)

### get_distribution_plot_figure(\*, current_distribution: [Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution), reference_distribution: Optional[[Distribution](evidently.utils.md#evidently.utils.visualizations.Distribution)], color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions), orientation: str = 'v')

### plot_distr(\*, hist_curr, hist_ref=None, orientation='v', color_options: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions))
## Module contents
