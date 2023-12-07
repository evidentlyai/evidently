## Recall 

**Evidently Metric**: `RecallTopKMetric`. 

Recall at K reflects the ability of the recommender or ranking system to retrieve all relevant items within the top K results. 

**Implemented method:**
* **Compute recall at K by user**. Compute the recall at K for each individual user, by measuring the share of all relevant items in the dataset (e.g. that a given user liked or interacted with) that appear in the top K results.
$$\text{Recall at } K = \frac{\text{Number of relevant items in } K}{\text{Total number of relevant items}}$$
* **Compute overall recall**. Average the results across all users in the dataset. 

**Range**: 0 to 1.

**Interpretation**: a higher recall at K indicates that the model is able to retrieve a higher proportion of relevant items, which is generally desirable. 

**Notes**: if the total number of relevant items is greater than K, it's impossible to recall all of them within the top K results (making 100% recall impossible).

## Precision 

**Evidently Metric**: `PrecisionTopKMetric`. 

Precision at K reflects the ability of the system to suggest items that are truly relevant to the users’ preferences. 

**Implemented method:**
* **Compute precision at K by user**. Compute the precision at K for each user by measuring the share of the relevant results within the top K (e.g. that the user liked or interacted with). 
$$\text{Precision at } K = \frac{\text{Number of relevant items in } K}{\text{Total number of items in }K}$$
* **Compute overall precision**. Average the results across all users in the dataset. 

**Range**: 0 to 1.

**Interpretation**: a higher precision at K indicates that a larger proportion of the top results are relevant, which is generally desirable.

## F Beta

**Evidently Metric**: `FBetaTopKMetric`.

The F Beta score at K combines precision and recall into a single value, providing a balanced measure of a recommendation system's performance. 

$$F_{\beta} = \frac{(1 + \beta^2) \times \text{Precision at K} \times \text{Recall at K}}{(\beta^2 \times \text{Precision at K}) + \text{Recall at K}} \$$

`Beta` is a parameter that determines the weight assigned to recall relative to precision. `Beta` > 1 gives more weight to recall, while `beta` < 1 favors precision.

If `Beta` = 1 (default), it is a traditional F1 score that provides a harmonic mean of precision and recall at K. It provides a balanced estimation, considering both false positives (items recommended that are not relevant) and false negatives (relevant items not recommended).

**Range**: 0 to 1.

**Interpretation**: Higher F Beta at K values indicate better overall performance.

## Mean average precision (MAP) 

**Evidently Metric**: `MAPKMetric`.

MAP (Mean Average Precision) at K assesses the ability of the recommender system to suggest relevant items in the top-K results, while placing more relevant items at the top. 

Compared to precision at K, MAP at K is rank-aware. It penalizes the system for placing relevant items lower in the list, even if the total number of relevant items at K is the same.

**Implemented method:**
* **Compute Average Precision (AP) at K by user**. The Average Precision at K is computed for each user as an average of precision values at each relevant item position within the top K. To do that, we sum up precision at all values of K when the item is relevant (e.g., Precision @1, Precision@2..), and divide it by the total number of relevant items in K.
$$\text{AP@K} = \frac{1}{N} \sum_{k=1}^{K} Precision(k) \times rel(k)$$
Where *N* is the total number of relevant items at K, and *rel(k)* is equal to 1 if the item is relevant, and is 0 otherwise.

Example: if K = 10, and items in positions 1, 2, and 10 are relevant, the formula will look as:
$$AP@10 = \frac{Precision@1+Precision@2+Precision@10}{3}$$
* **Compute Mean Average Precision (MAP) at K**. Average the results across all users in the dataset.
$$\text{MAP@K} = \frac{1}{U} \sum_{u=1}^{U} \text{AP@K}_u$$
Where *U* is the total number of users or queries in the dataset, and *AP* is the average precision for a given list.

**Range**: 0 to 1.

**Interpretation**: Higher MAP at K values indicates a better ability of the system to place relevant items high in the list. 

## Mean average recall (MAR) 

**Evidently Metric**: `MARKMetric`.

MAR (Mean Average Recall) at K assesses the ability of a recommendation system to retrieve all relevant items within the top-K results, averaged by all relevant positions. 

**Implemented method:**
* **Compute the average recall at K by user**. Compute and average the recall at each relevant position within the top K for every user. To do that, we sum up the recall at all values of K when the item is relevant (e.g. Recall @1, Recall@2..), and divide it by the total number of relevant recommendations in K.
$$\text{AR@K} = \frac{1}{N} \sum_{k=1}^{K} Recall(k) \times rel(k)$$
Example: if K = 10, and items in positions 1, 2, and 10 are relevant, the formula will look as:
$$\text{AR@10} = \frac{Recall@1+Recall@2+Recall@10}{3}$$
* **Compute mean average recall at K**. Average the results across all users.
$$\text{MAR@K} = \frac{1}{U} \sum_{u=1}^{U} \text{AR@K}_u$$
Where *U* is the total number of users or queries in the dataset, and *AR* is the average recall for a given list.

**Range**: 0 to 1.

**Interpretation**: Higher MAR at K values indicates a better ability of the system to retrieve relevant items across all users.  

## Normalized Discounted Cumulative Gain (NDCG)

**Evidently Metric**: `NDCGKMetric`.

NDCG (Normalized Discounted Cumulative Gain) at K reflects the ranking quality, compared to an ideal order where all relevant items for each user are placed at the top of the list.

**Implemented method**:
* **Provide the item relevance score**. You can assign a relevance score for each item in each user’s top-K list. Depending on the model type, it can be a binary outcome (1 is relevant, 0 is not) or a score.  
* **Compute the discounted cumulative gain (DCG)** at K by the user. DCG at K measures the quality of the ranking (= total relevance) for a list of top-K items. We add a logarithmic discount to account for diminishing returns from each following item being lower on the list. To get the resulting DCG, you can compute a weighted sum of the relevance scores for all items from the top of the list to K with an applied discount.
$$\text{DCG@K} = \sum_{k=1}^{K} \frac{rel_i}{\log_2(i + 1)}$$
Where *Rel(i)* is the relevance score of the item at rank *i*. 
* **Compute the normalized DCG (NDCG)**. To normalize the metric, we divide the resulting DCG by the ideal DCG (IDCG) at K. Ideal DCG at K represents the maximum achievable DCG for a user when the items are perfectly ranked in descending order of relevance. 
$$\text{NDCG@K} = \frac{DCG@K}{IDCG@K}$$
This way, it is possible to compare NDCG values across different use cases. The resulting NDCG values for all users are averaged to measure the overall performance of a model. 

**Range**: 0 to 1, where 1 indicates perfect ranking.

**Interpretation**: Higher NDCG at K indicates a better ability of the system to place more relevant items higher up in the ranking.

## Hit Rate

**Evidently Metric**: `HitRateKMetric`.

Hit Rate at K calculates the share of users for which at least one relevant item is included in the K.

**Implemented method**:
* **Compute “hit” for each user**. For each user, we evaluate if any of the top-K recommended items is relevant. It is a binary metric equal to 1 if any relevant item is included in K, or 0 otherwise.
* **Compute average hit rate**. The average of this metric is calculated across all users.

**Range**: 0 to 1, where 1 indicates that each user gets at least one relevant recommendation.

**Interpretation**: A higher Hit Rate indicates that a higher share of users have relevant recommendations in their lists. 

**Note**: the Hit Rate will typically increase for higher values of K (since there is a higher chance that a relevant item will be recommended in a longer list).

## Mean Reciprocal Rank (MRR)

**Evidently Metric**: `MRRKMetric`

Mean Reciprocal Rank (MRR) measures the ranking quality considering the position of the first relevant item in the list of recommendations.

**Implemented method:**
* For each user, identify the position of the **first relevant item** in the recommended list.
* Calculate the **reciprocal rank**, taking the reciprocal of the position of the first relevant item for each user (i.e., 1/position). 
Example: if the first relevant item is at the top of the list - the reciprocal rank is 1, if it is on the 2nd position - the reciprocal rank ½, if on the 3rd - ⅓, etc.
* Calculate the **mean reciprocal rank** (MRR). Compute the average reciprocal rank across all users.
$$\text{MRR} = \frac{1}{U} \sum_{u=1}^{U}\frac{1}{rank_i}$$
Where *U* is the total number of users, and *rank(i)* is the rank of the first relevant item for user *u* in the top-K results.

