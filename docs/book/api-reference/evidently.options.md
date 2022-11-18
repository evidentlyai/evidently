# evidently.options package

## Submodules

## evidently.options.color_scheme module


### _class_ evidently.options.color_scheme.ColorOptions(primary_color: str = '#ed0400', secondary_color: str = '#4d4d4d', current_data_color: Optional[str] = None, reference_data_color: Optional[str] = None, color_sequence: Sequence[str] = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4'), fill_color: str = 'LightGreen', zero_line_color: str = 'green', non_visible_color: str = 'white', underestimation_color: str = '#6574f7', overestimation_color: str = '#ee5540', majority_color: str = '#1acc98', vertical_lines: str = 'green', heatmap: str = 'RdBu_r')
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


#### color_sequence(_: Sequence[str_ _ = ('#ed0400', '#0a5f38', '#6c3461', '#71aa34', '#d8dcd6', '#6b8ba4'_ )

#### current_data_color(_: Optional[str_ _ = Non_ )

#### fill_color(_: st_ _ = 'LightGreen_ )

#### get_current_data_color()

#### get_reference_data_color()

#### heatmap(_: st_ _ = 'RdBu_r_ )

#### majority_color(_: st_ _ = '#1acc98_ )

#### non_visible_color(_: st_ _ = 'white_ )

#### overestimation_color(_: st_ _ = '#ee5540_ )

#### primary_color(_: st_ _ = '#ed0400_ )

#### reference_data_color(_: Optional[str_ _ = Non_ )

#### secondary_color(_: st_ _ = '#4d4d4d_ )

#### underestimation_color(_: st_ _ = '#6574f7_ )

#### vertical_lines(_: st_ _ = 'green_ )

#### zero_line_color(_: st_ _ = 'green_ )
## evidently.options.data_drift module


### _class_ evidently.options.data_drift.DataDriftOptions(confidence: Optional[Union[float, Dict[str, float]]] = None, threshold: Optional[Union[float, Dict[str, float]]] = None, drift_share: float = 0.5, nbinsx: Union[int, Dict[str, int]] = 10, xbins: Optional[Dict[str, int]] = None, feature_stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest), Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]] = None, all_features_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, cat_features_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_features_stattest: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, per_feature_stattest: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]] = None, cat_target_threshold: Optional[float] = None, num_target_threshold: Optional[float] = None, cat_target_stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None, num_target_stattest_func: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]] = None)
Bases: `object`

Configuration for Data Drift calculations.


#### confidence()
Defines the confidence level for statistical tests.
Applies to all features (if passed as float) or certain features (if passed as dictionary).
(Deprecated) Use threshold to define confidence level for statistical

> tests as more universal solution.


* **Type**

    Optional[Union[float, Dict[str, float]]]



#### threshold()
Defines thresholds for statistical tests.
Applies to all features (if passed as float) or certain features (if passed as dictionary).


* **Type**

    Optional[Union[float, Dict[str, float]]]



#### drift_share()
Sets the share of drifting features as a condition for Dataset Drift in the Data Drift report.


* **Type**

    float



#### nbinsx()
Defines the number of bins in a histogram.
Applies to all features (if passed as int) or certain features (if passed as dictionary).


* **Type**

    Union[int, Dict[str, int]]



#### xbins()
Defines the boundaries for the size of a specific bin in a histogram.


* **Type**

    Optional[Dict[str, int]]



#### feature_stattest_func()
Defines a custom statistical test for drift detection in the Data Drift report.
Applies to all features (if passed as a function) or individual features (if a dict).
(Deprecated) Use all_features_stattest or per_feature_stattest.


* **Type**

    Optional[Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest), Dict[str, Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]]



#### all_features_stattest()
Defines a custom statistical test for drift detection in the Data Drift report
for all features.


* **Type**

    Optional[Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]



#### cat_features_stattest()
Defines a custom statistical test for drift detection in the Data Drift report
for categorical features only.


* **Type**

    Optional[Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]



#### num_features_stattest()
Defines a custom statistical test for drift detection in the Data Drift report
for numerical features only.


* **Type**

    Optional[Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]



#### per_feature_stattest()
Defines a custom statistical test for drift detection in the Data Drift report
per feature.


* **Type**

    Optional[Dict[str, Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]



#### cat_target_stattest_func()
Defines a custom statistical test to detect target drift in category target.


* **Type**

    Optional[Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]



#### num_target_stattest_func()
Defines a custom statistical test to detect target drift in numeric target.


* **Type**

    Optional[Union[str, Callable[[pandas.core.series.Series, pandas.core.series.Series, str, float], Tuple[float, bool]], [evidently.calculations.stattests.registry.StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]



#### all_features_stattest(_: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]_ _ = Non_ )

#### as_dict()

#### cat_features_stattest(_: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]_ _ = Non_ )

#### cat_target_stattest_func(_: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]_ _ = Non_ )

#### cat_target_threshold(_: Optional[float_ _ = Non_ )

#### confidence(_: Optional[Union[float, Dict[str, float]]_ _ = Non_ )

#### drift_share(_: floa_ _ = 0._ )

#### feature_stattest_func(_: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest), Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]]_ _ = Non_ )

#### get_feature_stattest_func(feature_name: str, feature_type: str)

#### get_nbinsx(feature_name: str)

#### get_threshold(feature_name: str)

#### nbinsx(_: Union[int, Dict[str, int]_ _ = 1_ )

#### num_features_stattest(_: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]_ _ = Non_ )

#### num_target_stattest_func(_: Optional[Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]_ _ = Non_ )

#### num_target_threshold(_: Optional[float_ _ = Non_ )

#### per_feature_stattest(_: Optional[Dict[str, Union[str, Callable[[Series, Series, str, float], Tuple[float, bool]], [StatTest](api-reference/evidently.calculations.stattests.md#evidently.calculations.stattests.registry.StatTest)]]_ _ = Non_ )

#### threshold(_: Optional[Union[float, Dict[str, float]]_ _ = Non_ )

#### xbins(_: Optional[Dict[str, int]_ _ = Non_ )
## evidently.options.quality_metrics module


### _class_ evidently.options.quality_metrics.QualityMetricsOptions(conf_interval_n_sigmas: int = 1, classification_threshold: float = 0.5, cut_quantile: Union[NoneType, Tuple[str, float], Dict[str, Tuple[str, float]]] = None)
Bases: `object`


#### as_dict()

#### classification_threshold(_: floa_ _ = 0._ )

#### conf_interval_n_sigmas(_: in_ _ = _ )

#### cut_quantile(_: Union[None, Tuple[str, float], Dict[str, Tuple[str, float]]_ _ = Non_ )

#### get_cut_quantile(feature_name: str)
## Module contents


### _class_ evidently.options.OptionsProvider()
Bases: `object`


#### add(options)

#### get(options_type: Type[TypeParam])
