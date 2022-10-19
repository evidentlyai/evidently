# Contributing to Evidently

Thank you for considering contributing to Evidently!

## How can you contribute?
We welcome both code and non-code contributions. You can:
* Report a bug
* Improve documentation
* Submit a bug fix
* Propose a new feature or improvement 
* Contribute a new feature or improvement  
* Test Evidently 

## Code contributions
Here is the general workflow:
* Fork the Evidently repository 
* Clone the repository 
* Make the changes and commit them 
* Push the branch to your local fork
* Make sure that all the tests are passing sucessfully 
* Submit a Pull Request with described changes 

### Additional information
- Evidently is under active development. 
- We are happy to receive a Pull Request for bug fixes or new functions for any section of the library. If you need help or guidance, you can open an Issue first.
- The only exception is UI, because it is in the process of significant refactoring! If you want to contribute to UI, please first come to our [Discord channel](https://discord.gg/xZjKRaNp8b) for a quick chat.  
- We highly recommend that you open an issue, describe your contribution, share all needed information there and link it to a Pull Request.
- We evaluate Pull Requests taking into account: code architecture and quality, code style, comments & docstrings and coverage by tests.

## 1. Clone repository
```sh
git clone https://github.com/evidentlyai/evidently.git
```

## 2. (Optional, but recommended!) Create virtual environment with python 3.6
Note: 3.6 is the earliest python version we support. 
Although you probably use one of the most recent python version, it is important to make sure that your changes do not cause any issues in older python versions. This is why we sugget you test them under the oldest supported python version.

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

## 3. Install requirements
You need to have installed:
- `nodejs` and `npm` https://nodejs.org/en/download/
- `yarn` https://yarnpkg.com/getting-started/install

## 4. Use local copy as editable dependency
To use the cloned version in the virtual environment as a package, you need to install the package in the editable mode.
See official pip documentation for examples and explanations: https://pip.pypa.io/en/stable/cli/pip_install/#examples

#### MacOS / Linux
```sh
cd /path/to/evidently_repo
pip install -e ".[dev]"
```

#### Windows
```sh
cd C:\path\to\evidently_repo
pip install -e .[dev]
```

## 5. Run formatters, linters, unit tests
### Running black 
We use black for code auto formatting.
```sh
black .
```

### Running isort 
We use black for imports auto formatting.
```sh
isort .
```

### Running flake8 
We use flake8 for code style checks.
```sh
flake8 src
flake8 tests
```

### Running mypy
We use mypy for object types checks.
```sh
# if you are running for the first time, use `mypy --install-types` instead
mypy
```

### Running unit tests
Currently, the project is not fully covered by unit tests, but we are going to add more soon and expect to receive PRs with some unit tests 🙂
```sh
pytest -v tests
```

### Running smoke tests
Together with the unit tests we use smoke testing: we basically run all the notebooks from the [examples](https://github.com/evidentlyai/evidently/tree/main/evidently/examples).
To run the tests, first convert all the notebooks to a python script, then download the required datasets and run the script to check that all computation is executed correctly. It can be done by using the following commands: 

```sh
jupyter nbconvert --to script evidently/examples/*.ipynb --output-dir example_scripts
curl https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip -o Bike-Sharing-Dataset.zip &&
             unzip Bike-Sharing-Dataset.zip -d Bike-Sharing-Dataset
python example_test.py
```

## 6. (first come to our [Discord channel](https://discord.gg/xZjKRaNp8b) for a quick chat) Working with UI

### Building UI
One-time build:
```shell
cd ui
yarn
yarn build
```

Watched build (any changes to the UI source files will be automatically recompiled):
```shell
cd ui
yarn
yarn watch
```
