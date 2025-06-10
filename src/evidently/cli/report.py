import json
import os
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

import typer
from typer import Argument
from typer import Option

from evidently import Dataset
from evidently import Report
from evidently._pydantic_compat import BaseModel
from evidently._pydantic_compat import parse_obj_as
from evidently.cli.main import app
from evidently.cli.utils import _URI
from evidently.core.container import MetricOrContainer
from evidently.core.datasets import Descriptor
from evidently.core.report import Snapshot
from evidently.legacy.options.base import Option as EvidentlyOption
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.legacy.tests.base_test import TestStatus
from evidently.metrics.column_testing import RowTestSummary

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
    descriptors: List[Descriptor]
    options: List[EvidentlyOption] = []
    metrics: List[MetricOrContainer]
    metadata: Dict[str, MetadataValueType] = {}
    tags: List[str] = []
    include_tests: bool = False

    def to_report(self) -> Report:
        return Report(metrics=self.metrics, metadata=self.metadata, tags=self.tags, include_tests=self.include_tests)


@app.command("report")
def run_report(
    config_path: str = Argument(..., help="Report configuration path"),
    input_path: str = Argument(..., help="Input dataset URI", metavar="input"),
    output: str = Argument(..., help="Output URI"),
    reference_path: Optional[str] = Option(default=None, help="reference dataset"),
    name: Optional[str] = Option(None, help="Name of dataset"),
    test_summary: bool = Option(False, help="Run tests summary"),
    save_dataset: bool = Option(True, help="Save output dataset"),
    save_report: bool = Option(True, help="Save output report"),
):
    """Run evidently report"""
    typer.echo(f"Loading config from {os.path.abspath(config_path)}")
    config = ReportConfig.load(config_path)
    typer.echo(f"Loading dataset from {input_path}")
    input_data = _URI(input_path).load_dataset()

    has_descriptors = len(config.descriptors) > 0
    has_report = len(config.metrics) > 0
    if has_descriptors:
        typer.echo(f"Running {len(config.descriptors)} descriptors")
        input_data.add_descriptors(config.descriptors, config.options)

    if not has_report:
        if save_dataset:
            typer.echo(f"Saving dataset to {output}")
            _URI(output).upload_dataset(input_data, name)
        if test_summary:
            typer.echo("Running tests summary")
            any_failed = _run_summary_report(input_data)
            if any_failed:
                typer.echo("Some tests failed")
                raise typer.Exit(code=1)
        return

    reference = None
    if has_report and reference_path is not None:
        typer.echo(f"Loading reference dataset from {reference_path}")
        reference = _URI(reference_path).load_dataset()
        reference.add_descriptors(config.descriptors, config.options)

    report = config.to_report()
    if test_summary and not any(isinstance(m, RowTestSummary) for m in report.metrics):
        report.metrics.append(RowTestSummary())
    snapshot = report.run(
        input_data,
        reference,
    )
    if save_report:
        _URI(output).upload_snapshot(snapshot, include_datasets=save_dataset)
    elif save_dataset:
        _URI(output).upload_dataset(input_data, name)
    if test_summary:
        typer.echo("Running tests summary")
        any_failed = _print_summary_report(snapshot)
        if any_failed:
            typer.echo("Some tests failed")
            raise typer.Exit(code=1)


def _run_summary_report(dataset: Dataset) -> bool:
    report = Report(metrics=[RowTestSummary()])
    summary = report.run(dataset)
    return _print_summary_report(summary)


def _print_summary_report(summary: Snapshot) -> bool:
    any_failed = False
    for tr in summary.tests_results:
        print(f"{tr.name}: {tr.status}")
        if tr.status not in (TestStatus.SUCCESS, TestStatus.WARNING, TestStatus.SKIPPED):
            any_failed = True
    return any_failed
