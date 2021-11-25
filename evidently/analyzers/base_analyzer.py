#!/usr/bin/env python
# coding: utf-8

import abc
import pandas as pd

from evidently.pipeline.column_mapping import ColumnMapping


class Analyzer:
    def __init__(self):
        pass

    @abc.abstractmethod
    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: pd.DataFrame,
                  column_mapping: ColumnMapping) -> object:
        raise NotImplementedError()
