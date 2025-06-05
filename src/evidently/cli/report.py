import json
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar
from typing import Union

from typer import Argument
from typer import Option

from evidently import Dataset
from evidently import Report
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.cli.main import app
from evidently.core.container import MetricOrContainer
from evidently.core.datasets import Descriptor
from evidently.core.report import Snapshot
from evidently.legacy.options.base import Option as EvidentlyOption
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.utils import NumpyEncoder
from evidently.ui.service.type_aliases import DatasetID
from evidently.ui.service.type_aliases import ProjectID
from evidently.ui.workspace import CloudWorkspace
from evidently.ui.workspace import RemoteWorkspace

T = TypeVar("T")


class _Config(BaseModel):
    @classmethod
    def load(cls: Type[T], path: str) -> "T":
        with open(path) as f:
            return parse_obj_as(cls, json.load(f))

    def save(self, path: str) -> None:
        with open(path, "w") as f:
            json.dump(self.dict(), f, indent=2, ensure_ascii=False)


class ReportConfig(_Config):
    metrics: List[MetricOrContainer]
    metadata: Dict[str, MetadataValueType] = {}
    tags: List[str] = []
    include_tests: bool = False

    def to_report(self) -> Report:
        return Report(metrics=self.metrics, metadata=self.metadata, tags=self.tags, include_tests=self.include_tests)


class _URI:
    def __init__(self, uri: str):
        self.uri = uri
        if self.is_cloud or self.is_remote:
            self.ws = self._get_ws()

    def _get_ws(self) -> Union[RemoteWorkspace, CloudWorkspace]:
        if self.is_remote:
            proto, addr = self.uri.split("://", maxsplit=1)
            return RemoteWorkspace(f"{proto}://{addr.split('/')[0]}")
        if self.is_cloud:
            _, addr = self.uri.split("://", maxsplit=1)
            if len(addr.split("/")) > 2:
                base_url = "https://" + addr.split("/")[0]
            else:
                base_url = None
            return CloudWorkspace(url=base_url)
        raise ValueError(f"{self.uri} is not a valid remote or cloud URI")

    @property
    def is_cloud(self):
        return self.uri.startswith("cloud://")

    @property
    def is_remote(self):
        return self.uri.startswith("http")

    @property
    def is_local(self):
        return not self.is_cloud and not self.is_remote

    def load_dataset(self) -> Dataset:
        if self.is_local:
            # raise NotImplementedError("not yet implemented")
            return Dataset.load(self.uri)
        if self.is_remote:
            raise ValueError("Remote workspace does not support dataset loading")
        if self.is_cloud:
            return self.ws.load_dataset(DatasetID(self.uri.split("/")[-1]))
        raise ValueError(f"{self.uri} is not a valid dataset URI")

    def upload_snapshot(self, snapshot: Snapshot):
        if self.is_local:
            with open(self.uri, "w") as f:
                f.write(json.dumps(snapshot.to_snapshot_model().dict(), indent=2, ensure_ascii=False, cls=NumpyEncoder))
            return
        if self.is_remote or self.is_cloud:
            self.ws.add_run(self.uri.split("/")[-1], snapshot)
            return
        raise ValueError(f"{self.uri} is not a valid URI")

    def upload_dataset(self, dataset: Dataset, name: Optional[str]):
        if self.is_local:
            dataset.save(self.uri)
            return
        if self.is_cloud:
            self.ws.add_dataset(ProjectID(self.uri.split("/")[-1]), dataset, name or "", None)
            return
        if self.is_remote:
            raise ValueError("Remote workspace does not support dataset uploading")
        raise ValueError(f"{self.uri} is not a valid URI")


class DescriptorsConfig(_Config):
    descriptors: List[Descriptor]
    options: List[EvidentlyOption] = []


@app.command("report")
def run_report(
    report_config: str = Argument(..., help="Report configuration path"),
    output: str = Argument(..., help="Output URI"),
    current: str = Option(help="current dataset"),
    reference: Optional[str] = Option(default=None, help="reference dataset"),
):
    """Run evidently report"""
    report = ReportConfig.load(report_config).to_report()
    snapshot = report.run(
        _URI(current).load_dataset(), _URI(reference).load_dataset() if reference is not None else None
    )
    output_uri = _URI(output)

    output_uri.upload_snapshot(snapshot)


@app.command("descriptors")
def run_descriptors(
    descriptors_config: str = Argument(..., help="Descriptors configuration path"),
    input_path: str = Argument(..., help="Input URI", metavar="input"),
    output: str = Argument(..., help="Output URI"),
    name: Optional[str] = Option(None, help="Name of dataset"),
):
    """Run evidently descriptors"""
    conf = DescriptorsConfig.load(descriptors_config)
    dataset = _URI(input_path).load_dataset()

    dataset.add_descriptors(conf.descriptors, conf.options)

    _URI(output).upload_dataset(dataset, name)
