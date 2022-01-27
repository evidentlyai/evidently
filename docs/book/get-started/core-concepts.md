# Core concepts

## **Reference and Current Data**

The primary use for Evidently is the comparison between two datasets. These datasets are model application logs. They can include model input features, predictions, and/or actuals (true labels).&#x20;

* **Reference** dataset serves as a basis for the comparison.
* **Current (Production)** dataset is the dataset that is compared to the first.&#x20;

![](../.gitbook/assets/two_datasets_classification.png)

In practice, you can use it in different combinations:

* **Training vs Test**&#x20;
  * To compare the model performance on a hold-out **Test** to the **Training**.&#x20;
  * Pass the training data as "Reference", and test data as "Current".
* **Production vs Training**&#x20;
  * To compare the **Production** model performance to the **Training** period.&#x20;
  * Pass the training data as "Reference", and production data as "Current".
* **Current perfromance vs Past**&#x20;
  * To compare the **Current** production performance to an **Earlier** period.&#x20;
  * For example, to compare the last week to the previous week or month.&#x20;
  * Pass the earlier data as "Reference", and newer data as "Current".&#x20;
* **Compare any two models or datasets**&#x20;
  * For example, to estimate the historical drift for different windows in your training data or to compare how two models perform in the test.&#x20;
  * Pass the first dataset as "Reference", and the second as "Current".&#x20;

You can generate a Performance report for a **single dataset**. Pass it as "Reference". In other cases, we need two datasets to run the statistical tests. &#x20;

Right now, you cannot choose a custom name for your dataset.&#x20;

**Note:** earlier, we referred to the second dataset as "Production". You might notice that in some older examples. &#x20;



