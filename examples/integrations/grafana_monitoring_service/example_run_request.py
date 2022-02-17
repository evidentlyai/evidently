#!/usr/bin/env python3

import argparse
import json
import os
import time

import numpy as np
import pandas as pd
import requests


# the encoder helps to convert NumPy types in source data to JSON-compatible types
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.void):
            return None

        if isinstance(obj, (np.generic, np.bool_)):
            return obj.item()

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return obj


def main(csv_file_path, sleep_timeout: int) -> None:
    print("Start send the data to the monitoring service one by one.")
    new_data = pd.read_csv(csv_file_path)

    for idx in range(0, new_data.shape[0]):
        data = new_data.iloc[idx].to_dict()
        print("Send a data item")

        response = requests.post(
            "http://localhost:5000/iterate",
            data=json.dumps([data], cls=NumpyEncoder),
            headers={"content-type": "application/json"},
        )

        if response.status_code == 200:
            print(f"Success.")

        else:
            print(
                f"Got an error code {response.status_code} for the data chunk. "
                f"Reason: {response.reason}, error text: {response.text}"
            )

        print(f"Wait {sleep_timeout} seconds till the next try.")
        time.sleep(sleep_timeout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data sending to Evidently metrics integration demo service"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=int,
        default=10,
        help="Sleep timeout between data send tries in seconds.",
    )
    args = parser.parse_args()
    production_data_file = os.path.abspath("production.csv")
    print(f"Get production data from {production_data_file} and send it to monitoring service each 10 seconds")
    main(production_data_file, args.timeout)
