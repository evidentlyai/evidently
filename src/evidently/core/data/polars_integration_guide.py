"""
Examples and guidelines for integrating Polars support into metrics.

This module demonstrates best practices for creating metrics that leverage Polars
for improved performance on large datasets. The patterns shown here can be applied
to existing metrics.

Key Example: How to update a metric calculation to use Polars
============================================================

Before (Pandas-only):
```python
class MeanValueCalculation(StatisticsCalculation[MeanValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        return column.data.mean()
```

After (Polars-compatible using lazy evaluation):
```python
from evidently.core.data import polars_optimized, to_polars_lazy, to_pandas_safe

@polars_optimized(enabled=True, lazy_eval=True)
class MeanValueCalculation(StatisticsCalculation[MeanValue]):
    def calculate_value(self, column: DatasetColumn) -> Union[float, int]:
        # Get the processor (added by decorator)
        processor = self.get_polars_processor()

        # Option 1: Use lazy evaluation for better performance
        if processor.polars_enabled:
            # Convert to Polars lazy frame
            series_data = column.data
            df = processor.to_polars(pd.DataFrame({column.name: series_data}), lazy=True)
            result = df.select(pl.col(column.name).mean()).collect()[0, 0]
            return result

        # Fallback: Pandas (and automatic if Polars not available)
        return column.data.mean()
```

For more complex multi-column operations:
```python
@polars_optimized(enabled=True, lazy_eval=True)
class ValueDriftCalculation(SingleValueCalculation[ValueDrift]):
    def calculate(self, context: Context, current_data: Dataset, reference_data: Optional[Dataset]):
        processor = self.get_polars_processor()

        # Get current and reference as dataframes
        current_df = current_data.as_dataframe()
        reference_df = reference_data.as_dataframe()

        column = self.metric.column

        if processor.polars_enabled:
            # Convert to Polars for processing
            current_pl = processor.to_polars(current_df, lazy=True)
            reference_pl = processor.to_polars(reference_df, lazy=True)

            # Perform aggregations on Polars
            current_stats = current_pl.select([
                pl.col(column).mean().alias("mean"),
                pl.col(column).std().alias("std"),
                pl.col(column).count().alias("count"),
            ]).collect()

            reference_stats = reference_pl.select([
                pl.col(column).mean().alias("mean"),
                pl.col(column).std().alias("std"),
            ]).collect()

            # Continue with drift calculation...
        else:
            # Pandas-based calculation (existing logic)
            pass
```

Integration Steps
================

1. **Identify High-Impact Metrics**: Start with metrics that process large amounts of data
   - Drift metrics (operate on entire columns)
   - Aggregation metrics (group_by operations)
   - Correlation metrics (matrix operations)

2. **Add @polars_optimized Decorator**: Mark the calculation class
   ```python
   @polars_optimized(enabled=True, lazy_eval=True)
   class MyCalculation(SingleValueCalculation):
       ...
   ```

3. **Implement Polars Path**: Add conditional logic for Polars operations
   - Check `self.get_polars_processor().polars_enabled`
   - Convert dataframes using processor methods
   - Use lazy evaluation for complex operations
   - Materialize results when needed

4. **Test**: Verify results match Pandas baseline
   - Run benchmark suite to compare performance
   - Use safe_mode=True during development to validate correctness

5. **Gradual Rollout**: Update metrics incrementally
   - Start with most impactful metrics
   - Validate performance improvements
   - Monitor for any edge cases

Performance Considerations
==========================

When to use Polars optimization:
✅ DO use when:
   - Processing 100k+ rows
   - Multiple group_by/aggregation operations
   - Complex filtering pipelines
   - Testing statistical significance (multiple tests)

❌ DON'T use when:
   - Processing <10k rows (overhead outweighs benefits)
   - Single column operations on Pandas Series
   - Already optimized Pandas code
   - Memory-constrained environments

Expected Performance Improvements:
- Small datasets (10k rows): 0-5% improvement (overhead)
- Medium datasets (100k rows): 20-40% improvement
- Large datasets (1M+ rows): 50-75% improvement
- Very large lazy operations: 2-3x improvement

Compatibility Notes
===================

1. Existing code remains unchanged - this is additive
2. Polars falls back to Pandas gracefully if unavailable
3. Use `to_pandas_safe()` when output must be Pandas
4. Lazy frames are automatically collected when needed
5. All operations are deterministic (same results as Pandas)

Common Patterns
===============

Pattern 1: Simple metric with optional Polars acceleration
```python
@polars_optimized()
class ColumnStatisticCalculation(StatisticsCalculation):
    def calculate_value(self, column: DatasetColumn) -> float:
        processor = self.get_polars_processor()
        if processor.polars_enabled:
            # Use Polars
            return compute_with_polars(column, processor)
        else:
            # Use Pandas
            return column.data.mean()
```

Pattern 2: Group-by aggregation optimized for Polars
```python
@polars_optimized(lazy_eval=True)
class GroupByCalculation(DataframeMetric):
    def calculate(self, context, current_data, reference_data):
        processor = self.get_polars_processor()
        df = current_data.as_dataframe()

        if processor.polars_enabled:
            df = processor.to_polars(df, lazy=True)
            result = df.groupby("group").agg(pl.col("value").mean()).collect()
            return processor.to_pandas(result)
        else:
            result = df.groupby("group")["value"].mean()
            return result
```

Pattern 3: Complex pipeline with multiple operations
```python
@polars_optimized(lazy_eval=True)
class ComplexPipelineCalculation(DataframeMetric):
    def calculate(self, context, current_data, reference_data):
        processor = self.get_polars_processor()

        if processor.polars_enabled:
            # Build lazy pipeline
            df = processor.to_polars(current_data.as_dataframe(), lazy=True)
            result = (df
                .filter(pl.col("category") == "A")
                .groupby("date")
                .agg(pl.col("value").mean())
                .sort("date")
                .collect())  # Materialize only at the end
            return processor.to_pandas(result)
        else:
            # Pandas implementation
            df = current_data.as_dataframe()
            return df[df["category"] == "A"].groupby("date")["value"].mean()
```

Testing Strategy
================

For metrics with Polars optimization:

1. **Correctness**: Verify Polars results match Pandas
   ```python
   def test_polars_correctness():
       # Create test data
       df = pd.DataFrame({"col": [1, 2, 3, 4, 5]})

       # Calculate with Pandas
       pandas_result = df["col"].mean()

       # Calculate with Polars (via metric)
       metric = MyMetric()
       polars_result = metric.calculate(...)

       assert abs(pandas_result - polars_result) < 1e-10
   ```

2. **Performance**: Benchmark improvement
   ```python
   def test_performance_improvement():
       large_df = pd.DataFrame({"col": range(1_000_000)})

       # Measure Pandas time
       pandas_time = timeit.timeit(lambda: aggregate_pandas(large_df), number=5)

       # Measure Polars time
       polars_time = timeit.timeit(lambda: aggregate_polars(large_df), number=5)

       # Verify improvement
       improvement = (pandas_time - polars_time) / pandas_time * 100
       assert improvement > 20  # 20% or better
   ```

3. **Edge Cases**: Handle missing values, nulls, etc.
   ```python
   def test_edge_cases():
       # Test with nulls
       df = pd.DataFrame({"col": [1, None, 3]})
       # ... test in both Pandas and Polars

       # Test with empty dataframe
       df = pd.DataFrame({"col": []})
       # ... test
   ```
"""


# This module serves primarily as documentation
# The actual Polars support is in polars_support.py
# and integrated via the @polars_optimized decorator

if __name__ == "__main__":
    print(__doc__)
