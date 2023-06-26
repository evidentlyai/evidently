import json
from typing import Dict
from typing import List

from pydantic import BaseModel
from pydantic import parse_obj_as

from evidently.base_metric import Metric
from evidently.options.base import Options
from evidently.report import Report
from evidently.utils import NumpyEncoder

CONFIG_PATH = "config.json"


class Config(BaseModel):
    @classmethod
    def load(cls, path: str):
        with open(path) as f:
            return parse_obj_as(cls, json.load(f))

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.dict(), f, cls=NumpyEncoder, indent=2)


class CollectorConfig(Config):
    snapshot_interval: float
    report_config_path: str
    project_id: str
    api_url: str = "http://localhost:8000"

    @classmethod
    def load_or_default(cls, path: str, default: "CollectorConfig"):
        try:
            return cls.load(path)
        except FileNotFoundError:
            default.save(path)
            return default

    def report_config(self):
        return ReportConfig.load(self.report_config_path)


class ReportConfig(Config):
    metrics: List[Metric]
    options: Options
    metadata: Dict[str, str]
    tags: List[str]


def create_config_report(report: Report, path: str):
    ReportConfig(metrics=report._first_level_metrics, options=report.options, metadata=report.metadata, tags=report.tags).save(path)
