import logging

import pandas as pd
import requests
import zipfile
import io
from sklearn.ensemble import RandomForestRegressor


logging.basicConfig(level=logging.INFO)


if __name__ == '__main__':
    content = requests.get("https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip").content
    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        raw_data = pd.read_csv(arc.open("day.csv"), header=0, sep=',', parse_dates=['dteday'])
    ref_data = raw_data[:120]
    prod_data = raw_data[120:]

    target = 'cnt'
    datetime = 'dteday'

    numerical_features = ['mnth', 'temp', 'atemp', 'hum', 'windspeed']
    categorical_features = ['season', 'holiday', 'weekday', 'workingday', 'weathersit',]

    features = numerical_features + categorical_features
    model = RandomForestRegressor(random_state=0)

    model.fit(ref_data[features], ref_data[target])

    ref_data['prediction'] = model.predict(ref_data[features])
    prod_data['prediction'] = model.predict(prod_data[features])

    ref_data.to_csv("reference.csv", index=False)
    prod_data.to_csv("production.csv", index=False)

    logging.info(f"Reference dataset create with {ref_data.shape[0]} rows")
    logging.info(f"Production dataset create with {prod_data.shape[0]} rows")
