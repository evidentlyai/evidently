import json
import numpy as np


_integer_types = (np.int_, np.intc, np.intp, np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64)
_float_types = (np.float_, np.float16, np.float32, np.float64)


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, _integer_types):
            return int(obj)
        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.void):
            return None

        return json.JSONEncoder.default(self, obj)
