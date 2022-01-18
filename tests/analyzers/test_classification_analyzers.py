from pytest import approx
import pandas as pd

from evidently import ColumnMapping
from evidently.analyzers.prob_classification_performance_analyzer import ProbClassificationPerformanceAnalyzer


def test_single_dataset_with_two_classes() -> None:
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

    assert result['utility_columns'] == {
        'date': None,
        'id': None,
        'target': 'target',
        'prediction': ['label_a', 'label_b']
    }
    assert result['cat_feature_names'] == []
    assert result['num_feature_names'] == []
    assert result['target_names'] is None

    reference_metrics = result['metrics']['reference']
    assert reference_metrics['accuracy'] == approx(1 / 6)
    assert reference_metrics['precision'] == approx(1 / 8)
    assert reference_metrics['recall'] == approx(1 / 6)
    assert reference_metrics['f1'] == approx(0.14285714285714288)
    # FIXME: as mentioned in comments, ROC and log_loss is currently buggy
    assert reference_metrics['roc_auc'] == approx(1.0)
    assert reference_metrics['log_loss'] == approx(0.46757375785181)
    assert reference_metrics['confusion_matrix'] == {
        'labels': ['label_a', 'label_b'],
        'values': [[0, 3], [2, 1]]
    }
    assert reference_metrics['roc_curve'] == {
        'fpr': [0.0, 0.0, 0.0, 1.0],
        'tpr': [0.0, 0.3333333333333333, 1.0, 1.0],
        'thrs': [1.6, 0.6, 0.4, 0.1]
    }
    assert reference_metrics['pr_curve'] == {
        'pr': [1.0, 1.0, 1.0, 1.0],
        'rcl': [1.0, 0.6666666666666666, 0.3333333333333333, 0.0],
        'thrs': [0.4, 0.5, 0.6]
    }
    assert reference_metrics['pr_table'] == [
        [16.7, 1, 0.5, 1, 0, 100.0, 33.3], [33.3, 2, 0.4, 2, 0, 100.0, 66.7],
        [50.0, 3, 0.3, 3, 0, 100.0, 100.0], [66.7, 4, 0.2, 3, 1, 75.0, 100.0],
        [83.3, 5, 0.1, 3, 2, 60.0, 100.0], [100.0, 6, 0.1, 3, 3, 50.0, 100.0]
    ]
    ###
    metrics_matrix = result['metrics']['reference']['metrics_matrix']
    assert metrics_matrix['label_a'], {
        'precision': 0.0,
        'recall': 0.0,
        'f1-score': 0.0,
        'support': 3
    }
    assert metrics_matrix['label_b'] == {
        'precision': 0.25,
        'recall': 1 / 3,
        'f1-score': 0.28571428571428575,
        'support': 3
    }
    assert metrics_matrix['accuracy'] == 1 / 6
    assert metrics_matrix['macro avg'] == {
        'precision': 0.125,
        'recall': 1 / 6,
        'f1-score': 0.14285714285714288,
        'support': 6
    }
    assert metrics_matrix['weighted avg'] == {
        'precision': 0.125,
        'recall': 1 / 6,
        'f1-score': 0.14285714285714288,
        'support': 6
    }


def test_single_dataset_with_three_classes() -> None:
    df = pd.DataFrame(
        {
            'target': ['label_a', 'label_a', 'label_b', 'label_b', 'label_c', 'label_c'],
            'label_a': [.1, .2, .3, .4, .4, .1],
            'label_b': [.3, .1, .7, .5, .5, .1],
            'label_c': [.7, .8, .0, .1, .1, .8],
        }
    )
    df_column_mapping = ColumnMapping(
        target='target',
        prediction=['label_a', 'label_c', 'label_b'],
    )
    analyzer = ProbClassificationPerformanceAnalyzer()
    result = analyzer.calculate(df, None, df_column_mapping)
    assert result['utility_columns'] == {
        'date': None,
        'id': None,
        'target': 'target',
        'prediction': ['label_a', 'label_c', 'label_b']
    }
    assert result['cat_feature_names'] == []
    assert result['num_feature_names'] == []
    assert result['target_names'] is None

    reference_metrics = result['metrics']['reference']
    assert reference_metrics['accuracy'] == .5
    assert reference_metrics['precision'] == 1 / 3
    assert reference_metrics['recall'] == .5
    assert reference_metrics['f1'] == approx(.4)
    assert reference_metrics['roc_auc'] == 0.20833333333333334
    assert reference_metrics['log_loss'] == 7.323289521082586
    assert reference_metrics['confusion_matrix'] == {
        'labels': ['label_a', 'label_b', 'label_c'],
        'values': [[0, 0, 2], [0, 2, 0], [0, 1, 1]]
    }
    assert reference_metrics['roc_curve'] == {
        'label_a': {
            'fpr': [0.0, 0.5, 0.75, 0.75, 1.0],
            'thrs': [1.4, 0.4, 0.3, 0.2, 0.1],
            'tpr': [0.0, 0.0, 0.0, 0.5, 1.0]
        },
        'label_b': {
            'fpr': [0.0, 0.25, 0.5, 0.75, 1.0],
            'thrs': [1.7, 0.7, 0.5, 0.3, 0.1],
            'tpr': [0.0, 0.0, 0.5, 0.5, 1.0]
        },
        'label_c': {
            'fpr': [0.0, 0.5, 0.75, 1.0, 1.0],
            'thrs': [1.8, 0.8, 0.7, 0.1, 0.0],
            'tpr': [0.0, 0.0, 0.0, 0.5, 1.0]
        }
    }
    assert reference_metrics['pr_curve'] == {
        'label_a': {'pr': [1 / 3, 0.25, 0.0, 0.0, 1.0],
                    'rcl': [1.0, 0.5, 0.0, 0.0, 0.0],
                    'thrs': [0.1, 0.2, 0.3, 0.4]},
        'label_b': {'pr': [1 / 3, 0.25, 1 / 3, 0.0, 1.0],
                    'rcl': [1.0, 0.5, 0.5, 0.0, 0.0],
                    'thrs': [0.1, 0.3, 0.5, 0.7]},
        'label_c': {'pr': [1 / 3, 0.2, 0.0, 0.0, 1.0],
                    'rcl': [1.0, 0.5, 0.0, 0.0, 0.0],
                    'thrs': [0.0, 0.1, 0.7, 0.8]}
    }
    assert reference_metrics['pr_table'] == {
        'label_a': [[16.7, 1, 0.4, 0, 1, 0.0, 0.0],
                    [33.3, 2, 0.3, 0, 2, 0.0, 0.0],
                    [50.0, 3, 0.2, 0, 3, 0.0, 0.0],
                    [66.7, 4, 0.1, 1, 3, 25.0, 50.0],
                    [83.3, 5, 0.1, 2, 3, 40.0, 100.0],
                    [100.0, 6, 0.1, 2, 4, 33.3, 100.0]],
        'label_b': [[16.7, 1, 0.5, 0, 1, 0.0, 0.0],
                    [33.3, 2, 0.5, 0, 2, 0.0, 0.0],
                    [50.0, 3, 0.3, 1, 2, 33.3, 50.0],
                    [66.7, 4, 0.1, 1, 3, 25.0, 50.0],
                    [83.3, 5, 0.1, 1, 4, 20.0, 50.0],
                    [100.0, 6, 0.1, 2, 4, 33.3, 100.0]],
        'label_c': [[16.7, 1, 0.8, 0, 1, 0.0, 0.0],
                    [33.3, 2, 0.7, 0, 2, 0.0, 0.0],
                    [50.0, 3, 0.1, 0, 3, 0.0, 0.0],
                    [66.7, 4, 0.1, 1, 3, 25.0, 50.0],
                    [83.3, 5, 0.0, 1, 4, 20.0, 50.0],
                    [100.0, 6, 0.0, 2, 4, 33.3, 100.0]]
    }
    ###
    metrics_matrix = result['metrics']['reference']['metrics_matrix']
    assert metrics_matrix['label_a'] == {
        'precision': 0.0,
        'recall': 0.0,
        'f1-score': 0.0,
        'support': 2
    }
    assert metrics_matrix['label_b'] == {
        'f1-score': 0.8,
        'precision': 2 / 3,
        'recall': 1.0,
        'support': 2
    }
    assert metrics_matrix['label_c'] == {
        'f1-score': 0.4,
        'precision': 1 / 3,
        'recall': 0.5,
        'support': 2
    }
    assert metrics_matrix['accuracy'] == .5
    assert metrics_matrix['macro avg'] == {
        'f1-score': 0.4000000000000001,
        'precision': 1 / 3,
        'recall': 0.5,
        'support': 6
    }
    assert metrics_matrix['weighted avg'] == {
        'f1-score': 0.4000000000000001,
        'precision': 0.3333333333333333,
        'recall': 0.5,
        'support': 6
    }


def test_two_datasets_with_two_classes_when_dataset_is_same() -> None:
    df1 = pd.DataFrame(
        {
            'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
            'label_a': [.1, .2, .3, .4, .5, .6],
            'label_b': [.9, .8, .7, .6, .5, .4],
        }
    )
    df2 = pd.DataFrame(
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
    result = analyzer.calculate(df1, df2, df_column_mapping)
    assert result['utility_columns'] == {
        'date': None,
        'id': None,
        'target': 'target',
        'prediction': ['label_a', 'label_b']
    }
    assert result['cat_feature_names'] == []
    assert result['num_feature_names'] == []
    assert result['target_names'] is None

    for reference in ['reference', 'current']:
        reference_metrics = result['metrics'][reference]
        assert reference_metrics['accuracy'] == 1 / 6
        assert reference_metrics['precision'] == 1 / 8
        assert reference_metrics['recall'] == 1 / 6
        assert reference_metrics['f1'] == 0.14285714285714288
        # FIXME: as mentioned in comments, ROC and log_loss is currently buggy
        assert reference_metrics['roc_auc'] == 1.0
        assert reference_metrics['log_loss'] == 0.46757375785181
        assert reference_metrics['confusion_matrix'] == {
            'labels': ['label_a', 'label_b'],
            'values': [[0, 3], [2, 1]]
        }
        assert reference_metrics['roc_curve'] == {
            'fpr': [0.0, 0.0, 0.0, 1.0],
            'tpr': [0.0, 0.3333333333333333, 1.0, 1.0],
            'thrs': [1.6, 0.6, 0.4, 0.1]
        }
        assert reference_metrics['pr_curve'] == {'pr': [1.0, 1.0, 1.0, 1.0],
                                                 'rcl': [1.0, 0.6666666666666666,
                                                         0.3333333333333333,
                                                         0.0],
                                                 'thrs': [0.4, 0.5, 0.6]}
        assert reference_metrics['pr_table'] == [[16.7, 1, 0.5, 1, 0, 100.0, 33.3], [33.3, 2, 0.4, 2, 0, 100.0, 66.7],
                                                 [50.0, 3, 0.3, 3, 0, 100.0, 100.0], [66.7, 4, 0.2, 3, 1, 75.0, 100.0],
                                                 [83.3, 5, 0.1, 3, 2, 60.0, 100.0], [100.0, 6, 0.1, 3, 3, 50.0, 100.0]]
        ###
        metrics_matrix = result['metrics'][reference]['metrics_matrix']
        assert metrics_matrix['label_a'] == {'precision': 0.0, 'recall': 0.0, 'f1-score': 0.0, 'support': 3}
        assert metrics_matrix['label_b'] == {
            'precision': 0.25,
            'recall': 1 / 3,
            'f1-score': 0.28571428571428575,
            'support': 3
        }
        assert metrics_matrix['accuracy'] == 1 / 6
        assert metrics_matrix['macro avg'] == {'precision': 0.125, 'recall': 1 / 6,
                                               'f1-score': 0.14285714285714288, 'support': 6}
        assert metrics_matrix['weighted avg'] == {'precision': 0.125, 'recall': 1 / 6,
                                                  'f1-score': 0.14285714285714288, 'support': 6}


def test_two_dataset_with_two_classes_when_dataset_is_different() -> None:
    df1 = pd.DataFrame(
        {
            'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
            'label_a': [.1, .2, .3, .4, .5, .6],
            'label_b': [.9, .8, .7, .6, .5, .4],
        }
    )
    df2 = pd.DataFrame(
        {
            'target': ['label_a', 'label_a', 'label_b', 'label_b'],
            'label_a': [.4, .8, .5, .4],
            'label_b': [.6, .2, .5, .6],
        }
    )
    df_column_mapping = ColumnMapping(
        target='target',
        prediction=['label_a', 'label_b'],
    )
    analyzer = ProbClassificationPerformanceAnalyzer()
    result = analyzer.calculate(df1, df2, df_column_mapping)

    assert result['utility_columns'] == {'date': None, 'id': None, 'target': 'target', 'prediction': ['label_a', 'label_b']}
    assert result['cat_feature_names'] == []
    assert result['num_feature_names'] == []
    assert result['target_names'] is None
    ###
    # tests for 'reference'
    # should be the same values as in other tests
    ###
    reference_metrics = result['metrics']['reference']
    assert reference_metrics['accuracy'] == 1 / 6
    assert reference_metrics['precision'] == 1 / 8
    assert reference_metrics['recall'] == 1 / 6
    assert reference_metrics['f1'] == 0.14285714285714288
    # FIXME: as mentioned in comments, ROC and log_loss is currently buggy
    assert reference_metrics['roc_auc'] == 1.0
    assert reference_metrics['log_loss'] == 0.46757375785181
    assert reference_metrics['confusion_matrix'] == {'labels': ['label_a', 'label_b'], 'values': [[0, 3], [2, 1]]}
    assert reference_metrics['roc_curve'] == {
        'fpr': [0.0, 0.0, 0.0, 1.0],
        'tpr': [0.0, 0.3333333333333333, 1.0, 1.0],
        'thrs': [1.6, 0.6, 0.4, 0.1]
    }
    assert reference_metrics['pr_curve'] == {
        'pr': [1.0, 1.0, 1.0, 1.0],
        'rcl': [1.0, 0.6666666666666666, 0.3333333333333333, 0.0],
        'thrs': [0.4, 0.5, 0.6]
    }
    assert reference_metrics['pr_table'] == [
        [16.7, 1, 0.5, 1, 0, 100.0, 33.3], [33.3, 2, 0.4, 2, 0, 100.0, 66.7],
        [50.0, 3, 0.3, 3, 0, 100.0, 100.0], [66.7, 4, 0.2, 3, 1, 75.0, 100.0],
        [83.3, 5, 0.1, 3, 2, 60.0, 100.0], [100.0, 6, 0.1, 3, 3, 50.0, 100.0]
    ]
    ###
    metrics_matrix = result['metrics']['reference']['metrics_matrix']
    assert metrics_matrix['label_a'] == {
        'precision': 0.0,
        'recall': 0.0,
        'f1-score': 0.0,
        'support': 3
    }
    assert metrics_matrix['label_b'] == {
        'precision': 0.25,
        'recall': 1 / 3,
        'f1-score': 0.28571428571428575,
        'support': 3
    }
    assert metrics_matrix['accuracy'] == 1 / 6
    assert metrics_matrix['macro avg'] == {
        'precision': 0.125,
        'recall': 1 / 6,
        'f1-score': 0.14285714285714288,
        'support': 6
    }
    assert metrics_matrix['weighted avg'] == {
        'precision': 0.125,
        'recall': 1 / 6,
        'f1-score': 0.14285714285714288,
        'support': 6
    }
    ###
    # tests for current
    # should be different from 'reference'
    ###
    reference_metrics = result['metrics']['current']
    assert reference_metrics['accuracy'] == .5
    assert reference_metrics['precision'] == .5
    assert reference_metrics['recall'] == .5
    assert reference_metrics['f1'] == .5
    # FIXME: as mentioned in comments, ROC and log_loss is currently buggy
    assert reference_metrics['roc_auc'] == 0.375
    assert reference_metrics['log_loss'] == 0.9324253621585479
    assert reference_metrics['confusion_matrix'] == {
        'labels': ['label_a', 'label_b'],
        'values': [[1, 1], [1, 1]]
    }
    assert reference_metrics['roc_curve'] == {
        'fpr': [0.0, 0.5, 0.5, 1.0],
        'thrs': [1.8, 0.8, 0.5, 0.4],
        'tpr': [0.0, 0.0, 0.5, 1.0]
    }
    assert reference_metrics['pr_curve'] == {
        'pr': [0.5, 0.5, 0.0, 1.0],
        'rcl': [1.0, 0.5, 0.0, 0.0],
        'thrs': [0.4, 0.5, 0.8]
    }
    assert reference_metrics['pr_table'] == [
        [25.0, 1, 0.5, 0, 1, 0.0, 0.0],
        [50.0, 2, 0.4, 1, 1, 50.0, 50.0],
        [75.0, 3, 0.4, 1, 2, 33.3, 50.0],
        [100.0, 4, 0.4, 2, 2, 50.0, 100.0]
    ]
    ###
    metrics_matrix = result['metrics']['current']['metrics_matrix']
    assert metrics_matrix['label_a'] == {
        'f1-score': 0.5,
        'precision': 0.5,
        'recall': 0.5,
        'support': 2
    }
    assert metrics_matrix['label_b'] == {
        'f1-score': 0.5,
        'precision': 0.5,
        'recall': 0.5,
        'support': 2
    }
    assert metrics_matrix['accuracy'] == .5
    assert metrics_matrix['macro avg'] == {
        'f1-score': 0.5,
        'precision': 0.5,
        'recall': 0.5,
        'support': 4
    }
    assert metrics_matrix['weighted avg'] == {
        'f1-score': 0.5,
        'precision': 0.5,
        'recall': 0.5,
        'support': 4
    }

# TODO: there a lot of different tests one may think of and should be implemented here. However, it will be
#  more efficient to first refactor the current code given the tests now, because we are right now testing
#  waaaaay to many things at once. This makes testing also way more difficult that it should be.
#  When we extract different parts parts of the code into their own functional equivalents (with tests!)
#  we will not need to test for many things here. In the following there are few interesting test cases.

# test what happens when probabilities do not sum to 1
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
#         'label_a': [.1, .2, .3, .4, .5, .6],
#         'label_b': [1.9, 2.8, 3.7, 4.6, 5.5, 6.4],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a', 'label_b'],
# )

# test what happens when there more labels in specification
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
#         'label_a': [.1, .2, .3, .4, .5, .6],
#         'label_b': [.9, .8, .7, .6, .5, .4],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a', 'label_b', 'label_c'],
# )

# test what happens when probabilities are equal (1)
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_b', 'label_b', 'label_b', 'label_b', 'label_b'],
#         'label_a': [.5, .5, .5, .5, .5, .5],
#         'label_b': [.5, .5, .5, .5, .5, .5],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a', 'label_b', 'label_c'],
# )

# test what happens when probabilities are equal (2)
# but the order of labels in dataframe is different
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_b', 'label_b', 'label_b', 'label_b', 'label_b'],
#         'label_b': [.5, .5, .5, .5, .5, .5],
#         'label_a': [.5, .5, .5, .5, .5, .5],
#
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a', 'label_b'],
# )

# test what happens when probabilities are equal (2)
# but the order of labels in column mapping is different
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_b', 'label_b', 'label_b', 'label_b', 'label_b'],
#         'label_b': [.5, .5, .5, .5, .5, .5],
#         'label_a': [.5, .5, .5, .5, .5, .5],
#
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_b', 'label_a'],
# )

# test what happens when labels are numeric
# df = pd.DataFrame(
#     {
#         'target': [0, 0, 0, 1, 1, 1],
#         0: [.1, .2, .3, .4, .5, .6],
#         1: [.9, .8, .7, .6, .5, .4],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=[0, 1],
# )

# test what happens when target name is different
# df = pd.DataFrame(
#     {
#         'different_target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
#         'label_a': [.1, .2, .3, .4, .5, .6],
#         'label_b': [1.9, 2.8, 3.7, 4.6, 5.5, 6.4],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='different_target',
#     prediction=['label_a', 'label_b'],
# )

# test what happens when only one label is present in target
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_a', 'label_a', 'label_a', 'label_a', 'label_a'],
#         'label_a': [.1, .2, .3, .4, .5, .6],
#         'label_b': [1.9, 2.8, 3.7, 4.6, 5.5, 6.4],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a', 'label_b'],
# )

# test what happens when prediction only contains one label
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
#         'label_a': [.1, .2, .3, .4, .5, .6],
#         'label_b': [1.9, 2.8, 3.7, 4.6, 5.5, 6.4],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a'],
# )

# test what happens when prediction only contains one label
# and this label is the only probable one
# df = pd.DataFrame(
#     {
#         'target': ['label_a', 'label_a', 'label_a', 'label_b', 'label_b', 'label_b'],
#         'label_a': [.9, .9, .9, .9, .9, .9],
#         'label_b': [.1, .1, .1, .1, .1, .1],
#     }
# )
# df_column_mapping = ColumnMapping(
#     target='target',
#     prediction=['label_a'],
# )

# test above tests cases with data frames with more than two classes
