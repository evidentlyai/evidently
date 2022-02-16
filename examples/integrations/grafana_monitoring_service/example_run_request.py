import argparse
import os
import time

import csv
import requests


def main(csv_file_path):
    print("Start send the data to the monitoring service one by one.")
    with open(csv_file_path, encoding='utf-8') as csv_file:
        production_data = csv.DictReader(csv_file)

        for data in production_data:
            print("Send a data item")
            requests.post("http://127.0.0.1:5000/iterate", data=data, headers={"content-type": "application/json"})
            print("Done.")
            time.sleep(10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    args = parser.parse_args()
    production_data_file = os.path.abspath("production.csv")
    print("Get production data from {production_data_file} and send it to monitoring service each 10 seconds")
    main(production_data_file)
