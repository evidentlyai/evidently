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
                'target': [0, 0, 0, 1, 1, 1],
                'prediction': [0, 0, 0, 1, 1, 1],
            }
        )
        analyzer = ProbClassificationPerformanceAnalyzer()
        blubb = analyzer.calculate(df, None, ColumnMapping())
        print(blubb)

    def test_single_dataset_with_three_classes(self):
        df = pd.DataFrame(
            {
                'target': [0, 0, 0, 1, 1, 1, 2, 2, 2],
                'prediction': [2, 2, 2, 1, 1, 1, 0, 0, 0],
            }
        )
        analyzer = ClassificationPerformanceAnalyzer()
        blubb = analyzer.calculate(df, None, ColumnMapping())
        print(blubb)

