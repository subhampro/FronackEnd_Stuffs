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
        
        # Positive volatility contraction check
        elif pattern_type.lower() == "volatility contraction positive":
            # First check ATR decrease
            if atr_decrease <= 0.1:
                return False
                
            # Get last 10 candles
            last_10_candles = data.tail(10).copy()  # Using .copy() to avoid SettingWithCopyWarning
            
            # Get first candle's low and last candle's close
            first_candle_low = last_10_candles['Low'].iloc[0]
            last_candle_close = last_10_candles['Close'].iloc[-1]
            
            # Debug prints to verify the condition
            print(f"First candle low: {first_candle_low}")
            print(f"Last candle close: {last_candle_close}")
            print(f"Close above low?: {last_candle_close > first_candle_low}")
            
            # Strict condition: last close must be ABOVE (not equal to) first candle's low
            if last_candle_close <= first_candle_low:
                print(f"Rejected: Last close ({last_candle_close}) not above first candle low ({first_candle_low})")
                return False
                
            return True
    
    return False