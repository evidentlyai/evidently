import pandas as pd
from sklearn.ensemble import RandomForestRegressor


if __name__ == '__main__':
    raw_data = pd.read_csv('Bike-Sharing-Dataset/day.csv', header=0, sep=',', parse_dates=['dteday'])
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
