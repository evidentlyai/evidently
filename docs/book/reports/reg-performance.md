**TL;DR:** You can monitor and analyze the performance of a regression model. 

For Reports, use `RegressionPreset`. For Test Suites, use `RegressionTestPreset`.

# Use case

These presets help evaluate and test the quality of classification models. You can use them in different scenarios.

**1. To monitor the performance of a regression model in production.** You can run the test suite as a regular job (e.g., weekly or every time you get the labels) to contrast the model performance against expectation. You can generate visual reports for documentation and sharing with stakeholders.

**2. To trigger or decide on the model retraining.** You can use the test suite to check if the model performance is below the threshold to initiate a model update. 

**3. To debug or improve model performance.** If you detect a quality drop, you can use the visual report to explore the model errors. You can use the Error Bias table to identify the groups that contribute way more to the total error, or where the model under- or over-estimates the target function. By manipulating the input data frame, you can explore how the model performs on different data segments (e.g., users from a specific region). You can also combine it with the [Data Drift](data-drift.md) report.

**4. To analyze the results of the model test.** You can explore the results of an online or offline test and contrast it to the performance in training. Though this is not the primary use case, you can use this report to compare the model performance in an A/B test or during a shadow model deployment.

# Regression Performance Report

If you want to visually explore the model performance, create a new Report object and include the `RegressionPreset`.

## Code example

```python
reg_performance_report = Report(metrics=[
    RegressionPreset(),
])

ref_performance_report.run(reference_data=ref, current_data=bcur)

reg_performance_report
```

## How it works

The **Regression Performance** report evaluates the quality of a regression model.

It can also compare it to the past performance of the same model, or the performance of an alternative model.

* Works for a **single model** or helps compare the **two**
* Displays a variety of plots related to the **performance** and **errors**
* Helps explore areas of **under-** and **overestimation**

## Data Requirements

To run this report, you need to have input features, and **both target and prediction** columns available. Input features are optional. Pass them if you want to explore the relations between features and target.

To generate a comparative report, you will need **two** datasets. The **reference** dataset serves as a benchmark. Evidently analyzes the change by comparing the **current** production data to the **reference** data.

![](<../.gitbook/assets/two\_datasets\_regression (1).png>)

You can also run this report for a **single** dataset, with no comparison performed. 

## How it looks

The report includes multiple components. All plots are interactive.

### **1. Model Quality Summary Metrics**

Evidently calculate a few standard model quality metrics: Mean Error (ME), Mean Absolute Error (MAE), Mean Absolute Percentage Error (MAPE).

![](<../.gitbook/assets/reg\_perf\_model\_quality\_summary (1).png>)

For each quality metric, Evidently also shows one standard deviation of its value (in brackets) to estimate the stability of the performance.

**To support the model performance analysis, Evidently also generates interactive visualizations. They help analyze where the model makes mistakes and come up with improvement ideas.**

### 2. **Predicted vs Actual**

Predicted versus actual values in a scatter plot.

![](<../.gitbook/assets/reg\_perf\_predicted\_actual (1).png>)

### 3. **Predicted vs Actual in Time**

Predicted and Actual values over time or by index, if no datetime is provided.

![](<../.gitbook/assets/reg\_perf\_predicted\_actual\_in\_time (1) (1).png>)

### 4. Error (Predicted - Actual)

Model error values over time or by index, if no datetime is provided.

![](<../.gitbook/assets/reg\_perf\_error (1).png>)

### 5. Absolute Percentage Error

Absolute percentage error values over time or by index, if no datetime is provided.

![](../.gitbook/assets/reg\_perf\_abs\_per\_error.png)

### 6. Error Distribution

Distribution of the model error values.

![](<../.gitbook/assets/reg\_perf\_error\_distribution (1).png>)

### 7. Error Normality

Quantile-quantile plot ([Q-Q plot](https://en.wikipedia.org/wiki/Q%E2%80%93Q\_plot)) to estimate value normality.

![](<../.gitbook/assets/reg\_perf\_error\_normality (1).png>)

**Next, Evidently explore in detail the two segments in the dataset: 5% of predictions with the highest negative and positive errors. We refer to them as "underestimation" and "overestimation" groups. We refer to the rest of the predictions as "majority".**

### **8. Mean Error per Group**

A summary of the model quality metrics for each of the two segments: mean Error (ME), Mean Absolute Error (MAE), Mean Absolute Percentage Error (MAPE).

![](../.gitbook/assets/reg\_perf\_mean\_error\_per\_group.png)

### **9. Predicted vs Actual per Group**

Prediction plots that visualize the regions where the model underestimates and overestimates the target function.

![](<../.gitbook/assets/reg\_perf\_predicted\_actual\_per\_group (1).png>)

### **10. Error Bias: Mean/Most Common Feature Value per Group**

This table helps quickly see the differences in feature values between the 3 groups:

* **OVER** (top-5% of predictions with overestimation)
* **UNDER** (top-5% of the predictions with underestimation)
* **MAJORITY** (the rest 90%)

For the numerical features, it shows the mean value per group. For the categorical features, it shows the most common value.

If you have two datasets, the table displays the values for both REF (reference) and CURR (current).

![](../.gitbook/assets/reg\_perf\_error\_bias\_table.png)

If you observe a large difference between the groups, it means that the model error is sensitive to the values of a given feature.

**To search for cases like this, you can sort the table using the column "Range(%)".** It increases when either or both of the "extreme" groups are different from the majority.

Here is the formula used to calculate the Range %:

$$
Range = 100*|(Vover-Vunder)/(Vmax-Vmin)|
$$

_**Where:**  **V**over = average feature value in the OVER group; **V**under = average feature value in the UNDER group; **V**max = maximum feature value; **V**min = minimum feature value_

### **11. Error Bias per Feature**

For each feature, Evidently shows a histogram to visualize the **distribution of its values in the segments with extreme errors** and in the rest of the data. You can visually explore if there is a relationship between the high error and the values of a given feature.

Here is an example where extreme errors are dependent on the "temperature" feature.

![](../.gitbook/assets/reg\_perf\_error\_bias\_per\_feature.png)

### 12. Predicted vs Actual per Feature

For each feature, Evidently also show the Predicted vs Actual scatterplot. It helps visually detect and explore underperforming segments which might be sensitive to the values of the given feature.

![](../.gitbook/assets/reg\_perf\_error\_bias\_predicted\_actual\_per\_feature.png)

## Metrics output

You can get the report output as a JSON or a Python dictionary:

```yaml
{
  "regression_performance": {
    "name": "regression_performance",
    "datetime": "datetime",
    "data": {
      "utility_columns": {
        "date": "date",
        "id": null,
        "target": "target",
        "prediction": "prediction"
      },
      "cat_feature_names": [],
      "num_feature_names": [],
      "metrics": {
        "reference": {
          "mean_error": mean_error,
          "mean_abs_error": mean_abs_error,
          "mean_abs_perc_error": mean_abs_perc_error,
          "error_std": error_std,
          "abs_error_std": abs_error_std,
          "abs_perc_error_std": abs_perc_error_std,
          "error_normality": {
            "order_statistic_medians": [],
            "slope": slope,
            "intercept": intercept,
            "r": r
          },
          "underperformance": {
            "majority": {
              "mean_error": mean_error,
              "std_error": std_error
            },
            "underestimation": {
              "mean_error": mean_error,
              "std_error": std_error
            },
            "overestimation": {
              "mean_error": mean_error,
              "std_error": std_error
            }
          }
        },
        "current": {
          "mean_error": mean_error,
          "mean_abs_error": mean_abs_error,
          "mean_abs_perc_error": mean_abs_perc_error,
          "error_std": error_std,
          "abs_error_std": abs_error_std,
          "abs_perc_error_std": abs_perc_error_std,
          "error_normality": {
            "order_statistic_medians": [],
            "slope": slope,
            "intercept": intercept,
            "r": r
          },
          "underperformance": {
            "majority": {
              "mean_error": mean_error,
              "std_error": std_error
            },
            "underestimation": {
              "mean_error": mean_error,
              "std_error": std_error
            },
            "overestimation": {
              "mean_error": mean_error,
              "std_error": std_error
            }
          }
        },
        "error_bias": {
          "feature_name": {
            "feature_type": "num",
            "ref_majority": ref_majority,
            "ref_under": ref_under,
            "ref_over": ref_over,
            "ref_range": ref_range,
            "prod_majority": prod_majority,
            "prod_under": prod_under,
            "prod_over": prod_over,
            "prod_range": prod_range
          },
          
          "holiday": {
            "feature_type": "cat",
            "ref_majority": 0,
            "ref_under": 0,
            "ref_over": 0,
            "ref_range": 0,
            "prod_majority": 0,
            "prod_under": 0,
            "prod_over": 1,
            "prod_range": 1
          },
        }
      }
    }
  },
  "timestamp": "timestamp"
}
```


## Report customization

* You can perform the Error bias analysis only for selected columns.
* You can use a [different color schema for the report](../customization/options-for-color-schema.md). 
* If you want to exclude some of the metrics, you can create a custom report by combining the chosen metrics. See the complete list [here](../reference/all-metrics.md)

# Regression Performance Test Suite

If you want to run regression performance checks as part of a pipeline, you can create a Test Suite and include the `RegressionTestPreset`.

## Code example

```python
regression_performance = TestSuite(tests=[
   RegressionTestPreset(),
])
 
regression_performance.run(reference_data=ref, current_data=curr)
regression_performance
```

## How it works

You can use the `RegressionTestPreset` to evaluate the quality of a regression model, when you have the ground truth data (actuals).

* It compares **regression quality metrics** against the defined expectation. 
* For Evidently to **generate the test conditions automatically**, you should pass the reference dataset (e.g., performance during model validation or a previous period). You can also set the performance expectations manually by passing a custom test condition. 
* If you neither pass the reference dataset nor set custom test conditions, Evidently will compare the model performance to a **dummy model**.

Head here to the [All tests](../reference/all-tests.md) table to see the composition of each preset and default parameters. 

## Test Suite customization

* You can set custom test conditions.
* If you want to exclude some tests or add additional ones, you can create a custom test suite by combining the chosen tests. See the complete list [here](../reference/all-tests.md).

# Examples

* Browse the [examples](../get-started/examples.md) for sample Jupyter notebooks and Colabs.
* See a tutorial "[How to break a model in 20 days](https://evidentlyai.com/blog/tutorial-1-model-analytics-in-production)" where we create a demand prediction model and analyze its gradual decay.
