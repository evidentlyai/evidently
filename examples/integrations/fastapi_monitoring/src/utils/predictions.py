import numpy as np
import pandas as pd

from config.config import DATABASE_URI, DATA_COLUMNS
from sqlalchemy import create_engine
from src.utils.db_utils import open_sqa_session
from src.utils.models import PredictionTable


def prepare_scoring_data(data: pd.DataFrame) -> pd.DataFrame:
    """Prepare scoring data.

    Args:
        data (pd.DataFrame): Input data - Pandas dataframe.

    Returns:
        pd.DataFrame: Pandas dataframe with specific features (columns).
    """

    # Define the target variable, numerical features, and categorical features
    num_features = DATA_COLUMNS['num_features']
    cat_features = DATA_COLUMNS['cat_features']
    data = data.loc[:, num_features + cat_features]

    return data


def get_predictions(data: pd.DataFrame, model) -> np.ndarray:
    """Predictions generation.

    Args:
        data (pd.DataFrame): Pandas dataframe.
        model (_type_): Model object.

    Returns:
        pd.DataFrame: Pandas dataframe with predictions column.
    """

    scoring_data = prepare_scoring_data(data)
    predictions = model.predict(scoring_data)

    return predictions


def save_predictions(predictions: pd.DataFrame) -> None:
    """Save predictions to database.

    Args:
        predictions (pd.DataFrame): Pandas dataframe with predictions column.
    """

    engine = create_engine(DATABASE_URI)
    session = open_sqa_session(engine)
    session.add_all([
        PredictionTable(**pred) for pred in predictions.to_dict('records')
    ])
    session.commit()
