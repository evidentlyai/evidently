---
description: You can modify certain options when calculating the Data and Target drift.
---

# Quality Metrics Options

**An example of setting custom options in Data Drift and Probabilistic Classification Performance reports on Wine Quality Dataset:**

## Available Options

You can specify the following parameters:

* **conf_interval_n_sigmas**: _int_ Default = 1.&#x20;
  * Defines the width of confidence interval depicted on plots. Confidence level indicated in sigmas (standard deviation).
* **classification_threshold**: _float._ Default = 0.5.&#x20;
  * Defines classification threshold for binary probabilistic classification.&#x20;
* **cut_quantile**: _tuple[str, float]_ or _dict[str, tuple[str, float]._ Default = None.&#x20;
  * Cut the data above the given quantile from the histogram plot if side parameter == _'right'_. 
  * Cut the data below the given quantile from the histogram plot if side parameter == _'left'_. 
  * Cut the data below the given quantile and above _1 - the given quantile_ from the histogram plot if side parameter == _'two-sided'_. 
  * Data used for metric calculation doesn't change. &#x20;
  * Applies to all features (if passed as _tuple_) or certain features (if passed as _dictionary_).

### How to define Data/Target Drift options
