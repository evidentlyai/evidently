"""Metrics for evaluating data quality, model performance, and data drift.

This module provides individual metrics that can be used in `Report` objects.
Metrics compute specific values from your data, such as:
- Column statistics (mean, max, min, etc.)
- Data quality metrics (missing values, duplicates, etc.)
- Classification metrics (accuracy, precision, recall, etc.)
- Regression metrics (MAE, RMSE, R2, etc.)
- Ranking metrics (NDCG, MAP, MRR, etc.)
- Data drift metrics (PSI, Wasserstein distance, etc.)

Use metrics individually in a `Report`, or use `Preset` objects that combine
multiple related metrics together.

**Documentation**: See [All Metrics](https://docs.evidentlyai.com/metrics/all_metrics) for a complete reference.

Example:
```python
from evidently import Report
from evidently.metrics import MeanValue, ColumnCount

report = Report([
    ColumnCount(),
    MeanValue(column="age")
])
snapshot = report.run(dataset, None)
```
"""

from .classification import FNR
from .classification import FPR
from .classification import TNR
from .classification import TPR
from .classification import Accuracy
from .classification import DummyAccuracy
from .classification import DummyF1Score
from .classification import DummyFNR
from .classification import DummyFPR
from .classification import DummyLogLoss
from .classification import DummyPrecision
from .classification import DummyRecall
from .classification import DummyRocAuc
from .classification import DummyTNR
from .classification import DummyTPR
from .classification import F1ByLabel
from .classification import F1Score
from .classification import LogLoss
from .classification import Precision
from .classification import PrecisionByLabel
from .classification import Recall
from .classification import RecallByLabel
from .classification import RocAuc
from .classification import RocAucByLabel
from .column_statistics import CategoryCount
from .column_statistics import DriftedColumnsCount
from .column_statistics import InListValueCount
from .column_statistics import InRangeValueCount
from .column_statistics import MaxValue
from .column_statistics import MeanValue
from .column_statistics import MedianValue
from .column_statistics import MinValue
from .column_statistics import MissingValueCount
from .column_statistics import OutListValueCount
from .column_statistics import OutRangeValueCount
from .column_statistics import QuantileValue
from .column_statistics import StdValue
from .column_statistics import SumValue
from .column_statistics import UniqueValueCount
from .column_statistics import ValueDrift
from .data_quality import ColumnCorrelationMatrix
from .data_quality import ColumnCorrelations
from .data_quality import CorrelationMatrix
from .data_quality import DatasetCorrelations
from .dataset_statistics import AlmostConstantColumnsCount
from .dataset_statistics import AlmostDuplicatedColumnsCount
from .dataset_statistics import ColumnCount
from .dataset_statistics import ConstantColumnsCount
from .dataset_statistics import DatasetMissingValueCount
from .dataset_statistics import DuplicatedColumnsCount
from .dataset_statistics import DuplicatedRowCount
from .dataset_statistics import EmptyColumnsCount
from .dataset_statistics import EmptyRowsCount
from .dataset_statistics import RowCount
from .group_by import GroupBy
from .recsys import MAP
from .recsys import MRR
from .recsys import NDCG
from .recsys import Diversity
from .recsys import FBetaTopK
from .recsys import HitRate
from .recsys import ItemBias
from .recsys import Novelty
from .recsys import Personalization
from .recsys import PopularityBiasMetric
from .recsys import PrecisionTopK
from .recsys import RecallTopK
from .recsys import RecCasesTable
from .recsys import ScoreDistribution
from .recsys import Serendipity
from .recsys import UserBias
from .regression import MAE
from .regression import MAPE
from .regression import RMSE
from .regression import AbsMaxError
from .regression import DummyMAE
from .regression import DummyMAPE
from .regression import DummyRMSE
from .regression import MeanError
from .regression import R2Score
from .row_test_summary import RowTestSummary

__all__ = [
    "GroupBy",
    "RowTestSummary",
    # column statistics metrics
    "CategoryCount",
    "ValueDrift",
    "DriftedColumnsCount",
    "MaxValue",
    "MeanValue",
    "MedianValue",
    "MinValue",
    "MissingValueCount",
    "InListValueCount",
    "InRangeValueCount",
    "OutListValueCount",
    "OutRangeValueCount",
    "QuantileValue",
    "StdValue",
    "SumValue",
    "UniqueValueCount",
    # dataset statistics metrics
    "ColumnCount",
    "RowCount",
    "DuplicatedRowCount",
    "DuplicatedColumnsCount",
    "DatasetMissingValueCount",
    "AlmostConstantColumnsCount",
    "AlmostDuplicatedColumnsCount",
    "ConstantColumnsCount",
    "EmptyRowsCount",
    "EmptyColumnsCount",
    # classification
    "DummyF1Score",
    "DummyPrecision",
    "DummyRecall",
    "F1Score",
    "Accuracy",
    "Precision",
    "Recall",
    "TPR",
    "TNR",
    "FPR",
    "FNR",
    "LogLoss",
    "RocAuc",
    "F1ByLabel",
    "PrecisionByLabel",
    "RecallByLabel",
    "RocAucByLabel",
    # regression
    "MeanError",
    "MAE",
    "MAPE",
    "RMSE",
    "R2Score",
    "AbsMaxError",
    "DummyMAE",
    "DummyMAPE",
    "DummyRMSE",
    "ScoreDistribution",
    "NDCG",
    "FBetaTopK",
    "HitRate",
    "MAP",
    "MRR",
    "PrecisionTopK",
    "RecallTopK",
    "PopularityBiasMetric",
    "Personalization",
    "Diversity",
    "Serendipity",
    "Novelty",
    "ItemBias",
    "UserBias",
    "RecCasesTable",
    "DummyTPR",
    "DummyTNR",
    "DummyRocAuc",
    "DummyLogLoss",
    "DummyFPR",
    "DummyFNR",
    "DummyAccuracy",
    # Data Quality
    "ColumnCorrelations",
    "CorrelationMatrix",
    "DatasetCorrelations",
    "ColumnCorrelationMatrix",
]
