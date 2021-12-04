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
        result = analyzer.calculate(df, None, df_column_mapping)

        self.assertEqual(result['utility_columns'],
                         {'date': None, 'id': None, 'target': 'target', 'prediction': ['label_a', 'label_b']})
        self.assertEqual(result['cat_feature_names'], [])
        self.assertEqual(result['num_feature_names'], [])
        self.assertIsNone(result['target_names'])
        reference_metrics = result['metrics']['reference']
        self.assertAlmostEqual(reference_metrics['accuracy'], 1/6)
        self.assertAlmostEqual(reference_metrics['precision'], 1/8)
        self.assertAlmostEqual(reference_metrics['recall'], 1/6)
        self.assertAlmostEqual(reference_metrics['f1'], 0.14285714285714288)
        # FIXME: as mentioned in comments, ROC and log_loss is currently buggy
        self.assertAlmostEqual(reference_metrics['roc_auc'], 1.0)
        self.assertAlmostEqual(reference_metrics['log_loss'], 0.46757375785181)
        ###
        metrics_matrix = result['metrics']['reference']['metrics_matrix']
        self.assertEqual(metrics_matrix['label_a'],
                         {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 3})
        self.assertEqual(metrics_matrix['label_b'],
                         {'precision': 0.25, 'recall': 1/3,
                          'f1-score': 0.28571428571428575, 'support': 3})
        self.assertAlmostEqual(metrics_matrix['accuracy'], 1/6)
        self.assertEqual(metrics_matrix['macro avg'],
                         {'precision': 0.125, 'recall': 1/6,
                          'f1-score': 0.14285714285714288, 'support': 6})
        self.assertEqual(metrics_matrix['weighted avg'],
                         {'precision': 0.125, 'recall': 1/6,
                          'f1-score': 0.14285714285714288, 'support': 6})
        ###
        self.assertEqual(reference_metrics['confusion_matrix'],
                         {'labels': ['label_a', 'label_b'], 'values': [[0, 3], [2, 1]]})
        self.assertEqual(reference_metrics['roc_curve'],
                         {'fpr': [0.0, 0.0, 0.0, 1.0],
                          'tpr': [0.0, 0.3333333333333333, 1.0, 1.0],
                          'thrs': [1.6, 0.6, 0.4, 0.1]})
        self.assertEqual(reference_metrics['pr_curve'],
                         {'pr': [1.0, 1.0, 1.0, 1.0],
                          'rcl': [1.0, 0.6666666666666666,
                                  0.3333333333333333,
                                  0.0],
                          'thrs': [0.4, 0.5, 0.6]})
        self.assertEqual(reference_metrics['pr_table'],
                         [[16.7, 1, 0.5, 1, 0, 100.0, 33.3], [33.3, 2, 0.4, 2, 0, 100.0, 66.7],
                          [50.0, 3, 0.3, 3, 0, 100.0, 100.0], [66.7, 4, 0.2, 3, 1, 75.0, 100.0],
                          [83.3, 5, 0.1, 3, 2, 60.0, 100.0], [100.0, 6, 0.1, 3, 3, 50.0, 100.0]])

