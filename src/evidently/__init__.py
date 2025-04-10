#!/usr/bin/env python
# coding: utf-8
from evidently.core.datasets import BinaryClassification
from evidently.core.datasets import DataDefinition
from evidently.core.datasets import Dataset
from evidently.core.datasets import MulticlassClassification
from evidently.core.datasets import Recsys
from evidently.core.datasets import Regression
from evidently.core.report import Report
from evidently.legacy.core import ColumnType

from . import _registry
from ._version import __version__
from ._version import version_info
from .nbextension import _jupyter_nbextension_paths

__all__ = [
    "__version__",
    "version_info",
    "_jupyter_nbextension_paths",
    "_registry",
    "Report",
    "Dataset",
    "DataDefinition",
    "BinaryClassification",
    "MulticlassClassification",
    "Regression",
    "Recsys",
    "ColumnType",  # legacy support
]
