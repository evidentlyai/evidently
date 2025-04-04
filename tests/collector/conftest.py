import datetime
import os
from typing import Dict

import pandas as pd
import pytest
from litestar import get
from litestar.testing import TestClient

from evidently.legacy.collector.app import create_app
from evidently.legacy.collector.config import CollectorConfig
from evidently.legacy.collector.config import CollectorServiceConfig
from evidently.legacy.collector.config import ReportConfig
from evidently.legacy.collector.config import RowsCountTrigger
from evidently.legacy.core import IncludeOptions
from evidently.legacy.core import new_id
from evidently.legacy.options.base import Options
from evidently.legacy.suite.base_suite import ContextPayload
from evidently.legacy.suite.base_suite import ReportBase
from evidently.legacy.suite.base_suite import Snapshot
from evidently.legacy.suite.base_suite import Suite
from tests.ui.test_app import MockMetric
from tests.ui.test_app import MockMetricResult

os.environ["DO_NOT_TRACK"] = "1"


@pytest.fixture
def collector_test_client(tmp_path):
    app = create_app(str(tmp_path / "config.json"), debug=True)

    state = {}

    @get("/_init_tests")
    async def test_init(service: CollectorServiceConfig, service_workspace: str) -> None:
        state["config"] = service
        state["workspace"] = service_workspace

    app.register(test_init)

    client = TestClient(app)
    client.get("/_init_tests").raise_for_status()
    client.app.state.update(state)
    return client


@pytest.fixture()
def collector_service_config(collector_test_client) -> CollectorServiceConfig:
    return collector_test_client.app.state["config"]


@pytest.fixture()
def collector_workspace(collector_test_client) -> str:
    return collector_test_client.app.state["workspace"]


class ReportBaseMock(ReportBase):
    def __init__(self):
        super().__init__()
        self.id = new_id()

    def to_snapshot(self):
        return Snapshot(
            id=self.id,
            name="mock",
            timestamp=datetime.datetime.now(),
            metadata={},
            tags=[],
            suite=ContextPayload(
                metrics=[MockMetric()],
                metric_results=[MockMetricResult.create(1)],
                tests=[],
                test_results=[],
                options=Options(),
            ),
            metrics_ids=[],
            test_ids=[],
            options=Options(),
        )

    def as_dict(
        self,
        include_render: bool = False,
        include: Dict[str, IncludeOptions] = None,
        exclude: Dict[str, IncludeOptions] = None,
        **kwargs,
    ) -> dict:
        return {}

    def _build_dashboard_info(self):
        pass

    def run(self, *args, **kwargs):
        self._inner_suite = Suite(Options())

    @classmethod
    def _parse_snapshot(cls, payload: Snapshot):
        return ReportBaseMock()


class ReportConfigMock(ReportConfig):
    def to_report_base(self):
        return ReportBaseMock()


@pytest.fixture()
def mock_collector_config() -> CollectorConfig:
    return CollectorConfig(
        trigger=RowsCountTrigger(),
        report_config=ReportConfigMock(metrics=[], tests=[], options=Options(), metadata={}, tags=[]),
        project_id="",
    )


@pytest.fixture()
def mock_reference() -> pd.DataFrame:
    return pd.DataFrame({"a": [1, 2]}, index=["0", "1"])
