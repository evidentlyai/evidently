#Contributing

### Clone repository

```sh
git clone https://github.com/evidentlyai/evidently.git
```

### (Recommended) Create virtual environment

#### MacOS / Linux
```shell
cd /path/to/evidently_repo
python3 -m venv venv
. venv/bin/activate
```

#### Windows
```commandline
cd C:\path\to\evidently_repo
py -m venv venv
.\venv\Scripts\activate
```

### Using local copy as editable dependency
For using cloned version in virtual environment as package you need to install package in editable mode:

#### MacOS / Linux
```sh
cd /path/to/evidently_repo
pip install -e .[dev]
```

#### Windows
```sh
cd C:\path\to\evidently_repo
pip install -e .[dev]
```

### Running PyLint
Example of running PyLint checks as is is executed on GitHub CI.
```shell
pylint evidently --disable=R
```

### Running tests

```shell
python -m unittest discover -s evidently -p 'test_*.py' -v
```

### Running examples smoke tests

Convert all example notebooks to script, download required datasets and run all script to check that all computation executed correctly.

```shell
jupyter nbconvert --to script evidently/examples/*.ipynb --output-dir example_scripts
curl https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip -o Bike-Sharing-Dataset.zip &&
             unzip Bike-Sharing-Dataset.zip -d Bike-Sharing-Dataset
python example_test.py
```

## Working with UI

### Requirements

For building ui required:
- `nodejs` and `npm` https://nodejs.org/en/download/
- `yarn` https://yarnpkg.com/getting-started/install

### Building UI

One-time build:
```shell
cd ui
yarn
yarn build
```

Watched build (any changes to UI source files will be automatically recompiled):
```shell
cd ui
yarn
yarn watch
```