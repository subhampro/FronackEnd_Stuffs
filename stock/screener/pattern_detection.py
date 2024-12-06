import pandas as pd
import numpy as np

def detect_pattern(data, pattern_type="Volatility Contraction"):
    if data.empty or len(data) < 14:
        return False
    
    if pattern_type.lower() == "volatility contraction":
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
            
        first_atr = last_5_atr.iloc[0]
        last_atr = last_5_atr.iloc[-1]
        
        if pd.isna(first_atr) or pd.isna(last_atr) or first_atr == 0:
            return False
            
        atr_decrease = (first_atr - last_atr) / first_atr
        return atr_decrease > 0.1
    
    return False