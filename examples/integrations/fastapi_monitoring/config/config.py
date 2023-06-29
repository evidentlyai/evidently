import os
from typing import Dict, Text

host: Text = os.getenv('MONITORING_DB_HOST', 'localhost')
DATABASE_URI: Text = f'postgresql://admin:admin@{host}:5432/monitoring_db'

DATA_COLUMNS: Dict = {
    'target_col': 'duration_min',
    'prediction_col': 'predictions',
    'num_features': [
        'passenger_count', 'trip_distance', 'fare_amount', 'total_amount'
    ],
    'cat_features': ['PULocationID', 'DOLocationID']
}
DATA_COLUMNS['columns'] = (
    DATA_COLUMNS['num_features'] +
    DATA_COLUMNS['cat_features'] +
    [DATA_COLUMNS['target_col'], DATA_COLUMNS['prediction_col']]
)
