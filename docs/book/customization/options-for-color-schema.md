---
description: You can modify the colors in the Reports and Tests.
---

# Code example

You can refer to an example How-to-notebook showing how to customize the color schema in your reports and test suites:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_customize_color_schema.ipynb" %}

# Options for Color Scheme 

By default, Evidently widgets use the red-grey color scheme. However, you can either define individual colors or take advantage of preconfigured color schemes.

## Change individual colors
To change the colors in the widgets, you can create an object `ColorOptions` from the `evidently.options.color_scheme`, replace the values you need, and use it in the options list when you create a report or test suite.

```python
from evidently.options import ColorOptions

color_scheme = ColorOptions(
    color_scheme.primary_color = "#5a86ad"
    color_scheme.fill_color = "#fff4f2"
    color_scheme.zero_line_color = "#016795"
    color_scheme.current_data_color = "#c292a1" 
    color_scheme.reference_data_color = "#017b92"
)
```

To define values for the colors, you can use CSS and Plotly compatible strings. For example:
- color names: "blue", "orange", "green"
- RGB values: #fff4f2, #ee00aa
and so on.

Here is the list of all color scheme options with the type and meaning of each:

| A Variable in the ColorOptions object | Option type      | Option description                                                                                                                         |
|---------------------------------|------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| primary_color                   | string           | A basic color for data visualization. Used by default for all bars and lines in widgets with one dataset. Used as the default for the current data in widgets with two datasets. |
| secondary_color                 | string           | A basic color to visualize the second dataset in the widgets with two datasets. For example, the reference data.                                            |
| current_data_color              | string           | A color for the current data. By default, the primary color is used.                                                                               |
| reference_data_color            | string           | A color for the reference data. By default, the secondary color is used.                                                                               |
| color_sequence                  | array of strings | A set of colors to draw a number of lines in one graph. For example, in the Data Quality dashboard.                                                 |
| fill_color                      | string           | A fill color for areas in line graphs.                                                                                                        |
| zero_line_color                 | string           | A color for the base, zero line in line graphs.                                                                                                   |
| non_visible_color               | string           | A color for technical, not visible dots or points for better scalability.                                                                     |
| underestimation_color           | string           | A color for the "underestimation" line in the Regression Performance dashboard.                                                                                               |
| overestimation_color            | string           | A color for the "overestimation" line in the Regression Performance dashboard.                                                                                                |
| majority_color                  | string           | A color for the majority line in the Regression Performance dashboard.                                                                                                      |
| vertical_lines                  | string           | A color for vertical lines.                                                                                                      |
| heatmap                  | string           | Colors for heatmaps.                                                                                                      |
---


## Use existing color schemes

Evidently also provides some sensible alternative default schemas that have been pre-selected for your convenience:

- 'Solarised'
- 'Karachi Sunrise'
- 'Berlin Autumn'
- 'Nightowl'

To use them, simply import them directly and pass them into your `Report` or `TestSuite` options as follows (taking the Berlin Autumn scheme as an example):

```python
from evidently.options import BERLIN_AUTUMN_COLOR_OPTIONS
```


## Customize color in Reports
For example, here is how the Data Drift Report looks without customizing the color:

![Data Drift](../../images/01\_data\_drift.png)

Either pass the above defined `color_scheme` to `options` of your `Report`:
```python
from evidently.report import Report
from evidently.metric_preset.data_drift import DataDriftPreset

# import the data as usual...
data_drift_report = Report(
    metrics=[DataDriftPreset()], 
    options=[color_scheme]
)

data_drift_report.run(iris_ref, iris_cur)
```
Here is an example of the report with the modified color scheme:
![](<../.gitbook/assets/customization_color\_scheme\_example.png>)

Or pass one of the preconfigured schemes to your `Report`:
```python
data_drift_report = Report(
    metrics=[DataDriftPreset()], 
    options=[BERLIN_AUTUMN_COLOR_OPTIONS]
)

data_drift_report.run(iris_ref, iris_cur)

data_drift_report.save_html("output.html")
```

## Customize color in Test Suites
Either pass the above defined `color_scheme` to `options` of your `TestSuite`:
```python
from evidently.test_preset import DataDriftTestPreset

# import the data as usual...
data_drift_dataset_tests = TestSuite(
    tests=[DataDriftTestPreset()], 
    options=[color_scheme]
)

data_drift_dataset_tests.run(reference_data=iris_ref, current_data=iris_cur)
data_drift_dataset_tests
```

Or pass one of the preconfigured schemes to your `TestSuite`:
```python
data_drift_dataset_tests = TestSuite(
    tests=[DataDriftTestPreset()], 
    options=[BERLIN_AUTUMN_COLOR_OPTIONS]
)

data_drift_dataset_tests.run(reference_data=iris_ref, current_data=iris_cur)
data_drift_dataset_tests
```