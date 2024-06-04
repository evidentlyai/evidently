import datetime

import pandas as pd

from evidently import ColumnMapping
from evidently.metric_results import Histogram
from evidently.metric_results import HistogramData
from evidently.metrics.data_integrity.column_missing_values_metric import ColumnMissingValuesMetric
from evidently.metrics.data_integrity.column_regexp_metric import ColumnRegExpMetric
from evidently.metrics.data_integrity.column_summary_metric import CategoricalCharacteristics
from evidently.metrics.data_integrity.column_summary_metric import ColumnSummaryMetric
from evidently.metrics.data_integrity.column_summary_metric import ColumnSummaryResult
from evidently.metrics.data_integrity.column_summary_metric import DataInTime
from evidently.metrics.data_integrity.column_summary_metric import DataInTimePlots
from evidently.metrics.data_integrity.column_summary_metric import DataQualityPlot
from evidently.metrics.data_integrity.column_summary_metric import NumericCharacteristics
from evidently.metrics.data_integrity.dataset_missing_values_metric import DatasetMissingValuesMetric
from evidently.metrics.data_integrity.dataset_summary_metric import DatasetSummaryMetric
from tests.multitest.conftest import AssertExpectedResult
from tests.multitest.conftest import Error
from tests.multitest.conftest import NoopOutcome
from tests.multitest.datasets import TestDataset
from tests.multitest.metrics.conftest import TestMetric
from tests.multitest.metrics.conftest import metric


@metric
def column_missing_values_metric():
    return TestMetric(
        name="column_missing_values_metric",
        outcomes=NoopOutcome(),
        fingerprint="5d3b481ddcecc29ae0b4d13b6320584d",
        metric=ColumnMissingValuesMetric(column_name="education"),
        dataset_names=["adult"],
    )


@metric
def column_summary_metric():
    return TestMetric(
        name="column_summary_metric",
        metric=ColumnSummaryMetric(column_name="age"),
        fingerprint="197479ae0fbf53d686a80879c6dc15a0",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def column_summary_metric_period():
    m = ColumnSummaryMetric(column_name="feature1")
    return TestMetric(
        name="column_summary_metric_period",
        metric=m,
        fingerprint="70e0137212718c89b2ce52f86ab05568",
        outcomes={
            TestDataset(
                current=pd.DataFrame(
                    {
                        "feature1": [1.0, 2.0, 3.0],
                        "datetime": [
                            datetime.datetime(2023, 10, 1),
                            datetime.datetime(2023, 11, 1),
                            datetime.datetime(2023, 12, 1),
                        ],
                    },
                ),
                column_mapping=ColumnMapping(datetime="datetime"),
            ): AssertExpectedResult(
                metric=m,
                result=ColumnSummaryResult(
                    column_name="feature1",
                    column_type="num",
                    current_characteristics=NumericCharacteristics(
                        number_of_rows=3,
                        count=3,
                        missing=0,
                        missing_percentage=0,
                        infinite_count=0,
                        infinite_percentage=0,
                        max=3,
                        mean=2,
                        min=1,
                        most_common=1,
                        most_common_percentage=33.33,
                        p25=1.5,
                        p50=2,
                        p75=2.5,
                        std=1,
                        unique=3,
                        unique_percentage=100,
                    ),
                    plot_data=DataQualityPlot(
                        bins_for_hist=Histogram(
                            current=HistogramData(
                                x=pd.Series([1.0, 1.6666666666666665, 2.333333333333333], name="x"),
                                count=pd.Series([1, 1, 1], name="count"),
                            ),
                            current_log=HistogramData(
                                x=pd.Series(
                                    [0.0, 0.11928031367991561, 0.23856062735983122, 0.35784094103974684], name="x"
                                ),
                                count=pd.Series([1, 0, 1, 1], name="count"),
                            ),
                        ),
                        counts_of_values={"current": pd.DataFrame({"x": [1.0, 2.0, 3.0], "count": [1, 1, 1]})},
                        data_in_time=DataInTime(
                            data_for_plots=DataInTimePlots(
                                current=pd.DataFrame(
                                    {
                                        "period": [
                                            pd.Period(freq="D", year=2023, month=10, day=1),
                                            pd.Period(freq="D", year=2023, month=11, day=1),
                                            pd.Period(freq="D", year=2023, month=12, day=1),
                                        ],
                                        "feature1": [1.0, 2.0, 3.0],
                                        "datetime": [
                                            datetime.datetime(2023, 10, 1),
                                            datetime.datetime(2023, 11, 1),
                                            datetime.datetime(2023, 12, 1),
                                        ],
                                    }
                                )
                            ),
                            freq="day",
                            datetime_name="datetime",
                        ),
                    ),
                ),
            )
        },
    )


@metric
def column_summary_metric_success():
    m = ColumnSummaryMetric(column_name="target")
    return TestMetric(
        name="column_summary_metric_success",
        metric=m,
        fingerprint="57b116392d131f49a9bfddc96ed47981",
        outcomes={
            TestDataset(
                current=pd.DataFrame({"target": [1, "ff", 3], "prediction": ["a", "b", "c"]}),
                reference=None,
                column_mapping=ColumnMapping(),
            ): AssertExpectedResult(
                metric=m,
                result=ColumnSummaryResult(
                    column_name="target",
                    column_type="cat",
                    reference_characteristics=None,
                    current_characteristics=CategoricalCharacteristics(
                        number_of_rows=3,
                        count=3,
                        unique=3,
                        unique_percentage=100.0,
                        most_common=1,
                        most_common_percentage=33.33,
                        missing=0,
                        missing_percentage=0.0,
                        new_in_current_values_count=None,
                        unused_in_current_values_count=None,
                    ),
                    plot_data=DataQualityPlot(
                        bins_for_hist=Histogram(
                            current=HistogramData.from_df(pd.DataFrame(dict(x=["1", "ff", "3"], count=[1, 1, 1])))
                        ),
                        data_in_time=None,
                        data_by_target=None,
                        counts_of_values={"current": pd.DataFrame(dict(x=[1, "ff", 3], count=[1, 1, 1]))},
                    ),
                ),
            ),
            TestDataset(
                current=pd.DataFrame(
                    {
                        "col": [1, 2, 1, 2, 1],
                    }
                ),
                reference=None,
            ): Error(ValueError, "Column 'target' not found in dataset."),
            TestDataset(
                current=pd.DataFrame(
                    {
                        "col2": [1, 2, 1, 2, 1],
                    }
                ),
                reference=pd.DataFrame(
                    {
                        "col": [1, 2, 1, 2, 1],
                    }
                ),
            ): Error(ValueError, "Column 'target' not found in dataset."),
        },
    )


@metric
def dataset_summary_metric():
    return TestMetric(
        name="dataset_summary_metric",
        metric=DatasetSummaryMetric(),
        fingerprint="73e2d2120edf79849d278a646b956563",
        outcomes=NoopOutcome(),
    )


@metric
def column_reg_exp_metric():
    return TestMetric(
        name="column_reg_exp_metric",
        metric=ColumnRegExpMetric(column_name="relationship", reg_exp=r".*child.*"),
        fingerprint="1df27c0657e9d250aca810f0b4a5d0d1",
        outcomes=NoopOutcome(),
        dataset_names=["adult"],
    )


@metric
def dataset_missing_values_metric():
    return TestMetric(
        name="dataset_missing_values_metric",
        metric=DatasetMissingValuesMetric(),
        fingerprint="3f7377d36855eeb727e71a2a8cc255b9",
        outcomes=NoopOutcome(),
    )
