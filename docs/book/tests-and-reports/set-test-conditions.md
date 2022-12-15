

# Custom test parameters

**Defaults**. Each test compares the value of a specific metric in the current dataset against the reference. If you do not specify the condition explicitly, Evidently will use a default. 

For example, the `TestShareOfOutRangeValues` test will fail if over 10% of values are out of range. The normal range for each feature will be automatically derived from the reference.

{% hint style="info" %} 
**Reference**: The defaults are described in the same [All tests](../reference/all-tests.md) table.
{% endhint %}

## How to set the parameters

You can override the default and set the parameters for specific tests.

For example, you can set the upper or lower boundaries of a specific value by defining `gt` (greater than) and `lt` (less than).

Here is an example:

```python
feature_level_tests = TestSuite(tests=[
TestMeanInNSigmas(column_name='hours-per-week', n_sigmas=3),
TestShareOfOutRangeValues(column_name='hours-per-week', lte=0),
TestNumberOfOutListValues(column_name='education', lt=0),
TestColumnShareOfMissingValues(column_name='education', lt=0.2),
])

feature_level_tests.run(reference_data=ref, current_data=curr)

Feature_level_test
```
## Available parameters

### Standard parameters 

The following standard parameters are available: 

| Condition parameter name | Explanation                                | Usage Example                                                   |
|--------------------------|--------------------------------------------|-----------------------------------------------------------------|
| eq: val                  | test_result == val                         | TestFeatureMin(feature_name=”numeric_feature”, eq=5)            |
| not_eq: val              | test_result != val                         | TestFeatureMin(feature_name=”numeric_feature”, ne=0)            |
| gt: val                  | test_result > val                          | TestFeatureMin(feature_name=”numeric_feature”, gt=5)            |
| gte: val                 | test_result >= val                         | TestFeatureMin(feature_name=”numeric_feature”, gte=5)           |
| lt: val                  | test_result < val                          | TestFeatureMin(feature_name=”numeric_feature”, lt=5)            |
| lte: val                 | test_result <= val                         | TestFeatureMin(feature_name=”numeric_feature”, lte=5)           |
| is_in: list              | test_result == one of the values from list | TestFeatureMin(feature_name=”numeric_feature”, is_in=[3,5,7])   |
| not_in: list             | test_result != any of the values from list | TestFeatureMin(feature_name=”numeric_feature”, not_in=[-1,0,1]) |

### Approx

If you want to set an upper and/or lower limit to the value, you can use **approx** instead of calculating the value itself. You can set the relative or absolute range. 

```python
approx(value, relative=None, absolute=None)
```
To apply approx, you need to first import this component:

```python
from evidently.tests.utils import approx
```

Here is how you can set the upper boundary as 5+10%:

```python
lte=approx(5, relative=0.1)
```

Here is how you can set the boundary as 5 +/-10%:
```python
eq=approx(5, relative=0.1)
```

### Additional parameters

Some tests require additional parameters or might have optional parameters.

For example, if you want to test a quantile value, you need to pass the quantile as a parameter (required). Or, you can pass the K parameter to evaluate classification precision@K instead of using the default decision threshold of 0.5 (optional). 

{% hint style="info" %} 
**Reference**: the additional parameters that apply to specific tests and defaults are described in the same [All tests](../reference/all-tests.md) table.
{% endhint %}
