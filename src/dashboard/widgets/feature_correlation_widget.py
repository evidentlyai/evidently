import plotly.express as px
import pandas as pd

def plot_correlation_heatmap(correlations):
    """
    Plots feature correlations as a heatmap using Plotly
    correlations: pandas Series with feature names as index
    """
    # Convert Series to DataFrame: 1 row (target) x n columns (features)
    df = pd.DataFrame([correlations.values], columns=correlations.index, index=[correlations.name if correlations.name else "target"])

    fig = px.imshow(
        df,
        text_auto=True,                     # shows values on the heatmap
        color_continuous_scale='Viridis',
        labels={'x': 'Features', 'y': 'Target', 'color': 'Correlation'}
    )

    fig.update_layout(title="Feature Correlation Heatmap")
    return fig

