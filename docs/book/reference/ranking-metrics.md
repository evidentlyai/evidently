## Recall at K

**Evidently Metric**: `RecallTopKMetric`. 

Recall at K reflects the ability of the recommender or ranking system to retrieve all relevant items within the top K results. 

**Implemented method:**
* **Compute recall at K by user**. Compute the recall at K for each individual user, by measuring the share of all relevant items in the dataset (e.g. that a given user liked or interacted with) that appear in the top K results.
$$\text{Recall at } K = \frac{\text{Number of relevant items in } K}{\text{Total number of relevant items}}$$
* **Compute overall recall**. Average the results across all users in the dataset. 

**Range**: 0 to 1.

**Interpretation**: a higher recall at K indicates that the model is able to retrieve a higher proportion of relevant items, which is generally desirable. 

**Notes**: if the total number of relevant items is greater than K, it's impossible to recall all of them within the top K results (making 100% recall impossible).

## Precision at K

**Evidently Metric**: `PrecisionTopKMetric`. 

Precision at K reflects the ability of the system to suggest items that are truly relevant to the users’ preferences. 

**Implemented method:**
* **Compute precision at K by user**. Compute the precision at K for each user by measuring the share of the relevant results within the top K (e.g. that the user liked or interacted with). 
$$\text{Precision at } K = \frac{\text{Number of relevant items in } K}{\text{Total number of items in }K}$$
* **Compute overall precision**. Average the results across all users in the dataset. 

**Range**: 0 to 1.

**Interpretation**: a higher precision at K indicates that a larger proportion of the top results are relevant, which is generally desirable.

## F Beta at K

**Evidently Metric**: `FBetaTopKMetric`.

The F Beta score at K combines precision and recall into a single value, providing a balanced measure of a recommendation system's performance. 

$$F_{\beta} = \frac{(1 + \beta^2) \times \text{Precision at K} \times \text{Recall at K}}{(\beta^2 \times \text{Precision at K}) + \text{Recall at K}} \$$

`Beta` is a parameter that determines the weight assigned to recall relative to precision. `Beta` > 1 gives more weight to recall, while `beta` < 1 favors precision.

If `Beta` = 1 (default), it is a traditional F1 score that provides a harmonic mean of precision and recall at K. It provides a balanced estimation, considering both false positives (items recommended that are not relevant) and false negatives (relevant items not recommended).

**Range**: 0 to 1.

**Interpretation**: Higher F Beta at K values indicate better overall performance.

