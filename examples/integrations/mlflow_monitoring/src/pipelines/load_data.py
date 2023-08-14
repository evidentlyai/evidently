import datetime
import io
import os
import pandas as pd
import requests
from typing import Text
import zipfile

import requests
from tqdm import tqdm

from config import DATA_DIR, FILENAME


def download_data(destination_path: Text):
    """
    Download the Bike Sharing dataset from UCI machine learning repository
    
    More information about the dataset can be found in UCI machine learning repository: https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset

    Acknowledgement: Fanaee-T, Hadi, and Gama, Joao, 'Event labeling combining ensemble detectors and background knowledge', Progress in Artificial Intelligence (2013): pp. 1-15, Springer Berlin Heidelberg
    """

    SOURCE_URL = "https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip"

    content = requests.get(SOURCE_URL).content
    with zipfile.ZipFile(io.BytesIO(content)) as arc:
        raw_data = pd.read_csv(arc.open("hour.csv"), header=0, sep=',', parse_dates=['dteday']) 
        
    raw_data.index = raw_data.apply(lambda row: datetime.datetime.combine(row.dteday.date(), datetime.time(row.hr)), axis=1)

    raw_data.to_csv(destination_path, index=False)
    print(f"Data downloaded to file: {destination_path}")


if __name__ == "__main__":
    download_data(f"{DATA_DIR}/{FILENAME}")
