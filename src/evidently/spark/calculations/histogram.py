from typing import Optional
from typing import Tuple

import numpy as np
from pyspark.sql import functions as sf

from evidently.spark.base import SparkSeries


def get_histogram(df: SparkSeries, column_name: str, nbinsx: int, density: bool, *,         dmax: Optional[float] = None,
        dmin: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
    if dmax is None or dmin is None:
        col_range = df.select(sf.min(df[column_name]).alias("min"), sf.max(df[column_name]).alias("max")).first()
        min_val, max_val = col_range["min"], col_range["max"]
        if min_val == max_val:
            min_val -= .5
            max_val += .5
    else:
        min_val, max_val = dmin, dmax
    step = (max_val - min_val) / nbinsx
    hist = (
        df.select(column_name, sf.floor((sf.col(column_name) - min_val) / step).alias("bucket"))
        .select(column_name, sf.when(sf.col("bucket") >= nbinsx, nbinsx - 1).otherwise(sf.col("bucket")).alias("bucket"))
        .groupby("bucket")
        .count()
    )
    hist_values = {r.bucket: r["count"] for r in hist.collect()}
    n = np.array([hist_values.get(i, 0) for i in range(nbinsx)])
    bin_edges = np.array([min_val + step * i for i in range(nbinsx + 1)])

    if density:
        db = np.array(np.diff(bin_edges), float)

        return (n/db/n.sum()).tolist(), bin_edges

    return n, bin_edges


def hist_bin_doane(data: SparkSeries, column_name: str) -> Tuple[int, Optional[float], Optional[float]]:
    """
    Doane's histogram bin estimator.

    Improved version of Sturges' formula which works better for
    non-normal data. See
    stats.stackexchange.com/questions/55134/doanes-formula-for-histogram-binning
    """
    data = data.cache()
    size = data.count()
    if size > 2:
        sg1 = np.sqrt(6.0 * (size - 2) / ((size + 1.0) * (size + 3)))
        stats = data.select(sf.max(column_name).alias("max"), sf.min(column_name).alias("min"), sf.mean(column_name).alias("mean"), sf.stddev_pop(column_name).alias("std")).first()
        sigma = stats["std"]
        if sigma > 0.0:
            g1 = data.select(sf.mean(sf.pow(((sf.col(column_name) - stats["mean"]) / sigma), 3)).alias("g1")).first()["g1"]
            dmax, dmin = stats["max"], stats["min"]
            width = (dmax - dmin) / (1.0 + np.log2(size) + np.log2(1.0 + np.absolute(g1) / sg1))
            return int(np.ceil((dmax - dmin) / width)), dmax, dmin
    return 1, None, None

