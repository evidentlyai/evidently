import os
from typing import Text

import requests
from tqdm import tqdm


def download_data(destination: Text):
    """
    Download a list of files from a specified URL and
    save them to the given destination directory.

    Parameters:
    ----------
    destination : Text
        The path to the directory where the downloaded files will be saved.

    Example:
    -------
    destination_directory = "path/to/destination_directory"
    download_data(destination_directory)
    """

    NYC_SOURCE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

    files = ["green_tripdata_2021-01.parquet", "green_tripdata_2021-02.parquet"]

    print("Download files:")
    for file in files:

        url = f"{NYC_SOURCE_URL}/{file}"
        resp = requests.get(url, stream=True)

        # Ensure destination directory exists
        os.makedirs(destination, exist_ok=True)
        save_path = os.path.join(destination, file)

        with open(save_path, "wb") as handle:

            total_size = int(resp.headers.get("Content-Length", 0))
            progress_bar = tqdm(total=total_size, desc=file, unit="B", unit_scale=True)

            for data in resp.iter_content(chunk_size=8192):

                handle.write(data)
                progress_bar.update(len(data))

            progress_bar.close()

    print("Download complete.")


if __name__ == "__main__":

    DATA_RAW_DIR = "data/raw"

    download_data(DATA_RAW_DIR)
