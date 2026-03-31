import pandas as pd
from src.metrics.feature_correlation import feature_correlation
from src.dashboard.widgets.feature_correlation_widget import plot_correlation_heatmap

# Sample data
df = pd.DataFrame({
    "A": [1, 2, 3, 4],
    "B": [2, 4, 6, 8],
    "target": [1, 0, 1, 0]
})

correlations = feature_correlation(df, "target")
fig = plot_correlation_heatmap(correlations)
fig.show()
