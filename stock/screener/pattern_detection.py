import pandas as pd
import numpy as np

def detect_pattern(data, pattern_type="Volatility Contraction", ticker="Unknown"):
    if data.empty or len(data) < 60:
        return False
    
    if pattern_type.lower() == "volatility contraction":
        # Calculate True Range and ATR
        data['TR'] = np.maximum(
            data['High'] - data['Low'],
            np.maximum(
                abs(data['High'] - data['Close'].shift(1)),
                abs(data['Low'] - data['Close'].shift(1))
            )
        )
        
        # Make ATR check more strict for daily timeframe
        if data.index.freq == 'D' or len(data) >= 60:
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
        atr_threshold = 0.15 if (data.index.freq == 'D' or len(data) >= 60) else 0.1
        
        return atr_decrease > atr_threshold
    
    elif pattern_type.lower() == "lucifer custom filter":
        try:
            # Get last 180 candles for analysis
            last_180_candles = data.tail(180).copy()
            if len(last_180_candles) < 140:  # Minimum required candles
                return False
            
            # Calculate 20 EMA
            last_180_candles['EMA20'] = last_180_candles['Close'].ewm(span=20, adjust=False).mean()
            
            # 1. Check first 40-50 candles for tight consolidation
            first_50_candles = last_180_candles.head(50)
            consolidation_range = (first_50_candles['High'].max() - first_50_candles['Low'].min()) / first_50_candles['Close'].mean()
            if consolidation_range > 0.03:  # 3% range for tight consolidation
                return False
            
            # 2. Check next 40-50 candles for higher low formation
            next_50_candles = last_180_candles.iloc[50:100]
            lows = next_50_candles['Low'].values
            higher_lows = False
            min_points = []
            
            # Find significant low points
            for i in range(2, len(lows)-2):
                if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and 
                    lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                    min_points.append(lows[i])
            
            # Verify higher lows
            if len(min_points) >= 3:
                higher_lows = all(min_points[i] > min_points[i-1] for i in range(1, len(min_points)))
                if not higher_lows:
                    return False
            else:
                return False
            
            # 3. Check next 30 candles for volatility and impulses
            volatility_section = last_180_candles.iloc[100:130]
            
            # Calculate ATR for volatility
            volatility_section['TR'] = np.maximum(
                volatility_section['High'] - volatility_section['Low'],
                np.maximum(
                    abs(volatility_section['High'] - volatility_section['Close'].shift(1)),
                    abs(volatility_section['Low'] - volatility_section['Close'].shift(1))
                )
            )
            volatility_section['ATR'] = volatility_section['TR'].rolling(window=5).mean()
            
            # Check for impulse moves
            price_moves = volatility_section['Close'].pct_change()
            has_impulse = any(abs(move) > 0.02 for move in price_moves)  # 2% moves
            if not has_impulse:
                return False
            
            # 4. Check last 25 candles for consolidation with low volumes
            last_25_candles = last_180_candles.tail(25)
            
            # Volume comparison
            avg_volume = last_180_candles['Volume'].mean()
            recent_volume = last_25_candles['Volume'].mean()
            if recent_volume > (avg_volume * 0.8):  # Volume should be lower
                return False
            
            # Check for tight consolidation
            recent_range = (last_25_candles['High'].max() - last_25_candles['Low'].min()) / last_25_candles['Close'].mean()
            if recent_range > 0.04:  # 4% range for recent consolidation
                return False
            
            # 5. Check last 15 candles proximity to 20 EMA
            last_15_candles = last_180_candles.tail(15)
            for _, candle in last_15_candles.iterrows():
                ema_distance = abs(candle['Close'] - candle['EMA20']) / candle['Close']
                if ema_distance > 0.03:  # More than 3% away from EMA
                    return False
            
            # If all conditions are met
            return True
            
        except Exception as e:
            print(f"Error in Lucifer pattern detection: {str(e)}")
            return False

    return False