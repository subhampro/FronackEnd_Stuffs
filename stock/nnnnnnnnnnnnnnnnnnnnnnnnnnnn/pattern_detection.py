import pandas as pd
import numpy as np

def detect_pattern(data, pattern_type="volatility_contraction"):
    if data.empty or len(data) < 14:
        return False
    
    if pattern_type.lower() == "volatility_contraction":
        data['TR'] = np.maximum(
            data['High'] - data['Low'],
            np.maximum(
                abs(data['High'] - data['Close'].shift(1)),
                abs(data['Low'] - data['Close'].shift(1))
            )
        )
        data['ATR'] = data['TR'].rolling(window=14).mean()
        
        last_5_atr = data['ATR'].tail(5)
        if not last_5_atr.is_monotonic_decreasing:
            return False
            
        atr_decrease = (last_5_atr.iloc[0] - last_5_atr.iloc[-1]) / last_5_atr.iloc[0]
        return atr_decrease > 0.1
    
    return False