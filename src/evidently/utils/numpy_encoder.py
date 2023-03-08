import datetime
import json

import numpy as np
import pandas as pd

from evidently.utils.types import ApproxValue

_TYPES_MAPPING = (
    (
        (
            np.int_,
            np.intc,
            np.intp,
            np.int8,
            np.int16,
            np.int32,
            np.int64,
            np.uint8,
            np.uint16,
            np.uint32,
            np.uint64,
        ),
        int,
    ),
    ((np.float_, np.float16, np.float32, np.float64), float),
    ((np.ndarray,), lambda obj: obj.tolist()),
    ((np.bool_), bool),
    ((pd.Timedelta,), str),
    (
        (np.void, type(pd.NaT)),
        lambda obj: None,
    ),  # should be before datetime as NaT is subclass of datetime.
    ((pd.Timestamp, datetime.datetime, datetime.date), lambda obj: obj.isoformat()),
    # map ApproxValue to json value
    ((ApproxValue,), lambda obj: obj.as_dict()),
)


class NumpyEncoder(json.JSONEncoder):
    """Numpy and Pandas data types to JSON types encoder"""

    def default(self, o):
        """JSON converter calls the method when it cannot convert an object to a Python type
        Convert the object to a Python type

        If we cannot convert the object, leave the default `JSONEncoder` behaviour - raise a TypeError exception.
        """
        for types_list, python_type in _TYPES_MAPPING:
            if isinstance(o, types_list):
                return python_type(o)

        return json.JSONEncoder.default(self, o)
