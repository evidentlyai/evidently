from typing import Dict
from typing import List
from typing import Optional

import numpy as np

from evidently.base_metric import InputData
from evidently.calculations.stattests import PossibleStatTestType
from evidently.metric_results import DatasetColumns
from evidently.metrics.data_drift.embedding_drift_methods import DriftMethod
from evidently.pipeline.column_mapping import TaskType
from evidently.test_preset.test_preset import TestPreset
from evidently.tests import TestAllFeaturesValueDrift
from evidently.tests import TestColumnDrift
from evidently.tests import TestEmbeddingsDrift
from evidently.tests import TestShareOfDriftedColumns
from evidently.utils.data_drift_utils import add_emb_drift_to_reports
from evidently.utils.data_drift_utils import resolve_stattest_threshold


class DataDriftTestPreset(TestPreset):
    """
    Data Drift tests.

    Contains tests:
    - `TestShareOfDriftedColumns`
    - `TestColumnValueDrift`
    - `TestAllFeaturesValueDrift`
    - 'TestEmbeddingsDrift'
    """

    columns: Optional[List[str]]
    embeddings: Optional[List[str]]
    embeddings_drift_method: Optional[Dict[str, DriftMethod]]
    drift_share: Optional[float]
    stattest: Optional[PossibleStatTestType]
    cat_stattest: Optional[PossibleStatTestType]
    num_stattest: Optional[PossibleStatTestType]
    text_stattest: Optional[PossibleStatTestType]
    per_column_stattest: Optional[Dict[str, PossibleStatTestType]]
    stattest_threshold: Optional[float]
    cat_stattest_threshold: Optional[float]
    num_stattest_threshold: Optional[float]
    text_stattest_threshold: Optional[float]
    per_column_stattest_threshold: Optional[Dict[str, float]]

    def __init__(
        self,
        columns: Optional[List[str]] = None,
        embeddings: Optional[List[str]] = None,
        embeddings_drift_method: Optional[Dict[str, DriftMethod]] = None,
        drift_share: Optional[float] = None,
        stattest: Optional[PossibleStatTestType] = None,
        cat_stattest: Optional[PossibleStatTestType] = None,
        num_stattest: Optional[PossibleStatTestType] = None,
        text_stattest: Optional[PossibleStatTestType] = None,
        per_column_stattest: Optional[Dict[str, PossibleStatTestType]] = None,
        stattest_threshold: Optional[float] = None,
        cat_stattest_threshold: Optional[float] = None,
        num_stattest_threshold: Optional[float] = None,
        text_stattest_threshold: Optional[float] = None,
        per_column_stattest_threshold: Optional[Dict[str, float]] = None,
    ):
        super().__init__()
        self.columns = columns
        self.embeddings = embeddings
        self.embeddings_drift_method = embeddings_drift_method
        self.drift_share = drift_share
        self.stattest = stattest
        self.cat_stattest = cat_stattest
        self.num_stattest = num_stattest
        self.text_stattest = text_stattest
        self.per_column_stattest = per_column_stattest
        self.stattest_threshold = stattest_threshold
        self.cat_stattest_threshold = cat_stattest_threshold
        self.num_stattest_threshold = num_stattest_threshold
        self.text_stattest_threshold = text_stattest_threshold
        self.per_column_stattest_threshold = per_column_stattest_threshold

    def generate_tests(self, data: InputData, columns: DatasetColumns):
        embeddings_data = data.column_mapping.embeddings
        if embeddings_data is not None:
            embs = list(set(v for values in embeddings_data.values() for v in values))
            if self.columns is None:
                self.columns = list(
                    np.setdiff1d(
                        columns.num_feature_names + columns.cat_feature_names + columns.text_feature_names, embs
                    )
                )
            else:
                self.columns = list(np.setdiff1d(self.columns, embs))

        preset_tests: list = [
            TestShareOfDriftedColumns(
                columns=self.columns,
                lt=0.3 if self.drift_share is None else self.drift_share,
                stattest=self.stattest,
                cat_stattest=self.cat_stattest,
                num_stattest=self.num_stattest,
                text_stattest=self.text_stattest,
                per_column_stattest=self.per_column_stattest,
                stattest_threshold=self.stattest_threshold,
                cat_stattest_threshold=self.cat_stattest_threshold,
                num_stattest_threshold=self.num_stattest_threshold,
                text_stattest_threshold=self.text_stattest_threshold,
                per_column_stattest_threshold=self.per_column_stattest_threshold,
            ),
        ]

        if columns.utility_columns.target is not None:
            stattest, threshold = resolve_stattest_threshold(
                columns.utility_columns.target,
                "cat" if columns.task == TaskType.CLASSIFICATION_TASK else "num",
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.text_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.text_stattest_threshold,
                self.per_column_stattest_threshold,
            )
            preset_tests.append(
                TestColumnDrift(
                    column_name=columns.utility_columns.target,
                    stattest_threshold=threshold,
                    stattest=stattest,
                )
            )

        if columns.utility_columns.prediction is not None and isinstance(columns.utility_columns.prediction, str):
            stattest, threshold = resolve_stattest_threshold(
                columns.utility_columns.prediction,
                "cat" if columns.task == TaskType.CLASSIFICATION_TASK else "num",
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.text_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.text_stattest_threshold,
                self.per_column_stattest_threshold,
            )
            preset_tests.append(
                TestColumnDrift(
                    column_name=columns.utility_columns.prediction,
                    stattest_threshold=threshold,
                    stattest=stattest,
                )
            )

        preset_tests.append(
            TestAllFeaturesValueDrift(
                self.columns,
                self.stattest,
                self.cat_stattest,
                self.num_stattest,
                self.text_stattest,
                self.per_column_stattest,
                self.stattest_threshold,
                self.cat_stattest_threshold,
                self.num_stattest_threshold,
                self.text_stattest_threshold,
                self.per_column_stattest_threshold,
            )
        )

        if embeddings_data is None:
            return preset_tests
        preset_tests = add_emb_drift_to_reports(
            preset_tests,
            embeddings_data,
            self.embeddings,
            self.embeddings_drift_method,
            TestEmbeddingsDrift,
        )
        return preset_tests
