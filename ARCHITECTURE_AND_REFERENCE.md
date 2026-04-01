# Issue #1805 Resolution - Architecture & Reference Document

## GitHub Issue #1805

**Title**: Legacy metrics to new Report API
**Status**: Open (Opened Jan 23, 2026)
**Problem**: Certain older "legacy" metrics (like RegressionErrorBiasTable, RegressionPredictedVsActualScatter, etc.) from the legacy API don't currently work with the new Report API.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  USER CODE (New Report API)                     │
│                                                                 │
│  from evidently import Report                                   │
│  from evidently.metrics import RegressionErrorBiasTable        │
│                                                                 |
│  report = Report([RegressionErrorBiasTable(columns=['age'])])  │
│  snapshot = report.run(current_dataset, reference_dataset)      │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│            NEW METRIC CLASSES (src/evidently/metrics/)           │
│                                                                 │
│  class RegressionErrorBiasTable(SingleValueRegressionMetric):   │
│      columns: Optional[List[str]] = None                        │
│      top_error: Optional[float] = None                          │
│      regression_name: str = "default"                           │
│                                                                  │
│  (User-facing API, just configuration, no calculation logic)    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│       CALCULATION WRAPPER (src/evidently/metrics/regression.py)  │
│                                                                 │
│  class RegressionErrorBiasTableCalculation(                     │
│      LegacyMetricCalculation[                                  │
│          SingleValue,                # New result type          │
│          RegressionErrorBiasTable,   # New metric               │
│          RegressionErrorBiasTableResults,  # Legacy result      │
│          LegacyRegressionErrorBiasTable,   # Legacy metric      │
│      ]                                                          │
│  ):                                                             │
│      def legacy_metric(self):                                   │
│          # Bridge to legacy implementation                      │
│          return LegacyRegressionErrorBiasTable(...)             │
│                                                                 │
│      def calculate_value(self, context, legacy_result, render): │
│          # Transform legacy result to new format                │
│          return self.result(...)                                │
│                                                                 │
│      def display_name(self) -> str:                             │
│          return "Regression Error Bias Table"                   │
│                                                                 │
│  (The bridge that adapts legacy to new system)                 │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│    LEGACY METRIC (src/evidently/legacy/metrics/regression_...)   │
│                                                                 │
│  class RegressionErrorBiasTable(UsesRawDataMixin, Metric[...]):  │
│      def calculate(self, data: InputData):                       │
│          # Complex calculation logic                            │
│          # Error bias analysis across features                  │
│          # Feature detection and visualization                  │
│          return RegressionErrorBiasTableResults(...)            │
│                                                                 │
│  (Original implementation, unchanged, reused via bridge)        │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    REPORT OUTPUT                                 │
│                                                                 │
│  snapshot.get_metric_result('RegressionErrorBiasTable')         │
│  → SingleValue                                                   │
│     ├─ current: 5.0 (number of features analyzed)              │
│     ├─ reference: 5.0 (optional)                               │
│     └─ widget: [HTML visualization from legacy renderer]       │
└─────────────────────────────────────────────────────────────────┘
```

## System Layers

```
┌──────────────────────────────────────────┐
│      New Report API (Main)               │
│   (src/evidently/core/report.py)         │
│                                          │
│  ├─ Report class                         │
│  ├─ Context class                        │
│  ├─ MetricCalculation base class         │
│  └─ Snapshot                             │
└──────────────────────────────────────────┘
            ▲
            │ uses
            │
┌──────────────────────────────────────────┐
│    Metric Adapter Layer                  │
│  (src/evidently/metrics/)                │
│                                          │
│  ├─ New metric classes API               │
│  ├─ Calculation implementations          │
│  ├─ LegacyMetricCalculation base         │
│  └─ Result type definitions              │
└──────────────────────────────────────────┘
            ▲
            │ delegates
            │
┌──────────────────────────────────────────┐
│    Legacy Metric Layer                   │
│  (src/evidently/legacy/metrics/)         │
│                                          │
│  ├─ Original metric implementations      │
│  ├─ Result classes                       │
│  ├─ Renderers (HTML widgets)             │
│  └─ Visualizations                       │
└──────────────────────────────────────────┘
            ▲
            │ processes
            │
┌──────────────────────────────────────────┐
│    Data Layer                            │
│  (src/evidently/legacy/base_metric.py)   │
│                                          │
│  ├─ InputData                            │
│  ├─ ColumnMapping                        │
│  ├─ Dataset definitions                  │
│  └─ Column utilities                     │
└──────────────────────────────────────────┘
```

## Data Flow Example

```
USER:
  from evidently import Report
  from evidently.metrics import RegressionErrorBiasTable
  
  metric = RegressionErrorBiasTable(columns=['age', 'income'])
  report = Report([metric])
  snapshot = report.run(current_dataset, reference_dataset)

SYSTEM:
  1. Report.__init__([RegressionErrorBiasTable(...)])
     └─ Stores metric instance

  2. report.run(current_dataset, reference_dataset)
     ├─ Creates Context
     ├─ Initializes datasets
     └─ For each metric:

  3. RegressionErrorBiasTableCalculation.calculate()
     ├─ Calls legacy_metric()
     │  └─ Returns LegacyRegressionErrorBiasTable(columns=['age', 'income'])
     │
     ├─ Calls context.get_legacy_metric(legacy_metric)
     │  └─ Executes LegacyRegressionErrorBiasTable.calculate(input_data)
     │
     ├─ Legacy calculation returns RegressionErrorBiasTableResults
     └─ Calls calculate_value(context, legacy_result, render)
        └─ Returns SingleValue(value=2.0)  # 2 features analyzed

  4. Result attached to snapshot
     └─ snapshot.get_metric_result('RegressionErrorBiasTable')
        → SingleValue(current=2.0, reference=2.0, widget=[...])

  5. User retrieves results
     └─ Can serialize, visualize, or export
```

## Class Inheritance Hierarchy

```
MetricCalculation (src/evidently/core/metric_types.py)
    │
    └─ LegacyMetricCalculation (src/evidently/metrics/_legacy.py)
        │
        ├─ LegacyRegressionMeanStdMetric
        │   │
        │   ├─ MeanErrorCalculation
        │   ├─ MAECalculation
        │   ├─ MAPECalculation
        │   └─ RMSECalculation
        │
        ├─ LegacyRegressionSingleValueMetric
        │   │
        │   ├─ R2ScoreCalculation
        │   ├─ AbsMaxErrorCalculation
        │   ├─ RegressionPredictedVsActualScatterCalculation  ← TO IMPLEMENT
        │   └─ RegressionErrorBiasTableCalculation  ← TO IMPLEMENT
        │
        └─ [Classification/Ranking similar patterns]


Metric (src/evidently/core/metric_types.py) 
    │
    ├─ SingleValueMetric
    │   │
    │   ├─ SingleValueRegressionMetric
    │   │   ├─ R2Score
    │   │   ├─ AbsMaxError
    │   │   ├─ RegressionPredictedVsActualScatter  ← TO IMPLEMENT
    │   │   └─ RegressionErrorBiasTable  ← TO IMPLEMENT
    │   │
    │   └─ [Other metric types]
    │
    └─ [Other metric base classes]


Legacy Metric (src/evidently/legacy/base_metric.py)
    │
    ├─ RegressionErrorBiasTable (legacy)
    │   (Used by: RegressionErrorBiasTableCalculation)
    │
    ├─ RegressionPredictedVsActualScatter (legacy)
    │   (Used by: RegressionPredictedVsActualScatterCalculation)
    │
    └─ [Other legacy metrics]
```

## Implementation Pattern Summary

### 3-Component Pattern

```
LEGACY METRIC (Existing)
    ├─ Calculation logic
    ├─ Result structure
    └─ HTML rendering

            ↓ Bridge via

NEW METRIC CLASS (Create)
    ├─ Parameter definition
    ├─ Docstring/metadata
    └─ User-facing interface

         + 

CALCULATION CLASS (Create)
    ├─ Instantiate legacy metric
    ├─ Transform results
    └─ Adapt interface
```

### Template Code

```python
# Step 1: New Metric
class NewMetric(SingleValueRegressionMetric):
    """Docstring and parameter definition."""
    param1: Type = default
    param2: Type = default
    regression_name: str = "default"

# Step 2: Calculation Bridge
class NewMetricCalculation(
    LegacyMetricCalculation[
        ResultType,           # SingleValue, MeanStdValue, etc.
        NewMetric,            # New metric class
        LegacyResultClass,    # Legacy result class
        LegacyMetricClass,    # Legacy metric class
    ]
):
    def legacy_metric(self):
        return LegacyMetricClass(
            param1=self.metric.param1,
            param2=self.metric.param2,
        )
    
    def calculate_value(self, context, legacy_result, render):
        # Extract/transform
        return self.result(value)
    
    def display_name(self):
        return "Display Name"
    
    # Optional:
    def task_name(self):
        return self.metric.regression_name
    
    def _gen_input_data(self, context, task_name):
        return _gen_regression_input_data(context, task_name)

# Step 3: Export
# In __init__.py:
# from .regression import NewMetric
# __all__ = [..., "NewMetric", ...]
```

## Metrics Requiring Migration

### Regression Metrics

From `src/evidently/legacy/metrics/regression_performance/`:

```
error_bias_table.py
    ├─ RegressionErrorBiasTable
    └─ RegressionErrorBiasTableResults

predicted_vs_actual.py
    ├─ RegressionPredictedVsActualScatter
    └─ RegressionPredictedVsActualScatterResults

predicted_and_actual_in_time.py
    ├─ RegressionPredictedVsActualPlot
    └─ RegressionPredictedVsActualPlotResults

error_in_time.py
    ├─ RegressionErrorPlot
    └─ RegressionErrorPlotResults

error_distribution.py
    ├─ RegressionErrorDistribution
    └─ RegressionErrorDistributionResults

error_normality.py
    ├─ RegressionErrorNormality
    └─ RegressionErrorNormalityResults

abs_perc_error_in_time.py
    ├─ RegressionAbsPercentageErrorPlot
    └─ RegressionAbsPercentageErrorPlotResults

top_error.py
    ├─ RegressionTopErrorMetric
    └─ RegressionTopErrorMetricResults
```

## Key Files Reference

```
src/evidently/
├─ core/
│   ├─ report.py
│   │   ├─ Report class
│   │   ├─ Context class
│   │   └─ Snapshot class
│   └─ metric_types.py
│       ├─ Metric base class
│       ├─ MetricCalculation base class
│       ├─ MetricResult types
│       ├─ SingleValue, MeanStdValue, DataframeValue
│       └─ Result type definitions
│
├─ metrics/
│   ├─ _legacy.py ⭐
│   │   └─ LegacyMetricCalculation (MAIN BRIDGE CLASS)
│   ├─ regression.py ⭐
│   │   ├─ Existing: MAE, RMSE, R2Score, etc.
│   │   └─ TO ADD: RegressionErrorBiasTable, RegressionPredictedVsActualScatter, etc.
│   ├─ classification.py
│   │   └─ Similar migration pattern (reference)
│   ├─ recsys.py
│   │   └─ Similar migration pattern (reference)
│   ├─ __init__.py ⭐
│   │   └─ Export new metrics here
│   └─ [other metric files]
│
└─ legacy/
    ├─ base_metric.py
    │   ├─ Metric class
    │   ├─ InputData class
    │   └─ MetricResult base class
    ├─ metrics/
    │   ├─ regression_performance/ ⭐
    │   │   ├─ error_bias_table.py (REFERENCE)
    │   │   ├─ predicted_vs_actual.py (REFERENCE)
    │   │   ├─ error_in_time.py (REFERENCE)
    │   │   ├─ error_distribution.py (REFERENCE)
    │   │   ├─ error_normality.py (REFERENCE)
    │   │   ├─ abs_perc_error_in_time.py (REFERENCE)
    │   │   └─ top_error.py (REFERENCE)
    │   │
    │   ├─ classification_performance/
    │   │   └─ [similar structure]
    │   │
    │   └─ other groups
    │
    └─ utils/
        ├─ data_preprocessing.py
        ├─ data_operations.py
        └─ [support utilities]

tests/
├─ metrics/
│   ├─ regression_performance/
│   │   ├─ test_error_bias_table.py (update if needed)
│   │   ├─ test_predicted_vs_actual.py (update if needed)
│   │   └─ test_legacy_migrations.py ⭐ (CREATE NEW)
│   │
│   └─ [other test files]
│
└─ [other test directories]
```

⭐ = Files to modify or create

## Important Type Unions

```python
# Result type options (from evidently.core.metric_types)
SingleValue      # Metric[float]
MeanStdValue     # Metric[mean: float, std: float]
DataframeValue   # Metric[pd.DataFrame]

# Return patterns
def calculate_value(...) -> SingleValue:
    return self.result(value)

def calculate_value(...) -> Tuple[SingleValue, Optional[SingleValue]]:
    return (
        self.result(current_value),
        self.result(reference_value) if ref else None
    )

def calculate_value(...) -> DataframeValue:
    return self.result(df=dataframe)
```

## Testing Pattern

```python
# tests/metrics/regression_performance/test_legacy_migrations.py

def test_metric_instantiation():
    metric = RegressionErrorBiasTable()
    assert metric is not None

def test_metric_in_report(regression_data):
    current, reference = regression_data
    report = Report([RegressionErrorBiasTable()])
    snapshot = report.run(current, reference)
    assert snapshot is not None
    
def test_metric_result_accessible(regression_data):
    current, reference = regression_data
    report = Report([RegressionErrorBiasTable()])
    snapshot = report.run(current, reference)
    result = snapshot.get_metric_result("RegressionErrorBiasTable")
    assert result is not None
    assert result.current is not None
```

## Completion Checklist for Each Metric

- [ ] New metric class created in src/evidently/metrics/regression.py
- [ ] Calculation class created in src/evidently/metrics/regression.py  
- [ ] Metric exported in src/evidently/metrics/__init__.py
- [ ] `legacy_metric()` method maps parameters correctly
- [ ] `calculate_value()` method transforms result correctly
- [ ] `display_name()` method returns proper string
- [ ] `task_name()` override added if needed
- [ ] `_gen_input_data()` override added if needed
- [ ] `get_additional_widgets()` override added if needed
- [ ] Test file created in tests/metrics/
- [ ] Basic instantiation test passes
- [ ] Integration test with Report passes
- [ ] Reference data handling tested
- [ ] No breaking changes to existing tests
- [ ] Docstrings complete
- [ ] PR submitted and reviewed

---

## Summary

**Issue**: Legacy metrics incompatible with new Report API

**Solution**: Use `LegacyMetricCalculation` bridge pattern

**Pattern**: 
1. Create new metric class (interface)
2. Create calculation class (adapter)
3. Export and test

**Effort**: 8-12 hours for all regression metrics

**Files**: Primarily `src/evidently/metrics/regression.py` and tests

**Backward Compatibility**: ✓ (unchanged, fully maintained)

**Reference Documentation**: 
- LEGACY_METRICS_MIGRATION_GUIDE.md  
- MIGRATION_CHECKLIST.md
- COMPLETE_IMPLEMENTATION_EXAMPLE.md
- MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
- ISSUE_1805_RESOLUTION_SUMMARY.md
