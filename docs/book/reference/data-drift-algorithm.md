In some tests and metrics, Evidently uses the default Data Drift Detection algorithm. It helps detect the distribution drift in the individual features, prediction, or target. 

## How it works

Evidently compares the distributions of the values in a given column (or columns) of the two datasets. You should pass these datasets as **reference** and **current**. Evidently applies several statistical tests and metrics to detect if the distribution has changed significantly. It returns a "drift detected" or "not detected" result for each column.   

There is a default logic to choosing the appropriate drift test for each column. It is based on:

* column type: categorical, numerical or text data
* the number of observations in the reference dataset
* the number of unique values in the column (n\_unique)

For **small data with <= 1000 observations** in the reference dataset:

* For numerical columns (n\_unique \> 5): [two-sample Kolmogorov-Smirnov test](https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test).
* For categorical columns or numerical columns with n\_unique <= 5: [chi-squared test](https://en.wikipedia.org/wiki/Chi-squared_test).
* For binary categorical features (n\_unique <= 2): proportion difference test for independent samples based on Z-score.

All tests use a 0.95 confidence level by default.  

For **larger data with \> 1000 observations** in the reference dataset:

* For numerical columns (n\_unique \> 5):[Wasserstein Distance](https://en.wikipedia.org/wiki/Wasserstein_metric).
* For categorical columns or numerical with n\_unique <= 5):[Jensen--Shannon divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence).

All metrics use a threshold = 0.1 by default.  

{% hint style="info" %}
**You can always modify this drift detection logic**. You can select any of the statistical tests available in the library (including PSI, K-L divergence, Jensen-Shannon distance, Wasserstein distance, etc.), specify custom thresholds, or pass a custom test. You can read more about using [data drift parameters and available drift detection methods](../customization/options-for-statistical-tests.md).
{% endhint %}

For **text data**:

* Text content drift using a **domain classifier**. Evidently trains a binary classification model to discriminate between data from reference and current distributions. 

<details>
<summary>Text content drift detection method</summary>
The drift score, in this case, is the ROC-AUC score of the domain classifier computed on a validation dataset. To ensure the result is statistically meaningful, we repeat the calculation 1000 times with randomly assigned target class probabilities. This produces a distribution with a mean of 0,5. We then take the 95th percentile (default) of this distribution and compare it to the ROC-AUC score of the classifier. If the classifier score is higher, we consider the data drift to be detected. You can also set a different percentile as a parameter.
</details>

## Dataset-level drift

The method above calculates drift for each column individually.   

To detect dataset-level drift, you can set a rule on top of the individual feature results. For example, you can declare dataset drift if at least 50% of all features (columns) drifted or if ⅓ of the most important features drifted. Some of the Evidently tests and presets include such defaults. You can always modify them and set custom parameters.

## Nulls in the input data 

### Empty columns 

To evaluate data or prediction drift in the dataset, you need to ensure that the columns you test for drift are not empty. If these columns are empty in either reference or current data, Evidently will not calculate distribution drift and will raise an error.

### Rows with empty values 

Evidently applies the following pre-processing before calculating the drift metric or test:
- Filters out rows with infinite values `(+- np.inf)`
- Filters out rows with nulls 

By default, drift tests do not react to changes or increases in the number of empty values. Drift calculations only consider complete rows.

Since the high number of nulls can be an important indicator, we recommend grouping the data drift tests (that check for distribution shift) with data integrity tests (that check for a share of nulls). You can choose from several null-related [tests](all-tests.md#data-integrity) and metrics and set a thresholds.

## Resources

To build up a better intuition for which tests are better in different kinds of use cases, you can read our in-depth blog with experimental code:   

[Which test is the best? We compared 5 methods to detect data drift on large datasets](https://evidentlyai.com/blog/data-drift-detection-large-datasets).  

Additional links:  

* [How to interpret data and prediction drift together? ](https://evidentlyai.com/blog/data-and-prediction-drift)  

* [Do I need to monitor data drift if I can measure the ML model quality?](https://evidentlyai.com/blog/ml-monitoring-do-i-need-data-drift)  

* ["My data drifted. What's next?" How to handle ML model drift in production.](https://evidentlyai.com/blog/ml-monitoring-data-drift-how-to-handle)  

* [What is the difference between outlier detection and data drift detection?](https://evidentlyai.com/blog/ml-monitoring-drift-detection-vs-outlier-detection)
