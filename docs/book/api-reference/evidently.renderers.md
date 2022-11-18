# evidently.renderers package

## Submodules


### _class _ BaseRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `object`

Base class for all renderers


#### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

### _class _ DetailsInfo(title: str, info: evidently.model.widget.BaseWidgetInfo, id: str = <factory>)
Bases: `object`


#### id _: str_ 

#### info _: BaseWidgetInfo_ 

#### title _: str_ 

### _class _ MetricRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseRenderer`


#### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### render_html(obj)

#### render_json(obj)

### _class _ RenderersDefinitions(typed_renderers: dict = <factory>, default_html_test_renderer: Optional[evidently.renderers.base_renderer.TestRenderer] = None, default_html_metric_renderer: Optional[evidently.renderers.base_renderer.MetricRenderer] = None)
Bases: `object`


#### default_html_metric_renderer _: Optional[MetricRenderer]_ _ = None_ 

#### default_html_test_renderer _: Optional[TestRenderer]_ _ = None_ 

#### typed_renderers _: dict_ 

### _class _ TestHtmlInfo(name: str, description: str, status: str, details: List[DetailsInfo], groups: Dict[str, str])
Bases: `object`


#### description _: str_ 

#### details _: List[DetailsInfo]_ 

#### groups _: Dict[str, str]_ 

#### name _: str_ 

#### status _: str_ 

#### with_details(title: str, info: BaseWidgetInfo)

### _class _ TestRenderer(color_options: Optional[[ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)] = None)
Bases: `BaseRenderer`


#### color_options _: [ColorOptions](evidently.options.md#evidently.options.color_scheme.ColorOptions)_ 

#### html_description(obj)

#### json_description(obj)

#### render_html(obj)

#### render_json(obj)

### default_renderer(wrap_type)

### _class _ ColumnDefinition(title: str, field_name: str, type: evidently.renderers.html_widgets.ColumnType = <ColumnType.STRING: 'string'>, sort: Optional[evidently.renderers.html_widgets.SortDirection] = None, options: Optional[dict] = None)
Bases: `object`


#### as_dict()

#### field_name _: str_ 

#### options _: Optional[dict]_ _ = None_ 

#### sort _: Optional[SortDirection]_ _ = None_ 

#### title _: str_ 

#### type _: ColumnType_ _ = 'string'_ 

### _class _ ColumnType(value)
Bases: `Enum`

An enumeration.


#### HISTOGRAM _ = 'histogram'_ 

#### LINE _ = 'line'_ 

#### SCATTER _ = 'scatter'_ 

#### STRING _ = 'string'_ 

### _class _ CounterData(label: str, value: str)
Bases: `object`


#### _static _ float(label: str, value: float, precision: int)
create CounterData for float value with given precision.


* **Parameters**

    - **label** – counter label

    - **value** – float value of counter

    - **precision** – decimal precision



#### _static _ int(label: str, value: int)
create CounterData for int value.


* **Parameters**

    - **label** – counter label

    - **value** – int value



#### label _: str_ 

#### _static _ string(label: str, value: str)
create CounterData for string value with given precision.


* **Parameters**

    - **label** – counter label

    - **value** – string value of counter



#### value _: str_ 

### _class _ DetailsPartInfo(title: str, info: Union[BaseWidgetInfo, PlotlyGraphInfo])
Bases: `object`


#### info _: Union[BaseWidgetInfo, PlotlyGraphInfo]_ 

#### title _: str_ 

### _class _ GraphData(title: str, data: dict, layout: dict)
Bases: `object`


#### data _: dict_ 

#### _static _ figure(title: str, figure: Figure)
create GraphData from plotly figure itself
:param title: title of graph
:param figure: plotly figure for getting data from


#### layout _: dict_ 

#### title _: str_ 

### _class _ HeatmapData(name: str, matrix: pandas.core.frame.DataFrame)
Bases: `object`


#### matrix _: DataFrame_ 

#### name _: str_ 

### _class _ HistogramData(name: str, x: list, y: List[Union[int, float]])
Bases: `object`


#### name _: str_ 

#### x _: list_ 

#### y _: List[Union[int, float]]_ 

### _class _ RichTableDataRow(fields: dict, details: Optional[RowDetails] = None)
Bases: `object`


#### details _: Optional[RowDetails]_ 

#### fields _: dict_ 

### _class _ RowDetails(parts: Optional[List[DetailsPartInfo]] = None)
Bases: `object`


#### parts _: List[DetailsPartInfo]_ 

#### with_part(title: str, info: Union[BaseWidgetInfo, PlotlyGraphInfo])

### _class _ SortDirection(value)
Bases: `Enum`

An enumeration.


#### ASC _ = 'asc'_ 

#### DESC _ = 'desc'_ 

### _class _ TabData(title: str, widget: evidently.model.widget.BaseWidgetInfo)
Bases: `object`


#### title _: str_ 

#### widget _: BaseWidgetInfo_ 

### _class _ WidgetSize(value)
Bases: `Enum`

An enumeration.


#### FULL _ = 2_ 

#### HALF _ = 1_ 

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
