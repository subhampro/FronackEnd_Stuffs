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

    def ensure_cache_directory(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

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