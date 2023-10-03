import logging
from typing import Callable, Text

from evidently import ColumnMapping
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
    Response,
    FileResponse
)
from pydantic import BaseModel
import pandas as pd

from config.config import DATA_COLUMNS
from src.utils.data import load_current_data, load_reference_data
from src.utils.predictions import get_predictions, save_predictions
from src.utils.reports import (
    get_column_mapping,
    build_model_performance_report,
    build_target_drift_report
)
from utils import ModelLoader


logging.basicConfig(
    level=logging.INFO,
    format='FASTAPI_APP - %(asctime)s - %(levelname)s - %(message)s'
)


class Features(BaseModel):
    """Features model."""
    features: Text


app = FastAPI()
model_loader: ModelLoader = ModelLoader()


@app.get('/')
def index() -> HTMLResponse:
    return HTMLResponse('<h1><i>Evidently + FastAPI</i></h1>')


@app.post('/predict')
def predict(
    response: Response,
    features_item: Features,
    background_tasks: BackgroundTasks
) -> JSONResponse:
    try:
        # Receive features item and read features batch
        features: pd.DataFrame = pd.read_json(features_item.features)
        # Compute predictions
        model: Callable = model_loader.get_model()
        features['predictions'] = get_predictions(features, model)
        # Save predictions to database (in the background)
        background_tasks.add_task(save_predictions, features)
        # Return JSON with predictions dataframe serialized to JSON string
        return JSONResponse(content={'predictions': features.to_json()})
    except Exception as e:
        response.status_code = 500
        logging.error(e, exc_info=True)
        return JSONResponse(content={'error_msg': str(e)})


@app.get('/monitor-model')
def monitor_model_performance(window_size: int = 3000) -> FileResponse:

    logging.info('Read current data')
    current_data: pd.DataFrame = load_current_data(window_size)

    logging.info('Read reference data')
    reference_data = load_reference_data(columns=DATA_COLUMNS['columns'])

    logging.info('Build report')
    column_mapping: ColumnMapping = get_column_mapping(**DATA_COLUMNS)
    report_path: Text = build_model_performance_report(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )

    logging.info('Return report as html')
    return FileResponse(report_path)


@app.get('/monitor-target')
def monitor_target_drift(window_size: int = 3000) -> FileResponse:

    logging.info('Read current data')
    current_data: pd.DataFrame = load_current_data(window_size)

    logging.info('Read reference data')
    reference_data = load_reference_data(columns=DATA_COLUMNS['columns'])

    logging.info('Build report')
    column_mapping: ColumnMapping = get_column_mapping(**DATA_COLUMNS)
    report_path: Text = build_target_drift_report(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )

    logging.info('Return report as html')
    return FileResponse(report_path)
