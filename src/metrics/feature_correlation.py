import pandas as pd

def feature_correlation(df, target_col):
    """
    Computes correlation of all features with the target column.
    Returns a sorted pandas Series.
    """
    correlations = df.corr()[target_col].sort_values(ascending=False)
    return correlations
