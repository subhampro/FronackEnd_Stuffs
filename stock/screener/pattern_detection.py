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
            conditions_met = {
                "sample_size": False,
                "tight_consolidation": False,
                "higher_lows": False,
                "volatility_impulse": False,
                "low_volume_consolidation": False,
                "ema_proximity": False
            }
            
            # 1. Check sample size (changed from 180 to 126)
            last_126_candles = data.tail(126).copy()
            if len(last_126_candles) >= 126:  # Changed from 100 to 126 to match required candle count
                conditions_met["sample_size"] = True
            else:
                print(f"{ticker}: Failed - Insufficient candles ({len(last_126_candles)})")
                return False
            
            # Calculate 20 EMA
            last_126_candles['EMA20'] = last_126_candles['Close'].ewm(span=20, adjust=False).mean()
            
            # 2. Check first 45 candles for tight consolidation - MODIFIED
            first_45_candles = last_126_candles.head(45)  # Changed from 40 to 45
            consolidation_range = (first_45_candles['High'].max() - first_45_candles['Low'].min()) / first_45_candles['Close'].mean()
            if 0.05 <= consolidation_range <= 0.25:  # Changed to check if range is between 5% and 25%
                conditions_met["tight_consolidation"] = True
            
            # 3. Modified Higher Lows Check - After consolidation period
            # Look at candles 5-50 after the consolidation period
            check_start = 45 + 5  # Start 5 candles after consolidation
            check_end = min(45 + 50, len(last_126_candles))  # Look up to 50 candles after consolidation
            check_section = last_126_candles.iloc[check_start:check_end]
            
            if len(check_section) >= 10:  # Ensure we have enough candles to analyze
                # Find local minima using rolling window of 5 candles
                lows = check_section['Low'].values
                min_points = []
                min_indices = []
                
                for i in range(2, len(lows)-2):
                    if (lows[i] < lows[i-1] and lows[i] < lows[i-2] and 
                        lows[i] < lows[i+1] and lows[i] < lows[i+2]):
                        min_points.append(lows[i])
                        min_indices.append(i)
                
                # Check if we found at least 3 minima and they're forming higher lows
                if len(min_points) >= 3:
                    # Verify higher lows with minimum price increase threshold
                    is_higher_lows = True
                    min_increase = 0.001  # 0.1% minimum increase between lows
                    
                    for i in range(1, len(min_points)):
                        if min_points[i] <= min_points[i-1] or \
                           (min_points[i] - min_points[i-1]) / min_points[i-1] < min_increase:
                            is_higher_lows = False
                            break
                        
                        # Verify the distance between minima is at least 3 candles
                        if min_indices[i] - min_indices[i-1] < 3:
                            is_higher_lows = False
                            break
                    
                    conditions_met["higher_lows"] = is_higher_lows
            
            # 4. Check volatility and impulses (adjusted range)
            volatility_section = last_126_candles.iloc[76:96].copy()  # Adjusted range
            volatility_section['TR'] = np.maximum(
                volatility_section['High'] - volatility_section['Low'],
                np.maximum(
                    abs(volatility_section['High'] - volatility_section['Close'].shift(1)),
                    abs(volatility_section['Low'] - volatility_section['Close'].shift(1))
                )
            )
            volatility_section['ATR'] = volatility_section['TR'].rolling(window=5).mean()
            price_moves = volatility_section['Close'].pct_change()
            # Changed impulse threshold to 15-25% range
            if any((move >= 0.15 and move <= 0.25) for move in price_moves):  # Changed from 0.02 to 0.15-0.25 range
                conditions_met["volatility_impulse"] = True
            
            # 5. Check low volume consolidation - RELAXED
            last_20_candles = last_126_candles.tail(20)
            avg_volume = last_126_candles['Volume'].mean()
            recent_volume = last_20_candles['Volume'].mean()
            recent_range = (last_20_candles['High'].max() - last_20_candles['Low'].min()) / last_20_candles['Close'].mean()
            
            # Relaxed volume and range requirements
            if (recent_volume >= (avg_volume * 0.3) and  # Changed from 0.5 to 0.3
                recent_volume <= (avg_volume * 0.9) and  # Changed from 0.8 to 0.9
                recent_range <= 0.06):  # Changed from 0.04 to 0.06 (6% range allowed)
                conditions_met["low_volume_consolidation"] = True
            
            # 6. Check EMA proximity - RELAXED
            last_15_candles = last_126_candles.tail(15)
            ema_proximity = True
            for _, candle in last_15_candles.iterrows():
                if abs(candle['Close'] - candle['EMA20']) / candle['Close'] > 0.05:  # Changed from 0.03 to 0.05 (5% deviation allowed)
                    ema_proximity = False
                    break
            if ema_proximity:
                conditions_met["ema_proximity"] = True
            
            # Count conditions met
            conditions_count = sum(conditions_met.values())
            
            # Debug output for stocks meeting at least 2 conditions
            if conditions_count >= 2:
                met_conditions = [cond for cond, met in conditions_met.items() if met]
                print(f"\n{ticker} fulfilled {conditions_count} conditions:")
                for cond in met_conditions:
                    print(f"✓ {cond.replace('_', ' ').title()}")
                if conditions_count < 6:
                    failed_conditions = [cond for cond, met in conditions_met.items() if not met]
                    print("Failed conditions:")
                    for cond in failed_conditions:
                        print(f"✗ {cond.replace('_', ' ').title()}")
                print("------------------------")
            
            # Return True only if all conditions are met
            return all(conditions_met.values())
            
        except Exception as e:
            print(f"Error in Lucifer pattern detection for {ticker}: {str(e)}")
            return False

    return False