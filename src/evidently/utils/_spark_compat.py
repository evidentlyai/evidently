import warnings
from typing import List
from typing import Tuple
from typing import Union

import numpy as np
import pandas as pd
import pyspark.pandas as ps

Series = Union[pd.Series, ps.Series]
DataFrame = Union[pd.DataFrame, ps.DataFrame]

# todo: overload


def concat(data: Union[List[Series], List[DataFrame]]) -> Union[Series, DataFrame]:
    if all(not isinstance(s, (ps.Series, ps.DataFrame)) for s in data):
        return pd.concat(data)
    spark_type = ps.DataFrame if any(isinstance(d, ps.DataFrame) for d in data) else ps.Series
    data = [s if isinstance(s, spark_type) else spark_type(s) for s in data]
    return ps.concat(data)


def histogram(a: Series, bins: int, density: bool = False) -> Tuple[np.ndarray, np.ndarray]:
    if isinstance(a, pd.Series):
        return np.histogram(a, bins=bins, density=density)

    # todo: check if density needed
    # todo: avoid flatMap somehow
    bins, values = a.to_frame().to_spark().rdd.flatMap(lambda x: x).histogram(bins)  # type: ignore[assignment]
    return np.array(values), np.array(bins)


def spark_warn(*args, message: str):
    if any("spark" in dir(a) for a in args):
        warnings.warn(message)
