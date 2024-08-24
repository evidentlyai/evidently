---
description: How to pass additional data for ranking and recommendations.
---

# Column mapping 
You must define column mapping to run evaluations for recommender or ranking systems on your `current` and (optional) `reference` data. Column mapping helps point to the columns with user ID, item ID, prediction, and target. 

# Recommender systems
To evaluate the quality of a ranking or a recommendation system, you must pass:
* The model score or rank as the prediction.
* The information about user actions (e.g., click, assigned score) as the target. 

Here are the examples of the expected data inputs.

If the model prediction is a score (expected by default):

| user_id | item_id | prediction (score) | target (interaction result) |
|---|---|---|---|
| user_1 | item_1 | 1.95 | 0 |
| user_1 | item_2 | 0.8 | 1 |
| user_1 | item_3 | 0.05 | 0 |

If the model prediction is a rank:
| user_id | item_id | prediction (rank) | target (interaction result) |
|---|---|---|---|
| user_1 | item_1 | 1 | 0 |
| user_1 | item_2 | 2 | 1 |
| user_1 | item_3 | 3 | 0 |

The **target** column with the interaction result can contain either:
* a binary label (where `1` is a positive outcome)
* any true labels or scores (any positive values, where a higher value corresponds to a better recommendation match or a more valuable user action).

You might need to add additional details about your dataset via column mapping:
* `recommendations_type`: `score` (default) or `rank`. Helps specify whether the prediction column contains ranking or predicted score.
* `user_id`: helps specify the column that contains user IDs.
* `item_id`: helps specify the column that contains ranked items.

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

# Code example

Notebook example on using column mapping and additional data for recommender systems:

{% embed url="https://github.com/evidentlyai/evidently/blob/main/examples/how_to_questions/how_to_run_recsys_metrics.ipynb" %}

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



