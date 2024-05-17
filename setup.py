#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
from os.path import join as pjoin

from setuptools import setup

from setupbase import HERE
from setupbase import combine_commands
from setupbase import create_cmdclass
from setupbase import ensure_targets
from setupbase import install_npm

nb_path = pjoin(HERE, "src", "evidently", "nbextension", "static")

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, "index.js"),
]

package_data_spec = {
    "evidently": [
        "nbextension/static/*.*js*",
        "nbextension/static/*.*woff2*",
        "ui/assets/*",
        "ui/assets/static/css/*",
        "ui/assets/static/js/*",
        "ui/assets/static/img/*",
    ]
}

data_files_spec = [
    ("share/jupyter/nbextensions/evidently", nb_path, "*.js*"),
    ("share/jupyter/nbextensions/evidently", nb_path, "*.woff2"),
    ("etc/jupyter/nbconfig/notebook.d", HERE, "evidently.json"),
]

cmdclass = create_cmdclass("jsdeps", package_data_spec=package_data_spec, data_files_spec=data_files_spec)
cmdclass["jsdeps"] = combine_commands(
    install_npm(os.path.join(HERE, "ui"), build_cmd="build"),
    ensure_targets(jstargets),
)

setup_args = dict(
    cmdclass=cmdclass,
    author_email="emeli.dral@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "plotly>=5.10.0",
        "statsmodels>=0.12.2",
        "scikit-learn>=1.0.1",
        "pandas[parquet]>=1.3.5",
        "numpy>=1.22.0",
        "nltk>=3.6.7",
        "scipy>=1.10.0",
        "requests>=2.31.0",
        "PyYAML>=5.4",
        "pydantic>=1.10.13",
        "litestar>=2.8.3",
        "typing-inspect>=0.9.0",
        "uvicorn[standard]>=0.22.0",
        "watchdog>=3",
        "typer>=0.3",
        "rich>=13",
        "iterative-telemetry>=0.0.5",
        "dynaconf>=3.2.4",
        "certifi>=2023.07.22",
        "urllib3>=1.26.18",
        "fsspec>=2024.2.0",
        "ujson>=5.4.0",
    ],
    extras_require={
        "dev": [
            "pip-audit>=2.7.2",
            "wheel==0.38.1",
            "setuptools==65.5.1; python_version < '3.12'",
            "setuptools==68.2.2; python_version >= '3.12'",
            "jupyter==1.0.0",
            "mypy==0.981",
            "pytest==7.4.4",
            "types-PyYAML==6.0.1",
            "types-requests==2.26.0",
            "types-dataclasses==0.6",
            "types-python-dateutil==2.8.19",
            "types-ujson>=5.4.0",
            "pillow==10.3.0",
            "httpx==0.24.1",
            "ruff==0.3.7",
            "pre-commit==3.5.0",
        ],
        "llm": [
            "openai>=1.16.2",
            "evaluate>=0.4.1",
            "transformers[torch]>=4.39.3",
            "sentence-transformers==2.7.0",
        ],
        "spark": ["pyspark>=3.4.0"],
        "fsspec": ["fsspec[full]>=2024.2.0"],
    },
    entry_points={"console_scripts": ["evidently=evidently.cli:app"]},
)

if __name__ == "__main__":
    setup(**setup_args)
