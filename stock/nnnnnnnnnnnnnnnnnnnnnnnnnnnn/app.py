import streamlit as st
from fetch_data import fetch_stock_data, get_company_name, fetch_all_tickers
from plot_chart import plot_candlestick
from pattern_detection import detect_pattern
from datetime import datetime

def main():
    # Initialize session state
    if 'matching_stocks' not in st.session_state:
        st.session_state.matching_stocks = []
    if 'stop_scan' not in st.session_state:
        st.session_state.stop_scan = False

    def stop_scan():
        st.session_state.stop_scan = True

    st.title("Indian Stock Market Screener")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pattern = st.selectbox(
            "Select the chart pattern to search for:",
            ["volatility_contraction"]
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
        # Reset state for new scan
        st.session_state.matching_stocks = []
        st.session_state.stop_scan = False
        
        tickers = fetch_all_tickers(exchange)
        if not tickers:
            st.error("Unable to fetch stock list. Please try again later.")
            return
            
        total_stocks = len(tickers)
        st.info(f"Found {total_stocks} stocks to scan. Estimated time: {total_stocks * 2} seconds")
        st.write(f"Scanning for {pattern} pattern...")
        
        # Create stop button
        st.button("Stop Scan", on_click=stop_scan, key='stop_button')
        
        progress_text = st.empty()
        progress_bar = st.progress(0)
        stats_text = st.empty()
        
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
                if not data.empty and detect_pattern(data, pattern):
                    company_name = get_company_name(ticker)
                    st.session_state.matching_stocks.append((ticker, company_name, data))
                    
                stocks_processed += 1
                
            except Exception as e:
                st.write(f"Error scanning {ticker}: {e}")
                continue
        
        # Show results
        total_time = (datetime.now() - start_time).seconds
        if st.session_state.stop_scan:
            st.info(f"Scan stopped after {total_time} seconds. Showing partial results...")
        else:
            progress_bar.progress(1.0)
            st.success(f"Scan completed in {total_time} seconds!")
    
    # Always show results if we have any matches (even after stopping)
    if st.session_state.matching_stocks:
        st.success(f"Found {len(st.session_state.matching_stocks)} stocks matching the {pattern} pattern")
        for ticker, company_name, data in st.session_state.matching_stocks:
            with st.expander(f"{company_name} ({ticker})"):
                st.write(data.tail())
                plot_candlestick(data, ticker, company_name)
                st.image('chart.png')
    elif st.session_state.stop_scan:
        st.warning("No matching stocks found before scan was stopped")

if __name__ == "__main__":
    main()