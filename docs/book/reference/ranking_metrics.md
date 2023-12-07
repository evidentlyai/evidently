## Recall at K

Evidently Metric: `RecallTopKMetric`. Recall at K reflects the ability of the recommender or ranking system to retrieve all relevant items within the top K results. 

**Implemented method:**
* **Compute recall at K by user**. Compute the recall at K for each individual user, by measuring the share of all relevant items in the dataset (that a given user liked or interacted with) that appear in the top K results.  
* **Compute overall recall**. Average the results across all users in the dataset. 

**Range**: 0 to 1.

**Interpretation**: a higher recall at K indicates that the model is able to retrieve a higher proportion of relevant items, which is generally desirable. 

**Notes**: if the total number of relevant items is greater than K, it's impossible to recall all of them within the top K results (making 100% recall impossible).

