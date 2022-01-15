# Analyze historical data drift

**TL;DR:** You can use Evidently to evaluate drift in your training data. Understanding past data changes helps define monitoring and retraining strategy. Here is a [sample Jupyter notebook](../../evidently/tutorials/historical\_drift\_visualization.ipynb).

## Tutorial - "How to detect, evaluate and visualize historical drifts"

![](../../.gitbook/assets/7\_feature\_drift\_boolean.png)

In this tutorial, we check historical drift on a month-by-month basis. We add a custom function to set drift conditions on the dataset level. We use Evidently **Data Drift Profile** to calculate drift, Plotly to generate custom visuals, and integrate with Mlflow to log the results.

* ​[Full text](https://evidentlyai.com/blog/tutorial-3-historical-data-drift) of the tutorial
* Jupyter [notebook](../../evidently/tutorials/historical\_drift\_visualization.ipynb) w/source code
* Source [data](https://www.kaggle.com/c/bike-sharing-demand/data?select=train.csv) and description on Kaggle

