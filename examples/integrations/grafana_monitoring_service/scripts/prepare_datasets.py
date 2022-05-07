#!/usr/bin/env python3

import argparse
import io
import logging
import os
import shutil
import zipfile
from typing import Tuple

import pandas as pd
import requests


# suppress SettingWithCopyWarning: warning
pd.options.mode.chained_assignment = None


BIKE_DATA_SOURCE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"


def setup_logger() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler()
        ]
    )


def get_data_bike_random_forest() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get bike dataset with random forest model prediction"""
    return get_data_bike(True)


def get_data_bike_gradient_boosting() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Get bike dataset with gradient boosting model"""
    return get_data_bike(False)


def get_data_bike(use_model: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
    content = requests.get(BIKE_DATA_SOURCE_URL).content

    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        with arc.open("day.csv") as datafile:
            raw_data = pd.read_csv(datafile, header=0, sep=",", parse_dates=["dteday"])

    reference_bike_data = raw_data[:120]
    production_bike_data = raw_data[120:]

    target = "cnt"
    numerical_features = ["mnth", "temp", "atemp", "hum", "windspeed"]
    categorical_features = ["season", "holiday", "weekday", "workingday", "weathersit"]

    features = numerical_features + categorical_features

    if use_model:
        from sklearn.ensemble import RandomForestRegressor
        # get predictions with random forest
        model = RandomForestRegressor(random_state=0)

    else:
        from sklearn.ensemble import GradientBoostingRegressor
        model = GradientBoostingRegressor(random_state=0)

    model.fit(reference_bike_data[features], reference_bike_data[target])
    reference_bike_data["prediction"] = model.predict(reference_bike_data[features])
    production_bike_data["prediction"] = model.predict(production_bike_data[features])

    return reference_bike_data, production_bike_data


def get_data_kdd_classification() -> Tuple[pd.DataFrame, pd.DataFrame]:
    from sklearn import neighbors
    from sklearn import model_selection

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

    return reference_kdd_data[features + [target, "prediction"]], production_kdd_data


def main(dataset_name: str, dataset_path: str) -> None:
    logging.info("Generate test data for dataset %s", dataset_name)
    dataset_path = os.path.abspath(dataset_path)

    if os.path.exists(dataset_path):
        logging.info("Path %s already exists, remove it", dataset_path)
        shutil.rmtree(dataset_path)

    os.makedirs(dataset_path)

    reference_data, production_data = DATA_SOURCES[dataset_name]()
    logging.info("Save datasets to %s", dataset_path)
    reference_data.to_csv(os.path.join(dataset_path, "reference.csv"), index=False)
    production_data.to_csv(os.path.join(dataset_path, "production.csv"), index=False)

    logging.info("Reference dataset was created with %s rows", reference_data.shape[0])
    logging.info("Production dataset was created with %s rows", production_data.shape[0])


DATA_SOURCES = {
    "bike_random_forest": get_data_bike_random_forest,
    "bike_gradient_boosting": get_data_bike_gradient_boosting,
    "kdd_k_neighbors_classifier": get_data_kdd_classification,
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Script for data and config generation for demo Evidently metrics integration with Grafana"
    )
    parser.add_argument(
        "-d",
        "--dataset",
        choices=DATA_SOURCES.keys(),
        type=str,
        help="Dataset name for reference.csv= and production.csv files generation.",
    )
    parser.add_argument(
        "-p",
        "--path",
        type=str,
        help="Path for saving dataset files.",
    )

    args = parser.parse_args()
    setup_logger()
    if args.dataset not in DATA_SOURCES:
        exit(f"Incorrect dataset name {args.dataset}, try to see correct names with --help")
    main(args.dataset, args.path)
