## When to use it?

You can use the Classification Performance test preset to evaluate the quality of a classification model, when you have the ground truth labels.

There are several presets for different classification tasks: 

```python
MulticlassClassification
BinaryClassificationTopK
BinaryClassification
```

## Multiclass Classification

You can set prediction type as `probas` or `labels`.

### Code example

```python
classification_performance = TestSuite(tests=[
   MulticlassClassification(prediction_type='labels')
])

classification_performance.run(reference_data=iris_ref, current_data=iris_cur)
classification_performance
```

### Preset contents

The preset contains the following tests:

```python
TestAccuracyScore(),
TestF1Score(),
TestPrecisionScore(), 
TestRecallScore(),
TestFeatureValueDrift(column=target)
```

If prediction type is `probas`, also: `TestLogLoss()`, `TestRocAuc()`.

## BinaryClassificationTopK

### Code example

```python
binary_topK_classification_performance = TestSuite(tests=[
    BinaryClassificationTopK(k=10),
])

binary_topK_classification_performance.run(reference_data=bcancer_ref, current_data=bcancer_cur)
binary_topK_classification_performance
```

### Preset contents

The preset contains the following tests:

```python
TestAccuracyScore(k=self.k),
TestPrecisionScore(k=self.k),
TestRecallScore(k=self.k),
TestF1Score(k=self.k),
TestFeatureValueDrift(column_name=target),
TestRocAuc(),
TestLogLoss(),     
```

## BinaryClassification

You can set prediction type as `probas` or `labels`.

### Code example

```python
binary_classification_performance = TestSuite(tests=[
    BinaryClassification(prediction_type='probas'),
])

binary_classification_performance.run(reference_data=bcancer_ref, current_data=bcancer_cur)
binary_classification_performance
```

### Preset contents

The preset contains the following tests:

```python
TestFeatureValueDrift(column=target),
TestPrecisionScore(),
TestRecallScore(),
TestF1Score(),
TestAccuracyScore()        
```

If prediction type is `probas`, also: `TestRocAuc()`.

## More information

Consult the [user guide](../tests-and-reports/run-tests.md) for the complete instructions on how to run tests. 

Unless specified otherwise, the default settings are applied. 

Head here to the [All tests](../reference/all-tests.md) table to see the description of individual tests and default parameters. 

{% hint style="info" %} 
We are doing our best to maintain this page up to date. In case of discrepancies, consult the code on GitHub (API reference coming soon!) or the current version of the "All tests" example notebook in the [Examples](../get-started/examples.md) section. If you notice an error, please send us a pull request to update the documentation! 
{% endhint %}
