# evidently.model package

## Submodules

## evidently.model.dashboard module


### _class_ evidently.model.dashboard.DashboardInfo(name: str, widgets: List[evidently.model.widget.BaseWidgetInfo])
Bases: `object`


#### name(_: st_ )

#### widgets(_: List[BaseWidgetInfo_ )
## evidently.model.widget module


### _class_ evidently.model.widget.AdditionalGraphInfo(id: str, params: Any)
Bases: `object`


#### id(_: st_ )

#### params(_: An_ )

### _class_ evidently.model.widget.Alert(value: Union[str, int, float], state: str, text: str, longText: str)
Bases: `object`


#### longText(_: st_ )

#### state(_: st_ )

#### text(_: st_ )

#### value(_: Union[str, int, float_ )

### _class_ evidently.model.widget.AlertStats(active: int, triggered: TriggeredAlertStats)
Bases: `object`


#### active()
Number of active alerts.


* **Type**

    int



#### eggs()
An integer count of the eggs we have laid.


#### active(_: in_ )

#### triggered(_: TriggeredAlertStat_ )

### _class_ evidently.model.widget.BaseWidgetInfo(type: str, title: str, size: int, id: str = <factory>, details: str = '', alertsPosition: Optional[str] = None, alertStats: Optional[evidently.model.widget.AlertStats] = None, params: Any = None, insights: Iterable[evidently.model.widget.Insight] = (), additionalGraphs: Iterable[Union[evidently.model.widget.AdditionalGraphInfo, ForwardRef('BaseWidgetInfo'), evidently.model.widget.PlotlyGraphInfo]] = (), alerts: Iterable[evidently.model.widget.Alert] = (), tabs: Iterable[ForwardRef('TabInfo')] = (), widgets: Iterable[ForwardRef('BaseWidgetInfo')] = (), pageSize: int = 5)
Bases: `object`


#### additionalGraphs(_: Iterable[Union[AdditionalGraphInfo, BaseWidgetInfo, PlotlyGraphInfo]_ _ = (_ )

#### alertStats(_: Optional[AlertStats_ _ = Non_ )

#### alerts(_: Iterable[Alert_ _ = (_ )

#### alertsPosition(_: Optional[str_ _ = Non_ )

#### details(_: st_ _ = '_ )

#### get_additional_graphs()

#### id(_: st_ )

#### insights(_: Iterable[Insight_ _ = (_ )

#### pageSize(_: in_ _ = _ )

#### params(_: An_ _ = Non_ )

#### size(_: in_ )

#### tabs(_: Iterable[TabInfo_ _ = (_ )

#### title(_: st_ )

#### type(_: st_ )

#### widgets(_: Iterable[BaseWidgetInfo_ _ = (_ )

### _class_ evidently.model.widget.Insight(title: str, severity: str, text: str)
Bases: `object`


#### title()
Insight title


* **Type**

    str



#### severity()
Severity level for insight information (one of ‘info’, ‘warning’, ‘error’, ‘success’)


* **Type**

    str



#### text()
Insidght information


* **Type**

    str



#### severity(_: st_ )

#### text(_: st_ )

#### title(_: st_ )

### _class_ evidently.model.widget.PlotlyGraphInfo(data: Any, layout: Any, id: str = <factory>)
Bases: `object`


#### data(_: An_ )

#### id(_: st_ )

#### layout(_: An_ )

### _class_ evidently.model.widget.TabInfo(id: str, title: str, widget: evidently.model.widget.BaseWidgetInfo)
Bases: `object`


#### id(_: st_ )

#### title(_: st_ )

#### widget(_: BaseWidgetInf_ )

### _class_ evidently.model.widget.TriggeredAlertStats(period: int, last_24h: int)
Bases: `object`


#### last_24h(_: in_ )

#### period(_: in_ )

### _class_ evidently.model.widget.WidgetType(value)
Bases: `Enum`

An enumeration.


#### BIG_GRAPH(_ = 'big_graph_ )

#### BIG_TABLE(_ = 'big_table_ )

#### COUNTER(_ = 'counter_ )

#### RICH_DATA(_ = 'rich_data_ )

#### TABBED_GRAPH(_ = 'tabbed_graph_ )

#### TABLE(_ = 'table_ )

#### TABS(_ = 'tabs_ )
## Module contents
