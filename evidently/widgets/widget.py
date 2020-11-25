#!/usr/bin/env python
# coding: utf-8

import abc

import pandas

from evidently.model.widget import BaseWidgetInfo


class Widget:
    def __init__(self):
        pass

    @abc.abstractmethod
    def calculate(self, reference_data: pandas.DataFrame,
                  production_data: pandas.DataFrame, column_mapping):
        raise NotImplemented()

    @abc.abstractmethod
    def get_info(self) -> BaseWidgetInfo:
        raise NotImplemented()
