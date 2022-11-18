# evidently.options package

## Submodules


### _class _ ColorOptions(primary_color: str = '#ed0400', secondary_color: str = '#4d4d4d', current_data_color: Optional[str] = None, reference_data_color: Optional[str] = None, color_sequence: Sequence[str] = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4'), fill_color: str = 'LightGreen', zero_line_color: str = 'green', non_visible_color: str = 'white', underestimation_color: str = '#6574f7', overestimation_color: str = '#ee5540', majority_color: str = '#1acc98', vertical_lines: str = 'green', heatmap: str = 'RdBu_r')
Bases: `object`

Collection of colors for data visualization

- primary_color - basic color for data visualization.

    Uses by default for all bars and lines for widgets with one dataset and as a default for current data.

- secondary_color - basic color for second data visualization if we have two data sets, for example, reference data.

- current_data_color - color for all current data, by default primary color is used

- reference_data_color - color for reference data, by default secondary color is used

- color_sequence - set of colors for drawing a number of lines in one graph, in for data quality, for example

- fill_color - fill color for areas in line graphs

- zero_line_color - color for base, zero line in line graphs

- non_visible_color - color for technical, not visible dots or points for better scalability

- underestimation_color - color for underestimation line in regression

- overestimation_color - color for overestimation line in regression

- majority_color - color for majority line in regression

- lines - color for vertical lines

- heatmap_colors - colors for heatmap


#### color_sequence _: Sequence[str]_ _ = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4')_ 

#### current_data_color _: Optional[str]_ _ = None_ 

#### fill_color _: str_ _ = 'LightGreen'_ 

#### get_current_data_color()

#### get_reference_data_color()

#### heatmap _: str_ _ = 'RdBu_r'_ 

#### majority_color _: str_ _ = '#1acc98'_ 

#### non_visible_color _: str_ _ = 'white'_ 

#### overestimation_color _: str_ _ = '#ee5540'_ 

#### primary_color _: str_ _ = '#ed0400'_ 

#### reference_data_color _: Optional[str]_ _ = None_ 

#### secondary_color _: str_ _ = '#4d4d4d'_ 

#### underestimation_color _: str_ _ = '#6574f7'_ 

#### vertical_lines _: str_ _ = 'green'_ 

#### zero_line_color _: str_ _ = 'green'_ 

### _class _ DataDriftOptions(confidence: Optional[Union[float, Dict[str, float]]] = None, threshold: Optional[Union[float, Dict[str, float]]] = None, drift_share: float = 0.5, nbinsx: Union[int, Dict[str, int]] = 10, xbins: Optional[Dict[str, int]] = None, feature_stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest), Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]] = None, all_features_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_features_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_features_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_feature_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, cat_target_threshold: Optional[float] = None, num_target_threshold: Optional[float] = None, cat_target_stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_target_stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None)
Bases: `object`

Configuration for Data Drift calculations.


* **Parameters**

    - **confidence** – Defines the confidence level for statistical tests.
    Applies to all features (if passed as float) or certain features (if passed as dictionary).
    (Deprecated) Use threshold to define confidence level for statistical
    tests as more universal solution.

    - **threshold** – Defines thresholds for statistical tests.
    Applies to all features (if passed as float) or certain features (if passed as dictionary).

    - **drift_share** – Sets the share of drifting features as a condition for Dataset Drift in the Data Drift report.

    - **nbinsx** – Defines the number of bins in a histogram.
    Applies to all features (if passed as int) or certain features (if passed as dictionary).

    - **xbins** – Defines the boundaries for the size of a specific bin in a histogram.

    - **feature_stattest_func** – Defines a custom statistical test for drift detection in the Data Drift report.
    Applies to all features (if passed as a function) or individual features (if a dict).
    (Deprecated) Use all_features_stattest or per_feature_stattest.

    - **all_features_stattest** – Defines a custom statistical test for drift detection in the Data Drift report
    for all features.

    - **cat_features_stattest** – Defines a custom statistical test for drift detection in the Data Drift report
    for categorical features only.

    - **num_features_stattest** – Defines a custom statistical test for drift detection in the Data Drift report
    for numerical features only.

    - **per_feature_stattest** – Defines a custom statistical test for drift detection in the Data Drift report
    per feature.

    - **cat_target_stattest_func** – Defines a custom statistical test to detect target drift in category target.

    - **num_target_stattest_func** – Defines a custom statistical test to detect target drift in numeric target.



#### all_features_stattest _: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]_ _ = None_ 

#### as_dict()

#### cat_features_stattest _: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]_ _ = None_ 

#### cat_target_stattest_func _: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]_ _ = None_ 

#### cat_target_threshold _: Optional[float]_ _ = None_ 

#### confidence _: Optional[Union[float, Dict[str, float]]]_ _ = None_ 

#### drift_share _: float_ _ = 0.5_ 

#### feature_stattest_func _: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest), Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]]_ _ = None_ 

#### get_feature_stattest_func(feature_name: str, feature_type: str)

#### get_nbinsx(feature_name: str)

#### get_threshold(feature_name: str)

#### nbinsx _: Union[int, Dict[str, int]]_ _ = 10_ 

#### num_features_stattest _: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]_ _ = None_ 

#### num_target_stattest_func _: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]_ _ = None_ 

#### num_target_threshold _: Optional[float]_ _ = None_ 

#### per_feature_stattest _: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]_ _ = None_ 

#### threshold _: Optional[Union[float, Dict[str, float]]]_ _ = None_ 

#### xbins _: Optional[Dict[str, int]]_ _ = None_ 

### _class _ QualityMetricsOptions(conf_interval_n_sigmas: int = 1, classification_threshold: float = 0.5, cut_quantile: Union[NoneType, Tuple[str, float], Dict[str, Tuple[str, float]]] = None)
Bases: `object`


#### as_dict()

#### classification_threshold _: float_ _ = 0.5_ 

#### conf_interval_n_sigmas _: int_ _ = 1_ 

#### cut_quantile _: Union[None, Tuple[str, float], Dict[str, Tuple[str, float]]]_ _ = None_ 

#### get_cut_quantile(feature_name: str)
## Module contents


### _class _ OptionsProvider()
Bases: `object`


#### add(options)

#### get(options_type: Type[TypeParam])
