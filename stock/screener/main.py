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

def main():
    load_css()
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
        
        # Create placeholder for real-time results
        results_container = st.container()
        results_text = results_container.empty()
        results_area = results_container.empty()
        
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
                    
                    # Update results in real-time
                    results_text.success(f"Found {len(st.session_state.matching_stocks)} stocks matching the {pattern} pattern")
                    with results_area.container():
                        # Show only the last found stock
                        with st.expander(f"{company_name} ({ticker})", expanded=True):
                            st.write(data.tail())
                            plot_candlestick(data, ticker, company_name)
                            st.image('chart.png')
                    
                stocks_processed += 1
                
            except Exception as e:
                st.write(f"Error scanning {ticker}: {e}")
                continue
        
        # Show final results
        total_time = (datetime.now() - start_time).seconds
        if st.session_state.stop_scan:
            st.info(f"Scan stopped after {total_time} seconds. Showing all results...")
        else:
            progress_bar.progress(1.0)
            st.success(f"Scan completed in {total_time} seconds!")

    # Show complete results list
    if st.session_state.matching_stocks:
        st.header("All Matching Stocks")
        for ticker, company_name, data in st.session_state.matching_stocks:
            with st.expander(f"{company_name} ({ticker})"):
                st.write(data.tail())
                plot_candlestick(data, ticker, company_name)
                st.image('chart.png')
    elif st.session_state.stop_scan:
        st.warning("No matching stocks found before scan was stopped")

if __name__ == "__main__":
    main()