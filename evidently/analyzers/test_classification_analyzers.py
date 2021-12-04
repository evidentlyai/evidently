from unittest import TestCase

import numpy as np
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.classification_performance_analyzer import ClassificationPerformanceAnalyzer
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer


class TestProbClassificationAnalyzer(TestCase):

    def test_single_dataset_with_two_classes(self):
        df = pd.DataFrame(
            {
                'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
                'label_a': [.1, .2, .3, .4, .5, .6],
                'label_b': [.9, .8, .7, .6, .5, .4],
            }
        )
        df_column_mapping = ColumnMapping(
            target='target',
            prediction=['label_a', 'label_b'],
        )
        analyzer = ProbClassificationPerformanceAnalyzer()
        blubb = analyzer.calculate(df, None, df_column_mapping)
        print(blubb)

