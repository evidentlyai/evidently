from evidently.base_metric import ColumnNotFound
from evidently.calculation_engine.engine import metric_implementation
from evidently.calculations.data_drift import ColumnDataDriftMetrics
from evidently.core import ColumnType
from evidently.metrics import ColumnDriftMetric
from evidently.options.data_drift import DataDriftOptions
from evidently.spark.calculations.data_drift import get_one_column_drift
from evidently.spark.engine import SparkInputData
from evidently.spark.engine import SparkMetricImplementation


@metric_implementation(ColumnDriftMetric)
class SparkColumnDriftMetric(SparkMetricImplementation[ColumnDriftMetric]):
    def calculate(self, context, data: SparkInputData) -> ColumnDataDriftMetrics:
        if data.reference_data is None:
            raise ValueError("Reference dataset should be present")

        datetime_column = data.data_definition.get_datetime_column()
        datetime_column_name = datetime_column.column_name if datetime_column is not None else None
        try:
            current_feature_data = data.get_current_column(self.metric.column_name, datetime_column_name)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in current dataset")
        try:
            reference_feature_data = data.get_reference_column(self.metric.column_name, datetime_column_name)
        except ColumnNotFound as ex:
            raise ValueError(f"Cannot find column '{ex.column_name}' in reference dataset")

        column_type = ColumnType.Numerical
        if self.metric.column_name.is_main_dataset():
            column_type = data.data_definition.get_column(self.metric.column_name.name).column_type

        options = DataDriftOptions(all_features_stattest=self.metric.stattest, threshold=self.metric.stattest_threshold)
        if self.metric.get_options().render_options.raw_data:
            agg_data = False
        else:
            agg_data = True
        drift_result = get_one_column_drift(
            current_feature_data=current_feature_data,
            reference_feature_data=reference_feature_data,
            column=self.metric.column_name,
            column_type=column_type,
            datetime_column=datetime_column_name,
            data_definition=data.data_definition,
            options=options,
            agg_data=agg_data,
        )

        return ColumnDataDriftMetrics(
            column_name=drift_result.column_name,
            column_type=drift_result.column_type,
            stattest_name=drift_result.stattest_name,
            stattest_threshold=drift_result.stattest_threshold,
            drift_score=drift_result.drift_score,
            drift_detected=drift_result.drift_detected,
            current=drift_result.current,
            scatter=drift_result.scatter,
            reference=drift_result.reference,
        )
