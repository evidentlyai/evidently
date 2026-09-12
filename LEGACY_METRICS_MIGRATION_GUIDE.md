# Legacy Metrics to New Report API Migration Guide

## Issue Overview
GitHub Issue #1805: Certain legacy regression metrics (like `RegressionErrorBiasTable`, `RegressionPredictedVsActualScatter`, etc.) from the legacy API don't work with the new Report API. This guide explains how to migrate them.

## Problem Statement
The new Report API (in `src/evidently/core/report.py`) uses a `MetricCalculation` base class pattern, while legacy metrics (in `src/evidently/legacy/metrics/`) use an older `Metric` base class. Legacy metrics need adapters to integrate with the new Report system.

## Current Architecture

### Legacy Metrics (Old System)
- **Location**: `src/evidently/legacy/metrics/`
- **Base class**: `Metric[TResult]` (in `legacy/base_metric.py`)
- **Process**: Direct calculation via `calculate(InputData) -> MetricResult`
- **Example**: `RegressionErrorBiasTable`, `RegressionPredictedVsActualScatter`

### New Report API (New System)
- **Location**: `src/evidently/metrics/` and `src/evidently/core/report.py`
- **Base class**: `MetricCalculation[TResult, TMetric]`
- **Process**: Two-layer calculation via `calculate(context, current_data, reference_data)`
- **Pattern**: Create a `MetricCalculation` subclass that wraps the legacy metric

## Migration Pattern: `LegacyMetricCalculation`

The framework already provides a bridge pattern called `LegacyMetricCalculation` in `src/evidently/metrics/_legacy.py`:

```python
class LegacyMetricCalculation(
    MetricCalculation[TResult, TMetric],
    Generic[TResult, TMetric, TLegacyResult, TLegacyMetric],
    abc.ABC,
):
    @abc.abstractmethod
    def legacy_metric(self) -> TLegacyMetric:
        """Return the legacy metric instance to calculate."""
        raise NotImplementedError()

    def calculate(self, context: "Context", current_data: Dataset, reference_data: Optional[Dataset]) -> TMetricResult:
        """Calculate using the legacy metric, then extract/apply results."""
        result, render = context.get_legacy_metric(self.legacy_metric(), self._gen_input_data, self.task_name())
        metric_result = self.calculate_value(context, result, render)
        # Handle single or tuple results (current, reference)
        if isinstance(metric_result, tuple):
            current, reference = metric_result
        else:
            current, reference = metric_result, None
        current.widget = current.widget or get_default_render(self.display_name(), current)
        return current, reference

    @abc.abstractmethod
    def calculate_value(
        self,
        context: "Context",
        legacy_result: TLegacyResult,
        render: List[BaseWidgetInfo],
    ) -> TMetricResult:
        """Extract/transform the legacy result into new metric result."""
        raise NotImplementedError()
```

## Step-by-Step Migration Process

### Step 1: Define New Metric Class

Create a new metric class in `src/evidently/metrics/` that inherits from the appropriate new base class:

```python
from evidently.core.metric_types import SingleValue, SingleValueMetric, DataframeValue
from evidently.metrics._legacy import LegacyMetricCalculation

# 1. Create the new metric class (data model)
class RegressionErrorBiasTable(SingleValueMetric):
    """New Report API metric for regression error bias analysis.
    
    This metric calculates error bias across different features in regression predictions.
    """
    regression_name: str = "default"
    columns: Optional[List[str]] = None
    top_error: Optional[float] = None
```

### Step 2: Create Calculation Class

Create a corresponding calculation class that inherits from `LegacyMetricCalculation`:

```python
from evidently.legacy.metrics import RegressionErrorBiasTable as LegacyRegressionErrorBiasTable
from evidently.legacy.metrics.regression_performance.error_bias_table import RegressionErrorBiasTableResults as LegacyRegressionErrorBiasTableResults

class RegressionErrorBiasTableCalculation(
    LegacyMetricCalculation[
        SingleValue,  # New result type
        RegressionErrorBiasTable,  # New metric type
        LegacyRegressionErrorBiasTableResults,  # Legacy result type
        LegacyRegressionErrorBiasTable,  # Legacy metric type
    ],
):
    def legacy_metric(self) -> LegacyRegressionErrorBiasTable:
        """Instantiate the legacy metric with parameters from new metric."""
        return LegacyRegressionErrorBiasTable(
            columns=self.metric.columns,
            top_error=self.metric.top_error,
        )

    def calculate_value(
        self,
        context: "Context",
        legacy_result: LegacyRegressionErrorBiasTableResults,
        render: List[BaseWidgetInfo],
    ) -> TMetricResult:
        """Extract values from legacy result and create new metric result."""
        # Transform legacy result into new format
        if legacy_result.error_bias is None:
            value = 0.0
        else:
            # Example: compute summary statistic from error_bias dict
            value = len(legacy_result.error_bias)
        
        return self.result(value)

    def display_name(self) -> str:
        return "Regression Error Bias Table"
```

### Step 3: Register Calculation

Make sure your new metric-calculation pair are properly connected in the `Report` system. Registration typically happens automatically via imports if you follow the standard pattern.

## Working Examples in Codebase

### Example 1: MAE (Mean Absolute Error)

**Metric class** (`src/evidently/metrics/regression.py`):
```python
class MAE(MeanStdRegressionMetric):
    """Calculate Mean Absolute Error (MAE) for regression."""
    error_plot: bool = False
    error_distr: bool = True
    error_normality: bool = False
```

**Calculation class** (`src/evidently/metrics/regression.py`):
```python
class MAECalculation(LegacyRegressionMeanStdMetric[MAE]):
    def calculate_value(
        self, context: Context, legacy_result: RegressionQualityMetricResults, render: List[BaseWidgetInfo]
    ):
        return (
            self.result(
                legacy_result.current.mean_absolute_error,
                legacy_result.current.abs_error_std,
            ),
            None if legacy_result.reference is None
            else self.result(
                legacy_result.reference.mean_absolute_error,
                legacy_result.reference.abs_error_std,
            ),
        )

    def display_name(self) -> str:
        return "Mean Absolute Error"
```

### Example 2: Classification ROC AUC

Similar pattern in `src/evidently/metrics/classification.py` using `LegacyMetricCalculation`.

## Key Metrics to Migrate

Based on the issue and codebase analysis, these metrics need migration:

1. **RegressionErrorBiasTable** - Error bias analysis by feature
2. **RegressionPredictedVsActualScatter** - Predicted vs actual scatter plots
3. **RegressionPredictedVsActualPlot** - Time-series predicted vs actual
4. **RegressionErrorPlot** - Error visualization over time
5. **RegressionErrorDistribution** - Error distribution analysis
6. **RegressionErrorNormality** - Normality test of errors
7. **RegressionAbsPercentageErrorPlot** - Absolute percentage error
8. **RegressionTopErrorMetric** - Top errors analysis

## Implementation Checklist

For each legacy metric to migrate:

- [ ] Create new metric class in `src/evidently/metrics/regression.py`
- [ ] Create calculation class inheriting from `LegacyMetricCalculation`
- [ ] Implement `legacy_metric()` to instantiate legacy metric with new params
- [ ] Implement `calculate_value()` to extract legacy result into new format
- [ ] Implement `display_name()` for UI display
- [ ] Add `_gen_input_data()` if task-specific data prep needed (e.g., regression_name)
- [ ] Define `get_additional_widgets()` if extra visualizations needed
- [ ] Export metric in `src/evidently/metrics/__init__.py`
- [ ] Add unit tests in `tests/metrics/`
- [ ] Update documentation

## Type Considerations

When migrating, consider what result type best fits:

- **SingleValue** - For scalar metrics (single number result)
- **MeanStdValue** - For metrics with mean and std dev
- **DataframeValue** - For table/dataframe results
- **Custom types** - For complex structures (use MetricResult subclass)

## Testing Approach

1. **Unit tests**: Verify calculation returns correct values
2. **Integration tests**: Use new metric in Report with new Report API
3. **Backward compatibility**: Legacy code should still work via `legacy.Report`
4. **Widget rendering**: Verify HTML/JSON output renders correctly

## Common Pitfalls

1. **Forgetting `task_name()`** - Return the metric field name if it has a task selector
2. **Widget handling** - Must properly set `widget` field on result
3. **Reference data** - Handle None reference data correctly
4. **Column mapping** - Pass through `_gen_input_data()` override if needed
5. **Parameter mapping** - Map new metric parameters to legacy metric constructor

## Files to Examine

- `src/evidently/metrics/regression.py` - Existing regression metric implementations
- `src/evidently/metrics/_legacy.py` - LegacyMetricCalculation base class
- `src/evidently/legacy/metrics/regression_performance/` - Legacy metric implementations
- `src/evidently/core/metric_types.py` - Metric result types
- `tests/metrics/regression_performance/` - Test patterns

## Next Steps

1. Identify which specific metrics are most critical (check GitHub issues/PRs)
2. Start with simpler scalar metrics (like RegressionErrorBiasTable summary stat)
3. Gradually move to more complex visualization metrics
4. Ensure tests pass before merging
5. Update presets to use new metrics
6. Document migration in changelog

## Additional Resources

- **New Report API**: `src/evidently/core/report.py` - `Report`, `Context` classes
- **Metric Types**: `src/evidently/core/metric_types.py` - Base classes and result types
- **Legacy Pattern**: `src/evidently/metrics/classification.py` - Similar migrations done
- **Examples**: `examples/cookbook/metrics.ipynb` - Usage patterns

---

**Key Insight**: The migration pattern is a bridge between old and new. You're not rewriting the calculation logic—you're wrapping it and adapting the interface. This allows gradual migration while maintaining backward compatibility.
