# Contributing to Evidently

Thank you for considering contributing to Evidently!

## How can you contribute?
We welcome both code and none-code contributions. You can:
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
* Make sure that all the tests are passed sucessfully 
* Submit a Pull Request with described changes 

### Additional information
- Evidently is under active development. 
- We are happy to receive a pull request for bug fixes or new functions for any section of the library. If you need help or guidance, you can open an Issue first.
- The only exception is UI, because it is in the process of significant refactoring! If you want to contribute to UI, please first come to our [Discord channel](https://discord.gg/xZjKRaNp8b) for a quick chat.  
- We highly recommend that you open an issue, describe your contribution, share all needed information there and link it to a pull request.
- We evaluate pull requests taking into account: code architecture and quality, code style, comments & docstrings and coverage by tests.

## 1. Clone repository
```sh
git clone https://github.com/evidentlyai/evidently.git
```

## 2. (Optional, but recommended!) Create virtual environment

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

## 3. Use local copy as editable dependency
To use the cloned version in the virtual environment as a package, you need to install the package in the editable mode:

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

## 4. Run the tests
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
To run the tests, first convert all the notebooks to a python script, then download the required datasets and run the script to check that all computation is executed correctly. It can be done by using the following commands: 

```sh
jupyter nbconvert --to script evidently/examples/*.ipynb --output-dir example_scripts
curl https://archive.ics.uci.edu/ml/machine-learning-databases/00275/Bike-Sharing-Dataset.zip -o Bike-Sharing-Dataset.zip &&
             unzip Bike-Sharing-Dataset.zip -d Bike-Sharing-Dataset
python example_test.py
```

## 5. (first come to our [Discord channel](https://discord.gg/xZjKRaNp8b) for a quick chat) Working with UI


### Requirements
To build UI, you need:
- `nodejs` and `npm` https://nodejs.org/en/download/
- `yarn` https://yarnpkg.com/getting-started/install


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
