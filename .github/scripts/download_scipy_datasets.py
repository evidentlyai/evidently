import os

from sklearn import datasets

data_home = datasets.get_data_home()
print("Path of download datasets to: ", data_home)

print("Download California Housing dataset...")
datasets.fetch_california_housing()
print("Download LFW people dataset...")
datasets.fetch_lfw_people()
print("Download 20 news group dataset...")
datasets.fetch_20newsgroups()
print("Download completed.")
print(f"Content of datasets cache: {os.listdir(data_home)}")
