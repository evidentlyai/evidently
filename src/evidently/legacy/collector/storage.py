import abc
from asyncio import Lock
from typing import Any
from typing import Dict
from typing import List
from typing import Sequence

import pandas as pd

from evidently._pydantic_compat import BaseModel
from evidently.legacy.suite.base_suite import ReportBase
from evidently.pydantic_utils import PolymorphicModel
from evidently.pydantic_utils import autoregister


class LogEvent(BaseModel):
    type: str
    report_id: str
    ok: bool
    error: str = ""


class CreateReportEvent(LogEvent):
    type = "CreateReport"


class UploadReportEvent(LogEvent):
    type = "UploadReport"


class ReportPopper:
    def __init__(self, value: ReportBase, snapshot_list: List[ReportBase]):
        self.value = value
        self.report_list = snapshot_list

    def __enter__(self) -> ReportBase:
        return self.value

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.report_list.insert(0, self.value)


class CollectorStorage(PolymorphicModel):
    class Config:
        underscore_attrs_are_private = True
        is_base_type = True

    _locks: Dict[str, Lock] = {}

    def lock(self, id: str):
        return self._locks[id]

    def init(self, id: str):
        self._locks[id] = Lock()

    def init_all(self, config):
        for id in config.collectors:
            self.init(id)

    @abc.abstractmethod
    def append(self, id: str, data: Any):
        raise NotImplementedError

    @abc.abstractmethod
    def get_buffer_size(self, id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def get_and_flush(self, id: str):
        raise NotImplementedError

    @abc.abstractmethod
    def log(self, id: str, event: LogEvent):
        raise NotImplementedError

    @abc.abstractmethod
    def get_logs(self, id: str) -> List[LogEvent]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_report(self, id: str, report: ReportBase):
        raise NotImplementedError

    @abc.abstractmethod
    def take_reports(self, id: str) -> Sequence[ReportPopper]:
        raise NotImplementedError


@autoregister
class InMemoryStorage(CollectorStorage):
    class Config:
        type_alias = "evidently:collector_storage:InMemoryStorage"

    max_log_events: int = 10

    _buffers: Dict[str, List[Any]] = {}
    _logs: Dict[str, List[LogEvent]] = {}
    _reports: Dict[str, List[ReportBase]] = {}

    def init(self, id: str):
        super().init(id)
        self._buffers[id] = []
        self._logs[id] = []
        self._reports[id] = []

    def append(self, id: str, data: Any):
        self._buffers[id].append(data)

    def get_buffer_size(self, id: str):
        return len(self._buffers[id])

    def get_and_flush(self, id: str):
        if id not in self._buffers or len(self._buffers[id]) == 0:
            return None

        res = pd.concat([pd.DataFrame.from_dict(o) for o in self._buffers[id]])
        self._buffers[id].clear()
        return res

    def log(self, id: str, event: LogEvent):
        self._logs[id].insert(0, event)
        if self.max_log_events > 0:
            self._logs[id] = self._logs[id][: self.max_log_events]

    def get_logs(self, id: str) -> List[LogEvent]:
        return self._logs.get(id, [])

    def add_report(self, id: str, report: ReportBase):
        self._reports[id].append(report)

    def take_reports(self, id: str) -> Sequence[ReportPopper]:
        report_list = self._reports.get(id, [])
        while len(report_list) > 0:
            yield ReportPopper(report_list.pop(0), report_list)
