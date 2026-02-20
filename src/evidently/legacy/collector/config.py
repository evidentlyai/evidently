import abc
import json
import time
import warnings
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import pandas as pd
from pydantic import BaseModel
from pydantic import Field
from pydantic import TypeAdapter

from evidently.legacy.base_metric import Metric
from evidently.legacy.collector.storage import CollectorStorage
from evidently.legacy.collector.storage import InMemoryStorage
from evidently.legacy.options.base import Options
from evidently.legacy.report import Report
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.test_suite import TestSuite
from evidently.legacy.tests.base_test import Test
from evidently.legacy.ui.workspace import CloudWorkspace
from evidently.legacy.ui.workspace.remote import RemoteWorkspace
from evidently.legacy.ui.workspace.view import WorkspaceView
from evidently.legacy.utils import NumpyEncoder
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import autoregister

CONFIG_PATH = "collector_config.json"


class Config(BaseModel):
    @classmethod
    def load(cls, path: str):
        with open(path) as f:
            return TypeAdapter(cls).validate_python(json.load(f))

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.dict(), f, cls=NumpyEncoder, indent=2)


class CollectorTrigger(PolymorphicModel):
    __is_base_type__: ClassVar[bool] = True

    @abc.abstractmethod
    def is_ready(self, config: "CollectorConfig", storage: "CollectorStorage") -> bool:
        raise NotImplementedError


@autoregister
class IntervalTrigger(CollectorTrigger):
    __type_alias__: ClassVar[Optional[str]] = "evidently:collector_trigger:IntervalTrigger"

    interval: float = Field(gt=0)
    last_triggered: float = 0

    def is_ready(self, config: "CollectorConfig", storage: "CollectorStorage") -> bool:
        now = time.time()
        is_ready = (now - self.last_triggered) > self.interval
        if is_ready:
            self.last_triggered = now
        return is_ready


@autoregister
class RowsCountTrigger(CollectorTrigger):
    __type_alias__: ClassVar[Optional[str]] = "evidently:collector_trigger:RowsCountTrigger"

    rows_count: int = Field(default=1, gt=0)

    def is_ready(self, config: "CollectorConfig", storage: "CollectorStorage") -> bool:
        buffer_size = storage.get_buffer_size(config.id)
        return buffer_size > 0 and buffer_size >= self.rows_count


@autoregister
class RowsCountOrIntervalTrigger(CollectorTrigger):
    __type_alias__: ClassVar[Optional[str]] = "evidently:collector_trigger:RowsCountOrIntervalTrigger"

    rows_count_trigger: RowsCountTrigger
    interval_trigger: IntervalTrigger

    def is_ready(self, config: "CollectorConfig", storage: "CollectorStorage") -> bool:
        return self.interval_trigger.is_ready(config, storage) or self.rows_count_trigger.is_ready(config, storage)


class ReportConfig(Config):
    metrics: List[Metric]
    tests: List[Test]
    options: Options
    metadata: Dict[str, MetadataValueType]
    tags: List[str]

    @classmethod
    def from_report(cls, report: Report):
        return ReportConfig(
            metrics=report._first_level_metrics,
            tests=[],
            options=report.options,
            metadata=report.metadata,
            tags=report.tags,
        )

    @classmethod
    def from_test_suite(cls, test_suite: TestSuite):
        return ReportConfig(
            tests=test_suite._inner_suite.context.tests,
            metrics=[],
            options=test_suite.options,
            metadata=test_suite.metadata,
            tags=test_suite.tags,
        )

    def to_report_base(self) -> Union[TestSuite, Report]:
        if len(self.tests) > 0:
            return TestSuite(
                tests=self.tests,  # type: ignore[arg-type]
                options=self.options,
                metadata=self.metadata,
                tags=self.tags,
            )
        return Report(
            metrics=self.metrics,  # type: ignore[arg-type]
            options=self.options,
            metadata=self.metadata,
            tags=self.tags,
        )


class CollectorConfig(Config):
    id: str = ""
    trigger: CollectorTrigger
    report_config: ReportConfig
    reference_path: Optional[str] = None

    project_id: str
    api_url: str = "http://localhost:8000"
    api_secret: Optional[str] = None
    cache_reference: bool = True
    is_cloud: Optional[bool] = None  # None means autodetect
    save_datasets: bool = False

    __reference__: Any = None
    __workspace__: Optional[WorkspaceView] = None

    @property
    def is_cloud_resolved(self) -> bool:
        return self.is_cloud if self.is_cloud is not None else self.api_url == "https://app.evidently.cloud"

    @property
    def workspace(self) -> WorkspaceView:
        if self.__workspace__ is None:
            if self.is_cloud_resolved:
                if self.api_secret is None:
                    raise ValueError("Please provide token and org_id for CloudWorkspace")
                self.__workspace__ = CloudWorkspace(token=self.api_secret, url=self.api_url)
            else:
                if self.save_datasets:
                    warnings.warn("'save_datasets' is not supported for self-hosted Evidently UI")
                self.__workspace__ = RemoteWorkspace(base_url=self.api_url, secret=self.api_secret)
        return self.__workspace__

    def _read_reference(self):
        return pd.read_parquet(self.reference_path)

    @property
    def reference(self):
        if self.reference_path is None:
            return None
        if self.__reference__ is not None:
            return self.__reference__
        if not self.cache_reference:
            return self._read_reference()
        self.__reference__ = self._read_reference()
        return self.__reference__


class CollectorServiceConfig(Config):
    check_interval: float = 1
    collectors: Dict[str, CollectorConfig] = {}
    storage: CollectorStorage = InMemoryStorage()
    autosave: bool = True

    @classmethod
    def load_or_default(cls, path: str):
        try:
            return cls.load(path)
        except FileNotFoundError:
            default = CollectorServiceConfig()
            default.save(path)
            return default
