import io
import json
import logging
import zipfile

import pandas as pd
import requests
import yaml
from sklearn import neighbors, model_selection
from sklearn.datasets import fetch_kddcup99
from sklearn.ensemble import RandomForestRegressor

logging.basicConfig(level=logging.INFO)

DATA_SOURCE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"


base_configuration = {
    "data_format": {
        "separator": ",",
        "header": True,
    },
    "column_mapping": { },
    "service": {
        "reference_path": "./reference.csv",
        "min_reference_size": 30,
        "use_reference": True,
        "moving_reference": False,
        "window_size": 30,
        "calculation_period_sec": 10,
    }
}


def get_data_bike() -> (pd.DataFrame, pd.DataFrame):
    content = requests.get(DATA_SOURCE_URL).content
    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        with arc.open("day.csv") as datafile:
            raw_data = pd.read_csv(datafile, header=0, sep=',', parse_dates=['dteday'])
    ref_data = raw_data[:120]
    prod_data = raw_data[120:]

    target = 'cnt'

    numerical_features = ['mnth', 'temp', 'atemp', 'hum', 'windspeed']
    categorical_features = ['season', 'holiday', 'weekday', 'workingday', 'weathersit']

    features = numerical_features + categorical_features

    logging.info(f"num features: {json.dumps(numerical_features)}")
    logging.info(f"cat features: {json.dumps(categorical_features)}")
    logging.info(f"target: {target}")
    model = RandomForestRegressor(random_state=0)

    model.fit(ref_data[features], ref_data[target])

    ref_data['prediction'] = model.predict(ref_data[features])
    prod_data['prediction'] = model.predict(prod_data[features])

    configuration = base_configuration

    configuration['column_mapping']['target'] = target
    configuration['column_mapping']['numerical_features'] = numerical_features
    configuration['column_mapping']['categorical_features'] = categorical_features

    configuration['service']['monitors'] = ['data_drift', 'regression_performance']

    return ref_data, prod_data, configuration


def get_data_kdd_classification() -> (pd.DataFrame, pd.DataFrame):
    data = fetch_kddcup99(as_frame=True)
    features = list(set(data.feature_names) - {'protocol_type', 'service', 'flag'})
    ref_data, prod_data = model_selection.train_test_split(data.frame, random_state=0, train_size=0.2, test_size=0.1)
    target = data.target_names[0]
    ref_data.reset_index(inplace=True, drop=True)
    ref_data[target] = ref_data[target].apply(lambda x: x.decode('utf8'))
    prod_data.reset_index(inplace=True, drop=True)
    prod_data[target] = prod_data[target].apply(lambda x: x.decode('utf8'))

    model = neighbors.KNeighborsClassifier(n_neighbors=1)
    model.fit(ref_data[features], ref_data[target])

    ref_data['prediction'] = model.predict(ref_data[features])
    prod_data['prediction'] = model.predict(prod_data[features])

    configuration = base_configuration

    configuration['column_mapping']['target'] = target
    configuration['column_mapping']['numerical_features'] = features
    configuration['column_mapping']['categorical_features'] = []

    configuration['service']['monitors'] = ['classification_performance']

    return ref_data[features + [target, 'prediction']], prod_data, configuration


def main(dataset: str):
    if dataset == 'bike':
        ref_data, prod_data, configuration = get_data_bike()
    elif dataset == 'kddcup99':
        ref_data, prod_data, configuration = get_data_kdd_classification()
    else:
        raise ValueError(f'Unexpected dataset: {dataset}, available datasets is ["bike", "kddcup99"]')
    ref_data.to_csv("reference.csv", index=False)
    prod_data.to_csv("production.csv", index=False)

    with open("config.yaml", 'w', encoding='utf8') as conf_file:
        yaml.dump(configuration, conf_file)

    logging.info(f"Reference dataset create with {ref_data.shape[0]} rows")
    logging.info(f"Production dataset create with {prod_data.shape[0]} rows")


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset', type=str, help='Dataset to generate reference.csv, current.csv and config.yaml')

    parsed = parser.parse_args(sys.argv[1:])
    main(parsed.dataset)
