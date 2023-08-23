import abc
import json
import time
from typing import Any, Dict, Optional
from typing import List

import pandas as pd
from pydantic import BaseModel
from pydantic import parse_obj_as

from evidently.base_metric import Metric
from evidently.options.base import Options
from evidently.pydantic_utils import PolymorphicModel
from evidently.report import Report
from evidently.ui.remote import RemoteWorkspace
from evidently.utils import NumpyEncoder
from storage import CollectorStorage, InMemoryStorage

CONFIG_PATH = "config.json"


class Config(BaseModel):
    @classmethod
    def load(cls, path: str):
        with open(path) as f:
            return parse_obj_as(cls, json.load(f))

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.dict(), f, cls=NumpyEncoder, indent=2)

class CollectorTrigger(PolymorphicModel):
    @abc.abstractmethod
    def is_ready(self, config: "CollectorConfig", storage: "CollectorStorage") -> bool:
        raise NotImplementedError

class IntervalTrigger(CollectorTrigger):
    interval: float
    last_triggered: float = 0

    def is_ready(self, config: "CollectorConfig", storage: "CollectorStorage") -> bool:
        now = time.time()
        if now - self.last_triggered > self.interval:
            self.last_triggered = now
            return True
        return False

class ReportConfig(Config):
    metrics: List[Metric]
    options: Options
    metadata: Dict[str, str]
    tags: List[str]

    @classmethod
    def from_report(cls, report: Report):
        return ReportConfig(metrics=report._first_level_metrics,
                     options=report.options,
                     metadata=report.metadata,
                     tags=report.tags)


class CollectorConfig(Config):
    class Config:
        underscore_attrs_are_private = True
    id: str = ""
    trigger: CollectorTrigger
    report_config: ReportConfig
    reference_path: Optional[str]

    project_id: str
    api_url: str = "http://localhost:8000"
    api_secret: Optional[str] = None
    cache_reference: bool = True

    _reference: Any = None
    _workspace: RemoteWorkspace = None


    @property
    def workspace(self) -> RemoteWorkspace:
        if self._workspace is None:
            self._workspace = RemoteWorkspace(base_url=self.api_url, secret=self.api_secret)
        return self._workspace

    def _read_reference(self):
        return pd.read_parquet(self.reference_path)

    @property
    def reference(self):
        if self.reference_path is None:
            return None
        if self._reference is not None:
            return self._reference
        if not self.cache_reference:
            return self._read_reference()
        self._reference = self._read_reference()
        return self._reference




class CollectorServiceConfig(Config):
    check_interval: float = 1
    collectors: Dict[str, CollectorConfig] = {}
    storage: CollectorStorage = InMemoryStorage()

    @classmethod
    def load_or_default(cls, path: str):
        try:
            return cls.load(path)
        except FileNotFoundError:
            default = CollectorServiceConfig()
            default.save(path)
            return default



