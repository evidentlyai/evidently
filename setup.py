#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

from __future__ import print_function

import os
from glob import glob
from os.path import join as pjoin

from setuptools import setup

from setupbase import (
    create_cmdclass, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, HERE, install_npm
)

# The name of the project
NAME = 'evidently'

# Ensure a valid python version
ensure_python('3.6')

# Get our version
version = get_version(pjoin(NAME, '_version.py'))

nb_path = pjoin(HERE, NAME, 'nbextension', 'static')
lab_path = pjoin(HERE, NAME, 'labextension')

# Representative files that should exist after a successful build
jstargets = [
    pjoin(nb_path, 'index.js'),
    # pjoin(HERE, 'lib', 'plugin.js'),
]

package_data_spec = {
    NAME: [
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
    install_npm(os.path.join(HERE, "ui"), build_cmd='build'),
    ensure_targets(jstargets),
)

with open("requirements.txt", encoding="utf-8") as dep_file:
    dependencies = dep_file.readlines()
with open("dev_requirements.txt", encoding="utf-8") as dev_dep_file:
    dev_dependencies = dev_dep_file.readlines()
setup_args = dict(
    name=NAME,
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
    install_requires=dependencies,
    extras_require={
        "dev": dev_dependencies,
    },
    entry_points={
    },
)

if __name__ == '__main__':
    setup(**setup_args)
