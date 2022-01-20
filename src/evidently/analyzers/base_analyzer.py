#!/usr/bin/env python
# coding: utf-8
import abc
from typing import Optional, List

import pandas as pd

from evidently.options import OptionsProvider
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.preprocessing.base_preprocess import Preprocess


class Analyzer:
    """
    Base analyzer interface
    """
    def get_preprocesses(self) -> List[Preprocess]:
        """
        Should return list of preprocess instances for data processing,
         which will be executed on reference and current data beforehand
        Returns:
             List of preprocess instances.
        """
        return []

    @abc.abstractmethod
    def calculate(self,
                  reference_data: pd.DataFrame,
                  current_data: Optional[pd.DataFrame],
                  column_mapping: ColumnMapping) -> object:
        """
        Execute analyzer on given reference and current data with given mapping and return result-object.
        Analyzers should not change reference and current data,
         all changes to `reference_data` and `current_data` will be discarded.

        Args:
            reference_data (pd.DataFrame): reference dataset for processing.
            current_data (pd.DataFrame):  current dataset for processing.
            column_mapping (ColumnMapping): columns mapping and definition for datasets.

        Returns:
            Analyzer result data-object.
        """
        raise NotImplementedError()

    options_provider: OptionsProvider
