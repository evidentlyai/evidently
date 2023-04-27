from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base


Base = declarative_base()


# [Data drift]


class DataDriftPredictionTable(Base):
    """Implement table for prediction column drift metrics.
    Evidently metric functions:
        - DataDriftPreset/DataDriftTable
    """

    __tablename__ = "data_drift_prediction"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)
    column_name = Column(String)
    column_type = Column(String)
    stattest_name = Column(String)
    drift_score = Column(Float)
    drift_detected = Column(Boolean)
    threshold = Column(Float)


# [Data quality]


class DataQualityTable(Base):
    """Implement table for data quality metrics.
    Evidently metric functions:
        - DataDriftPreset/DatasetDriftMetric
        - DatasetSummaryMetric
    """

    __tablename__ = "data_quality"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)

    # DataDriftPreset/DatasetDriftMetric fields
    drift_share = Column(Float)
    ds_drift_metric_number_of_columns = Column(Integer)
    number_of_drifted_columns = Column(Integer)
    share_of_drifted_columns = Column(Float)
    dataset_drift = Column(Boolean)

    # DatasetSummaryMetric fields
    summary_metric_number_of_columns = Column(Integer)
    number_of_rows = Column(Integer)
    number_of_missing_values = Column(Integer)
    number_of_categorical_columns = Column(Integer)
    number_of_numeric_columns = Column(Integer)
    number_of_text_columns = Column(Integer)
    number_of_datetime_columns = Column(Integer)
    number_of_constant_columns = Column(Integer)
    number_of_almost_constant_columns = Column(Integer)
    number_of_duplicated_columns = Column(Integer)
    number_of_almost_duplicated_columns = Column(Integer)
    number_of_empty_rows = Column(Integer)
    number_of_empty_columns = Column(Integer)
    number_of_duplicated_rows = Column(Integer)


# [Model performance]


class ModelPerformanceTable(Base):
    """Implement table for model performance metrics.
    Evidently metric functions:
        - RegressionQualityMetric
    """

    __tablename__ = "model_performance"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)
    r2_score = Column(Float)
    rmse = Column(Float)
    rmse_default = Column(Float)
    mean_error = Column(Float)
    me_default_sigma = Column(Float)
    mean_abs_error = Column(Float)
    mean_abs_error_default = Column(Float)
    mean_abs_perc_error = Column(Float)
    mean_abs_perc_error_default = Column(Float)
    abs_error_max = Column(Float)
    abs_error_max_default = Column(Float)
    error_std = Column(Float)
    abs_error_std = Column(Float)
    abs_perc_error_std = Column(Float)
    mean_error_ref = Column(Float)
    mean_abs_error_ref = Column(Float)
    mean_abs_perc_error_ref = Column(Float)
    rmse_ref = Column(Float)
    r2_score_ref = Column(Float)
    abs_error_max_ref = Column(Float)
    error_std_ref = Column(Float)
    abs_error_std_ref = Column(Float)
    abs_perc_error_std_ref = Column(Float)


# [Target drift]


class TargetDriftTable(Base):
    """Implement table for target drift metrics.
    Evidently metric functions:
        - ColumnDriftMetric from target column
    """

    __tablename__ = "target_drift"
    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)
    stattest_name = Column(String)
    stattest_threshold = Column(Float)
    drift_score = Column(Float)
    drift_detected = Column(Boolean)
