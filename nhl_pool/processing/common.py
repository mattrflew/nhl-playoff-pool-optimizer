import pandas as pd
import numpy as np

def weighted_average(series, weights):
    # Compute weighted average of multiple series, given a weight.
    # In processing scripts, the weight would be gamesPlayed for example.
    
    s = pd.to_numeric(series, errors="coerce")
    w = pd.to_numeric(weights, errors="coerce")
    
    # Exit early if problem
    m = s.notna() & w.notna()
    if not m.any():
        return np.nan
    
    # Avoid divide by zero errors
    denom = w[m].sum()
    if denom == 0:
        return np.nan
    
    return (s[m] * w[m]).sum() / denom