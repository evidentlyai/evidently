import json

import numpy as np
import pandas as pd


_TYPES_MAPPING = (
    (
        (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64),
        int,
    ),
    ((np.float_, np.float16, np.float32, np.float64), float),
    ((np.ndarray,), lambda obj: obj.tolist()),
    ((np.bool, np.bool_), bool),
    ((pd.Timestamp, pd.Timedelta), str),
    ((np.void, type(pd.NaT)), lambda obj: None),
)


class NumpyEncoder(json.JSONEncoder):
    """Numpy and Pandas data types to JSON types encoder"""

    def default(self, obj):
        """JSON converter calls the method when it cannot convert an object to a Python type
        Convert the object to a Python type

        If we cannot convert the object, leave the default `JSONEncoder` behaviour - raise a TypeError exception.
        """
        for types_list, python_type in _TYPES_MAPPING:
            if isinstance(obj, types_list):
                return python_type(obj)

        return json.JSONEncoder.default(self, obj)
