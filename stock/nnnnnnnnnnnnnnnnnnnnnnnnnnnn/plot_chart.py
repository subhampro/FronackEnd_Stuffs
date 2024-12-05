import mplfinance as mpf

def plot_candlestick(data, ticker, company_name):
    mpf.plot(data, type='candle', style='charles', title=f"{company_name} ({ticker})", volume=True, savefig='chart.png')