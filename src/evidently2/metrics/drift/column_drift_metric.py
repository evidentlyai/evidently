from typing import Optional

from evidently2.calculations.basic import CleanColumn
from evidently2.calculations.basic import CreateSet
from evidently2.calculations.basic import DropInf
from evidently2.calculations.basic import DropNA
from evidently2.calculations.basic import Histogram
from evidently2.calculations.basic import UnionList
from evidently2.calculations.basic import Unique
from evidently2.calculations.stattests.base import get_stattest
from evidently2.core.calculation import Calculation
from evidently2.core.calculation import InputColumnData
from evidently2.core.calculation import InputData
from evidently2.core.metric import BaseMetric
from evidently2.core.metric import ColumnMetricResultCalculation
from evidently.base_metric import ColumnMetricResult
from evidently.base_metric import ColumnName
from evidently.base_metric import ColumnNotFound
from evidently.core import ColumnType
from evidently.metric_results import Distribution
from evidently.options import DataDriftOptions
from evidently.utils.data_preprocessing import DataDefinition


class ColumnDriftResult(ColumnMetricResult):
    stattest_name: str
    stattest_threshold: Optional[float]
    drift_score: float
    drift_detected: bool

    current_small_distribution: Distribution
    reference_small_distribution: Optional[Distribution]


# todo: generate dynamically?
class ColumnDriftResultCalculation(ColumnMetricResultCalculation[ColumnDriftResult]):
    stattest_name: str
    stattest_threshold: Optional[float]
    drift_score: Calculation
    drift_detected: Calculation

    current_small_distribution: Calculation
    reference_small_distribution: Calculation


class ColumnDriftMetric(BaseMetric[ColumnDriftResult]):
    """Calculate drift metric for a column"""

    column_name: ColumnName
    stattest: Optional[str]
    stattest_threshold: Optional[float]

    def get_calculation(self, data: InputData) -> ColumnDriftResultCalculation:
        try:
            current_feature_data = data.get_current_column(self.column_name)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in current dataset")
        try:
            reference_feature_data = data.get_reference_column(self.column_name)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in reference dataset")

        column_type = ColumnType.Numerical
        if self.column_name.is_main_dataset():
            column_type = data.data_definition.get_column(self.column_name.name).column_type
        options = DataDriftOptions(all_features_stattest=self.stattest, threshold=self.stattest_threshold)
        drift_result = get_one_column_drift(
            current_feature_data=current_feature_data,
            reference_feature_data=reference_feature_data,
            column=self.column_name,
            column_type=column_type,
            options=options,
            data_definition=data.data_definition,
        )

        return drift_result




def get_unique_not_nan_values_list_from_series(current_data: Calculation, reference_data: Calculation) -> Calculation:
    """Get unique values from current and reference series, drop NaNs"""
    return UnionList(
        input_data=CreateSet(input_data=Unique(input_data=DropNA(input_data=current_data))),
        second=CreateSet(input_data=Unique(input_data=DropNA(input_data=reference_data))),
    )
    # return list(set(reference_data.dropna().unique()) | set(current_data.dropna().unique()))






def get_one_column_drift(
    *,
    current_feature_data: InputColumnData,
    reference_feature_data: InputColumnData,
    column: ColumnName,
    options: DataDriftOptions,
    data_definition: DataDefinition,
    column_type: ColumnType,
) -> ColumnDriftResultCalculation:
    if column_type not in (ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text):
        raise ValueError(f"Cannot calculate drift metric for column '{column}' with type {column_type}")

    target = data_definition.get_target_column()
    stattest = None
    threshold = None
    if column.is_main_dataset():
        if target and column.name == target.column_name and column_type == ColumnType.Numerical:
            stattest = options.num_target_stattest_func

        elif target and column.name == target.column_name and column_type == ColumnType.Categorical:
            stattest = options.cat_target_stattest_func

        if not stattest:
            stattest = options.get_feature_stattest_func(column.name, column_type.value)

        threshold = options.get_threshold(column.name, column_type.value)
    current_column = current_feature_data
    reference_column = reference_feature_data

    # clean and check the column in reference dataset
    reference_column = CleanColumn(
        input_data=reference_column
    )  # reference_column.replace([-np.inf, np.inf], np.nan).dropna()

    if reference_column.empty:
        raise ValueError(
            f"An empty column '{column.name}' was provided for drift calculation in the reference dataset."
        )

    # clean and check the column in current dataset
    current_column = CleanColumn(
        input_data=current_column
    )  # current_column.replace([-np.inf, np.inf], np.nan).dropna()

    if current_column.empty:
        raise ValueError(f"An empty column '{column.name}' was provided for drift calculation in the current dataset.")

    current_small_distribution = None
    reference_small_distribution = None

    # if column_type == ColumnType.Numerical:
    #     if not pd.api.types.is_numeric_dtype(reference_column):
    #         raise ValueError(f"Column '{column}' in reference dataset should contain numerical values only.")
    #
    #     if not pd.api.types.is_numeric_dtype(current_column):
    #         raise ValueError(f"Column '{column}' in current dataset should contain numerical values only.")

    drift_test_function = get_stattest(reference_column, column_type.value, stattest)
    drift_result = drift_test_function(reference_column, current_column, column_type.value, threshold)

    if column_type == ColumnType.Numerical:
        current_nbinsx = options.get_nbinsx(column.name)

        current_small_distribution = Histogram(DropInf(input_data=current_column), bins=current_nbinsx, density=True)
        reference_small_distribution = Histogram(
            DropInf(input_data=reference_column), bins=current_nbinsx, density=True
        )

    metrics = ColumnDriftResultCalculation(
        column_name=column.name,
        column_type=column_type.name,
        stattest_name=drift_test_function.display_name,
        stattest_threshold=drift_result.actual_threshold,
        drift_score=drift_result.drift_score,
        drift_detected=drift_result.drifted,
        current_small_distribution=current_small_distribution,
        reference_small_distribution=reference_small_distribution,
    )

    return metrics
