import pandas as pd
import numpy as np

def detect_pattern(data, pattern_type="Volatility Contraction", ticker="Unknown"):  # Added ticker parameter
    if data.empty or len(data) < 60:  # Changed minimum required candles to 60
        return False
    
    if pattern_type.lower() in ["volatility contraction", "lucifer custom filter"]:
        # Calculate True Range and ATR
        data['TR'] = np.maximum(
            data['High'] - data['Low'],
            np.maximum(
                abs(data['High'] - data['Close'].shift(1)),
                abs(data['Low'] - data['Close'].shift(1))
            )
        )
        
        # Make ATR check more strict for daily timeframe
        if data.index.freq == 'D' or len(data) >= 60:  # Daily timeframe check
            atr_window = 14
            lookback_period = 10
        else:
            atr_window = 14
            lookback_period = 5
            
        data['ATR'] = data['TR'].rolling(window=atr_window).mean()
        last_n_atr = data['ATR'].tail(lookback_period)
        
        if not last_n_atr.is_monotonic_decreasing:
            return False
            
        first_atr = last_n_atr.iloc[0]
        last_atr = last_n_atr.iloc[-1]
        
        if pd.isna(first_atr) or pd.isna(last_atr) or first_atr == 0:
            return False
            
        atr_decrease = (first_atr - last_atr) / first_atr
        
        # Increase threshold for daily timeframe
        atr_threshold = 0.15 if (data.index.freq == 'D' or len(data) >= 60) else 0.1
        
        # Basic volatility contraction check
        if pattern_type.lower() == "volatility contraction":
            return atr_decrease > atr_threshold
        
        # Lucifer Custom Filter check (previously Volatility Contraction Positive)
        elif pattern_type.lower() == "lucifer custom filter":
            if atr_decrease <= atr_threshold:
                print(f"{ticker}: Rejected - ATR decrease ({atr_decrease:.2%}) below threshold ({atr_threshold:.2%})")
                return False
                
            # Get last 60 candles for higher lows check and last 10 for other conditions
            last_60_candles = data.tail(60).copy()
            last_10_candles = data.tail(10).copy()
            
            # Condition 1: Check for higher lows formation over 60 candles
            lows = last_60_candles['Low'].values
            min_points = []
            
            # Find significant low points (local minima)
            for i in range(2, len(lows)-2):
                if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and 
                    lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                    min_points.append(lows[i])
            
            # Need at least 3 min points to confirm higher lows trend
            if len(min_points) >= 3:
                higher_lows = all(min_points[i] > min_points[i-1] for i in range(1, len(min_points)))
                print(f"{ticker}: Higher lows check - Found {len(min_points)} low points, trend {'confirmed' if higher_lows else 'failed'}")
                if not higher_lows:
                    print(f"{ticker}: Rejected - Not in higher lows formation over 60 candles")
                    return False
            else:
                print(f"{ticker}: Rejected - Insufficient low points ({len(min_points)}) to confirm trend")
                return False
            
            # Condition 2: Current close vs first candle's low (using last 10 candles)
            first_candle_low = last_10_candles['Low'].iloc[0]
            current_close = last_10_candles['Close'].iloc[-1]
            
            print(f"First candle low: {first_candle_low}")
            print(f"Current close: {current_close}")
            print(f"Higher lows found: {len(min_points)} points")
            
            # For daily timeframe, add minimum price move requirement
            if data.index.freq == 'D' or len(data) >= 60:
                price_move = (current_close - first_candle_low) / first_candle_low
                if price_move < 0.02:  # Minimum 2% move
                    print(f"{ticker}: Rejected - Price move ({price_move:.2%}) below minimum threshold (2%)")
                    return False
            
            if current_close <= first_candle_low:
                print(f"{ticker}: Rejected - Current close ({current_close:.2f}) below first candle low ({first_candle_low:.2f})")
                return False
                
            print(f"Success: Pattern found with ATR decrease of {atr_decrease:.2%}")
            return True
    
    return False