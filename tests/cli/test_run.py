"""Test CLI run and validate-config commands."""
import os
import tempfile
from pathlib import Path

import pandas as pd
import pytest
from typer.testing import CliRunner

from evidently.cli import app

runner = CliRunner()


@pytest.fixture
def test_data_dir():
    """Create a temporary directory with test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        current_df = pd.DataFrame({
            "a": [1, 2, 3, 4, 5],
            "b": [10, 20, 30, 40, 50],
        })
        reference_df = pd.DataFrame({
            "a": [1, 2, 3, 4, 5],
            "b": [10, 20, 30, 40, 50],
        })
        
        current_df.to_csv(tmp_path / "current.csv", index=False)
        reference_df.to_csv(tmp_path / "reference.csv", index=False)
        
        yield tmp_path


class TestValidateConfig:
    """Test validate-config command."""

    def test_validate_valid_yaml_config(self, test_data_dir):
        """Test validating a valid YAML configuration."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:RowCount
  - type: evidently:metric_v2:ColumnCount

metadata:
  model_id: test_model

tags:
  - test
  - production

include_tests: false
""")
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Configuration is valid" in result.output
        assert "RowCount" in result.output
        assert "ColumnCount" in result.output

    def test_validate_valid_json_config(self, test_data_dir):
        """Test validating a valid JSON configuration."""
        import json
        
        config_path = test_data_dir / "config.json"
        config = {
            "metrics": [
                {"type": "evidently:metric_v2:RowCount"},
                {"type": "evidently:metric_v2:ColumnCount"},
            ],
            "metadata": {"model_id": "test_model"},
            "tags": ["test"],
            "include_tests": False,
        }
        config_path.write_text(json.dumps(config))
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Configuration is valid" in result.output

    def test_validate_invalid_syntax(self, test_data_dir):
        """Test validating a configuration with invalid YAML syntax."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:RowCount
    invalid: [unclosed list
""")
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 1
        assert "syntax error" in result.output

    def test_validate_nonexistent_file(self):
        """Test validating a non-existent configuration file."""
        result = runner.invoke(app, ["validate-config", "/nonexistent/config.yaml"])
        assert result.exit_code == 1
        assert "not found" in result.output

    def test_validate_config_with_presets(self, test_data_dir):
        """Test validating a configuration with presets."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_container:DataSummaryPreset

include_tests: true
""")
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Configuration is valid" in result.output


class TestRunCommand:
    """Test run command."""

    def test_run_with_basic_config(self, test_data_dir):
        """Test running a basic report with YAML config."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:RowCount
  - type: evidently:metric_v2:ColumnCount

metadata:
  model_id: test_model

tags:
  - test
""")
        
        output_path = test_data_dir / "output.json"
        current_path = test_data_dir / "current.csv"
        
        result = runner.invoke(app, [
            "run",
            "--config", str(config_path),
            "--current", str(current_path),
            "--output", str(output_path),
        ])
        
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Report completed successfully" in result.output
        assert output_path.exists()

    def test_run_with_reference_data(self, test_data_dir):
        """Test running a report with both current and reference data."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:RowCount

include_tests: true
""")
        
        output_path = test_data_dir / "output.json"
        current_path = test_data_dir / "current.csv"
        reference_path = test_data_dir / "reference.csv"
        
        result = runner.invoke(app, [
            "run",
            "--config", str(config_path),
            "--current", str(current_path),
            "--reference", str(reference_path),
            "--output", str(output_path),
        ])
        
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Report completed successfully" in result.output

    def test_run_with_html_output(self, test_data_dir):
        """Test running a report and saving HTML output."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:RowCount
  - type: evidently:metric_v2:MeanValue
    column: a
""")
        
        html_path = test_data_dir / "output.html"
        current_path = test_data_dir / "current.csv"
        
        result = runner.invoke(app, [
            "run",
            "--config", str(config_path),
            "--current", str(current_path),
            "--output-html", str(html_path),
        ])
        
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Report completed successfully" in result.output
        assert html_path.exists()
        assert html_path.stat().st_size > 0


class TestConfigStructure:
    """Test configuration structure and parsing."""

    def test_config_with_metrics_parameters(self, test_data_dir):
        """Test configuration with metrics that have parameters."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:MeanValue
    column: a
  - type: evidently:metric_v2:MinValue
    column: b
  - type: evidently:metric_v2:MaxValue
    column: a
""")
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Configuration is valid" in result.output
        assert "MeanValue" in result.output
        assert "MinValue" in result.output
        assert "MaxValue" in result.output

    def test_empty_metrics_list(self, test_data_dir):
        """Test configuration with empty metrics list."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics: []
metadata: {}
tags: []
include_tests: false
""")
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Configuration is valid" in result.output

    def test_config_with_metadata_and_tags(self, test_data_dir):
        """Test configuration with metadata and tags."""
        config_path = test_data_dir / "config.yaml"
        config_path.write_text("""
metrics:
  - type: evidently:metric_v2:RowCount

metadata:
  model_id: my_model_v1
  version: "1.0.0"
  environment: production
  batch_size: 1000

tags:
  - classification
  - production
  - v1.0.0

include_tests: true
""")
        
        result = runner.invoke(app, ["validate-config", str(config_path)])
        assert result.exit_code == 0, f"Output: {result.output}\nError: {result.exception}"
        assert "Configuration is valid" in result.output
