from typing import Optional, Tuple

import pandas as pd
from pyspark.sql import DataFrame, functions as sf

from evidently.core import ColumnType
from evidently.metric_results import Distribution
from evidently.spark.base import SparkSeries
from evidently.spark.calculations.histogram import get_histogram, hist_bin_doane
from evidently.utils.visualizations import OPTIMAL_POINTS

PERIOD_COL = "period"


def prepare_df_for_time_index_plot(
        df: DataFrame,
        column_name: str,
        datetime_name: Optional[str],
        # prefix: Optional[str] = None,
        # freq: Optional[str] = None,
        # bins: Optional[np.ndarray] = None,
) -> Tuple[pd.DataFrame, Optional[str]]:
    if datetime_name is not None:
        prefix, pattern, freq = choose_agg_period(df[datetime_name], None)
        date_col = sf.col(datetime_name)
        if pattern == "week":
            period_col = sf.concat(sf.year(date_col), "-", sf.weekofyear(date_col)).alias(PERIOD_COL)
        else:
            period_col = sf.date_format(date_col, pattern).alias(PERIOD_COL)
        plot_df = df.select(column_name, period_col).groupby(period_col).agg(sf.mean(column_name).alias("mean"),
                                                                             sf.stddev_pop(column_name).alias("std"))
        if pattern == "week":
            split = sf.split(PERIOD_COL, "-")
            week = split.getItem(1)
            year = sf.to_timestamp(split.getItem(0), "y")
            week_start_diff = sf.date_format(year, "F")
            plot_df = plot_df.select("*", sf.date_add(year, week * 7 - week_start_diff).alias(PERIOD_COL)).toPandas()
        return plot_df, prefix

    plot_df = df.rdd.zipWithIndex().toDF().select(sf.col("_1").getItem(column_name).alias(column_name),
                                                  sf.floor(sf.col("_2") / OPTIMAL_POINTS).alias(PERIOD_COL))
    plot_df = plot_df.groupby(PERIOD_COL).agg(sf.mean(column_name).alias("mean"), sf.stddev_pop(column_name).alias("std")).toPandas()
    return plot_df, None


def choose_agg_period(current_date: DataFrame, reference_date: Optional[DataFrame], date_column_name: str) -> Tuple[str, str, str]:
    prefix_dict = {
        "A": ("year", "y"),
        "Q": ("quarter", "y-Q"),
        "M": ("month", "y-M"),
        "W": ("week", "week"),  # exception cause date_format does not have week of year
        "D": ("day", "y-M-d"),
        "H": ("hour", "y-M-d:H"),
    }
    date_stats = current_date.select(sf.min(date_column_name).alias("max"), sf.max(date_column_name).alias("min")).first()
    max_date, min_date = date_stats["max"], date_stats["min"]
    if reference_date is not None:
        date_stats = current_date.select(sf.min(date_column_name).alias("max"), sf.max(date_column_name).alias("min")).first()
        max_date, min_date = max(max_date, date_stats["max"]), min(min_date, date_stats["min"])
    days = (max_date - min_date).days
    time_points = pd.Series(
        index=["A", "Q", "M", "W", "D", "H"],
        data=[
            abs(OPTIMAL_POINTS - days / 365),
            abs(OPTIMAL_POINTS - days / 90),
            abs(OPTIMAL_POINTS - days / 30),
            abs(OPTIMAL_POINTS - days / 7),
            abs(OPTIMAL_POINTS - days),
            abs(OPTIMAL_POINTS - days * 24),
        ],
    )
    period_prefix, pattern = prefix_dict[time_points.idxmin()]
    return period_prefix, pattern, str(time_points.idxmin())


def get_distribution_for_column(
        *, column_type: ColumnType, column_name: str, current: SparkSeries, reference: Optional[SparkSeries] = None
) -> Tuple[Distribution, Optional[Distribution]]:
    reference_distribution: Optional[Distribution] = None

    if column_type == ColumnType.Categorical:
        current_distribution = get_distribution_for_category_column(current, column_name)

        if reference is not None:
            reference_distribution = get_distribution_for_category_column(reference, column_name)

    elif column_type == ColumnType.Numerical:
        if reference is not None:
            bins, dmax, dmin = hist_bin_doane(current.dropna().union(reference.dropna()), column_name)
            reference_distribution = get_distribution_for_numerical_column(reference, column_name, bins=bins, dmax=dmax, dmin=dmin)

        else:
            bins, dmax, dmin = hist_bin_doane(current.dropna(), column_name)

        current_distribution = get_distribution_for_numerical_column(current, column_name, bins=bins, dmax=dmax, dmin=dmin)

    else:
        raise ValueError(f"Cannot get distribution for a column with type {column_type}")

    return current_distribution, reference_distribution


def get_distribution_for_category_column(column: SparkSeries, column_name: str) -> Distribution:
    value_counts = column.groupby(column_name).agg(sf.count_distinct(column_name).alias("count")).toPandas()
    return Distribution(
        x=value_counts["count"],
        y=value_counts[column_name],
    )


def get_distribution_for_numerical_column(
        column: SparkSeries,
        column_name: str,
        bins: Optional[int] = None,
        dmax: Optional[float] = None,
        dmin: Optional[float] = None
) -> Distribution:
    bins = bins or hist_bin_doane(column, column_name)
    histogram = get_histogram(column, column_name, nbinsx=bins, density=False, dmax=dmax, dmin=dmin)
    return Distribution(
        x=histogram[1],
        y=histogram[0],
    )
