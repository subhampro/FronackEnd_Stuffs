import pandas as pd
import numpy as np
from datetime import datetime
import os

TOTAL_STOCKS_SCANNED = 0

def get_scan_folder_name(pattern_type, interval, exchange):
    """Generate a unique folder name for each scan variation"""
    timestamp = datetime.now().strftime("%Y%m%d")
    sanitized_pattern = pattern_type.lower().replace(" ", "_")
    folder_name = f"{timestamp}_{sanitized_pattern}_{interval}_{exchange}"
    return folder_name

def log_pattern_result(ticker, conditions_met, met_conditions, failed_conditions=None, pattern_type=None, interval=None, exchange=None):
    global TOTAL_STOCKS_SCANNED
    TOTAL_STOCKS_SCANNED += 1
    
    # Create base log directory
    log_dir = "pattern_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Create unique scan folder
    scan_folder = get_scan_folder_name(pattern_type, interval, exchange)
    scan_dir = os.path.join(log_dir, scan_folder)
    if not os.path.exists(scan_dir):
        os.makedirs(scan_dir)
    
    # Use scan-specific log files
    log_file = os.path.join(scan_dir, "pattern_scan.log")
    summary_file = os.path.join(scan_dir, "pattern_summary.txt")
    
    # Append to daily log file
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"\n{'='*50}\n")
        f.write(f"Ticker: {ticker}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Conditions Met: {len(met_conditions)} of 6\n")
        f.write("\nSuccessful Conditions:\n")
        for cond in met_conditions:
            f.write(f"✓ {cond.replace('_', ' ').title()}\n")
        
        if failed_conditions:
            f.write("\nFailed Conditions:\n")
            for cond in failed_conditions:
                f.write(f"✗ {cond.replace('_', ' ').title()}\n")
    
    # Update summary after each stock scan
    update_summary_report(summary_file, ticker, len(met_conditions), pattern_type, interval, exchange)

def update_summary_report(summary_file, ticker, conditions_met_count, pattern_type=None, interval=None, exchange=None):
    # Read existing summary if it exists
    summary_data = {2: [], 3: [], 4: [], 5: [], 6: []}
    
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            current_section = None
            for line in f:
                if "Conditions Met (" in line:
                    current_section = int(line.split()[0])
                elif line.startswith("- ") and current_section:
                    ticker_name = line.strip("- \n")
                    summary_data[current_section].append(ticker_name)
    
    # Update with new ticker
    if conditions_met_count >= 2:
        for count in summary_data:
            if ticker in summary_data[count]:
                summary_data[count].remove(ticker)
        summary_data[conditions_met_count].append(ticker)
    
    # Read the log file for condition analysis
    log_dir = "pattern_logs"
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"pattern_scan_{timestamp}.log")
    
    condition_stats = {
        "sample_size": {'success': 0, 'failed': 0},
        "tight_consolidation": {'success': 0, 'failed': 0},
        "volatility_impulse": {'success': 0, 'failed': 0},
        "low_volume_consolidation": {'success': 0, 'failed': 0},
        "ema_proximity": {'success': 0, 'failed': 0},
        "reversal_level": {'success': 0, 'failed': 0}
    }
    
    # Analyze all logs for condition statistics
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            reading_success = False
            reading_failed = False
            
            for line in f:
                line = line.strip()
                if line.startswith("Successful Conditions:"):
                    reading_success = True
                    reading_failed = False
                elif line.startswith("Failed Conditions:"):
                    reading_success = False
                    reading_failed = True
                elif reading_success and line.startswith("✓"):
                    condition = line[2:].lower().replace(" ", "_")
                    if condition in condition_stats:
                        condition_stats[condition]['success'] += 1
                elif reading_failed and line.startswith("✗"):
                    condition = line[2:].lower().replace(" ", "_")
                    if condition in condition_stats:
                        condition_stats[condition]['failed'] += 1

    # Write updated summary with full analysis
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"Pattern Scan Summary Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        
        if pattern_type:
            f.write(f"Pattern Type: {pattern_type.title()}\n")
            f.write("-"*30 + "\n\n")
            
            f.write("Detailed Condition Analysis:\n")
            f.write("-"*30 + "\n")
            
            conditions = get_pattern_conditions(pattern_type)
            for idx, (condition, description) in enumerate(conditions.items(), 1):
                stats = condition_stats.get(condition, {'success': 0, 'failed': 0})
                total = stats['success'] + stats['failed']
                if total > 0:
                    success_pct = (stats['success'] / total) * 100
                    failure_pct = (stats['failed'] / total) * 100
                    
                    f.write(f"Condition {idx}: {description}\n")
                    f.write(f"✓ Success Rate: {success_pct:.1f}% ({stats['success']} stocks)\n")
                    f.write(f"✗ Failed: {stats['failed']} stocks ({failure_pct:.1f}%)\n")
                    f.write("-"*30 + "\n")
        
        f.write(f"\nTotal Stocks Scanned: {TOTAL_STOCKS_SCANNED}\n")
        f.write(f"Stocks Meeting 2+ Conditions: {sum(len(stocks) for stocks in summary_data.values())}\n\n")
        
        # Write stocks by conditions met
        for count in reversed(range(2, 7)):
            stocks = sorted(summary_data[count])
            if stocks:
                f.write(f"\n{count} Conditions Met ({len(stocks)} stocks):\n")
                f.write("-" * 30 + "\n")
                for stock in stocks:
                    f.write(f"- {stock}\n")

def detect_pattern(data, pattern_type="Volatility Contraction", ticker="Unknown", interval="1h", exchange="NSE"):
    if data.empty or len(data) < 60:
        return False
    
    if pattern_type.lower() == "volatility contraction":
        data['TR'] = np.maximum(
            data['High'] - data['Low'],
            np.maximum(
                abs(data['High'] - data['Close'].shift(1)),
                abs(data['Low'] - data['Close'].shift(1))
            )
        )
        
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
    
    elif pattern_type.lower() == "low volume stock selection":
        try:
            conditions_met = {
                "sample_size": False,
                "tight_consolidation": False,
                "volatility_impulse": False,
                "low_volume_consolidation": False,
                "ema_proximity": False
            }
            
            last_120_candles = data.tail(120).copy()  # Changed from 126 to 120
            if len(last_120_candles) >= 120:  # Changed from 126 to 120
                conditions_met["sample_size"] = True
            else:
                print(f"{ticker}: Failed - Insufficient candles ({len(last_120_candles)})")
                return False
            
            last_120_candles['EMA20'] = last_120_candles['Close'].ewm(span=20, adjust=False).mean()
            
            # Update all references from last_126_candles to last_120_candles
            first_45_candles = last_120_candles.head(45)
            consolidation_range = (first_45_candles['High'].max() - first_45_candles['Low'].min()) / first_45_candles['Close'].mean()
            if 0.05 <= consolidation_range <= 0.25:
                conditions_met["tight_consolidation"] = True
            
            volatility_section = last_120_candles.iloc[60:100].copy()
            volatility_section['TR'] = np.maximum(
                volatility_section['High'] - data['Low'],
                np.maximum(
                    abs(volatility_section['High'] - volatility_section['Close'].shift(1)),
                    abs(volatility_section['Low'] - volatility_section['Close'].shift(1))
                )
            )
            volatility_section['ATR'] = volatility_section['TR'].rolling(window=8).mean()
            price_moves = volatility_section['Close'].pct_change().abs()
            
            if any((move >= 0.03 and move <= 0.30) for move in price_moves):
                conditions_met["volatility_impulse"] = True
            
            last_20_candles = last_120_candles.tail(20)
            avg_volume = last_120_candles['Volume'].mean()
            recent_volume = last_20_candles['Volume'].mean()
            recent_range = (last_20_candles['High'].max() - last_20_candles['Low'].min()) / last_20_candles['Close'].mean()
            
            if (recent_volume >= (avg_volume * 0.10) and
                recent_volume <= (avg_volume * 1.5) and
                recent_range <= 0.15):
                conditions_met["low_volume_consolidation"] = True
            
            last_15_candles = last_120_candles.tail(15)
            ema_proximity = True
            for _, candle in last_15_candles.iterrows():
                if abs(candle['Close'] - candle['EMA20']) / candle['Close'] > 0.05:
                    ema_proximity = False
                    break
            if ema_proximity:
                conditions_met["ema_proximity"] = True
            
            conditions_count = sum(conditions_met.values())
            
            if conditions_count >= 2:
                met_conditions = [cond for cond, met in conditions_met.items() if met]
                failed_conditions = [cond for cond, met in conditions_met.items() if not met]
                log_pattern_result(ticker, conditions_met, met_conditions, failed_conditions, pattern_type, interval, exchange)
            
            return all(conditions_met.values())
            
        except Exception as e:
            print(f"Error in Lucifer pattern detection for {ticker}: {str(e)}")
            return False

    elif pattern_type.lower() == "15% reversal":
        try:
            conditions_met = {
                "sample_size": False,
                "tight_consolidation": False,
                "volatility_impulse": False,
                "low_volume_consolidation": False,
                "ema_proximity": False,
                "reversal_level": False
            }
            
            last_120_candles = data.tail(120).copy()  # Changed from 126 to 120
            if len(last_120_candles) >= 120:  # Changed from 126 to 120
                conditions_met["sample_size"] = True
            else:
                print(f"{ticker}: Failed - Insufficient candles ({len(last_120_candles)})")
                return False
            
            last_120_candles['EMA20'] = last_120_candles['Close'].ewm(span=20, adjust=False).mean()
            
            # Update all references from last_126_candles to last_120_candles
            first_45_candles = last_120_candles.head(45)
            consolidation_range = (first_45_candles['High'].max() - first_45_candles['Low'].min()) / first_45_candles['Close'].mean()
            if 0.05 <= consolidation_range <= 0.25:
                conditions_met["tight_consolidation"] = True
            
            volatility_section = last_120_candles.iloc[60:100].copy()
            volatility_section['TR'] = np.maximum(
                volatility_section['High'] - data['Low'],
                np.maximum(
                    abs(volatility_section['High'] - volatility_section['Close'].shift(1)),
                    abs(volatility_section['Low'] - volatility_section['Close'].shift(1))
                )
            )
            volatility_section['ATR'] = volatility_section['TR'].rolling(window=8).mean()
            price_moves = volatility_section['Close'].pct_change().abs()
            
            if any((move >= 0.03 and move <= 0.30) for move in price_moves):
                conditions_met["volatility_impulse"] = True
            
            last_20_candles = last_120_candles.tail(20)
            avg_volume = last_120_candles['Volume'].mean()
            recent_volume = last_20_candles['Volume'].mean()
            recent_range = (last_20_candles['High'].max() - last_20_candles['Low'].min()) / last_20_candles['Close'].mean()
            
            if (recent_volume >= (avg_volume * 0.10) and
                recent_volume <= (avg_volume * 1.5) and
                recent_range <= 0.15):
                conditions_met["low_volume_consolidation"] = True
            
            last_15_candles = last_120_candles.tail(15)
            ema_proximity = True
            for _, candle in last_15_candles.iterrows():
                if abs(candle['Close'] - candle['EMA20']) / candle['Close'] > 0.05:
                    ema_proximity = False
                    break
            if ema_proximity:
                conditions_met["ema_proximity"] = True
                
            first_100_candles = last_120_candles.head(100)
            top_high = first_100_candles['High'].max()
            
            reversal_percentage = 0.15  # Can be modified to any value between 0.15-0.20
            reversal_level = top_high * (1 - reversal_percentage)
            
            last_30_candles = last_120_candles.tail(30)
            above_reversal_level = all(close > reversal_level for close in last_30_candles['Close'])
            
            if above_reversal_level:
                conditions_met["reversal_level"] = True
            
            conditions_count = sum(conditions_met.values())
            if conditions_count >= 2:
                met_conditions = [cond for cond, met in conditions_met.items() if met]
                failed_conditions = [cond for cond, met in conditions_met.items() if not met]
                log_pattern_result(ticker, conditions_met, met_conditions, failed_conditions, pattern_type, interval, exchange)
            
            return all(conditions_met.values())
            
        except Exception as e:
            print(f"Error in 15% Reversal pattern detection for {ticker}: {str(e)}")
            return False

    return False

def get_pattern_conditions(pattern_type):
    """Returns a dictionary of conditions and their descriptions for each pattern"""
    if pattern_type.lower() == "volatility contraction":
        return {
            "atr_decrease": "ATR Decrease Over Period",
            "atr_threshold": "ATR Threshold Check"
        }
    elif pattern_type.lower() == "low volume stock selection":
        return {
            "sample_size": "Minimum 120 Candles Available",
            "tight_consolidation": "Price Range within 5-25% of Mean",
            "volatility_impulse": "Price Move between 3-30%",
            "low_volume_consolidation": "Volume 10-150% of Average & Range ≤15%",
            "ema_proximity": "Price within 5% of EMA20"
        }
    elif pattern_type.lower() == "15% reversal":
        return {
            "sample_size": "Minimum 120 Candles Available",
            "tight_consolidation": "Price Range within 5-25% of Mean",
            "volatility_impulse": "Price Move between 3-30%",
            "low_volume_consolidation": "Volume 10-150% of Average & Range ≤15%",
            "ema_proximity": "Price within 5% of EMA20",
            "reversal_level": "Price Above 15% Reversal Level"
        }
    return {}

def generate_summary_report():
    global TOTAL_STOCKS_SCANNED
    log_dir = "pattern_logs"
    if not os.path.exists(log_dir):
        return
        
    current_time = datetime.now()
    
    # Find the most recent scan folder
    scan_folders = []
    for folder in os.listdir(log_dir):
        folder_path = os.path.join(log_dir, folder)
        if os.path.isdir(folder_path):
            folder_time = datetime.fromtimestamp(os.path.getctime(folder_path))
            if (current_time - folder_time).total_seconds() < 3600:
                scan_folders.append(folder_path)
    
    if not scan_folders:
        return
    
    # Use the most recent scan folder
    latest_scan_dir = max(scan_folders, key=os.path.getctime)
    log_file = os.path.join(latest_scan_dir, "pattern_scan.log")
    summary_file = os.path.join(latest_scan_dir, "pattern_summary.txt")
    
    stocks_by_conditions = {i: [] for i in range(2, 7)}
    matching_stocks = 0
    processed_tickers = set()
    
    condition_stats = {
        "sample_size": {'success': 0, 'failed': 0},
        "tight_consolidation": {'success': 0, 'failed': 0},
        "volatility_impulse": {'success': 0, 'failed': 0},
        "low_volume_consolidation": {'success': 0, 'failed': 0},
        "ema_proximity": {'success': 0, 'failed': 0},
        "reversal_level": {'success': 0, 'failed': 0}
    }
    
    for log_file in log_files:
        with open(log_file, 'r', encoding='utf-8') as f:
            current_ticker = None
            reading_success = False
            reading_failed = False
            
            for line in f:
                line = line.strip()
                if line.startswith("Ticker:"):
                    current_ticker = line.split(":")[1].strip()
                    reading_success = False
                    reading_failed = False
                elif line.startswith("Successful Conditions:"):
                    reading_success = True
                    reading_failed = False
                elif line.startswith("Failed Conditions:"):
                    reading_success = False
                    reading_failed = True
                elif reading_success and line.startswith("✓"):
                    condition = line[2:].lower().replace(" ", "_")
                    if condition in condition_stats:
                        condition_stats[condition]['success'] += 1
                elif reading_failed and line.startswith("✗"):
                    condition = line[2:].lower().replace(" ", "_")
                    if condition in condition_stats:
                        condition_stats[condition]['failed'] += 1

    summary_file = os.path.join(log_dir, "pattern_summary.txt")
    with open(summary_file, 'r+', encoding='utf-8') as f:
        content = f.read()
        f.seek(0)
        f.write(f"Pattern Scan Summary Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*50 + "\n\n")
        
        # Add pattern type detection from logs
        pattern_type = None
        for log_file in log_files:
            with open(log_file, 'r', encoding='utf-8') as log:
                content = log.read()
                if "Volatility Contraction" in content:
                    pattern_type = "volatility contraction"
                elif "Low Volume Stock Selection" in content:
                    pattern_type = "low volume stock selection"
                elif "15% Reversal" in content:
                    pattern_type = "15% reversal"
                break
        
        if pattern_type:
            conditions = get_pattern_conditions(pattern_type)
            f.write(f"Pattern Type: {pattern_type.title()}\n")
            f.write("-"*30 + "\n\n")
            
            f.write("Detailed Condition Analysis:\n")
            f.write("-"*30 + "\n")
            
            for idx, (condition, description) in enumerate(conditions.items(), 1):
                stats = condition_stats.get(condition, {'success': 0, 'failed': 0})
                total = stats['success'] + stats['failed']
                if total > 0:
                    success_pct = (stats['success'] / total) * 100
                    failure_pct = (stats['failed'] / total) * 100
                    
                    f.write(f"Condition {idx}: {description}\n")
                    f.write(f"✓ Success Rate: {success_pct:.1f}% ({stats['success']} stocks)\n")
                    f.write(f"✗ Failed: {stats['failed']} stocks ({failure_pct:.1f}%)\n")
                    f.write("-"*30 + "\n")

        f.write(content[content.find("\nTotal Stocks Scanned:"):])
        f.truncate()

    TOTAL_STOCKS_SCANNED = 0