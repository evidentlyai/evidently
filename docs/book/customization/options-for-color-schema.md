---
description: You can modify the colors in the Evidently Dashboards.
---

# Options for Color Schema 

By default, Evidently widgets use the red-grey color scheme.

For example, here is how the Data Drift report looks:

![Data Drift](../../images/01\_data\_drift.png)

To change the colors in the widgets, you can create an object `ColorOptions` from the `evidently.options.color_scheme`, replace the values you need, and use it in options list when you create a dashboard.

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
Here is an example of the report with the modified color schema:
![](<../.gitbook/assets/customization_color\_scheme\_example.png>)

To define values for the colors, you can use CSS and Plotly compatible strings. For example:
- colors names: "blue", "orange", "green"
- RGB values: #fff4f2, #ee00aa
and so on.

## Available Options
Here is the list of all color scheme options with the type and meaning of each:
 
| Variable in ColorOptions object | Option type      | Option description                                                                                                                         |
|---------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| primary_color                   | string           | A basic color for data visualization. Used by default for all bars and lines in widgets with one dataset. Used as the default for the current data in widgets with two datasets. |
| secondary_color                 | string           | A basic color to visualize the second dataset in the widgets with two datasets. For example, the reference data.                                            |
| current_data_color              | string           | A color for the current data. By default, the primary color is used.                                                                               |
| reference_data_color            | string           | A color for the reference data. By default, the secondary color is used.                                                                               |
| color_sequence                  | array of strings | A set of colors to draw a number of lines in one graph. For example, in the Data Quality dashboard.                                                 |
| fill_color                      | string           | A fill color for areas in line graphs.                                                                                                        |
| zero_line_color                 | string           | A color for base, zero line in line graphs.                                                                                                   |
| non_visible_color               | string           | A color for technical, not visible dots or points for better scalability.                                                                     |
| underestimation_color           | string           | A color for the "underestimation" line in the Regression Performance dashboard.                                                                                               |
| overestimation_color            | string           | A color for the "overestimation" line in Regression Performance dashboard.                                                                                                |
| majority_color                  | string           | A color for the majority line in the Regression Performance dashboard.                                                                                                      |
--- 
