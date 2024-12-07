import os
import json
from datetime import datetime, timedelta
import pytz
import pandas as pd
from io import StringIO

class CacheManager:
    def __init__(self):
        self.cache_dir = "cache"
        self.ensure_cache_directory()
        self.cleanup_old_cache()  # Add cache cleanup on initialization

    def ensure_cache_directory(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def cleanup_old_cache(self):
        """Remove cache files older than 12 hours"""
        try:
            current_time = datetime.now()
            for file in os.listdir(self.cache_dir):
                file_path = os.path.join(self.cache_dir, file)
                file_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
                if (current_time - file_modified) > timedelta(hours=12):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning cache: {e}")

    def get_cache_key(self, pattern, interval, exchange):
        return f"{pattern}_{interval}_{exchange}"

    def get_next_expiry(self):
        ist = pytz.timezone('Asia/Kolkata')
        now = datetime.now(ist)
        next_day = now + timedelta(days=1)
        next_expiry = next_day.replace(hour=9, minute=15, second=0, microsecond=0)
        return next_expiry

    def is_cache_valid(self, cache_data):
        if not cache_data or 'expiry' not in cache_data:
            return False
        expiry = datetime.fromisoformat(cache_data['expiry'])
        current_time = datetime.now(pytz.UTC)
        return current_time < expiry

    def save_to_cache(self, pattern, interval, exchange, matching_stocks, stocks_with_issues):
        cache_key = self.get_cache_key(pattern, interval, exchange)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        # Convert stock data to serializable format
        serialized_matching_stocks = []
        for ticker, company_name, data in matching_stocks:
            serialized_matching_stocks.append({
                'ticker': ticker,
                'company_name': company_name,
                'data': data.to_json()
            })

        serialized_stocks_with_issues = []
        for ticker, company_name, data in stocks_with_issues:
            serialized_stocks_with_issues.append({
                'ticker': ticker,
                'company_name': company_name,
                'data': data.to_json()
            })

        cache_data = {
            'expiry': self.get_next_expiry().isoformat(),
            'matching_stocks': serialized_matching_stocks,
            'stocks_with_issues': serialized_stocks_with_issues
        }

        with open(cache_file, 'w') as f:
            json.dump(cache_data, f)

    def get_from_cache(self, pattern, interval, exchange):
        cache_key = self.get_cache_key(pattern, interval, exchange)
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")

        if not os.path.exists(cache_file):
            return None

        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)

            if not self.is_cache_valid(cache_data):
                return None

            # Convert cached data back to original format using StringIO
            matching_stocks = []
            for stock in cache_data['matching_stocks']:
                data = pd.read_json(StringIO(stock['data']))
                matching_stocks.append((
                    stock['ticker'],
                    stock['company_name'],
                    data
                ))

            stocks_with_issues = []
            for stock in cache_data['stocks_with_issues']:
                data = pd.read_json(StringIO(stock['data']))
                stocks_with_issues.append((
                    stock['ticker'],
                    stock['company_name'],
                    data
                ))

            return matching_stocks, stocks_with_issues

        except Exception as e:
            print(f"Error reading cache: {e}")
            return None

    def save_progress_to_cache(self, pattern, interval, exchange, processed_stocks, matching_stocks, stocks_with_issues, total_stocks):
        try:
            # Validate total_stocks and processed_stocks count
            total_stocks = max(total_stocks, len(processed_stocks))
            
            cache_key = self.get_cache_key(pattern, interval, exchange)
            progress_file = os.path.join(self.cache_dir, f"{cache_key}_progress.json")

            progress_data = {
                'last_update': datetime.now(pytz.UTC).isoformat(),
                'total_stocks': total_stocks,
                'processed_stocks': list(processed_stocks),
                'matching_stocks': [
                    {
                        'ticker': ticker,
                        'company_name': company_name,
                        'data': data.to_json()
                    }
                    for ticker, company_name, data in matching_stocks
                ],
                'stocks_with_issues': [
                    {
                        'ticker': ticker,
                        'company_name': company_name,
                        'data': data.to_json()
                    }
                    for ticker, company_name, data in stocks_with_issues
                ]
            }

            with open(progress_file, 'w') as f:
                json.dump(progress_data, f)
        except Exception as e:
            print(f"Error saving progress: {e}")

    def get_progress_from_cache(self, pattern, interval, exchange):
        cache_key = self.get_cache_key(pattern, interval, exchange)
        progress_file = os.path.join(self.cache_dir, f"{cache_key}_progress.json")

        if not os.path.exists(progress_file):
            return None

        try:
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)

            # Validate cache data
            required_keys = ['last_update', 'total_stocks', 'processed_stocks', 'matching_stocks', 'stocks_with_issues']
            if not all(key in progress_data for key in required_keys):
                return None

            last_update = datetime.fromisoformat(progress_data['last_update'])
            if (datetime.now(pytz.UTC) - last_update) > timedelta(hours=12):
                self.clear_progress_cache(pattern, interval, exchange)
                return None

            # Validate total_stocks
            if progress_data['total_stocks'] <= 0:
                return None

            matching_stocks = [
                (
                    stock['ticker'],
                    stock['company_name'],
                    pd.read_json(StringIO(stock['data']))
                )
                for stock in progress_data['matching_stocks']
            ]

            stocks_with_issues = [
                (
                    stock['ticker'],
                    stock['company_name'],
                    pd.read_json(StringIO(stock['data']))
                )
                for stock in progress_data['stocks_with_issues']
            ]

            return {
                'processed_stocks': set(progress_data['processed_stocks']),
                'matching_stocks': matching_stocks,
                'stocks_with_issues': stocks_with_issues,
                'total_stocks': progress_data['total_stocks']
            }

        except Exception as e:
            print(f"Error reading progress cache: {e}")
            self.clear_progress_cache(pattern, interval, exchange)
            return None

    def clear_progress_cache(self, pattern, interval, exchange):
        try:
            cache_key = self.get_cache_key(pattern, interval, exchange)
            for suffix in ['_progress.json', '_final.json']:
                cache_file = os.path.join(self.cache_dir, f"{cache_key}{suffix}")
                if os.path.exists(cache_file):
                    os.remove(cache_file)
        except Exception as e:
            print(f"Error clearing cache: {e}")

    def save_final_results(self, pattern, interval, exchange, matching_stocks, stocks_with_issues, total_stocks):
        """Save final results to a separate cache file"""
        try:
            cache_key = self.get_cache_key(pattern, interval, exchange)
            results_file = os.path.join(self.cache_dir, f"{cache_key}_final.json")
            
            results_data = {
                'timestamp': datetime.now(pytz.UTC).isoformat(),
                'total_stocks': total_stocks,
                'matching_stocks': [
                    {
                        'ticker': ticker,
                        'company_name': company_name,
                        'data': data.to_json()
                    }
                    for ticker, company_name, data in matching_stocks
                ],
                'stocks_with_issues': [
                    {
                        'ticker': ticker,
                        'company_name': company_name,
                        'data': data.to_json()
                    }
                    for ticker, company_name, data in stocks_with_issues
                ]
            }
            
            with open(results_file, 'w') as f:
                json.dump(results_data, f)
        except Exception as e:
            print(f"Error saving final results: {e}")

    def get_final_results(self, pattern, interval, exchange):
        """Get final results from cache"""
        try:
            cache_key = self.get_cache_key(pattern, interval, exchange)
            results_file = os.path.join(self.cache_dir, f"{cache_key}_final.json")
            
            if not os.path.exists(results_file):
                return None
                
            with open(results_file, 'r') as f:
                results_data = json.load(f)
                
            # Validate timestamp - clear if older than 12 hours
            timestamp = datetime.fromisoformat(results_data['timestamp'])
            if (datetime.now(pytz.UTC) - timestamp) > timedelta(hours=12):
                os.remove(results_file)
                return None
                
            matching_stocks = [
                (
                    stock['ticker'],
                    stock['company_name'],
                    pd.read_json(StringIO(stock['data']))
                )
                for stock in results_data['matching_stocks']
            ]
            
            stocks_with_issues = [
                (
                    stock['ticker'],
                    stock['company_name'],
                    pd.read_json(StringIO(stock['data']))
                )
                for stock in results_data['stocks_with_issues']
            ]
            
            return {
                'matching_stocks': matching_stocks,
                'stocks_with_issues': stocks_with_issues,
                'total_stocks': results_data['total_stocks']
            }
        except Exception as e:
            print(f"Error reading final results: {e}")
            return None