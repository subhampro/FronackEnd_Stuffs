import streamlit as st
from fetch_data import fetch_stock_data, get_company_name, fetch_all_tickers
from plot_chart import plot_candlestick
from pattern_detection import detect_pattern
from datetime import datetime

st.set_page_config(
    page_title="Indian Stock Market Screener",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

def load_css():
    with open('static/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def get_tradingview_url(ticker):
    symbol = ticker.replace('.NS', '')
    return f"https://www.tradingview.com/chart?symbol=NSE:{symbol}"

def main():
    load_css()
    if 'matching_stocks' not in st.session_state:
        st.session_state.matching_stocks = []
    if 'fetched_stocks' not in st.session_state:
        st.session_state.fetched_stocks = []
    if 'stop_scan' not in st.session_state:
        st.session_state.stop_scan = False

    def stop_scan():
        st.session_state.stop_scan = True

    st.title("Indian Stock Market Screener")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pattern = st.selectbox(
            "Select the chart pattern to search for:",
            ["Volatility Contraction"]
        )
    with col2:
        interval = st.selectbox(
            "Select time interval:",
            ["1h", "15m", "30m", "1d", "5d"],
            index=0
        )
    with col3:
        exchange = st.selectbox(
            "Select exchange:",
            ["NSE", "ALL"],
            index=0
        )
    
    if st.button("Scan for Patterns"):

        st.session_state.matching_stocks = []
        st.session_state.fetched_stocks = []
        st.session_state.stop_scan = False
        
        tickers = fetch_all_tickers(exchange)
        if not tickers:
            st.error("Unable to fetch stock list. Please try again later.")
            return
            
        total_stocks = len(tickers)
        st.info(f"Found {total_stocks} stocks to scan. Estimated time: {total_stocks * 2} seconds")
        st.write(f"Scanning for {pattern} pattern...")

        st.button("Stop Scan", on_click=stop_scan, key='stop_button')
        
        progress_text = st.empty()
        progress_bar = st.progress(0)
        stats_text = st.empty()
        
        results_header = st.empty()
        fetched_header = st.empty()
        results_container = st.container()
        fetched_container = st.container()
        
        start_time = datetime.now()
        stocks_processed = 0
        
        for i, ticker in enumerate(tickers):
            try:
                if st.session_state.stop_scan:
                    st.warning(f"Scan stopped by user after processing {i} stocks")
                    break
                
                progress = (i + 1) / total_stocks
                elapsed_time = (datetime.now() - start_time).seconds
                eta = (elapsed_time / (i + 1)) * (total_stocks - i - 1) if i > 0 else 0
                
                progress_text.text(f"Processing {ticker} ({i+1}/{total_stocks})")
                progress_bar.progress(progress)
                stats_text.text(f"Elapsed: {elapsed_time}s | ETA: {int(eta)}s | Found: {len(st.session_state.matching_stocks)} matches")
                
                data = fetch_stock_data(ticker, interval)
                if not data.empty:
                    company_name = get_company_name(ticker)
                    st.session_state.fetched_stocks.append((ticker, company_name, data))
                    fetched_header.info(f"Successfully fetched data for {len(st.session_state.fetched_stocks)} stocks")
                    
                    if detect_pattern(data, pattern):
                        st.session_state.matching_stocks.append((ticker, company_name, data))
                        results_header.success(f"Found {len(st.session_state.matching_stocks)} stocks matching the {pattern} pattern")
                        
                        with results_container:
                            with st.expander(f"{company_name} ({ticker}) - Pattern Match", expanded=True):
                                col1, col2 = st.columns([4, 1])
                                with col1:
                                    st.write(data.tail())
                                with col2:
                                    st.markdown(
                                        f'<a href="{get_tradingview_url(ticker)}" target="_blank" class="tradingview-button">'
                                        '📊 TradingView</a>',
                                        unsafe_allow_html=True
                                    )
                                plot_candlestick(data, ticker, company_name)
                                st.image('chart.png')
                    
                stocks_processed += 1
                
            except Exception as e:
                st.write(f"Error scanning {ticker}: {e}")
                continue
        
        total_time = (datetime.now() - start_time).seconds
        if st.session_state.stop_scan:
            st.info(f"Scan stopped after {total_time} seconds. Showing all results...")
        else:
            progress_bar.progress(1.0)
            st.success(f"Scan completed in {total_time} seconds!")

    # Display all successfully fetched stocks
    if st.session_state.fetched_stocks:
        st.header("All Stocks with Available Data")
        for ticker, company_name, data in st.session_state.fetched_stocks:
            with st.expander(f"{company_name} ({ticker})", expanded=False):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(data.tail())
                with col2:
                    st.markdown(
                        f'<a href="{get_tradingview_url(ticker)}" target="_blank" class="tradingview-button">'
                        '📊 TradingView</a>',
                        unsafe_allow_html=True
                    )
                plot_candlestick(data, ticker, company_name)
                st.image('chart.png')
    
    # Display pattern matching stocks
    if st.session_state.matching_stocks:
        st.header("Stocks Matching Pattern")
        for ticker, company_name, data in st.session_state.matching_stocks:
            with st.expander(f"{company_name} ({ticker})"):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(data.tail())
                with col2:
                    st.markdown(
                        f'<a href="{get_tradingview_url(ticker)}" target="_blank" class="tradingview-button">'
                        '📊 TradingView</a>',
                        unsafe_allow_html=True
                    )
                plot_candlestick(data, ticker, company_name)
                st.image('chart.png')
    elif st.session_state.stop_scan:
        st.warning("No matching stocks found before scan was stopped")

if __name__ == "__main__":
    main()