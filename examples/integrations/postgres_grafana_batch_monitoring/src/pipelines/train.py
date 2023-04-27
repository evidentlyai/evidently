import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_absolute_percentage_error


def train() -> None:
    """Train a linear regression model on the given dataset."""

    DATA_DIR = "data/features"

    # Define the target variable, numerical features, and categorical features
    target = "duration_min"
    num_features = ["passenger_count", "trip_distance", "fare_amount", "total_amount"]
    cat_features = ["PULocationID", "DOLocationID"]

    print("Load train data")
    data = pd.read_parquet(f"{DATA_DIR}/green_tripdata_2021-01.parquet")

    # Filter out outliers
    data = data[(data.duration_min >= 1) & (data.duration_min <= 60)]
    data = data[(data.passenger_count > 0) & (data.passenger_count <= 6)]

    # Split data into training and validation sets
    train_data = data.loc[:30000, :]
    val_data = data.loc[30000:, :]

    print("Train model")
    model = LinearRegression()
    model.fit(
        X=train_data[num_features + cat_features],
        y=train_data[target],
    )

    print("Get predictions for validation")
    train_preds = model.predict(train_data[num_features + cat_features])
    val_preds = model.predict(val_data[num_features + cat_features])

    print("Calculate validation metrics: MAE")
    # Scoring
    print(mean_absolute_error(train_data[target], train_preds))
    print(mean_absolute_error(val_data[target], val_preds))

    print("Calculate validation metrics: MAPE")
    print(mean_absolute_percentage_error(train_data[target], train_preds))
    print(mean_absolute_percentage_error(val_data[target], val_preds))

    print("Save the model")
    joblib.dump(model, "models/model.joblib")


if __name__ == "__main__":

    train()
