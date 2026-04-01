# Legacy Metrics Migration - Quick Reference Checklist

## Issue: #1805 - Legacy metrics to new Report API

**Problem**: Legacy regression metrics (RegressionErrorBiasTable, RegressionPredictedVsActualScatter, etc.) don't work with the new Report API.

**Solution**: Create wrapper classes using `LegacyMetricCalculation` pattern to bridge old and new metrics.

---

## Quick Start (5-step process)

### 1. Identify the Metric to Migrate
Find the legacy metric in `src/evidently/legacy/metrics/`

Example: `src/evidently/legacy/metrics/regression_performance/error_bias_table.py`
```python
class RegressionErrorBiasTable(UsesRawDataMixin, Metric[RegressionErrorBiasTableResults]):
    ...
```

### 2. Create New Metric Class  
In `src/evidently/metrics/regression.py`, add:

```python
class RegressionErrorBiasTable(SingleValueMetric):
    """New Report API metric."""
    regression_name: str = "default"
    columns: Optional[List[str]] = None
    top_error: Optional[float] = None
```

**Choose the right base class:**
- `SingleValueMetric` → Returns a single number
- `MeanStdMetric` → Returns mean ± std dev  
- Custom `MetricResult` → For complex structures

### 3. Create Calculation Wrapper
In `src/evidently/metrics/regression.py`, add:

```python
class RegressionErrorBiasTableCalculation(
    LegacyMetricCalculation[
        SingleValue,                                    # New result type
        RegressionErrorBiasTable,                      # New metric
        RegressionErrorBiasTableResults,               # Legacy result
        LegacyRegressionErrorBiasTable,                # Legacy metric
    ],
):
    def legacy_metric(self) -> LegacyRegressionErrorBiasTable:
        return LegacyRegressionErrorBiasTable(
            columns=self.metric.columns,
            top_error=self.metric.top_error,
        )
    
    def calculate_value(self, context, legacy_result, render):
        # Extract/transform result
        value = len(legacy_result.error_bias or {})
        return self.result(value)
    
    def display_name(self) -> str:
        return "Regression Error Bias Table"
```

### 4. Override Data Generation (if task-specific)
Add to calculation class if regression task selection is needed:

```python
def task_name(self) -> str:
    return self.metric.regression_name

def _gen_input_data(self, context: Context, task_name: Optional[str]) -> InputData:
    return _gen_regression_input_data(context, task_name)
```

### 5. Export and Test
In `src/evidently/metrics/__init__.py`:
```python
from .regression import RegressionErrorBiasTable
__all__ = [..., "RegressionErrorBiasTable", ...]
```

Test in `tests/metrics/`:
```python
from evidently import Report
from evidently.metrics import RegressionErrorBiasTable

report = Report([RegressionErrorBiasTable()])
snapshot = report.run(current_dataset, reference_dataset)
assert snapshot.get_metric_result("RegressionErrorBiasTable") is not None
```

---

## Metrics Needing Migration

**Priority 1 (Most Used)**
- [ ] `RegressionErrorBiasTable` - Error bias by feature
- [ ] `RegressionPredictedVsActualScatter` - Predicted vs actual plot
- [ ] `RegressionErrorDistribution` - Error distribution viz

**Priority 2 (Visualization)**
- [ ] `RegressionErrorPlot` - Errors over time
- [ ] `RegressionPredictedVsActualPlot` - Predicted/actual timeline
- [ ] `RegressionAbsPercentageErrorPlot` - Percentage error viz

**Priority 3 (Analysis)**
- [ ] `RegressionErrorNormality` - Normality test
- [ ] `RegressionTopErrorMetric` - Top errors analysis

---

## Key Concepts

### Result Types

| Type | Usage | Example |
|------|-------|---------|
| `SingleValue` | Single metric number | MAE value |
| `MeanStdValue` | Mean + std dev | Mean Error ± Std |
| `DataframeValue` | Table result | Feature importance |
| Custom | Complex structure | Error bias by feature |

### Calculation Flow

```
New Report API
    ↓
RegressionErrorBiasTable (metric config)
    ↓
RegressionErrorBiasTableCalculation.calculate()
    ↓
→ context.get_legacy_metric(LegacyRegressionErrorBiasTable)
    ↓
Legacy Calculation (heavy lifting)
    ↓
RegressionErrorBiasTableResults (legacy result)
    ↓
calculate_value() transforms → SingleValue
    ↓
Report output
```

### Task Names

Use for regression task selection:
```python
def task_name(self) -> str:
    return self.metric.regression_name  # Maps to Definition.regressions[name]
```

---

## Common Patterns

### Pattern 1: Simple Scalar Extraction
```python
def calculate_value(self, context, legacy_result, render):
    value = legacy_result.some_field
    return self.result(value)
```

### Pattern 2: Multiple Values (Mean + Std)
```python
def calculate_value(self, context, legacy_result, render):
    return (
        self.result(legacy_result.current.mean, legacy_result.current.std),
        self.result(legacy_result.reference.mean, legacy_result.reference.std) 
        if legacy_result.reference else None
    )
```

### Pattern 3: With Reference Data
```python
def calculate_value(self, context, legacy_result, render) -> Tuple[TResult, Optional[TResult]]:
    current = self.result(legacy_result.current.value)
    reference = None
    if legacy_result.reference is not None:
        reference = self.result(legacy_result.reference.value)
    return current, reference
```

### Pattern 4: Additional Widgets
```python
def get_additional_widgets(self, context: Context) -> List[BaseWidgetInfo]:
    # Return extra visualization widgets to include in report
    return [custom_widget1, custom_widget2]
```

---

## Troubleshooting

### Issue: "AttributeError: 'RegressionErrorBiasTable' not found"
**Solution**: Check import. Use legacy class in `legacy_metric()`, new class elsewhere.

### Issue: Reference data not handled
**Check**:
- Return tuple `(current, reference)` from `calculate_value()`
- Handle `None` reference case

### Issue: Column mapping lost
**Check**:
- Override `_gen_input_data()` to preserve column mapping
- Use `_gen_regression_input_data()` helper

### Issue: Widgets not rendering
**Check**:
- `render` parameter contains legacy widgets
- Set `self.result(...).widget = render` if needed
- Don't forget to return widgets from `get_additional_widgets()`

### Issue: Task name not working
**Check**:
- Override `task_name()` → returns `self.metric.regression_name`
- Register regression in `DataDefinition`
- Use `_gen_regression_input_data(context, task_name)`

---

## File Locations

| File | Purpose |
|------|---------|
| `src/evidently/metrics/regression.py` | Add new metric + calculation |
| `src/evidently/metrics/__init__.py` | Export the metric |
| `src/evidently/metrics/_legacy.py` | Base `LegacyMetricCalculation` |
| `src/evidently/legacy/metrics/regression_performance/*.py` | Legacy metric code (reference) |
| `tests/metrics/regression_performance/` | Add tests |
| `examples/cookbook/metrics.ipynb` | Update examples |

---

## Template: Implementation Checklist

```python
# In src/evidently/metrics/regression.py

# STEP 1: Import requirements
from evidently.legacy.metrics.regression_performance.{metric_file} import (
    {LegacyMetricClass},
    {LegacyMetricClass}Results,
)

# STEP 2: New metric class
class {NewMetricClass}({MetricBase}):
    """Documentation."""
    param1: Type = default
    param2: Type = default

# STEP 3: Calculation wrapper
class {NewMetricClass}Calculation(
    LegacyMetricCalculation[
        ResultType,                 # SingleValue, MeanStdValue, DataframeValue, etc.
        {NewMetricClass},          # This metric class
        {LegacyMetricClass}Results, # Legacy result type
        {LegacyMetricClass},       # Legacy metric class
    ],
):
    def legacy_metric(self) -> {LegacyMetricClass}:
        """Map new params -> legacy constructor."""
        return {LegacyMetricClass}(
            param1=self.metric.param1,
            param2=self.metric.param2,
        )
    
    def calculate_value(self, context, legacy_result, render) -> ResultType:
        """Extract/transform result."""
        return self.result(...)
    
    def display_name(self) -> str:
        return "Human Readable Name"
    
    # Optional:
    def task_name(self) -> str:
        return self.metric.{task_field}
    
    def _gen_input_data(self, context, task_name):
        return _gen_regression_input_data(context, task_name)
    
    def get_additional_widgets(self, context) -> List[BaseWidgetInfo]:
        return []
```

---

## Validation

After implementation, verify:

1. **Imports work**
   ```bash
   from evidently.metrics import RegressionErrorBiasTable  ✓
   ```

2. **Metric instantiation**
   ```python
   RegressionErrorBiasTable(columns=['feature1'])  ✓
   ```

3. **Report creation**
   ```python
   Report([RegressionErrorBiasTable()])  ✓
   ```

4. **Calculation runs**
   ```python
   snapshot = report.run(current_dataset, reference_dataset)  ✓
   ```

5. **Result accessible**
   ```python
   result = snapshot.get_metric_result('RegressionErrorBiasTable')
   assert result is not None  ✓
   ```

6. **Tests pass**
   ```bash
   pytest tests/metrics/regression_performance/test_error_bias_table.py  ✓
   ```

---

## Resources

- **Full Guide**: See LEGACY_METRICS_MIGRATION_GUIDE.md
- **Code Example**: See MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
- **Existing Migrations**: `src/evidently/metrics/regression.py` (MAE, RMSE, etc.)
- **Base Class**: `src/evidently/metrics/_legacy.py` (LegacyMetricCalculation)
- **API**: `src/evidently/core/report.py` (Context, Report)

---

**Issue Status**: 
- [ ] Identify blocking legacy metrics
- [ ] Create migration issues/PRs for each metric  
- [ ] Implement wrapper classes
- [ ] Add comprehensive tests
- [ ] Update documentation
- [ ] Close #1805

**Estimated Effort**: 
- Simple metric (scalar): 30-45 min
- Complex metric (visualization): 1-2 hours
- Full regression metrics set: 8-12 hours
