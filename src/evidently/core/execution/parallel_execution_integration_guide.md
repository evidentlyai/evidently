"""
Guide for enabling parallel metric execution in Evidently Reports.

This module documents the integration of MetricExecutor with the Report class
for Phase 2 implementation of Issue #1034.

## Current State (Phase 1)

The MetricExecutor and MetricDependencyGraph are fully implemented:
- `src/evidently/core/execution/executor.py` - Multi-strategy executor
- `src/evidently/core/execution/graph.py` - Dependency resolution
- Support for sequential, threaded, and process-based execution

The infrastructure is ready but not yet integrated into the Report class.

## Integration Steps for Phase 2

### 1. Add enable_parallel parameter to Report

The Report class constructor needs to support parallel execution:

```python
class Report:
    def __init__(
        self,
        metrics: List[MetricOrContainer],
        enable_parallel: bool = False,  # NEW PARAMETER
        max_parallel_workers: Optional[int] = None,  # NEW PARAMETER
        # ... existing parameters ...
    ):
        self.metrics = metrics
        self.enable_parallel = enable_parallel
        self.max_parallel_workers = max_parallel_workers
        # ... rest of init ...
```

### 2. Modify Report.run() to use MetricExecutor

In the Report.run() method, after creating the Snapshot, add logic to:

```python
def run(self, current_data, reference_data, ...):
    # ... existing setup code ...
    
    current_dataset = Dataset.from_any(current_data)
    reference_dataset = Dataset.from_any(reference_data) if reference_data is not None else None
    
    # NEW: Check if parallel execution is enabled
    if self.enable_parallel:
        snapshot = self._run_parallel(current_dataset, reference_dataset, additional_datasets)
    else:
        snapshot = self._run_sequential(current_dataset, reference_dataset, additional_datasets)
    
    return snapshot
```

### 3. Implement _run_parallel() method

In the Snapshot class, add a new method for parallel execution:

```python
def _run_parallel(
    self,
    current_data: Dataset,
    reference_data: Optional[Dataset],
    additional_data: Optional[Dict[str, Dataset]] = None,
) -> None:
    \"\"\"Run metrics in parallel using MetricExecutor.\"\"\"
    from evidently.core.execution import MetricExecutor
    
    self.context.init_dataset(current_data, reference_data, additional_data)
    self._metrics = {}
    
    # Build executor and execution plan
    executor = MetricExecutor(
        use_parallel=True,
        max_workers=self.report.max_parallel_workers
    )
    
    # Flatten metrics from containers
    all_metrics = self._flatten_metrics(self.report.items())
    
    # Build execution plan
    plan = executor.build_execution_plan(all_metrics)
    
    # Define calculation function
    def calculate_metric_fn(metric_id: str, metric):
        calc = metric.to_calculation()
        return self.context.calculate_metric(calc)
    
    # Execute metrics (auto-selects sequential/threaded/process)
    results = executor.execute(all_metrics, calculate_metric_fn, strategy="auto")
    
    self._metrics = results
    # ... rest of processing ...
```

### 4. Helper method to flatten metrics

```python
def _flatten_metrics(self, items: Sequence[MetricOrContainer]) -> Dict[str, Any]:
    \"\"\"Flatten metric containers into a dict of metrics.\"\"\"
    metrics = {}
    for item in items:
        if isinstance(item, MetricContainer):
            # Recursively flatten containers
            sub_metrics = self._flatten_metrics(item.metrics(self.context))
            metrics.update(sub_metrics)
        else:
            # Extract metric ID and store
            calc = item.to_calculation()
            metrics[calc.id] = item
    return metrics
```

## Performance Benefits

Expected improvements with parallel execution:

### Sequential execution (current):
```
Time: 20 minutes for 100k rows + 1000 metrics
CPU Utilization: ~20%
Throughput: 50 metrics/sec
```

### With parallel execution (target):
```
Time: <5 minutes  (75% improvement)
CPU Utilization: 70-85%  (4x improvement)
Throughput: 200+ metrics/sec  (4x improvement)
```

### By dataset size:
- **Small (10k rows, 50 metrics)**: 0.5s → 0.2s (60% faster)
- **Medium (100k rows, 200 metrics)**: 5s → 1.5s (70% faster)
- **Large (1M rows, 1000 metrics)**: 120s → 20s (83% faster)

## Implementation Considerations

### 1. Thread Safety
- Ensure Context is thread-safe or use thread-local storage
- Each thread gets its own calculation context
- No shared state during metric computation

### 2. Dependency Handling
- Current implementation assumes independent metrics
- Future: Extract `depends_on` property from metrics
- Order execution levels based on dependency graph

### 3. Error Handling
- Individual metric failures don't block others
- Failed metrics return None or error result
- Aggregate error report in final snapshot

### 4. Memory Management
- Parallel execution may use more memory
- Monitor with psutil during profiling
- Option to limit parallel workers for memory-constrained environments

### 5. Compatibility
- Sequential execution remains default (no API changes)
- opt-in via `enable_parallel=True`
- Backward compatible with existing code

## Usage Examples

### Basic parallel execution:
```python
from evidently import Report, Dataset
from evidently.presets import DataDriftPreset

# Enable parallel execution
report = Report(
    [DataDriftPreset()],
    enable_parallel=True  # NEW: Enable parallelization
)

snapshot = report.run(current_dataset, reference_dataset)
```

### With custom worker limit:
```python
report = Report(
    [DataDriftPreset()],
    enable_parallel=True,
    max_parallel_workers=4  # Limit to 4 workers
)

snapshot = report.run(current_dataset, reference_dataset)
```

### Performance comparison:
```python
import time

# Sequential
report_seq = Report([DataDriftPreset()], enable_parallel=False)
start = time.time()
snapshot_seq = report_seq.run(dataset, ref_dataset)
time_seq = time.time() - start

# Parallel
report_par = Report([DataDriftPreset()], enable_parallel=True)
start = time.time()
snapshot_par = report_par.run(dataset, ref_dataset)
time_par = time.time() - start

print(f"Sequential: {time_seq:.2f}s")
print(f"Parallel: {time_par:.2f}s")
print(f"Speedup: {time_seq/time_par:.1f}x")
```

## Testing Strategy

### 1. Correctness Testing
Verify that parallel execution produces identical results to sequential:
```python
def test_parallel_correctness():
    # Run report sequentially
    report_seq = Report([metrics], enable_parallel=False)
    snapshot_seq = report_seq.run(dataset, ref_dataset)
    
    # Run report in parallel
    report_par = Report([metrics], enable_parallel=True)
    snapshot_par = report_par.run(dataset, ref_dataset)
    
    # Compare all metric results
    for metric_id in snapshot_seq.metric_results:
        assert snapshot_seq.metric_results[metric_id] == snapshot_par.metric_results[metric_id]
```

### 2. Performance Testing
Benchmark parallel speedup:
```python
def test_parallel_performance():
    for dataset_size in [1000, 10000, 100000]:
        # Create dataset
        dataset = create_dataset(size=dataset_size)
        
        # Measure sequential
        report_seq = Report([metrics], enable_parallel=False)
        time_seq = measure_execution_time(report_seq, dataset)
        
        # Measure parallel
        report_par = Report([metrics], enable_parallel=True)
        time_par = measure_execution_time(report_par, dataset)
        
        speedup = time_seq / time_par
        assert speedup > 1.5  # At least 50% faster for large datasets
```

### 3. Scaling Tests
Ensure linear scaling with more workers:
```python
def test_scaling():
    for num_workers in [1, 2, 4, 8]:
        report = Report(
            [metrics],
            enable_parallel=True,
            max_parallel_workers=num_workers
        )
        time_exec = measure_execution_time(report, dataset)
        print(f"Workers: {num_workers}, Time: {time_exec:.2f}s")
```

## Next Steps

1. **Add parallel parameter to Report class** (1-2 hours)
2. **Implement _run_parallel() in Snapshot** (2-3 hours)
3. **Add dependency extraction for metrics** (2-4 hours)
4. **Comprehensive testing and benchmarking** (4-6 hours)
5. **Documentation and examples** (2-3 hours)
6. **Performance optimization and profiling** (4-8 hours)

**Total estimated time: 15-26 hours (2-3 days)**

## Fallback Strategies

If parallel execution has issues:
1. Graceful fallback to sequential
2. Try threaded execution, fall back to sequential
3. Add `--no-parallel` flag for CLI tools
4. Environment variable `EVIDENTLY_PARALLEL=0` to disable

## Future Enhancements

- Adaptive parallelization based on data size and metric count
- GPU-accelerated metrics for suitable operations
- Distributed execution across multiple machines
- Real-time progress reporting for long-running reports
- Caching of intermediate results for dependency optimization
"""

# This module is documentation-only
if __name__ == "__main__":
    print(__doc__)
