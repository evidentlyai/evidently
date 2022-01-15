# What is Evidently?

## What is it?

Evidently helps **evaluate** and **monitor** machine learning models in production. It generates interactive reports or JSON profiles from pandas `DataFrames`or `csv` files.&#x20;

You can use **visual reports** for ad hoc analysis, debugging and team sharing, and **JSON profiles** to integrate Evidently in prediction pipelines or with other visualization tools.

Evidently currently works with **tabular data**. 6 reports are available.

### [1. Data Drift](reports/data-drift.md)

Detects changes in feature distribution.

![Part of the Data Drift Report.](.gitbook/assets/evidently\_github.png)

### [2. Numerical Target Drift](reports/num-target-drift.md)

Detects changes in numerical target and feature behavior.

![Part of the Target Drift Report.](.gitbook/assets/evidently\_num\_target\_drift\_github.png)

### [3. Categorical Target Drift](reports/categorical-target-drift.md)

Detects changes in categorical target and feature behavior.

![Part of the Categorical Target Drift Report.](.gitbook/assets/evidently\_cat\_target\_drift\_github.png)

### [4. Regression Model Performance](reports/reg-performance.md)

Analyzes the performance of a regression model and model errors.

![Part of the Regression Model Performance Report.](.gitbook/assets/evidently\_regression\_performance\_report\_github.png)

### [5. Classification Model Performance](reports/classification-performance.md)

Analyzes the performance and errors of a classification model. Works both for binary and multi-class models.

![Part of the Classification Model Performance Report.](.gitbook/assets/evidently\_classification\_performance\_report\_github.png)

### [6. Probabilistic Classification Model Performance](reports/probabilistic-classification-performance.md)

Analyzes the performance of a probabilistic classification model, quality of the model calibration, and model errors. Works both for binary and multi-class models.

![Part of the Probabilstic Classification Model Performance Report.](.gitbook/assets/evidently\_prob\_classification\_performance\_report\_github.png)

{% content-ref url="(get-started/install-evidently.md" %}
[install-evidently.md](get-started/install-evidently.md)
{% endcontent-ref %}

{% content-ref url="get-started/quick-start.md" %}
[quick-start.md](quick-start.md)
{% endcontent-ref %}

{% content-ref url="examples.md" %}
[examples.md](get-started/examples.md)
{% endcontent-ref %}



