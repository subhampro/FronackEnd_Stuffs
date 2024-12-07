import pandas as pd
import numpy as np
from datetime import datetime
import os

# Add new global variable at top of file
TOTAL_STOCKS_SCANNED = 0

def log_pattern_result(ticker, conditions_met, met_conditions, failed_conditions=None):
    global TOTAL_STOCKS_SCANNED
    TOTAL_STOCKS_SCANNED += 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "pattern_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    log_file = os.path.join(log_dir, f"pattern_scan_{timestamp}.log")
    
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Ticker: {ticker}\n")
        f.write(f"Conditions Met: {len(met_conditions)} of 6\n")
        f.write("\nSuccessful Conditions:\n")
        for cond in met_conditions:
            f.write(f"✓ {cond.replace('_', ' ').title()}\n")
        
        if failed_conditions:
            f.write("\nFailed Conditions:\n")
            for cond in failed_conditions:
                f.write(f"✗ {cond.replace('_', ' ').title()}\n")
        f.write(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

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
            
            # 3. Modified Higher Lows Check - MUCH MORE RELAXED
            check_start = 45 + 3  # Reduced from 5 to 3 candles after consolidation
            check_end = min(45 + 65, len(last_126_candles))  # Extended window further
            check_section = last_126_candles.iloc[check_start:check_end]

            if len(check_section) >= 6:  # Reduced from 8 to 6 minimum candles
                lows = check_section['Low'].values
                min_points = []
                min_indices = []
                
                # Use smaller window to find more potential low points
                for i in range(1, len(lows)-1):
                    # More lenient low point detection - allow equal lows
                    if (lows[i] <= lows[i-1] * 1.001 and lows[i] <= lows[i+1] * 1.001):  # Allow 0.1% variance
                        min_points.append(lows[i])
                        min_indices.append(i)
                
                if len(min_points) >= 2:  # Keep minimum 2 points
                    is_higher_lows = True
                    min_increase = 0.0001  # Reduced from 0.0003 to 0.0001 (0.01% minimum increase)
                    
                    for i in range(1, len(min_points)):
                        # Allow more deviation in higher lows
                        if min_points[i] < min_points[i-1] * (1 - 0.005):  # Allow 0.5% deviation instead of 0.2%
                            is_higher_lows = False
                            break
                        
                        # Minimum distance between lows remains at 1 candle
                        if min_indices[i] - min_indices[i-1] < 1:
                            is_higher_lows = False
                            break
                    
                    conditions_met["higher_lows"] = is_higher_lows
            
            # 4. Check volatility and impulses - MUCH MORE RELAXED
            # Extended section to look for impulses
            volatility_section = last_126_candles.iloc[60:100].copy()  # Extended window from 65:96 to 60:100
            volatility_section['TR'] = np.maximum(
                volatility_section['High'] - data['Low'],
                np.maximum(
                    abs(volatility_section['High'] - volatility_section['Close'].shift(1)),
                    abs(volatility_section['Low'] - volatility_section['Close'].shift(1))
                )
            )
            volatility_section['ATR'] = volatility_section['TR'].rolling(window=8).mean()  # Increased from 5 to 8
            price_moves = volatility_section['Close'].pct_change().abs()  # Added abs() for both up/down moves
            
            # Much more relaxed impulse threshold
            if any((move >= 0.03 and move <= 0.30) for move in price_moves):  # Changed from 0.05-0.25 to 0.03-0.30
                conditions_met["volatility_impulse"] = True
            
            # 5. Check low volume consolidation - MORE RELAXED
            last_20_candles = last_126_candles.tail(20)
            avg_volume = last_126_candles['Volume'].mean()
            recent_volume = last_20_candles['Volume'].mean()
            recent_range = (last_20_candles['High'].max() - last_20_candles['Low'].min()) / last_20_candles['Close'].mean()
            
            # Further relaxed volume and range requirements
            if (recent_volume >= (avg_volume * 0.10) and  # Changed from 0.15 to 0.10
                recent_volume <= (avg_volume * 1.5) and   # Changed from 1.2 to 1.5
                recent_range <= 0.15):                    # Changed from 0.10 to 0.15
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
            
            # Log results for stocks meeting at least 2 conditions
            if conditions_count >= 2:
                met_conditions = [cond for cond, met in conditions_met.items() if met]
                failed_conditions = [cond for cond, met in conditions_met.items() if not met]
                log_pattern_result(ticker, conditions_met, met_conditions, failed_conditions)
            
            # Return True only if all conditions are met
            return all(conditions_met.values())
            
        except Exception as e:
            print(f"Error in Lucifer pattern detection for {ticker}: {str(e)}")
            return False

    return False

def generate_summary_report():
    global TOTAL_STOCKS_SCANNED
    log_dir = "pattern_logs"
    if not os.path.exists(log_dir):
        return
        
    # Get all log files created in the last hour
    current_time = datetime.now()
    log_files = []
    for file in os.listdir(log_dir):
        if file.startswith('pattern_scan_') and file.endswith('.log'):
            file_path = os.path.join(log_dir, file)
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if (current_time - file_time).total_seconds() < 3600:  # Within last hour
                log_files.append(file_path)
    
    if not log_files:
        return
    
    stocks_by_conditions = {i: [] for i in range(2, 7)}
    matching_stocks = 0
    processed_tickers = set()
    
    # Track failed conditions
    condition_failures = {
        "sample_size": 0,
        "tight_consolidation": 0,
        "higher_lows": 0,
        "volatility_impulse": 0,
        "low_volume_consolidation": 0,
        "ema_proximity": 0
    }
    stocks_with_failures = 0
    
    for log_file in log_files:
        with open(log_file, 'r', encoding='utf-8') as f:
            current_ticker = None
            reading_failed = False
            
            for line in f:
                line = line.strip()
                if line.startswith("Ticker:"):
                    current_ticker = line.split(":")[1].strip()
                    if current_ticker not in processed_tickers:
                        stocks_with_failures += 1
                        processed_tickers.add(current_ticker)
                elif line.startswith("Failed Conditions:"):
                    reading_failed = True
                elif reading_failed and line.startswith("✗"):
                    condition = line[2:].lower().replace(" ", "_")
                    condition_failures[condition] += 1
                elif line.startswith("Timestamp:"):
                    reading_failed = False
                elif line.startswith("Conditions Met:") and current_ticker:
                    conditions = int(line.split(":")[1].split()[0])
                    if conditions >= 2 and current_ticker not in processed_tickers:
                        stocks_by_conditions[conditions].append(current_ticker)
                        matching_stocks += 1
    
    summary_file = os.path.join(log_dir, "pattern_summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Pattern Scan Summary Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*50}\n\n")
        f.write(f"Total Stocks Scanned: {TOTAL_STOCKS_SCANNED}\n")
        f.write(f"Stocks Meeting 2+ Conditions: {matching_stocks}\n\n")
        
        # Write condition failure statistics
        f.write("Condition Failure Analysis:\n")
        f.write("-" * 30 + "\n")
        for condition, failures in condition_failures.items():
            readable_condition = condition.replace("_", " ").title()
            percentage = (failures / TOTAL_STOCKS_SCANNED) * 100 if TOTAL_STOCKS_SCANNED > 0 else 0
            f.write(f"{readable_condition}:\n")
            f.write(f"Not fulfilled by {failures} stocks out of {TOTAL_STOCKS_SCANNED} stocks ({percentage:.1f}%)\n\n")
        
        f.write("\nStocks by Conditions Met:\n")
        f.write("-" * 30 + "\n")
        for conditions in range(6, 1, -1):
            stocks = sorted(stocks_by_conditions[conditions])
            if stocks:
                f.write(f"\n{conditions} Conditions Met ({len(stocks)} stocks):\n")
                f.write("-" * 30 + "\n")
                for stock in stocks:
                    f.write(f"- {stock}\n")
        
        f.write(f"\nLog Sources:\n")
        f.write("-" * 30 + "\n")
        for log_file in log_files:
            f.write(f"- {os.path.basename(log_file)}\n")
    
    TOTAL_STOCKS_SCANNED = 0