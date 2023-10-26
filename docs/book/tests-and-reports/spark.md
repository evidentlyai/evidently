---
description: How to run calculations on Spark.
---

You can run distributed computation using Spark if you work with large datasets. 

# Supported metrics

Currently, the following metrics are supported: 
* `ColumnDriftMetric()`
* `DataDriftTable()`
  
For drift calculation, the following methods are supported:
* `chisquare`
* `jensen shannon`
* `psi`
* `wasserstein`

The following data types are supported:
* `numerical_features`
* `categorical_features`

# Code example

You can refer to an example How-to-notebook showing how to use Evidently on Spark:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_run_calculations_on_spark.ipynb" %}

# Run Evidently with Spark

To run Evidently on a Spark DataFrame, you need to specify the corresponding engine in the `run()` method for the Report calculation:

To import `SparkEngine` from Evidently, use the following command:  
```
from evidently.spark.engine import SparkEngine
```

Pass the `SparkEngine` to the `run` method when you create the Report: 

```
spark_report_table = Report(metrics=[
    DataDriftTable()
])
spark_report_table.run(reference_data=reference, current_data=current, engine=SparkEngine)

spark_report_table.show()  # OR spark_report_table.show(mode='inline')
```
Notebook example on setting Test criticality:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_specify_test_criticality.ipynb" %} 

