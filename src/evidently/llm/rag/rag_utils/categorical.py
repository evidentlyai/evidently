import pandas as pd
import numpy as np

def detect_mismatches(ref_data:pd.DataFrame,ana_data:pd.DataFrame,feature:str):  ###NOT USED YETTTTT
    ref_unique = set(ref_data[feature].unique())
    ana_unique = set(ana_data[feature].unique())
    
    # Categories in train but not in test
    ref_only = ref_unique - ana_unique
    # Categories in test but not in train
    ana_only = ana_unique - ref_unique
    
    return ref_only,ana_only
