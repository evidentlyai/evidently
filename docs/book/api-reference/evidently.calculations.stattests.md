# evidently.calculations.stattests package

## Submodules


### CVM_2samp(x: ndarray, y: ndarray, method: str = 'auto')
Perform the two-sample Cramér-von Mises test
:param x: array_like
:param y: array_like
:param method: {‘auto’, ‘asymptotic’, ‘exact’}, optional


* **Returns**

    object with attributes
    statistic : Cramér-von Mises statistic.
    pvalue : float



* **Return type**

    res



### _class _ CramerVonMisesResult(statistic, pvalue)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; labels _: Sequence[Union[str, int]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; values _: list_ 

#### Methods: 

### _class _ StatTest(name: str, display_name: str, func: Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], allowed_feature_types: List[str], default_threshold: float = 0.05)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; allowed_feature_types _: List[str]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; default_threshold _: float_ _ = 0.05_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; display_name _: str_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; func _: Callable[[Series, Series, str, float], Tuple[float, bool]]_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; name _: str_ 

#### Methods: 

### _exception _ StatTestInvalidFeatureTypeError(stattest_name: str, feature_type: str)
Bases: `ValueError`


### _exception _ StatTestNotFoundError(stattest_name: str)
Bases: `ValueError`


### _class _ StatTestResult(drift_score: float, drifted: bool, actual_threshold: float)
Bases: `object`


#### Attributes: 

#####&nbsp;&nbsp;&nbsp;&nbsp; actual_threshold _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; drift_score _: float_ 

#####&nbsp;&nbsp;&nbsp;&nbsp; drifted _: bool_ 

#### Methods: 

### get_stattest(reference_data: Series, current_data: Series, feature_type: str, stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], StatTest]])

### register_stattest(stat_test: StatTest)

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



### proportions_diff_z_stat_ind(ref: DataFrame, curr: DataFrame)

### proportions_diff_z_test(z_stat, alternative='two-sided')
## Module contents
