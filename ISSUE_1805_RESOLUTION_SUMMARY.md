# Summary: How to Resolve Issue #1805 - Legacy Metrics to New Report API

## Problem Statement

GitHub Issue #1805 reports that certain legacy regression metrics (like `RegressionErrorBiasTable`, `RegressionPredictedVsActualScatter`, etc.) don't work with Evidently's new Report API. These metrics exist only in the legacy API (`src/evidently/legacy/metrics/`) but not in the new unified metrics system (`src/evidently/metrics/`).

## Root Cause

The legacy metrics use the old `Metric[TResult]` base class from the legacy system, which is incompatible with the new Report API that expects metrics to be derived from the new `MetricCalculation` base class with specific calculation patterns.

## Solution Overview

The framework provides a bridge pattern called **`LegacyMetricCalculation`** that allows legacy metrics to be wrapped and used with the new Report API without rewriting the calculation logic. This is the recommended approach used throughout the codebase for gradual migration.

## The Pattern: LegacyMetricCalculation

The solution involves creating two items for each legacy metric:

1. **A new Metric class** - Defines parameters and acts as the user-facing metric
2. **A Calculation class** - Wraps the legacy metric and adapts it to the new system

### Example Structure

```python
# Step 1: Create the new metric class
class RegressionErrorBiasTable(SingleValueRegressionMetric):
    """New Report API metric of the user-facing side of RegressionErrorBiasTable"""
    columns: Optional[List[str]] = None
    top_error: Optional[float] = None
    regression_name: str = "default"

# Step 2: Create the calculation class that wraps the legacy metric
class RegressionErrorBiasTableCalculation(
    LegacyMetricCalculation[
        SingleValue,                                # What the new metric returns
        RegressionErrorBiasTable,                  # The new metric class
        RegressionErrorBiasTableResults,           # Legacy metric's result type
        LegacyRegressionErrorBiasTable,            # The legacy metric class
    ]
):
    def legacy_metric(self) -> LegacyRegressionErrorBiasTable:
        """Map new metric params to legacy metric"""
        return LegacyRegressionErrorBiasTable(
            columns=self.metric.columns,
            top_error=self.metric.top_error,
        )
    
    def calculate_value(self, context, legacy_result, render):
        """Transform legacy result to new metric result"""
        value = len(legacy_result.error_bias or {})
        return self.result(value)
    
    def display_name(self) -> str:
        return "Regression Error Bias Table"

# Step 3: Export in __init__.py
# from .regression import RegressionErrorBiasTable
# in __all__: "RegressionErrorBiasTable"
```

## How It Works

```
User Code (New API)
    ↓
Report([RegressionErrorBiasTable()])
    ↓
RegressionErrorBiasTableCalculation.calculate()
    ↓
context.get_legacy_metric(
    LegacyRegressionErrorBiasTable(...),  ← Legacy metric does the work
    _gen_input_data_func,
    task_name
)
    ↓
LegacyRegressionErrorBiasTableResults  ← Legacy result
    ↓
calculate_value() transforms it
    ↓
SingleValue + Widgets  ← New metric result
    ↓
Report output
```

## Step-by-Step Implementation Guide

### Step 1: Identify Metrics to Migrate

From `src/evidently/legacy/metrics/regression_performance/`:

**Priority 1 (Most Critical):**
- `RegressionErrorBiasTable` - Error bias analysis by feature
- `RegressionPredictedVsActualScatter` - Predicted vs actual visualization
- `RegressionErrorDistribution` - Error histogram

**Priority 2:**
- `RegressionErrorPlot` - Error timeline
- `RegressionPredictedVsActualPlot` - Predicted/actual timeline
- `RegressionAbsPercentageErrorPlot` - Percentage error visualization

**Priority 3:**
- `RegressionErrorNormality` - Normality test
- `RegressionTopErrorMetric` - Top errors ranking

### Step 2: Create New Metrics (in `src/evidently/metrics/regression.py`)

```python
from evidently.core.metric_types import SingleValueMetric

class RegressionErrorBiasTable(SingleValueRegressionMetric):
    """Your docstring"""
    columns: Optional[List[str]] = None
    top_error: Optional[float] = None
```

### Step 3: Create Calculation Wrapper (in `src/evidently/metrics/regression.py`)

```python
class RegressionErrorBiasTableCalculation(
    LegacyMetricCalculation[
        SingleValue,
        RegressionErrorBiasTable,
        RegressionErrorBiasTableResults,
        LegacyRegressionErrorBiasTable,
    ]
):
    def legacy_metric(self):
        return LegacyRegressionErrorBiasTable(...)
    
    def calculate_value(self, context, legacy_result, render):
        return self.result(...)
    
    def display_name(self):
        return "..."
```

### Step 4: Export (in `src/evidently/metrics/__init__.py`)

```python
from .regression import RegressionErrorBiasTable

__all__ = [
    # ... existing ...
    "RegressionErrorBiasTable",
    # ... rest ...
]
```

### Step 5: Test

```python
from evidently import Report
from evidently.metrics import RegressionErrorBiasTable

report = Report([RegressionErrorBiasTable()])
snapshot = report.run(current_dataset, reference_dataset)
assert snapshot.get_metric_result("RegressionErrorBiasTable") is not None
```

## Key Implementation Details

### Result Types

Choose the appropriate result type based on what the metric returns:

| Type | Usage | Returns |
|------|-------|---------|
| `SingleValue` | Single numeric value | One number |
| `MeanStdValue` | Mean ± standard deviation | Two numbers |
| `DataframeValue` | Tabular data | DataFrame |

### Task Names (for multi-task regression)

If the metric supports multiple regression tasks:

```python
def task_name(self) -> str:
    return self.metric.regression_name

def _gen_input_data(self, context, task_name):
    return _gen_regression_input_data(context, task_name)
```

### Handling Reference Data

Return a tuple if the metric should compute separate values for reference data:

```python
def calculate_value(self, context, legacy_result, render):
    current = self.result(legacy_result.current.value)
    reference = None
    if legacy_result.reference is not None:
        reference = self.result(legacy_result.reference.value)
    return current, reference
```

### Preserving Visualizations

The legacy renderer's HTML widgets are automatically preserved:

```python
def get_additional_widgets(self, context: Context) -> List[BaseWidgetInfo]:
    # Widgets from legacy renderer are already included
    return []
```

## Files to Modify

1. **`src/evidently/metrics/regression.py`**
   - Add new metric class
   - Add calculation wrapper class

2. **`src/evidently/metrics/__init__.py`**
   - Import new metric
   - Add to `__all__`

3. **`tests/metrics/regression_performance/`**
   - Add test file with basic and integration tests

4. **Documentation** (optional but recommended)
   - Update docstrings
   - Update examples/cookbook if needed

## Reference Implementations

Existing working examples in the codebase:

- **`MAE`, `RMSE`** - Simple single-value metrics (src/evidently/metrics/regression.py)
- **`MeanError`** - Mean ± std metrics
- **Classification metrics** - Similar pattern in src/evidently/metrics/classification.py
- **Recommendation metrics** - src/evidently/metrics/recsys.py

## Development Workflow

1. **Pick one metric** to start (e.g., `RegressionErrorBiasTable`)
2. **Copy template** from MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
3. **Implement the 3 methods**: `legacy_metric()`, `calculate_value()`, `display_name()`
4. **Test locally**:
   ```bash
   pytest tests/metrics/regression_performance/test_error_bias_table.py -v
   ```
5. **Verify exports**:
   ```bash
   from evidently.metrics import RegressionErrorBiasTable
   ```
6. **PR and review**
7. **Repeat** for next metric

## Expected Effort per Metric

- **Simple (scalar output)**: 30-45 minutes
- **Complex (with visualizations)**: 1-2 hours
- **Full regression metrics set**: 8-12 hours

## Common Pitfalls to Avoid

1. ❌ **Wrong base class** - Use `LegacyMetricCalculation` not other base classes
2. ❌ **Parameter mapping** - Must map all new metric params to legacy metric constructor
3. ❌ **Forgetting widgets** - Make sure HTML widgets are included in result
4. ❌ **Missing reference handling** - Return tuple `(current, reference)` when applicable
5. ❌ **Skipping task_name()** - If metric supports tasks, override this method
6. ❌ **Not exporting** - Must add to `__init__.py` `__all__` list

## Validation Checklist

- [ ] Metric imports without error
- [ ] Metric instantiates with no parameters
- [ ] Metric instantiates with all parameters
- [ ] Report with metric creates successfully
- [ ] Report.run() completes without error
- [ ] Results are accessible via snapshot.get_metric_result()
- [ ] Results have current value
- [ ] Tests pass: `pytest tests/metrics/...`
- [ ] No regressions in existing tests
- [ ] Multiple metrics can run together
- [ ] Both with and without reference data work

## Documentation Files Included

1. **LEGACY_METRICS_MIGRATION_GUIDE.md** - Comprehensive technical guide
2. **MIGRATION_CHECKLIST.md** - Quick reference with templates
3. **MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py** - Detailed implementation example
4. **COMPLETE_IMPLEMENTATION_EXAMPLE.md** - Production-ready code with tests
5. **This file** - Overview and summary

## Next Actions (Priority Order)

1. **Review** the migration guide and understand the pattern
2. **Pick** the most-used legacy metric from the list
3. **Copy** the implementation template
4. **Implement** following the checklist
5. **Test** thoroughly before submission
6. **Submit PR** with metric migration (one metric per PR recommended)
7. **Iterate** through other metrics

## Questions?

Refer to:
- **How to implement?** → COMPLETE_IMPLEMENTATION_EXAMPLE.md
- **What's the pattern?** → LEGACY_METRICS_MIGRATION_GUIDE.md
- **Quick reference?** → MIGRATION_CHECKLIST.md
- **Specific example?** → MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
- **Existing code?** → src/evidently/metrics/{regression,classification}.py

---

## Issue Resolution Summary

**Issue #1805**: "Certain older 'legacy' metrics don't currently work with the new Report API and need to be ported"

**Status**: RESOLVABLE using existing `LegacyMetricCalculation` pattern

**Effort**: Moderate (8-12 hours for all regression metrics)

**Impact**: Users can access regression analysis metrics through modern Report API

**Approach**: Bridge pattern - wrap legacy calculations with new metric interface

**Key Files**:
- src/evidently/metrics/regression.py (add implementations)
- src/evidently/metrics/__init__.py (export)
- tests/metrics/regression_performance/ (tests)

**Success Criteria**:
- All legacy regression metrics accessible through new Report API
- No changes to legacy system (backward compatible)
- Tests pass
- Documentation updated
