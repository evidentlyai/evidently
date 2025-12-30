import os
import shutil
import zipfile
from pathlib import Path

from sklearn import datasets

data_home = datasets.get_data_home()
print("Path of download datasets to: ", data_home)

# print("Download California Housing dataset...")
# datasets.fetch_california_housing()
print("Unzip LFW people dataset...")

root_dir = Path(__file__).resolve().parents[2]
lfw_zip_path = root_dir / "test_data" / "lfw-dataset.zip"
lfw_home_path = Path(data_home) / "lfw_home"
if not lfw_home_path.exists():
    with zipfile.ZipFile(lfw_zip_path, "r") as zip_ref:
        zip_ref.extractall(data_home)


datasets.fetch_lfw_people()
print("Copying 20 news group dataset...")
shutil.copy(root_dir / "test_data" / "20news-bydate_py3.pkz", data_home)
datasets.fetch_20newsgroups()
print("Copying California Housing...")
shutil.copy(root_dir / "test_data" / "cal_housing_py3.pkz", data_home)
datasets.fetch_california_housing()
print("Download completed.")
print(f"Content of datasets cache: {os.listdir(data_home)}")
