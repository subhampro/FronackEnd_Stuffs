try:
    import matplotlib
    matplotlib.use('Agg')
    import mplfinance as mpf  # type: ignore
    import matplotlib.pyplot as plt
except ImportError as e:
    print(f"Error importing required libraries: {e}")
    print("Please ensure mplfinance is installed in your virtual environment:")
    print("1. Activate your virtual environment")
    print("2. Run: pip install mplfinance")
    raise

def plot_candlestick(data, ticker, company_name):
    try:
        # Clear any existing plots
        plt.close('all')
        
        # Create the candlestick chart
        mpf.plot(data, 
                type='candle', 
                style='charles',
                title=f"{company_name} ({ticker})",
                volume=True,
                savefig='chart.png',
                figsize=(12, 8))
                
    except Exception as e:
        print(f"Error plotting chart for {ticker}: {str(e)}")
        # Create a blank figure if plotting fails
        plt.figure(figsize=(12, 8))
        plt.text(0.5, 0.5, f"Error plotting chart: {str(e)}", 
                ha='center', va='center')
        plt.savefig('chart.png')
        plt.close()

# To install mplfinance, run the following command:
# pip install mplfinance