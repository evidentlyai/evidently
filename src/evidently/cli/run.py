import os
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

import typer
from typer import Argument
from typer import Option

from evidently import Dataset
from evidently import Report
from evidently._pydantic_compat import parse_obj_as
from evidently.cli.main import app
from evidently.cli.utils import _Config
from evidently.cli.utils import _import_module_from_file
from evidently.cli.utils import _import_modules
from evidently.core.container import MetricOrContainer
from evidently.legacy.suite.base_suite import MetadataValueType
from evidently.pydantic_utils import ALLOWED_TYPE_PREFIXES


class RunConfig(_Config):
    modules: List[str] = []
    metrics: List[MetricOrContainer] = []
    metadata: Dict[str, MetadataValueType] = {}
    tags: List[str] = []
    include_tests: bool = False

    @classmethod
    def load(cls, path: str) -> "RunConfig":
        config_dir = os.path.dirname(os.path.abspath(path))
        data = cls._load_data(path)
        
        modules = data.get("modules", [])
        if modules:
            _import_modules(modules, config_dir)
        
        return parse_obj_as(cls, data)

    def to_report(self) -> Report:
        return Report(
            metrics=self.metrics,
            metadata=self.metadata,
            tags=self.tags,
            include_tests=self.include_tests,
        )


def _add_custom_module_prefix(module_path: str) -> None:
    """Add a module's name to allowed type prefixes if it's a custom module.
    
    This allows custom metrics defined in external modules to be loaded
    via PolymorphicModel.load_alias.
    
    For a file like 'custom_metrics.py', the module name 'custom_metrics'
    will be added to ALLOWED_TYPE_PREFIXES.
    """
    if os.path.exists(module_path):
        path = Path(module_path)
        if path.is_file():
            module_name = path.stem
        else:
            module_name = path.name
        
        if module_name and module_name not in ALLOWED_TYPE_PREFIXES:
            ALLOWED_TYPE_PREFIXES.append(module_name)


@app.command("run")
def run_command(
    config_path: str = Argument(..., help="Path to YAML/JSON configuration file"),
    current: str = Option(..., "--current", "-c", help="Path to current dataset CSV file"),
    reference: Optional[str] = Option(None, "--reference", "-r", help="Path to reference dataset CSV file"),
    output: Optional[str] = Option(None, "--output", "-o", help="Output path for snapshot (JSON)"),
    output_html: Optional[str] = Option(None, "--output-html", help="Output path for HTML report"),
):
    """Run Evidently report from a configuration file.
    
    Example:
        evidently run --config config.yaml --current data.csv --reference reference.csv
    """
    typer.echo(f"Loading configuration from: {config_path}")
    
    config_dir = os.path.dirname(os.path.abspath(config_path))
    data = RunConfig._load_data(config_path)
    
    modules = data.get("modules", [])
    if modules:
        typer.echo(f"Importing {len(modules)} custom module(s)...")
        for module_path in modules:
            _add_custom_module_prefix(module_path)
        _import_modules(modules, config_dir)
    
    config = parse_obj_as(RunConfig, data)
    report = config.to_report()
    
    typer.echo(f"Loading current dataset: {current}")
    current_data = Dataset.load(current)
    
    reference_data = None
    if reference:
        typer.echo(f"Loading reference dataset: {reference}")
        reference_data = Dataset.load(reference)
    
    typer.echo(f"Running report with {len(report.metrics)} metric(s)...")
    snapshot = report.run(current_data=current_data, reference_data=reference_data)
    
    if output:
        typer.echo(f"Saving snapshot to: {output}")
        snapshot.save_json(output)
    
    if output_html:
        typer.echo(f"Saving HTML report to: {output_html}")
        snapshot.save_html(output_html)
    
    typer.echo("Report completed successfully!")
    
    if snapshot.tests_results:
        from collections import Counter
        from evidently.legacy.tests.base_test import TestStatus
        
        status_counter = Counter(tr.status for tr in snapshot.tests_results)
        typer.echo("\nTest Summary:")
        for status in [TestStatus.SUCCESS, TestStatus.WARNING, TestStatus.FAIL, TestStatus.ERROR, TestStatus.SKIPPED]:
            if status in status_counter:
                count = status_counter[status]
                color = {
                    TestStatus.SUCCESS: typer.colors.GREEN,
                    TestStatus.WARNING: typer.colors.YELLOW,
                    TestStatus.FAIL: typer.colors.RED,
                    TestStatus.ERROR: typer.colors.RED,
                    TestStatus.SKIPPED: typer.colors.WHITE,
                }.get(status, typer.colors.WHITE)
                typer.secho(f"  {status.value}: {count}", fg=color)
        
        if TestStatus.FAIL in status_counter or TestStatus.ERROR in status_counter:
            raise typer.Exit(code=1)


@app.command("validate-config")
def validate_config(
    config_path: str = Argument(..., help="Path to YAML/JSON configuration file to validate"),
):
    """Validate a configuration file for correctness.
    
    This command checks:
    - YAML/JSON syntax is valid
    - All referenced modules can be imported
    - All metrics can be instantiated
    - Configuration structure is correct
    
    Example:
        evidently validate-config config.yaml
    """
    typer.echo(f"Validating configuration: {config_path}")
    
    if not os.path.exists(config_path):
        typer.secho(f"Error: Configuration file not found: {config_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    try:
        config_dir = os.path.dirname(os.path.abspath(config_path))
        data = RunConfig._load_data(config_path)
        typer.secho("✓ Configuration syntax is valid", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"✗ Configuration syntax error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    modules = data.get("modules", [])
    if modules:
        typer.echo(f"\nValidating {len(modules)} module(s)...")
        for i, module_path in enumerate(modules, 1):
            try:
                _add_custom_module_prefix(module_path)
                if config_dir and not os.path.isabs(module_path):
                    module_path = os.path.join(config_dir, module_path)
                _import_module_from_file(module_path)
                typer.secho(f"  ✓ Module {i}: {module_path}", fg=typer.colors.GREEN)
            except Exception as e:
                typer.secho(f"  ✗ Module {i}: {module_path} - Error: {e}", fg=typer.colors.RED)
                raise typer.Exit(code=1)
    else:
        typer.echo("\nNo custom modules to validate")
    
    typer.echo("\nValidating metrics configuration...")
    try:
        if modules:
            _import_modules(modules, config_dir)
        config = parse_obj_as(RunConfig, data)
        typer.secho(f"  ✓ {len(config.metrics)} metric(s) configured correctly", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"  ✗ Metrics configuration error: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    
    typer.echo("\n" + "=" * 50)
    typer.secho("✓ Configuration is valid!", fg=typer.colors.GREEN)
    typer.echo("=" * 50)
    
    if config.metrics:
        typer.echo(f"\nConfigured Metrics ({len(config.metrics)}):")
        for i, metric in enumerate(config.metrics, 1):
            metric_type = metric.__class__.__name__
            typer.echo(f"  {i}. {metric_type}")
    
    if config.modules:
        typer.echo(f"\nCustom Modules ({len(config.modules)}):")
        for i, module in enumerate(config.modules, 1):
            typer.echo(f"  {i}. {module}")
