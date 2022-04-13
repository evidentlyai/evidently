# Options for Color Schema changes

By default, Evidently widgets uses red-grey color scheme.

And, for example, Data Drift report looks like

![Data Drift](../../images/01\_data\_drift.png)

For changing colors in widgets you can create an object `ColorOptions` from `evidently.options.color_scheme`, replace values that you needed, and use it in options list when you create a dashboard.

```python
from evidently.options import ColorOptions
from evidently.dashboard import Dashboard
from evidently.dashboard.tabs import DataDriftTab

color_scheme = ColorOptions()
color_scheme.primary_color = "#5a86ad"
color_scheme.fill_color = "#fff4f2"
color_scheme.zero_line_color = "#016795"
color_scheme.current_data_color = "#c292a1" 
color_scheme.reference_data_color = "#017b92"

iris_data_drift_dashboard = Dashboard(tabs=[DataDriftTab()], options=[color_scheme])
```

And your reports will be looks like
![Data Drift](../../images/09\_color\_scheme\_example.png)

If you want just change main colors,

As values for the colors you can use CSS and Plotly compatible strings, for example:
- colors names: "blue", "orange", "green"
- RGB values: #fff4f2, #ee00aa

and so on.


## Available Options
List of all color scheme options with a type and meaning of each:
 
| Variable in ColorOptions object | Option type      | Option description                                                                                                                         |
|---------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| primary_color                   | string           | basic color for data visualization. Uses by default for all bars and lines for widgets with one dataset and as a default for current data. |
| secondary_color                 | string           | basic color for second data visualization if we have two data sets, for example, reference data                                            |
| current_data_color              | string           | color for all current data, by default primary color is used                                                                               |
| reference_data_color            | string           | color for reference data, by default secondary color is used                                                                               |
| color_sequence                  | array of strings | set of colors for drawing a number of lines in one graph, in for data quality, for example                                                 |
| fill_color                      | string           | fill color for areas in line graphs                                                                                                        |
| zero_line_color                 | string           | color for base, zero line in line graphs                                                                                                   |
| non_visible_color               | string           | color for technical, not visible dots or points for better scalability                                                                     |
| underestimation_color           | string           | color for underestimation line in regression                                                                                               |
| overestimation_color            | string           | color for overestimation line in regression                                                                                                |
| majority_color                  | string           | color for majority line in regression                                                                                                      |
--- 
