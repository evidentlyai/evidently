import os
from typing import Text

import requests
from config import DATA_FILES
from config import DATA_RAW_DIR
from config import DATA_SOURCE_URL
from tqdm import tqdm


def download_data(destination: Text):
    """
    Download a list of DATA_FILES from a specified URL and
    save them to the given destination directory.

    Parameters:
    ----------
    destination : Text
        The path to the directory with saved DATA_FILES

    Example:
    -------
    destination_directory = "path/to/destination_directory"
    download_data(destination_directory)
    """

    print("Download DATA_FILES:")
    for file in DATA_FILES:

        url = f"{DATA_SOURCE_URL}/{file}"
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

    download_data(DATA_RAW_DIR)
