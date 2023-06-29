import pandas as pd
from sqlalchemy import create_engine, select
from typing import List, Text

from config.config import DATABASE_URI
from src.utils.models import PredictionTable


def load_current_data(window_size: int) -> pd.DataFrame:
    engine = create_engine(DATABASE_URI)
    with engine.connect() as db_connection:
        order = PredictionTable.lpep_pickup_datetime.desc()
        query = (
            select(PredictionTable).order_by(order)
                                   .limit(window_size)
        )
        current_data: pd.DataFrame = pd.read_sql_query(
            sql=query,
            con=db_connection
        )
        current_data.drop('id', axis=1, inplace=True)
    return current_data


def load_reference_data(columns: List[Text]) -> pd.DataFrame:

    DATA_REF_DIR = "data/reference"
    ref_path = f"{DATA_REF_DIR}/reference_data_2021-01.parquet"
    ref_data = pd.read_parquet(ref_path)
    reference_data = ref_data.loc[:, columns]
    return reference_data
