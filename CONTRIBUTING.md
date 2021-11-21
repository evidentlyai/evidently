# Contributing to Evidently

Thank you for considering contributing to Evidently!

## Support question
- Evidently is under active development. 
- We are happy to receive a pull request for bug fixes or new functions for any section of the library. 
- The only exception is UI, because it is a subject of significant refactoring! If you want to contribute to UI, please first come to our [Discord channel](https://discord.gg/xZjKRaNp8b) for a quick chat.  
- We highly recommend that you open an issue, describe your contribution, share all needed information there and link it to a pull request.
- We evaluate pull requests taking into account: code architecture and quality, code style, comments & docstrings and coverage by tests.

## Clone repository
```sh
git clone https://github.com/evidentlyai/evidently.git
```

## (Optional, but recommended!) Create virtual environment

#### MacOS / Linux
```sh
cd /path/to/evidently_repo
python3 -m venv venv
. venv/bin/activate
```

#### Windows
```sh
cd C:\path\to\evidently_repo
py -m venv venv
.\venv\Scripts\activate
```

## Use local copy as editable dependency
For using cloned version in the virtual environment as a package you need to install the package in the editable mode:

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

## Run the tests
### Running flake8 
We use flake8 for code style checks.
```sh
flake8 evidently
```

### Running mypy
We use mypy for object types checks.
```sh
mypy
```

### Running unit tests
Currently the project is not fully covered by unit tests, but we adding more soon and expect to receive PRs with some unit tests 🙂
```sh
python -m unittest discover -s evidently -p 'test_*.py' -v
```

### Running smoke tests
Together with the unit tests we use smoke testing: we basically run all the notebooks from the [examples](https://github.com/evidentlyai/evidently/tree/main/evidently/examples).
To run the tests first convert all the notebooks to python script, then download required datasets and run all script to check that all computation executed correctly. It can be done by using  the following commands: 

```sh
jupyter nbconvert --to script evidently/examples/*.ipynb --output-dir example_scripts
curl https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip -o Bike-Sharing-Dataset.zip &&
             unzip Bike-Sharing-Dataset.zip -d Bike-Sharing-Dataset
python example_test.py
```

## (first come to our [Discord channel](https://discord.gg/xZjKRaNp8b) for a quick chat) Working with UI


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