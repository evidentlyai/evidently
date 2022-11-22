# Supported Data Formats
At the moment Evidently works with datasets in **Pandas DataFrame** **format** **only**.
These datasets should fit into memory to be processed correctly.

In this tutorial you will see how to load and sample data from other data sources to Pandas DataFrame for further analysis with Evidently.


## Tensorflow Datasets
Tensorflow supports conversion from Tensorflow Dataset to Pandas DataFrame with `as_dataframe` method.

For bigger datasets that do not fit into memory use `take` for sampling before conversion.
Check that the dataset is **shuffled** to obtain a representative sample.
```python
import tensorflow_datasets as tfds

MAXIMUM_DATASET_SIZE = 10000 # set up the maximum number of lines in your sample

# tensorflow_ds is a shuffled Tensorflow Dataset
pandas_df = tfds.as_dataframe(tensorflow_ds.take(MAXIMUM_DATASET_SIZE))
```
> Note that `as_dataframe` method loads everything **in memory**,
make sure to run it on a sample from your dataset to control for its size

## Pytorch Datapipes
To sample data from Pytorch Datapipes shuffle it first with `shuffle()` and take the first batch of the chosen size.
This sample can be converted to Pandas DataFrame

See example with AG News dataset:
```python
import pandas as pd
from torchdata.datapipes.iter import HttpReader

MAXIMUM_DATASET_SIZE = 10000 # set up the maximum number of lines in your sample

# Load data to Pytorch Datapipe
URL = "https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/master/data/ag_news_csv/train.csv"
ag_news_train = HttpReader([URL]).parse_csv().map(lambda t: (int(t[0]), " ".join(t[1:])))

# Shuffle and sample data
batches = ag_news_train.shuffle().batch(MAXIMUM_DATASET_SIZE)
sample = next(iter(batches))

# Load sampled data to Pandas DataFrame
pandas_df = pd.DataFrame({'text': [el[1] for el in sample],
                         'label': [el[0] for el in sample]})
```
Note that resulting Pandas DataFrame schema is arbitrary, just make sure to specify text and target columns with
[column_mapping]((../../../../book/test-and-reports/column-mapping.md)) later

## PySpark DataFrames
PySpark supports conversion to Pandas DataFrame with `toPandas()` method.

For bigger DataFrames that do not fit into memory use `sample` for sampling before conversion.
```python
fraction = 0.5 # set the fraction of original DataFrame to be sampled

# df_spark is a PySpark DataFrame
df_pandas = df_spark.sample(withReplacement=False, fraction=fraction, seed=None).toPandas()
```
You can ensure that sampling provides the same result each run by passing a fixed `seed` value to `sample` method

## Files in a directory
If your data is organized in separate files for each text with folder names corresponding to class labels, like so:
```
main_directory/
...class_a/
......a_text_file_1.txt
......a_text_file_2.txt
...class_b/
......b_text_file_1.txt
......b_text_file_2.txt
```
use the following steps to sample data preserving the balance of classes:
```python
import os, random
import pandas as pd

DIRECTORY_NAME = '/main_directory/' # define data source directory
MAXIMUM_DATASET_SIZE = 10000 # set up the maximum number of lines in your sample

# find the names of classes
classes_names = [class_name for class_name in os.listdir(DIRECTORY_NAME) \
                if os.path.isdir(os.path.join(DIRECTORY_NAME, class_name))]

# determine classes sizes
classes_sizes_dict = {class_name: len(os.listdir(os.path.join(DIRECTORY_NAME,
                                                             class_name))) \
                     for class_name in classes_names}
total_size = sum(classes_sizes_dict.values())

# sample objects from classes in the correct proportion
texts = []
labels = []

for class_name in classes_names:
 sample_size = int((classes_sizes_dict[class_name] / total_size) * MAXIMUM_DATASET_SIZE)
 random_files_names = random.sample(os.listdir(os.path.join(DIRECTORY_NAME, class_name)),
                                    sample_size)
 for file_name in random_files_names:
   with open(os.path.join(DIRECTORY_NAME, class_name, file_name), 'r') as f:
         text = f.read()
   texts.append(text)
   labels.append(class_name)

# load sampled data to Pandas DataFrame
df_pandas = pd.DataFrame({'text': texts, 'label': labels})
```

