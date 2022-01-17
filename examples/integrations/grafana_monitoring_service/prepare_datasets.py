import io
import logging
import zipfile

import requests

import pandas as pd
from sklearn.ensemble import RandomForestRegressor

logging.basicConfig(level=logging.INFO)

DATA_SOURCE_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip"


def main():
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
    model = RandomForestRegressor(random_state=0)

    model.fit(ref_data[features], ref_data[target])

    ref_data['prediction'] = model.predict(ref_data[features])
    prod_data['prediction'] = model.predict(prod_data[features])

    ref_data.to_csv("reference.csv", index=False)
    prod_data.to_csv("production.csv", index=False)

    logging.info(f"Reference dataset create with {ref_data.shape[0]} rows")
    logging.info(f"Production dataset create with {prod_data.shape[0]} rows")


if __name__ == '__main__':
    main()
