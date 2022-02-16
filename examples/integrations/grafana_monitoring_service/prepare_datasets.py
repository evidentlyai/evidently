#!/usr/bin/env python3

import argparse
import io
import json
import zipfile

import pandas as pd
import requests
import yaml
from sklearn import neighbors, model_selection
from sklearn.ensemble import RandomForestRegressor


# suppress SettingWithCopyWarning: warning
pd.options.mode.chained_assignment = None


BIKE_DATA_SOURCE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"
BIKE_DATASET_NAME = "bike"
KDD_DATASET_NAME = "kdd"
DATA_SOURCES = (BIKE_DATASET_NAME, KDD_DATASET_NAME)


base_configuration = {
    "data_format": {
        "separator": ",",
        "header": True,
    },
    "column_mapping": {},
    "service": {
        "reference_path": "./reference.csv",
        "min_reference_size": 30,
        "use_reference": True,
        "moving_reference": False,
        "window_size": 30,
        "calculation_period_sec": 10,
    },
}


def get_data_bike() -> (pd.DataFrame, pd.DataFrame):
    print(f"Load data for dataset: {BIKE_DATASET_NAME}")

    content = requests.get(BIKE_DATA_SOURCE_URL).content
    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        with arc.open("day.csv") as datafile:
            raw_data = pd.read_csv(datafile, header=0, sep=",", parse_dates=["dteday"])
    reference_bike_data = raw_data[:120]
    production_bike__data = raw_data[120:]

    target = "cnt"
    numerical_features = ["mnth", "temp", "atemp", "hum", "windspeed"]
    categorical_features = ["season", "holiday", "weekday", "workingday", "weathersit"]

    features = numerical_features + categorical_features

    print(f"num features: {json.dumps(numerical_features)}")
    print(f"cat features: {json.dumps(categorical_features)}")
    print(f"target: {target}")

    # get predictions
    model = RandomForestRegressor(random_state=0)
    model.fit(reference_bike_data[features], reference_bike_data[target])
    reference_bike_data["prediction"] = model.predict(reference_bike_data[features])
    production_bike__data["prediction"] = model.predict(production_bike__data[features])

    # setup service configuration
    configuration = base_configuration
    configuration["column_mapping"]["target"] = target
    configuration["column_mapping"]["numerical_features"] = numerical_features
    configuration["column_mapping"]["categorical_features"] = categorical_features
    configuration["service"]["monitors"] = ["data_drift", "regression_performance"]

    return reference_bike_data, production_bike__data, configuration


def get_data_kdd_classification() -> (pd.DataFrame, pd.DataFrame):
    print(f"Load data for dataset: {KDD_DATASET_NAME}")

    # local import for make other cases faster
    from sklearn.datasets import fetch_kddcup99

    data = fetch_kddcup99(as_frame=True)
    features = list(set(data.feature_names) - {"protocol_type", "service", "flag"})
    reference_kdd_data, production_kdd_data = model_selection.train_test_split(
        data.frame, random_state=0, train_size=0.2, test_size=0.1
    )
    target = data.target_names[0]
    reference_kdd_data.reset_index(inplace=True, drop=True)
    reference_kdd_data[target] = reference_kdd_data[target].apply(lambda x: x.decode("utf8"))
    production_kdd_data.reset_index(inplace=True, drop=True)
    production_kdd_data[target] = production_kdd_data[target].apply(lambda x: x.decode("utf8"))

    classification_model = neighbors.KNeighborsClassifier(n_neighbors=1)
    classification_model.fit(reference_kdd_data[features], reference_kdd_data[target])

    reference_kdd_data["prediction"] = classification_model.predict(reference_kdd_data[features])
    production_kdd_data["prediction"] = classification_model.predict(production_kdd_data[features])

    # setup service configuration
    configuration = base_configuration
    configuration["column_mapping"]["target"] = target
    configuration["column_mapping"]["numerical_features"] = features
    configuration["column_mapping"]["categorical_features"] = []
    configuration["service"]["monitors"] = ["classification_performance"]

    return reference_kdd_data[features + [target, "prediction"]], production_kdd_data, configuration


def main(dataset: str) -> None:
    print(f'Generate test data for dataset "{dataset}"')

    if dataset == BIKE_DATASET_NAME:
        ref_data, prod_data, configuration = get_data_bike()

    elif dataset == KDD_DATASET_NAME:
        ref_data, prod_data, configuration = get_data_kdd_classification()

    else:
        raise ValueError(f"Unexpected dataset: {dataset}, available datasets: {DATA_SOURCES}")

    ref_data.to_csv("reference.csv", index=False)
    prod_data.to_csv("production.csv", index=False)

    print("Generate config file...")
    with open("config.yaml", "w", encoding="utf8") as conf_file:
        yaml.dump(configuration, conf_file)
    print("Done.")

    print(f"Reference dataset was created with {ref_data.shape[0]} rows")
    print(f"Production dataset was created with {prod_data.shape[0]} rows")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    parser.add_argument(
        "-d",
        "--dataset",
        choices=DATA_SOURCES,
        type=str,
        default=BIKE_DATASET_NAME,
        help="Dataset for reference.csv, current.csv and config.yaml generation.",
    )

    args = parser.parse_args()
    main(args.dataset)
