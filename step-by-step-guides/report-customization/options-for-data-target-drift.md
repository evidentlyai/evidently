---
description: You can modify certain options when calculating the Data and Target drift.
---

# Options for Data / Target drift

**An example of setting custom options in the Data Drift Report on California Housing Dataset:**

{% embed url="https://colab.research.google.com/drive/11tY2g-XbkZSLSqgyGBJ5ijVvyl1E2TpY?authuser=1" %}

You can set the custom options for the following Reports:&#x20;

* num\_target\_drift\_tab ([num-target-drift.md](../../reports/num-target-drift.md "mention"))
* cat\_target\_drift\_tab ( [categorical-target-drift.md](../../reports/categorical-target-drift.md "mention"))
* data\_drift\_tab ([data-drift.md](../../reports/data-drift.md "mention"))

## Available Options

You can specify the following parameters:

* **confidence**: _float_ or _dict\[str, float]._ Default = 0.95.&#x20;
  * Defines the confidence level for the statistical tests.
  * Applies to all features (if passed as _float_) or certain features (if passed as _dictionary_).&#x20;
* **drift\_share**: _float._ Default = 0.5.&#x20;
  * Sets the share of drifting features as a condition for Dataset Drift in the Data Drift report.&#x20;
* **nbinsx**: _int or dict\[str, int]._ Default = 10.&#x20;
  * Defines the number of bins in a histogram. &#x20;
  * Applies to all features (if passed as _int_) or certain features (if passed as _dictionary_).
* **xbins**: _dict\[str, int]._ Default = None.&#x20;
  * Defines the boundaries for the size of a specific bin in a histogram.&#x20;
* **feature\_stattest\_func**: _Callable_ or _Dict\[str, Callable_].  Default = None.
  * Defines a custom statistical test for drift detection in the Data Drift report.&#x20;
  * Applies to all features (if passed as a _functio_n) or individual features (if a _dictionary_).&#x20;
* **cat\_target\_stattest\_func**: _Callable._ Default = None.
  * Defines a custom statistical test to detect target drift in the Categorical Target Drift report.&#x20;
* **num\_target\_stattest\_func**: _Callable._ Default = None.
  * Defines a custom statistical test to detect target drift in the Numerical Target Drift report.&#x20;

### How to define Data/Target Drift options

1. Define a **DataDriftOptions** object**.** This is a single object for Data Drift and Target Drift Reports.

```python
options = DataDriftOptions(
                           num_target_stattest_func=anderson_stat_test, 
                           confidence=0.99, 
                           nbinsx={'MedInc':15, 'HouseAge': 25, 'AveRooms':20})
```

**Note:** when you pass the function as an argument it should satisfy two conditions:

* takes as an argument two DataFrame columns (series) - reference and production data
* returns a float - p\_value

2\. Pass it to the **Dashboard** class:

```
dashboard = Dashboard(tabs=[DataDriftTab(), NumTargetDriftTab()], 
options=[options])
```

### **Customization using CLI**

You can also set the options from the command-line interface. In this case, you cannot define the functions (e.g. change statistical tests). ****&#x20;

```json
"options": {
    "data_drift": {
      "confidence": 0.99,
      "drift_share": 0.5,
      "nbinsx": {
        "mean perimeter": 4,
        "mean symmetry": 4
      }
    }
  }
```

## Specific examples

The section below explains specific popular customizations in more detail.

### **1. Choose a different statistical test to detect Data Drift**

You can override the default statistical tests that Evidently uses in the [Data Drift report](../../reports/data-drift.md). &#x20;

To do that, set the following option:&#x20;

* **feature\_stattest\_func**: _Callable_ or _Dict\[str, Callable_]. &#x20;

This option can take a function or a dictionary as an argument.&#x20;

If you pass a **function**, this function will be used to detect drift **for all features**.&#x20;

If you pass a **dictionary**, the custom functions will be used for the **specified features**. The default Evidently tests would apply to the rest.

To add an alternative test, you need to **implement a function** that would return a float (p-value) after receiving two DataFrame columns that correspond to the reference and current datasets.&#x20;

```python
import numpy as np 
from scipy.stats import anderson_ksamp

def anderson_stat_test(reference_data: pd.DataFrame, current_data: pd.DataFrame):
    return anderson_ksamp(np.array([reference_data, current_data]))[2]
```

We suggest using statistical tests from [scipy](https://docs.scipy.org/doc/scipy/reference/stats.html#statistical-tests) or [statsmodels](https://www.statsmodels.org/stable/stats.html) or implementing your own.&#x20;

Then, define the **DataDriftOptions** object as shown above.

### **2. Set a custom Dataset Drift condition**

The [data-drift.md](../../reports/data-drift.md "mention") report contains a component that confirms whether the drift was detected on the Dataset level.&#x20;

To set custom drift conditions, you need to specify the following **options**:

* “**confidence**” - statistical test confidence level (default value 0.95; float or dict)
* “**drift\_share**” - share of the drifted features (default value 0.5; float)

**You can set the same confidence level for all features**. In this case, specify a float value for the "confidence" option. The Dataset Drift will be detected if the “**drift\_share**” share of the features drift at the defined “**confidence**” confidence level.&#x20;

**You can also set different confidence levels for different features**. In this case, you should pass a dictionary for the "confidence" option. A custom confidence level will be applied for the specified features. The rest will have the default confidence level = 0.95.

Then, define the **DataDriftOptions** object as shown above.

### 3. Customize the histogram plots&#x20;

You can customize how the distribution plots look for the individual features in the [Data Drift Report](../../reports/data-drift.md). It is helpful, for example, if you have NULL or other specific values and want to see them in a separate bin.

To customize the plots, specify the following **options**:

* “**nbinsx**” - to set the number of bins (default value = 10, integer or dictionary)
  * If you pass an integer value, the selected number of bins will apply to all features.
  * If you pass a dictionary, then specified features will have a custom number of bins. The rest will have the default number of bins = 10.
* “**xbins**” - to define the specific bin sizes (default value = none).&#x20;
  * Dict("start"=value, "end"=value, "size"=value) or [plotly.graph\_objects.histogram.XBins](https://plotly.github.io/plotly.py-docs/generated/plotly.graph\_objects.histogram.html#plotly.graph\_objects.histogram.XBins)

You can set different options for each feature. For example, you can specify “**nbinsx**” for one subset of the features, “**xbins**” for another, and apply defaults for the rest. [Here](https://github.com/evidentlyai/evidently/blob/main/evidently/examples/boston\_dataset\_drift\_with\_customized\_bins.ipynb) is an example.

Once you specify the options, define the **DataDriftOptions** object as shown above.

#### What these options change&#x20;

The Data Drift report has two sets of histograms:&#x20;

1. preview in the Data Drift table&#x20;
2. an interactive plot inside the Data Drift table that expands when you click on each feature.&#x20;

![](<../../.gitbook/assets/Screenshot 2021-09-07 at 23.54.08.png>)

Only “**nbinsx**”, if specified, impacts the **histogram previews** in the DataDrift table. In case you set both parameters, “**xbins**” will define the interactive plot, while “**nbinsx**” will affect the preview.&#x20;

Both “**nbinsx**” and “**xbins**” can influence how the **interactive plots** look inside the table. If you set one parameter, it will define the plot view. If you set both parameters, “**xbins**” will have a priority.&#x20;

##
