---
description: How to pass additional data for ranking and recommendations.
---

# Column mapping 
You must define column mapping to run evaluations for recommender or ranking systems on your `current` and (optional) `reference` data. Column mapping helps point to the columns with user ID, item ID, prediction, and target. 

Check out the section on the [column mapping page](https://docs.evidentlyai.com/user-guide/input-data/column-mapping#recommender-systems).

# Additional data 
Some metrics like novelty or popularity bias require training data, which has a different structure from production data. To pass it, use the `additional_data` object. You can pass your training data as `current_train_data` and (optional) `reference_train_data`.

Example: 

```python
report = Report(metrics=[
   UserBiasMetric(column_name='age'),
])
report.run(reference_data=ref, current_data=cur, column_mapping=column_mapping, additional_data={'current_train_data': train})
report
```

## Requirements:

* The additional training dataset should have the following structure: 

| user | item | target |
|---|---|---|
| id1 | id1 | 1 |
| id2 | id9 | 1 |
| id3 | id2 | 1 |
| id3 | id1 | 1 |
| id4 | id6 | 1 |

* The names of the columns with `user_id` and `item_id` should match the corresponding columns in the current (and optional reference) data.
* The name of the column with the interaction result should match the name of the `target` column in the current (and optional reference) data.
* If you use metrics that refer to specific columns (such as `UserBiasMetric` metric), these columns must also be present in the training dataset.  
* You can pass a single training dataset or two datasets (in case your reference and current dataset have different training data). 

{% hint style="info" %}

### What is the difference between training and reference data?

The reference dataset can belong to a previous production period or a different model you compare against. The training dataset is used to train the model. Their structure usually differs:
* Production data typically includes a list of all items recommended to the user, where some of them earn a positive interaction result. It contains negative examples (ignored recommendations) and data about model prediction (predicted rank or score). 
* Training data typically contains a history of user actions, such as user viewing history, or upvotes and downvotes. Since it only includes the interaction results, it lacks negative examples (e.g., ignored  recommendations) and column with the model output (predicted rank or score). 

{% endhint %}



