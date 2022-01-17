import json
import time

import pandas
import requests

from evidently.utils import NumpyEncoder


if __name__ == '__main__':
    new_data = pandas.read_csv("production.csv")
    for idx in range(0, new_data.shape[0]):
        # to test request to service sending new data
        data = new_data.iloc[idx].to_dict()
        requests.post('http://localhost:5000/iterate',
                      data=json.dumps([data], cls=NumpyEncoder),
                      headers={"content-type": "application/json"})
        time.sleep(10)
