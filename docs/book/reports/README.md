---
description: What each report contains and how and when to use them.
---

# Reports

Evidently includes a set of pre-built Reports. Each of them addresses a specific aspect of the data or model performance. You can think of reports as combinations of the metrics and statistical tests that are grouped together.  

The calculation results can be available in one of the following formats:

* An interactive visual **Dashboard** displayed inside the Jupyter notebook.
* An **HTML report.** Same as dashboard, but available as a standalone file.
* A **JSON profile.** A summary of the metrics, the results of statistical tests, and simple histograms.

## Reports by type

Evidently currently works with **tabular data**. 7 reports are available. You can combine, customize the reports or contribute your own report. 

## Data Drift and Quality

[Data Drift](data-drift.md): detects changes in feature distribution. [Data Quality](data-quality.md): provides the feature overview.

![Data Drift](../../images/01\_data\_drift.png) ![Data Quality](../../images/07\_data\_quality.png)

## Categorical and Numerical Target Drift

Detect changes in [Numerical](num-target-drift.md) or [Categorical](categorical-target-drift.md) target and feature behavior.

![Categorical target drift](../../images/02\_cat\_target\_drift.png) ![Numerical target drift](../../images/03\_num\_target\_drift.png)

## Classification Performance

Analyzes the performance and errors of a [Classification](classification-performance.md) or [Probabilistic Classification](probabilistic-classification-performance.md) model. Works both for binary and multi-class.

![Classification Performance](../../images/05\_class\_performance.png) ![Probabilistic Classification Performance](../../images/06\_prob\_class\_performance.png)

## Regression Performance

Analyzes the performance and errors of a [Regression](reg-performance.md) model. Time series version coming soon.

![Regression Performance](../../images/04\_reg\_performance.png) ![Time Series](../../images/08\_time\_series.png)


{% content-ref url="data-drift.md" %}
[data-drift.md](data-drift.md)
{% endcontent-ref %}

{% content-ref url="data-quality.md" %}
[data-quality.md](data-quality.md)
{% endcontent-ref %}

{% content-ref url="categorical-target-drift.md" %}
[categorical-target-drift.md](categorical-target-drift.md)
{% endcontent-ref %}

{% content-ref url="num-target-drift.md" %}
[num-target-drift.md](num-target-drift.md)
{% endcontent-ref %}

{% content-ref url="reg-performance.md" %}
[reg-performance.md](reg-performance.md)
{% endcontent-ref %}

{% content-ref url="classification-performance.md" %}
[classification-performance.md](classification-performance.md)
{% endcontent-ref %}

{% content-ref url="probabilistic-classification-performance.md" %}
[probabilistic-classification-performance.md](probabilistic-classification-performance.md)
{% endcontent-ref %}

## Show me the code

If you want to see the code, go straight to [examples](../get-started/examples.md).
