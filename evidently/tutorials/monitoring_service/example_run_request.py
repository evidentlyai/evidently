import json
import time

import numpy as np
import pandas
import requests

_integer_types = (np.int_, np.intc, np.intp,
                  np.int8, np.int16, np.int32,
                  np.int64, np.uint8, np.uint16, np.uint32, np.uint64)
_float_types = (np.float_, np.float16, np.float32, np.float64)


class NumpyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, _integer_types):
            return int(o)
        if isinstance(o, (np.float_, np.float16, np.float32, np.float64)):
            return float(o)
        if isinstance(o, (np.ndarray,)):
            return o.tolist()
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.void):
            return None

        return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    new_data = pandas.read_csv("production.csv")
    for idx in range(0, new_data.shape[0]):
        # to test request to service sending new data
        data = new_data.iloc[idx].to_dict()
        requests.post('http://localhost:5000/iterate',
                      data=json.dumps([data], cls=NumpyEncoder),
                      headers={"content-type": "application/json"})
        time.sleep(10)
