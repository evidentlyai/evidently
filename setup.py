#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
from os.path import join as pjoin

from setuptools import setup

from setupbase import (
    create_cmdclass, ensure_targets, combine_commands,
    HERE, install_npm
)

nb_path = pjoin(HERE, 'src', 'evidently', 'nbextension', 'static')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
]

package_data_spec = {
    'evidently': [
        'nbextension/static/*.*js*',
        'nbextension/static/*.*woff2*',
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/evidently', nb_path, '*.js*'),
    ('share/jupyter/nbextensions/evidently', nb_path, '*.woff2'),
    ('etc/jupyter/nbconfig/notebook.d', HERE, 'evidently.json')
]

cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    install_npm(os.path.join(HERE, "ui"), build_cmd='build'),
    ensure_targets(jstargets),
)

setup_args = dict(
    cmdclass=cmdclass,
    author_email='emeli.dral@gmail.com',
    include_package_data=True,
    install_requires=[
        "dataclasses>=0.6",
        "plotly>=4.12.0",
        "statsmodels>=0.12.2",
        "scikit-learn>=0.23.2",
        "pandas>=1.1.5",
        "numpy>=1.19.5",
        "scipy>=1.5.4",
        "requests>=2.19.0",
        "PyYAML~=5.1"],
    extras_require={
        "dev": [
            "setuptools==50.3.2",
            "flake8==4.0.1",
            "jupyter==1.0.0",
            "mypy==0.910",
            "pytest==6.2.5",
            "types-PyYAML==6.0.1",
            "types-requests==2.26.0",
            "packaging==21.0",
        ]
    },
    entry_points={},
)

if __name__ == '__main__':
    setup(**setup_args)
