"""Methods for clean null or NaN values in a dataset"""

import numpy as np
import pandas as pd


def replace_infinity_values_to_nan(dataframe: pd.DataFrame) -> pd.DataFrame:
    #   document somewhere, that all analyzers are mutators, i.e. they will change
    #   the dataframe, like here: replace inf and nan values.
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    return dataframe
