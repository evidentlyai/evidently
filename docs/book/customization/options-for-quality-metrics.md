# Quality Metrics Options

**An example of setting custom options in Data Drift and Probabilistic Classification Performance reports on Wine Quality Dataset:**
{% embed url="https://colab.research.google.com/drive/1W7l3iAILkMti-3qcBLrU5JrW24lSOMR3" %}

## Available Options

These options apply to different plots in the Evidently reports: Data Drift, Categorical Target Drift, Classification Performance, Probabilistic classification performance. 

You can specify the following parameters:

* **conf_interval_n_sigmas**: _int_ Default = 1.
  * Defines the width of confidence interval depicted on plots. Confidence level indicated in sigmas (standard deviation).
* **classification_threshold**: _float._ Default = 0.5.
  * Defines classification threshold for binary probabilistic classification.
* **cut_quantile**: _tuple[str, float]_ or _dict[str, tuple[str, float]._ Default = None.
  * Cut the data above the given quantile from the histogram plot if side parameter == _'right'_. 
  * Cut the data below the given quantile from the histogram plot if side parameter == _'left'_. 
  * Cut the data below the given quantile and above _1 - the given quantile_ from the histogram plot if side parameter == _'two-sided'_. 
  * Data used for metric calculation doesn't change. 
  * Applies to all features (if passed as _tuple_) or certain features (if passed as _dictionary_).

### How to define Quality Metrics Options

1\. Define a **QualityMetricsOptions** object.

```python
options = QualityMetricsOptions(
                           conf_interval_n_sigmas=3, 
                           classification_threshold=0.8, 
                           cut_quantile={'feature_1': ('left': 0.01), 'feature_2': 0.95, 'feature_3': 'two-sided': 0.05})
```

2\. Pass it to the **Dashboard** class:

```
dashboard = Dashboard(tabs=[DataDriftTab(), ProbClassificationPerformanceTab()], 
options=[options])
```
