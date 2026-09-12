# Issue #1805 Resolution - Complete Documentation Index

**GitHub Issue**: #1805  
**Title**: Legacy metrics to new Report API  
**Status**: RESOLVABLE (documented solution provided)  
**Created**: Jan 23, 2026

---

## Quick Start (5 minutes)

1. **Read**: [ISSUE_1805_RESOLUTION_SUMMARY.md](ISSUE_1805_RESOLUTION_SUMMARY.md) - Overview and next steps
2. **Understand**: [ARCHITECTURE_AND_REFERENCE.md](ARCHITECTURE_AND_REFERENCE.md) - System design and patterns
3. **Start Coding**: [MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md) - Template and checklist

---

## Documentation Files

### For Getting Started

#### 1. **[ISSUE_1805_RESOLUTION_SUMMARY.md](ISSUE_1805_RESOLUTION_SUMMARY.md)** ⭐ START HERE
   - **What**: Overview of the problem and solution
   - **Why**: Understand the issue and approach
   - **How**: Step-by-step implementation guide
   - **Time**: 10-15 minutes
   - **Best for**: First-time readers, project managers

### For Understanding Design

#### 2. **[ARCHITECTURE_AND_REFERENCE.md](ARCHITECTURE_AND_REFERENCE.md)**
   - **What**: System architecture and data flows
   - **Why**: Understand how components interact
   - **How**: ASCII diagrams and class hierarchies
   - **Time**: 15-20 minutes
   - **Best for**: Understanding system design, troubleshooting

#### 3. **[LEGACY_METRICS_MIGRATION_GUIDE.md](LEGACY_METRICS_MIGRATION_GUIDE.md)**
   - **What**: Comprehensive technical migration guide
   - **Why**: Detailed explanation of the pattern and approach
   - **How**: Concepts, patterns, and working examples
   - **Time**: 20-30 minutes
   - **Best for**: Learning the full pattern, reference material

### For Implementation

#### 4. **[MIGRATION_CHECKLIST.md](MIGRATION_CHECKLIST.md)** ⭐ USE DURING CODING
   - **What**: Quick reference checklist and template
   - **Why**: Keep track of implementation steps
   - **How**: Checkboxes, templates, common patterns
   - **Time**: Referenced while coding
   - **Best for**: Step-by-step implementation, validation

#### 5. **[MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py](MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py)**
   - **What**: Detailed code example with documentation
   - **Why**: See actual implementation with explanation
   - **How**: Annotated Python code with multiple examples
   - **Time**: 10-20 minutes to understand
   - **Best for**: Learning from concrete example, code reference

#### 6. **[COMPLETE_IMPLEMENTATION_EXAMPLE.md](COMPLETE_IMPLEMENTATION_EXAMPLE.md)** ⭐ COPY AND USE
   - **What**: Production-ready, copy-paste implementation
   - **Why**: Ready-to-integrate three metrics with full tests
   - **How**: Complete code + full test suite
   - **Time**: 30-60 minutes to implement and test
   - **Best for**: Quickest path to working implementation

---

## Implementation Roadmap

### Phase 1: Preparation (30 minutes)
1. ✓ Read ISSUE_1805_RESOLUTION_SUMMARY.md
2. ✓ Read ARCHITECTURE_AND_REFERENCE.md
3. ✓ Understand the LegacyMetricCalculation pattern
4. ✓ Review existing examples in src/evidently/metrics/regression.py

### Phase 2: Implementation (Pick a Metric)
1. Choose a metric from the list (Priority 1 recommended)
2. Use COMPLETE_IMPLEMENTATION_EXAMPLE.md as a template
3. Reference MIGRATION_CHECKLIST.md while coding
4. Consult MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py for details

### Phase 3: Testing (30 minutes per metric)
1. Run metric instantiation tests
2. Run integration tests with Report
3. Verify with and without reference data
4. Check that widgets render correctly

### Phase 4: Submission
1. Create PR with metric migration
2. Run all tests
3. Update documentation if needed
4. Get review and merge

### Phase 5: Iteration
Repeat Phases 2-4 for next metric

---

## Core Concepts Reference

### The LegacyMetricCalculation Bridge Pattern

```
┌────────────────────────────────────────────────────────┐
│                USER CODE (NEW API)                     │
│  from evidently.metrics import RegressionErrorBiasTable│
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│           NEW METRIC CLASS (Interface)                  │
│     RegressionErrorBiasTable(SingleValueRegressionMetric)│
│             columns, top_error, etc.                    │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│     CALCULATION CLASS (Adapter/Bridge)                  │
│  RegressionErrorBiasTableCalculation(                   │
│      LegacyMetricCalculation[...]                       │
│  )                                                      │
│  ├─ legacy_metric() → Maps to legacy implementation     │
│  ├─ calculate_value() → Transforms results              │
│  └─ display_name() → UI text                            │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│      LEGACY METRIC (Implementation/Calculation)         │
│    LegacyRegressionErrorBiasTable                       │
│    - Actual calculation logic (unchanged)               │
│    - Error bias analysis                                │
│    - Visualization rendering                           │
└────────────────────┬─────────────────────────────────────┘
                     │
┌────────────────────▼─────────────────────────────────────┐
│            REPORT OUTPUT (Results)                      │
│  SingleValue + HTML widgets + metadata                  │
└─────────────────────────────────────────────────────────┘
```

### 3-Method Implementation

Every `LegacyMetricCalculation` subclass needs:

```python
def legacy_metric(self) -> LegacyMetricType:
    """Map new metric parameters to legacy metric constructor."""
    return LegacyMetricType(
        param1=self.metric.param1,
        param2=self.metric.param2,
    )

def calculate_value(self, context, legacy_result, render) -> ResultType:
    """Extract/transform legacy result into new format."""
    return self.result(computed_value)

def display_name(self) -> str:
    """Human-readable name for UI."""
    return "Metric Display Name"
```

### Key Files

- **New Metrics**: `src/evidently/metrics/regression.py`
- **Bridge Classes**: `src/evidently/metrics/_legacy.py`
- **Exports**: `src/evidently/metrics/__init__.py`
- **Legacy Reference**: `src/evidently/legacy/metrics/regression_performance/`
- **Tests**: `tests/metrics/regression_performance/`

---

## Metrics to Migrate (Priority Order)

### ⭐⭐⭐ Priority 1 (HIGH VALUE)
- [ ] **RegressionErrorBiasTable** (error bias by feature)
- [ ] **RegressionPredictedVsActualScatter** (scatter plot)
- [ ] **RegressionErrorDistribution** (error histogram)

### ⭐⭐ Priority 2 (MEDIUM VALUE)
- [ ] **RegressionErrorPlot** (error timeline)
- [ ] **RegressionPredictedVsActualPlot** (actual/pred timeline)
- [ ] **RegressionAbsPercentageErrorPlot** (% error viz)

### ⭐ Priority 3 (LOWER VALUE)
- [ ] **RegressionErrorNormality** (statistical test)
- [ ] **RegressionTopErrorMetric** (ranking)

---

## Tools and Templates

### Copy-Paste Templates

#### Template 1: Basic Metric
```python
class NewMetric(SingleValueRegressionMetric):
    """Your docstring here."""
    param1: Type = default
```

#### Template 2: Basic Calculation
```python
class NewMetricCalculation(
    LegacyMetricCalculation[
        SingleValue,
        NewMetric,
        LegacyNewMetricResults,
        LegacyNewMetric,
    ]
):
    def legacy_metric(self):
        return LegacyNewMetric(param1=self.metric.param1)
    
    def calculate_value(self, context, legacy_result, render):
        return self.result(value)
    
    def display_name(self):
        return "Display Name"
```

#### Template 3: Export
```python
# In __init__.py
from .regression import NewMetric
__all__ = [..., "NewMetric", ...]
```

### Working Examples

- **Code**: MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
- **Tests**: COMPLETE_IMPLEMENTATION_EXAMPLE.md (test section)
- **Real Code**: src/evidently/metrics/regression.py (existing metrics)

---

## Common Patterns and Solutions

### Pattern 1: Simple Scalar Result
```python
def calculate_value(self, context, legacy_result, render):
    return self.result(legacy_result.some_value)
```

### Pattern 2: With Reference Data
```python
def calculate_value(self, context, legacy_result, render):
    current = self.result(legacy_result.current.value)
    reference = None
    if legacy_result.reference:
        reference = self.result(legacy_result.reference.value)
    return current, reference
```

### Pattern 3: Multi-Task Regression
```python
def task_name(self) -> str:
    return self.metric.regression_name

def _gen_input_data(self, context, task_name):
    return _gen_regression_input_data(context, task_name)
```

### Pattern 4: Preserving Widgets
The legacy renderer's widgets are automatically preserved by the base class.

---

## Troubleshooting Guide

| Problem | Cause | Solution |
|---------|-------|----------|
| Import error | Wrong import path | Check correct module in legacy |
| MetricCalculation not found | Missing subclass | Inherit from LegacyMetricCalculation |
| Result is None | calculate_value() returns None | Check return statement |
| Widgets missing | Not handling legacy render | render parameter passed in calculate() |
| Reference not working | Not returning tuple | Return (current, reference) tuple |
| Task name not recognized | task_name() override missing | Override task_name() method |
| Column mapping lost | Custom data gen needed | Override _gen_input_data() |

---

## Quality Checklist

Before submitting a PR:

- [ ] Metric imports without error
- [ ] Can instantiate with default parameters
- [ ] Can instantiate with custom parameters
- [ ] Works in Report without error
- [ ] Results are accessible via snapshot
- [ ] Tests pass (new + existing)
- [ ] No regressions in other tests
- [ ] Docstrings complete
- [ ] Parameter documentation clear
- [ ] Example usage included

---

## Learning Path

### Beginner (Want Quick Overview)
1. Read: ISSUE_1805_RESOLUTION_SUMMARY.md (10 min)
2. Skim: ARCHITECTURE_AND_REFERENCE.md (10 min)
3. Review: MIGRATION_CHECKLIST.md quick reference (5 min)
4. **Total: 25 minutes**

### Intermediate (Want to Understand Details)
1. Read: ISSUE_1805_RESOLUTION_SUMMARY.md (10 min)
2. Read: ARCHITECTURE_AND_REFERENCE.md (20 min)
3. Read: LEGACY_METRICS_MIGRATION_GUIDE.md (25 min)
4. Review: MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py (15 min)
5. **Total: 70 minutes**

### Advanced (Ready to Implement)
1. Skim: All documentation (30 min)
2. Use: COMPLETE_IMPLEMENTATION_EXAMPLE.md as template
3. Reference: MIGRATION_CHECKLIST.md while coding
4. Code: Follow 3-method pattern
5. Test: Run tests + manual verification
6. **Total: 1-2 hours per metric**

---

## Issue Resolution Summary

**Problem**: Legacy regression metrics incompatible with new Report API

**Root Cause**: Old `Metric` base class vs. new `MetricCalculation` base class

**Solution**: Use `LegacyMetricCalculation` wrapper pattern (already in codebase)

**Metrics Affected**: 8+ legacy regression visualization metrics

**Implementation Pattern**:
1. New metric class (interface) - defines user-facing API
2. Calculation class (4 methods) - bridges old and new
3. Export - register with system
4. Test - verify functionality

**Effort**: 
- Single metric: 30-60 minutes
- All regression metrics: 8-12 hours

**Backward Compatibility**: ✓ Fully maintained (no breaking changes)

**Status**: Ready to implement

---

## Document Map

```
ISSUE_1805_RESOLUTION_SUMMARY.md ⭐ START HERE
    ├─ Problem overview
    ├─ Solution pattern
    └─ Implementation steps

ARCHITECTURE_AND_REFERENCE.md
    ├─ System design diagrams
    ├─ Data flows
    ├─ Class hierarchies
    └─ File locations

LEGACY_METRICS_MIGRATION_GUIDE.md
    ├─ Detailed explanation
    ├─ Current architecture
    ├─ Migration pattern
    └─ Working examples

MIGRATION_CHECKLIST.md ⭐ USE WHILE CODING
    ├─ Quick start
    ├─ Templates
    ├─ Patterns
    ├─ Troubleshooting
    └─ Checklist

MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
    ├─ Detailed code example
    ├─ Multiple approaches
    ├─ Usage examples
    └─ Test patterns

COMPLETE_IMPLEMENTATION_EXAMPLE.md ⭐ COPY-PASTE READY
    ├─ Production ready code
    ├─ Two metric examples
    ├─ Full test suite
    └─ Integration tests

THIS FILE: INDEX
    ├─ Navigation guide
    ├─ Learning paths
    ├─ Quick reference
    └─ Document map
```

---

## Next Steps

1. **Read** ISSUE_1805_RESOLUTION_SUMMARY.md (establishes context)
2. **Understand** ARCHITECTURE_AND_REFERENCE.md (grasps design)
3. **Choose** a Priority 1 metric from the list
4. **Reference** COMPLETE_IMPLEMENTATION_EXAMPLE.md code
5. **Follow** MIGRATION_CHECKLIST.md while implementing
6. **Test** using provided test patterns
7. **Submit** PR for review
8. **Iterate** to next metric

---

## Key Takeaways

✓ **Pattern exists** - `LegacyMetricCalculation` is the bridge  
✓ **Examples work** - MAE, RMSE already use same pattern  
✓ **Simple to implement** - 3 methods + export  
✓ **No rewrites needed** - Legacy code unchanged  
✓ **Tests provided** - Templates included  
✓ **Backward compatible** - No breaking changes  
✓ **Well documented** - Comprehensive guides included  

---

## Support Resources

- **While learning**: Read LEGACY_METRICS_MIGRATION_GUIDE.md
- **While coding**: Follow MIGRATION_CHECKLIST.md template
- **When stuck**: Check MIGRATION_EXAMPLE_ERROR_BIAS_TABLE.py
- **For testing**: Use COMPLETE_IMPLEMENTATION_EXAMPLE.md patterns
- **For reference**: Check ARCHITECTURE_AND_REFERENCE.md

---

**Status**: Ready to implement  
**Effort**: Low to moderate  
**Impact**: High value feature  
**Complexity**: Medium  
**Risk**: Low (no breaking changes)  

**Estimated Timeline**:
- Single metric: 1-2 hours
- Complete set: 1-2 days (with testing)
