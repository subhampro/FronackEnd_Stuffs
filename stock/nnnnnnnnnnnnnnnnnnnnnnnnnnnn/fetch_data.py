import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_all_tickers():
    """Fetch all NSE stocks using Yahoo Finance"""
    try:
        # Use Yahoo Finance API to get Indian stocks
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
        
        # Extract symbols and filter NSE stocks
        stocks = []
        if 'quotes' in df['finance']['result'][0]:
            quotes = df['finance']['result'][0]['quotes']
            stocks = [q['symbol'] for q in quotes if '.NS' in q['symbol']]
            
            # Filter out Nifty50 stocks (usually have high market cap)
            stocks = [s for s in stocks if not any(x in s for x in ['NIFTY', 'SENSEX', 'BANKNIFTY'])]
        
        return stocks if stocks else []
    except Exception as e:
        print(f"Error fetching stock list: {e}")
        # Comprehensive list of active mid and small cap stocks
        return [
            # New Age Tech & Digital
            "ZOMATO.NS", "NYKAA.NS", "PAYTM.NS", "POLICYBZR.NS", "DELHIVERY.NS",
            
            # IT & Software
            "PERSISTENT.NS", "LTTS.NS", "COFORGE.NS", "HAPPSTMNDS.NS", "TANLA.NS",
            
            # Pharma & Healthcare
            "ALKEM.NS", "TORNTPHARM.NS", "AUROPHARMA.NS", "BIOCON.NS", "NATCO.NS",
            
            # Manufacturing & Industrial
            "DIXON.NS", "AMBER.NS", "POLYCAB.NS", "VGUARD.NS", "BLUESTARCO.NS",
            
            # Financial Services
            "MUTHOOTFIN.NS", "CHOLAFIN.NS", "MANAPPURAM.NS", "MASFIN.NS", "CREDITACC.NS",
            
            # Chemical & Materials
            "CLEAN.NS", "DEEPAKFERT.NS", "AARTIIND.NS", "ALKYLAMINE.NS", "GALAXYSURF.NS",
            
            # Consumer & Retail
            "VSTIND.NS", "RADICO.NS", "METROPOLIS.NS", "RELAXO.NS", "PGHL.NS",
            
            # Infrastructure & Real Estate
            "OBEROIRLTY.NS", "PRESTIGE.NS", "BRIGADE.NS", "SOBHA.NS", "MAHLIFE.NS",
            
            # Energy & Utilities
            "TATAPOWER.NS", "TORNTPOWER.NS", "KAVERITEL.NS", "MNRE.NS", "GIPCL.NS",
            
            # Others
            "LXCHEM.NS", "KIMS.NS", "CAMPUS.NS", "MEDPLUS.NS", "LATENTVIEW.NS"
        ]

def fetch_stock_data(ticker, interval='1h'):
    try:
        stock = yf.Ticker(ticker)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        # Get real-time data
        data = stock.history(period="1mo", interval=interval)
        if data.empty:
            return pd.DataFrame()
            
        return data
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()

def get_company_name(ticker):
    try:
        symbol = ticker.replace('.NS', '')
        url = f"https://www1.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol={symbol}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        company_name = soup.find('h2').text.strip()
        return company_name
    except:
        return ticker.replace('.NS', '')