#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
from os.path import join as pjoin

from setupbase import HERE
from setupbase import combine_commands
from setupbase import create_cmdclass
from setupbase import ensure_targets
from setupbase import install_npm
from setuptools import setup

nb_path = pjoin(HERE, "src", "evidently", "nbextension", "static")

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, "index.js"),
]

package_data_spec = {
    "evidently": [
        "nbextension/static/*.*js*",
        "nbextension/static/*.*woff2*",
        "ui/ui/*",
        "ui/ui/static/css/*",
        "ui/ui/static/js/*",
        "ui/ui/static/img/*",
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
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "plotly>=5.5.0",
        "statsmodels>=0.12.2",
        "scikit-learn>=0.24.0",
        "pandas[parquet]>=1.3.5",
        "numpy>=1.19.5",
        "nltk>=3.6.7",
        "scipy>=1.5.4",
        "requests>=2.21.0",
        "PyYAML>=5.1",
        "pydantic<2",
        "fastapi>=0.100.0",
        "fastapi-restful>=0.5.0",
        "typing-inspect>=0.9.0",
        "uvicorn>=0.22.0",
        "watchdog>=3",
        "typer>=0.3",
        "rich>=13",
        "iterative-telemetry>=0.0.5",
        "fsspec",
    ],
    extras_require={
        "dev": [
            "wheel==0.35.1",
            "setuptools==50.3.2; python_version < '3.12'",
            "setuptools==68.2.2; python_version >= '3.12'",
            "flake8==4.0.1",
            "jupyter==1.0.0",
            "mypy==0.910",
            "pytest==6.2.5",
            "types-PyYAML==6.0.1",
            "types-requests==2.26.0",
            "types-dataclasses==0.6",
            "types-python-dateutil==2.8.19",
            "pillow==9.5.0",
            "black==22.8.0",
            "isort==5.10.1",
            "httpx==0.24.1"
        ],
        "spark": [
            "pyspark"
        ],
        "fsspec": [
            "fsspec[full]"
        ]
    },
    entry_points={
        "console_scripts": ["evidently=evidently.cli:app"]
    },
)

if __name__ == "__main__":
    setup(**setup_args)
