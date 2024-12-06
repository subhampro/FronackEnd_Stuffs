import pandas as pd
import numpy as np

def detect_pattern(data, pattern_type="Volatility Contraction"):
    if data.empty or len(data) < 14:
        return False
    
    if pattern_type.lower() in ["volatility contraction", "volatility contraction positive"]:
        # Calculate True Range and ATR
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
        
        # Basic volatility contraction check
        if pattern_type.lower() == "volatility contraction":
            return atr_decrease > 0.1
        
        # Additional checks for positive volatility contraction
        elif pattern_type.lower() == "volatility contraction positive":
            if atr_decrease <= 0.1:
                return False
                
            # Get last 5 candles
            last_5_candles = data.tail(5)
            
            # Check if price is in uptrend
            is_uptrend = (last_5_candles['Close'].iloc[-1] > last_5_candles['Close'].iloc[0])
            
            # Check if closing prices are above opening prices (bullish candles)
            bullish_candles = (last_5_candles['Close'] > last_5_candles['Open']).sum() >= 3
            
            # Check for higher lows
            higher_lows = all(last_5_candles['Low'].iloc[i] >= last_5_candles['Low'].iloc[i-1] 
                            for i in range(1, len(last_5_candles)))
            
            # Volume trend check
            increasing_volume = (last_5_candles['Volume'].pct_change() > 0).sum() >= 3
            
            # Return True only if all conditions are met
            return (is_uptrend and bullish_candles and higher_lows and increasing_volume)
    
    return False