#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function
from glob import glob
from os.path import join as pjoin

from setupbase import (
    create_cmdclass, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, HERE
)

from setuptools import setup

# The name of the project
name = 'evidently'

# Ensure a valid python version
ensure_python('>=3.4')

# Get our version
version = get_version(pjoin(name, '_version.py'))

nb_path = pjoin(HERE, name, 'nbextension', 'static')
lab_path = pjoin(HERE, name, 'labextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    # pjoin(HERE, 'lib', 'plugin.js'),
]

package_data_spec = {
    name: [
        'nbextension/static/*.*js*',
        'nbextension/static/*.woff2',
        'labextension/*.tgz'
    ]
}

data_files_spec = [
    ('share/jupyter/nbextensions/evidently',
     nb_path, '*.js*'),
    ('share/jupyter/lab/extensions', lab_path, '*.tgz'),
    ('etc/jupyter/nbconfig/notebook.d', HERE, 'evidently.json')
]

cmdclass = create_cmdclass('jsdeps', package_data_spec=package_data_spec,
                           data_files_spec=data_files_spec)
cmdclass['jsdeps'] = combine_commands(
    # install_npm(HERE, build_cmd='build:all'),
    ensure_targets(jstargets),
)

setup_args = dict(
    name=name,
    description='Open-source tools to analyze, monitor, and debug machine learning model in production.',
    version=version,
    scripts=glob(pjoin('scripts', '*')),
    cmdclass=cmdclass,
    packages=find_packages(),
    author='Emeli Dral',
    author_email='emeli.dral@gmail.com',
    url='https://github.com/evidentlyai/evidently',
    license='Apache License 2.0',
    platforms="Linux, Mac OS X, Windows",
    keywords=[],
    classifiers=[],
    include_package_data=True,
    install_requires=[
        "dataclasses",
        "pandas",
        "numpy",
        #"matplotlib",
        "plotly",
        "scipy"
    ],
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
