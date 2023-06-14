import logging
from pathlib import Path
from typing import List, Text

import pandas as pd
import random
import requests
from sqlalchemy import create_engine

from config.config import DATABASE_URI, DATA_COLUMNS
from src.utils.models import PredictionTable
from src.utils.db_utils import open_sqa_session


logging.basicConfig(
    level=logging.INFO,
    format='SIMULATE - %(levelname)s - %(message)s'
)


def simulate() -> None:
    """Runs a simulation for predicting taxide mand in New York City.
    """

    # Minimal and maximum size of the next batch
    BATCH_MIN_SIZE: int = 10
    BATCH_MAX_SIZE: int = 100
    # Path to test data
    DATA_FEATURES_DIR: Path = Path('data/features')
    TEST_DATA_PATH: Path = DATA_FEATURES_DIR / 'green_tripdata_2021-02.parquet'

    # Load data
    additional_columns: List[Text] = [
        'lpep_pickup_datetime',
        'uuid',
        'duration_min'
    ]
    num_features: List[Text] = DATA_COLUMNS['num_features']
    cat_features: List[Text] = DATA_COLUMNS['cat_features']
    required_columns: List[Text] = (
        additional_columns + num_features + cat_features
    )

    test_data: pd.DataFrame = pd.read_parquet(TEST_DATA_PATH)
    test_data = test_data.loc[:, required_columns]

    # Delete results of previous simulation
    uuids: List[Text] = test_data['uuid'].to_list()
    engine = create_engine(DATABASE_URI)
    session = open_sqa_session(engine)
    delete_query = (
        PredictionTable.__table__.delete()
                                 .where(PredictionTable.uuid.in_(uuids))
    )
    session.execute(delete_query)
    session.commit()
    session.close()

    total_rows_taken: int = 0

    # Get batches until all rows taken
    while total_rows_taken <= test_data.shape[0]:

        # Get batch size (randomly)
        batch_size: int = random.randint(BATCH_MIN_SIZE, BATCH_MAX_SIZE)
        # Get batch
        start_row: int = total_rows_taken
        end_row: int = total_rows_taken + batch_size - 1
        batch: pd.DataFrame = test_data.loc[start_row:end_row, :]

        logging.info(f'Batch size = {batch_size}')

        """
        Make prediction request.
        Send data batch serialized to JSON string.
        """
        resp: requests.Response = requests.post(
            url='http://0.0.0.0:5000/predict',
            json={'features': batch.to_json()}
        )

        if resp.status_code == 200:
            # If OK then extract predictions
            preds_json: Text = resp.json()['predictions']
            predictions: pd.DataFrame = pd.read_json(preds_json)
            # Take just columns: timestamp, ID and predictions
            pred_columns: List[Text] = [
                'lpep_pickup_datetime',
                'uuid',
                'predictions'
            ]
            predictions = predictions[pred_columns].reset_index(drop=True)
            """
            Convert timestamp column to datetime:
                method `to_json()` converts datetime values (in format '%Y-%m-%d %H:%M:%S') to float timestamp (in milliseconds)
            """
            predictions['lpep_pickup_datetime'] = pd.to_datetime(
                predictions['lpep_pickup_datetime'], unit='ms'
            )
            # Output predictions dataframe
            logging.info(f'Predictions:\n{predictions}')
        else:
            error_msg: Text = resp.json()['error_msg']
            logging.info(f'Error: {error_msg}')

        total_rows_taken += batch_size


if __name__ == "__main__":

    simulate()
