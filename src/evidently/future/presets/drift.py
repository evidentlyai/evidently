from typing import Dict
from typing import List
from typing import Optional

from evidently import ColumnType
from evidently.calculations.stattests import PossibleStatTestType
from evidently.calculations.stattests import StatTest
from evidently.future.container import MetricContainer
from evidently.future.metric_types import Metric
from evidently.future.metric_types import MetricId
from evidently.future.metric_types import MetricResult
from evidently.future.metrics import ValueDrift
from evidently.future.metrics.column_statistics import DriftedColumnsCount
from evidently.future.report import Context
from evidently.future.report import _default_input_data_generator
from evidently.metrics import DataDriftTable
from evidently.metrics import DatasetDriftMetric
from evidently.metrics.data_drift.embedding_drift_methods import DriftMethod
from evidently.model.widget import BaseWidgetInfo
from evidently.options.data_drift import DataDriftOptions


class DataDriftPreset(MetricContainer):
    def __init__(
        self,
        columns: Optional[List[str]] = None,
        embeddings: Optional[List[str]] = None,
        embeddings_drift_method: Optional[Dict[str, DriftMethod]] = None,
        drift_share: float = 0.5,
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
        self.per_column_stattest_threshold = per_column_stattest_threshold
        self.text_stattest_threshold = text_stattest_threshold
        self.num_stattest_threshold = num_stattest_threshold
        self.cat_stattest_threshold = cat_stattest_threshold
        self.stattest_threshold = stattest_threshold
        self.per_column_stattest = per_column_stattest
        self.text_stattest = text_stattest
        self.num_stattest = num_stattest
        self.cat_stattest = cat_stattest
        self.stattest = stattest
        self.drift_share = drift_share
        self.embeddings_drift_method = embeddings_drift_method
        self.embeddings = embeddings
        self.columns = columns

    def generate_metrics(self, context: Context) -> List[Metric]:
        types = [ColumnType.Numerical, ColumnType.Categorical, ColumnType.Text]
        options = DataDriftOptions(
            drift_share=self.drift_share,
            all_features_stattest=self.stattest,
            cat_features_stattest=self.cat_stattest,
            num_features_stattest=self.num_stattest,
            text_features_stattest=self.text_stattest,
            per_feature_stattest=self.per_column_stattest,
            all_features_threshold=self.stattest_threshold,
            cat_features_threshold=self.cat_stattest_threshold,
            num_features_threshold=self.num_stattest_threshold,
            text_features_threshold=self.text_stattest_threshold,
            per_feature_threshold=self.per_column_stattest_threshold,
        )
        return [
            DriftedColumnsCount(
                columns=self.columns,
                drift_share=self.drift_share,
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
        ] + [
            ValueDrift(
                column=column,
                method=self._get_drift_stattest(
                    column,
                    False,
                    context.data_definition.get_column_type(column),
                    options,
                ),
            )
            for column in (self.columns if self.columns is not None else context.data_definition.get_columns(types))
        ]

    def render(self, context: Context, results: Dict[MetricId, MetricResult]) -> List[BaseWidgetInfo]:
        dataset_drift = context.get_legacy_metric(
            DatasetDriftMetric(
                columns=self.columns,
                drift_share=self.drift_share,
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
            _default_input_data_generator,
        )[1]
        table = context.get_legacy_metric(
            DataDriftTable(
                columns=self.columns,
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
            _default_input_data_generator,
        )[1]
        return dataset_drift + table

    def _get_drift_stattest(
        self,
        column_name: str,
        is_target: bool,
        column_type: ColumnType,
        options: DataDriftOptions,
    ):
        stattest = None

        if is_target and column_type == ColumnType.Numerical:
            stattest = options.num_target_stattest_func

        elif is_target and column_type == ColumnType.Categorical:
            stattest = options.cat_target_stattest_func

        if not stattest:
            stattest = options.get_feature_stattest_func(column_name, column_type.value)
        if stattest:
            if isinstance(stattest, str):
                return stattest
            if isinstance(stattest, StatTest):
                return stattest.name
            return stattest
        return None
