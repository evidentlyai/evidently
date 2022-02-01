---
description: You can create a new Widget and/or a new Tab.
---

# Add a custom Widget or Tab

You can add a new **Widget**, e.g. to visualize a metric that Evidently does not provide. You can also create a **Tab** by combining existing and custom widgets to get a new Dashboard and HTML report.

**Example 1 (California Housing, PSI metric for Data Drift).** Refer to it to reproduce and explore the implementation of a custom Widget and a Tab on your own:

{% embed url="https://colab.research.google.com/drive/1ROOpbUD7cQ9al9yQ3wJ_yMSzEdCVFsDT?usp=sharing" %}

Below is a step-by-step guide with a simplified example.

### Create your own Widget

To create a new Widget, you should create a class derived from our base class: [https://github.com/evidentlyai/evidently/blob/main/src/evidently/dashboard/widgets/widget.py](../../../../src/evidently/dashboard/widgets/widget.py)

Then you need to modify the **calculate** method. It takes as arguments `reference` data, `current` data, and `column_mapping`. Your Widget can use any information from these variables.

Here is an instruction on how to create a simple Widget with the information about the target distribution on reference and current data. &#x20;

**Example 2 (California Housing, Simple Widget and Tab):**

{% embed url="https://colab.research.google.com/drive/1d8kmGjlOsr5cr_Wl9In-CZwxyO5G4bRE?usp=sharing" %}

1. **We make a prototype of our Widget in Jupyter Notebook.** Using Plotly, we create a graph that we want to see in the Dashboard.&#x20;

```python
import plotly.figure_factory as ff
hist_data = [ref_data[target], prod_data[target]]
group_labels = ['reference', 'production']
colors = ['#333F44', '#37AA9C'] 
fig = ff.create_distplot(hist_data, group_labels, colors=colors, show_hist=False, show_rug=False)
fig.update_layout(     
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
```

![](<../../.gitbook/assets/image (5).png>)

**2. Now we need to write a class for our Widget**.&#x20;

Create a new Python file. Copy the code from [https://github.com/evidentlyai/evidently/blob/main/src/evidently/dashboard/widgets/reg_pred_and_actual_in_time_widget.py](../../../../src/evidently/dashboard/widgets/reg_pred_and_actual_in_time_widget.py) - we will use it as starting point and edit to create a custom implementation.&#x20;

We start from imports. We change the Plotly import, remove analyzer import, and the default colors:


![](<../.gitbook/assets/image (8).png>)

Then, we remove the arguments that we don’t need from the `init` function. We remove the `analyzers` function because we don't use its result in the custom Widget.

![](<../.gitbook/assets/image (9).png>)

Next, we remove everything from the **calculate** method until the JSON and return section. We then paste the code for the custom plot we created earlier from the Jupyter notebook.&#x20;

**Tip:** don't forget to replace the DataFrame names!

![](<../.gitbook/assets/image (13).png>)

Finally, we fix the JSON conversion and return sections:

![](<../.gitbook/assets/image (4).png>)

That’s it!&#x20;

Now you can put this file from where you can import the module, and paste it into the Evidently tab like this:

```
from my_widgets.target_distribution_widget import TargetDistributionWidget
dashboard = Dashboard(tabs=[RegressionPerformanceTab(include_widgets=[
    'Current: Predicted vs Actual',
    TargetDistributionWidget('Target distribution')
])])
dashboard.calculate(ref_data.sample(1000, random_state=0), 
                    prod_data.sample(1000, random_state=0), 
                    column_mapping=column_mapping)
dashboard.show()
```

![](<../.gitbook/assets/image (3).png>)

### Create your own Tab

Creating a custom Tab is even easier. You need to create a class derived from the base class: [https://github.com/evidentlyai/evidently/blob/main/src/evidently/dashboard/tabs/base_tab.py](../../../../src/evidently/dashboard/tabs/base_tab.py)

Again, let's take an existing Evidently tab as an example and change it.

Just import the custom widgets and list them in the attribute "**widgets"**. You can specify the "**verbose"** parameter to have an option to adjust the tab composition.&#x20;

![](<../.gitbook/assets/image (11).png>)

To generate the report, run these commands:

```
from my_tabs.my_simple_tab import MySimpleTab
dashboard = Dashboard(tabs=[MySimpleTab()])
dashboard.calculate(ref_data.sample(1000, random_state=0), 
                    prod_data.sample(1000, random_state=0), 
                    column_mapping=column_mapping)
                    
dashboard.show()
```

![](<../.gitbook/assets/image (15).png>)
