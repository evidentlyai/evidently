#!/usr/bin/env python3

import argparse
import json
import os
import time
from typing import Dict

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


def send_data_row(dataset_name: str, data: Dict) -> None:
    print(f"Send a data item for {dataset_name}")

    try:
        response = requests.post(
            f"http://localhost:8085/iterate/{dataset_name}",
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

    except requests.exceptions.ConnectionError as error:
        print(f"Cannot reach a metrics application, error: {error}, data: {data}")


def main(sleep_timeout: int) -> None:
    datasets_path = os.path.abspath("datasets")
    if not os.path.exists(datasets_path):
        exit("Cannot find datasets, try to run run_example.py script for initial setup")

    print(
        f"Get production data from {datasets_path} and send the data to monitoring service each {args.timeout} seconds"
    )
    datasets = {}
    max_index = 0

    for dataset_name in os.listdir(datasets_path):
        production_data_path = os.path.join(datasets_path, dataset_name, "production.csv")
        new_data = pd.read_csv(production_data_path)
        datasets[dataset_name] = new_data
        max_index = max(max_index, new_data.shape[0])

    for idx in range(0, max_index):
        for dataset_name, dataset in datasets.items():
            dataset_size = dataset.shape[0]
            data = dataset.iloc[idx % dataset_size].to_dict()
            send_data_row(dataset_name, data)

        print(f"Wait {sleep_timeout} seconds till the next try.")
        time.sleep(sleep_timeout)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data sending to Evidently metrics integration demo service"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=2,
        help="Sleep timeout between data send tries in seconds.",
    )
    args = parser.parse_args()
    main(args.timeout)
