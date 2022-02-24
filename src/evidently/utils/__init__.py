import json
import numpy as np
import pandas as pd


class NumpyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (np.void, type(pd.NaT))):
            return None
        if isinstance(o, (np.generic, np.bool_)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return o
