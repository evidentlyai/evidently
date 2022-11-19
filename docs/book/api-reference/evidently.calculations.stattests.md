# evidently.calculations.stattests package

## Submodules

## anderson_darling_stattest module

Anderson-Darling test of two samples.

Name: “anderson”

Import:

```python
>>> from evidently.calculations.stattests import anderson_darling_test
```

Properties:
- only for numerical features
- returns p-value

### Example

Using by object:

```python
>>> from evidently.options import DataDriftOptions
>>> from evidently.calculations.stattests import anderson_darling_test
>>> options = DataDriftOptions(feature_stattest_func=anderson_darling_test)
```

Using by name:

```python
>>> from evidently.options import DataDriftOptions
>>> options = DataDriftOptions(feature_stattest_func="anderson")
```

## chisquare_stattest module

Chisquare test of two samples.

Name: “chisquare”

Import:

```python
>>> from evidently.calculations.stattests import chi_stat_test
```

Properties:
- only for categorical features
- returns p-value

### Example

Using by object:

```python
>>> from evidently.options import DataDriftOptions
>>> from evidently.calculations.stattests import chi_stat_test
>>> options = DataDriftOptions(feature_stattest_func=chi_stat_test)
```

Using by name:

```python
>>> from evidently.options import DataDriftOptions
>>> options = DataDriftOptions(feature_stattest_func="chisquare")
```

## cramer_von_mises_stattest module

Cramer-Von-mises test of two samples.

Name: “cramer_von_mises”

Import:

```python
>>> from evidently.calculations.stattests import cramer_von_mises
```

Properties:
- only for numerical features
- returns p-value

### Example

Using by object:

```python
>>> from evidently.options import DataDriftOptions
>>> from evidently.calculations.stattests import cramer_von_mises
>>> options = DataDriftOptions(feature_stattest_func=cramer_von_mises)
```

Using by name:

```python
>>> from evidently.options import DataDriftOptions
>>> options = DataDriftOptions(feature_stattest_func="cramer_von_mises")
```


### class CramerVonMisesResult(statistic, pvalue)
Bases: `object`

## energy_distance module

Energy-distance test of two samples.

Name: “ed”

Import:

```python
>>> from evidently.calculations.stattests import energy_dist_test
```

Properties:
- only for numerical features
- returns p-value

### Example

Using by object:

```python
>>> from evidently.options import DataDriftOptions
>>> from evidently.calculations.stattests import energy_dist_test
>>> options = DataDriftOptions(feature_stattest_func=energy_dist_test)
```

Using by name:

```python
>>> from evidently.options import DataDriftOptions
>>> options = DataDriftOptions(feature_stattest_func="ed")
```

## epps_singleton_stattest module

Epps-Singleton test of two samples.

Name: “es”

Import:

```python
>>> from evidently.calculations.stattests import epps_singleton_test
```

Properties:
- only for numerical features
- returns p-value
- default threshold 0.05

### Example

Using by object:

```python
>>> from evidently.options import DataDriftOptions
>>> from evidently.calculations.stattests import epps_singleton_test
>>> options = DataDriftOptions(feature_stattest_func=epps_singleton_test)
```

Using by name:

```python
>>> from evidently.options import DataDriftOptions
>>> options = DataDriftOptions(feature_stattest_func="es")
```

## fisher_exact_stattest module

## g_stattest module

## hellinger_distance module

## jensenshannon module

## kl_div module

## ks_stattest module

## mann_whitney_urank_stattest module

## psi module

## registry module


### class StatTest(name: str, display_name: str, func: Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], allowed_feature_types: List[str], default_threshold: float = 0.05)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; allowed_feature_types : List[str] 

##### &nbsp;&nbsp;&nbsp;&nbsp; default_threshold : float  = 0.05 

##### &nbsp;&nbsp;&nbsp;&nbsp; display_name : str 

##### &nbsp;&nbsp;&nbsp;&nbsp; func : Callable[[Series, Series, str, float], Tuple[float, bool]] 

##### &nbsp;&nbsp;&nbsp;&nbsp; name : str 

### exception StatTestInvalidFeatureTypeError(stattest_name: str, feature_type: str)
Bases: `ValueError`


### exception StatTestNotFoundError(stattest_name: str)
Bases: `ValueError`


### class StatTestResult(drift_score: float, drifted: bool, actual_threshold: float)
Bases: `object`

#### Attributes: 

##### &nbsp;&nbsp;&nbsp;&nbsp; actual_threshold : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; drift_score : float 

##### &nbsp;&nbsp;&nbsp;&nbsp; drifted : bool 

### get_stattest(reference_data: Series, current_data: Series, feature_type: str, stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], StatTest]])

### register_stattest(stat_test: StatTest)
## t_test module

## tvd_stattest module

## utils module


### generate_fisher2x2_contingency_table(reference_data: Series, current_data: Series)
Generate 2x2 contingency matrix for fisher exact test
:param reference_data: reference data
:param current_data: current data


* **Raises**

    **ValueError** – if reference_data and current_data are not of equal length



* **Returns**

    contingency_matrix for binary data



* **Return type**

    contingency_matrix



### get_binned_data(reference_data: Series, current_data: Series, feature_type: str, n: int, feel_zeroes: bool = True)
Split variable into n buckets based on reference quantiles
:param reference_data: reference data
:param current_data: current data
:param feature_type: feature type
:param n: number of quantiles


* **Returns**

    % of records in each bucket for reference
    current_percents: % of records in each bucket for current



* **Return type**

    reference_percents



### get_unique_not_nan_values_list_from_series(current_data: Series, reference_data: Series)
Get unique values from current and reference series, drop NaNs


### permutation_test(reference_data, current_data, observed, test_statistic_func, iterations=100)
Perform a two-sided permutation test
:param reference_data: reference data
:param current_data: current data
:param observed: observed value
:param test_statistic_func: the test statistic function
:param iterations: number of times to permute


* **Returns**

    two-sided p_value



* **Return type**

    p_value


## wasserstein_distance_norm module

## z_stattest module


### proportions_diff_z_stat_ind(ref: DataFrame, curr: DataFrame)

### proportions_diff_z_test(z_stat, alternative='two-sided')
## Module contents
