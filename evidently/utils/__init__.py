import json
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, np.void):
            return None
        if isinstance(o, (np.generic, np.bool_)):
            return o.item()
        if isinstance(o, np.ndarray):
            return o.tolist()
        return o
