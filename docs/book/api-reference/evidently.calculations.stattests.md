# evidently.calculations.stattests package

## Submodules

## evidently.calculations.stattests.anderson_darling_stattest module

## evidently.calculations.stattests.chisquare_stattest module

## evidently.calculations.stattests.cramer_von_mises_stattest module


### evidently.calculations.stattests.cramer_von_mises_stattest.CVM_2samp(x: ndarray, y: ndarray, method: str = 'auto')
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



### _class_ evidently.calculations.stattests.cramer_von_mises_stattest.CramerVonMisesResult(statistic, pvalue)
Bases: `object`

## evidently.calculations.stattests.energy_distance module

## evidently.calculations.stattests.epps_singleton_stattest module

## evidently.calculations.stattests.fisher_exact_stattest module

## evidently.calculations.stattests.g_stattest module

## evidently.calculations.stattests.hellinger_distance module

## evidently.calculations.stattests.jensenshannon module

## evidently.calculations.stattests.kl_div module

## evidently.calculations.stattests.ks_stattest module

## evidently.calculations.stattests.mann_whitney_urank_stattest module

## evidently.calculations.stattests.psi module

## evidently.calculations.stattests.registry module


### _class_ evidently.calculations.stattests.registry.StatTest(name: str, display_name: str, func: Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], allowed_feature_types: List[str], default_threshold: float = 0.05)
Bases: `object`


#### allowed_feature_types(_: List[str_ )

#### default_threshold(_: floa_ _ = 0.0_ )

#### display_name(_: st_ )

#### func(_: Callable[[Series, Series, str, float], Tuple[float, bool]_ )

#### name(_: st_ )

### _exception_ evidently.calculations.stattests.registry.StatTestInvalidFeatureTypeError(stattest_name: str, feature_type: str)
Bases: `ValueError`


### _exception_ evidently.calculations.stattests.registry.StatTestNotFoundError(stattest_name: str)
Bases: `ValueError`


### _class_ evidently.calculations.stattests.registry.StatTestResult(drift_score: float, drifted: bool, actual_threshold: float)
Bases: `object`


#### actual_threshold(_: floa_ )

#### drift_score(_: floa_ )

#### drifted(_: boo_ )

### evidently.calculations.stattests.registry.get_stattest(reference_data: Series, current_data: Series, feature_type: str, stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], StatTest]])

### evidently.calculations.stattests.registry.register_stattest(stat_test: StatTest)
## evidently.calculations.stattests.t_test module

## evidently.calculations.stattests.tvd_stattest module

## evidently.calculations.stattests.utils module


### evidently.calculations.stattests.utils.generate_fisher2x2_contingency_table(reference_data: Series, current_data: Series)
Generate 2x2 contingency matrix for fisher exact test
:param reference_data: reference data
:param current_data: current data


* **Raises**

    **ValueError** – if reference_data and current_data are not of equal length



* **Returns**

    contingency_matrix for binary data



* **Return type**

    contingency_matrix



### evidently.calculations.stattests.utils.get_binned_data(reference_data: Series, current_data: Series, feature_type: str, n: int, feel_zeroes: bool = True)
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



### evidently.calculations.stattests.utils.get_unique_not_nan_values_list_from_series(current_data: Series, reference_data: Series)
Get unique values from current and reference series, drop NaNs


### evidently.calculations.stattests.utils.permutation_test(reference_data, current_data, observed, test_statistic_func, iterations=100)
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


## evidently.calculations.stattests.wasserstein_distance_norm module

## evidently.calculations.stattests.z_stattest module


### evidently.calculations.stattests.z_stattest.proportions_diff_z_stat_ind(ref: DataFrame, curr: DataFrame)

### evidently.calculations.stattests.z_stattest.proportions_diff_z_test(z_stat, alternative='two-sided')
## Module contents
