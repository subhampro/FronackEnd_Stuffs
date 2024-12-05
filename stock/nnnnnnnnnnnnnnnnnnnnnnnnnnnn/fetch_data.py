import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_all_tickers():
    try:
        url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved"
        params = {
            "formatted": "true",
            "lang": "en-US",
            "region": "IN",
            "scrIds": "all_stocks_with_earnings_estimates",
            "count": 250
        }
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        df = pd.read_json(url, params=params)
        stocks = []
        if 'quotes' in df['finance']['result'][0]:
            quotes = df['finance']['result'][0]['quotes']
            stocks = [q['symbol'] for q in quotes if '.NS' in q['symbol']]
            stocks = [s for s in stocks if not any(x in s for x in ['NIFTY', 'SENSEX', 'BANKNIFTY'])]
        
        return stocks if stocks else [
            "ZOMATO.NS", "NYKAA.NS", "PAYTM.NS", "POLICYBZR.NS", "DELHIVERY.NS",
            "PERSISTENT.NS", "LTTS.NS", "COFORGE.NS", "HAPPSTMNDS.NS", "TANLA.NS",
            "ALKEM.NS", "TORNTPHARM.NS", "AUROPHARMA.NS", "BIOCON.NS", "NATCO.NS",
            "DIXON.NS", "AMBER.NS", "POLYCAB.NS", "VGUARD.NS", "BLUESTARCO.NS",
            "MUTHOOTFIN.NS", "CHOLAFIN.NS", "MANAPPURAM.NS", "MASFIN.NS", "CREDITACC.NS",
            "CLEAN.NS", "DEEPAKFERT.NS", "AARTIIND.NS", "ALKYLAMINE.NS", "GALAXYSURF.NS",
            "VSTIND.NS", "RADICO.NS", "METROPOLIS.NS", "RELAXO.NS", "PGHL.NS",
            "OBEROIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS", "SOBHA.NS", "MAHLIFE.NS",
            "TATAPOWER.NS", "TORNTPOWER.NS", "KAVERITEL.NS", "MNRE.NS", "GIPCL.NS",
            "LXCHEM.NS", "KIMS.NS", "CAMPUS.NS", "MEDPLUS.NS", "LATENTVIEW.NS"
        ]
    except Exception as e:
        print(f"Error fetching stock list: {e}")
        return []

def fetch_stock_data(ticker, interval='1h'):
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        data = stock.history(period="1mo", interval=interval)
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def get_company_name(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock.info['longName']
    except:
        return ticker.replace('.NS', '')