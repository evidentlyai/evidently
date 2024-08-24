
## Prediction column(s) in classification 

To evaluate the classification performance, you need both true labels and prediction. Depending on the classification type (e.g., binary, multi-class, probabilistic), you have different options of how to pass the predictions.

### Multiclass classification, option 1

Target: encoded labels, Preds: encoded labels + Optional[target_names].

| target | prediction |
|---|---|
| 1 | 1 |
| 0 | 2 |
| … | … |
| 2 | 2 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
column_mapping.target_names = ['Setosa', 'Versicolour', 'Virginica']
```

If you pass the target names, they will appear on the visualizations. 

You can also pass the target names as a dictionary:

```python
column_mapping.target_names = {'0':'Setosa', '1':'Versicolor', '2':'Virginica'}
```

or

```python
column_mapping.target_names = {0:'Setosa', 1:'Versicolor', 2:'Virginica'} 
```

### Multiclass classification, option 2

Target: labels, Preds: labels. 

| target | prediction |
|---|---|
| ‘Versicolour’ | ‘Versicolour’ |
| ‘Setosa’ | ‘Virginica’ |
| … | … |
| ‘Virginica’ | ‘Virginica’ |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
```

### Multiclass probabilistic classification

Target: labels, Preds: columns named after labels.

| target | ‘Versicolour’ | ‘Setosa’ | ‘Virginica’ |
|---|---|---|---|
| ‘Setosa’ | 0.98 | 0.01 | 0.01 |
| ‘Virginica’ | 0.5 | 0.2 | 0.3 |
| … | … |  |  |
| ‘Virginica’ | 0.2 | 0.7 | 0.1 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = ['Setosa', 'Versicolour', 'Virginica']

```

Naming the columns after the labels is a requirement. You cannot pass a custom list.

### Binary classification, option 1

Target: encoded labels, Preds: encoded labels + pos_label + Optional[target_names]

| target | prediction |
|---|---|
| 1 | 1 |
| 0 | 1 |
| … | … |
| 1 | 0 |

By default, Evidently expects the positive class to be labeled as ‘1’. If you have a different label, specify it explicitly.

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
column_mapping.target_names = ['churn', 'not_churn']
column_mapping.pos_label = 0

```

If you pass the target names, they will appear on the visualizations. 

### Binary classification, option 2 

Target: labels, Preds: labels + pos_label

| target | prediction |
|---|---|
| ‘churn’ | ‘churn’ |
| ‘not_churn’ | ‘churn’ |
| … | … |
| ‘churn’ | ‘not_churn’ |

Passing the name of the positive class is a requirement in this case.

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
column_mapping.pos_label = 'churn'

```

### Binary probabilistic classification, option 1 

Target: labels, Preds: columns named after labels + pos_label

| target | ‘churn’ | ‘not_churn’ |
|---|---|---|
| ‘churn’ | 0.9 | 0.1 |
| ‘churn’ | 0.7 | 0.3 |
| … | … |  |
| ‘not_churn’ | 0.5 | 0.5 |

Passing the name of the positive class is a requirement in this case.

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = ['churn', 'not_churn']
column_mapping.pos_label = 'churn'

```

### Binary probabilistic classification, option 2 

Target: labels, Preds: a column named like one of the labels + pos_label

| target | ‘not_churn’ |
|---|---|
| ‘churn’ | 0.5 |
| ‘not_churn’ | 0.1 |
| … | … |
| ‘churn’ | 0.9 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'not_churn'
column_mapping.pos_label = 'churn'

```
Both naming the column after one of the labels and passing the name of the positive class are requirements.

### Binary probabilistic classification, option 3

Target: encoded labels, Preds: one column with any name + pos_label

| target | prediction |
|---|---|
| 1 | 0.5 |
| 1 | 0.1 |
| … | … |
| 0 | 0.9 |

```python
column_mapping = ColumnMapping()

column_mapping.target = 'target'
column_mapping.prediction = 'prediction'
column_mapping.pos_label = 1
column_mapping.target_names = ['churn', 'not_churn']

```
If you pass the target names, they will appear on the visualizations.

