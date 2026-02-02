"""
Dashboard for Evidently: Feature Correlation Heatmap Integration
Author: Your Name
Date: 2026-02-02
"""

# Imports
import pandas as pd
from src.metrics.feature_correlation import feature_correlation
from src.dashboard.widgets.feature_correlation_widget import plot_correlation_heatmap

# ----------------------------
# Widget Function
# ----------------------------
def add_feature_correlation_widget(df, target_col):
    """
    Adds the Feature Correlation Heatmap to the dashboard.

    Parameters:
    - df: pandas DataFrame containing your dataset
    - target_col: name of the target column to compute correlations against

    Returns:
    - fig: Plotly heatmap figure
    """
    correlations = feature_correlation(df, target_col)
    fig = plot_correlation_heatmap(correlations)
    fig.show()  # For testing; later integrate directly into the web dashboard
    return fig

# ----------------------------
# Sample Test Dataset
# ----------------------------
if __name__ == "__main__":
    # Sample dataset for testing the heatmap
    df = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [5, 4, 3, 2, 1],
        "C": [2, 3, 2, 3, 2],
        "target": [0, 1, 0, 1, 0]
    })

    target_col = "target"

    # Add the feature correlation heatmap to the dashboard
    add_feature_correlation_widget(df, target_col)

    # TODO: Replace the sample dataset with real project dataset or user-uploaded CSV
    # TODO: Embed the Plotly figure directly into the web dashboard layout

