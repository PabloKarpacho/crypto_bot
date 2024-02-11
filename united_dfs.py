import pandas as pd

def united_dfs(candles, ta_indicators):
    df = candles.copy()
    
    for key in ta_indicators.__dict__.keys():
        df = pd.concat([df, ta_indicators.__dict__[key]], axis=1)
    
    df.dropna(axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df