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
    if 'stocks_with_issues' not in st.session_state:
        st.session_state.stocks_with_issues = []
    if 'stop_scan' not in st.session_state:
        st.session_state.stop_scan = False
    if 'scanning' not in st.session_state:
        st.session_state.scanning = False
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {
            'pattern': 'Volatility Contraction',
            'interval': '1h',
            'exchange': 'NSE'
        }

    def stop_scan():
        st.session_state.stop_scan = True
        st.session_state.scanning = False

    def new_search():
        st.session_state.scanning = False
        st.session_state.stop_scan = False
        st.session_state.matching_stocks = []
        st.session_state.stocks_with_issues = []
        st.rerun()

    if not st.session_state.scanning:
        with st.form(key='scan_form'):
            st.title("Indian Stock Market Screener")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                pattern = st.selectbox(
                    "Select the chart Pattern",
                    ["Volatility Contraction", "Lucifer Custom Filter"]
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
                    ["NSE", "NIFTY50", "ALL"],
                    index=0
                )
            
            submitted = st.form_submit_button("Scan for Patterns")
            if submitted:
                st.session_state.form_data = {
                    'pattern': pattern,
                    'interval': interval,
                    'exchange': exchange
                }
                st.session_state.scanning = True
                st.rerun()

    if st.session_state.scanning:
        pattern = st.session_state.form_data['pattern']
        interval = st.session_state.form_data['interval']
        exchange = st.session_state.form_data['exchange']
        
        st.session_state.matching_stocks = []
        st.session_state.stocks_with_issues = []
        st.session_state.stop_scan = False
        
        tickers = fetch_all_tickers(exchange)
        if not tickers:
            st.error("Unable to fetch stock list. Please try again later.")
            return
            
        total_stocks = len(tickers)
        start_time = datetime.now()
        stocks_processed = 0
        
        scan_container = st.container()
        with scan_container:
            st.markdown("""
                <div class="scan-container">
                    <div class="website-header">
                        <h2 class="header-title">Indian Stock Market Screener By SubhaM</h2>
                    </div>
                    """, unsafe_allow_html=True)
            
            st.markdown(f'''
                <div class="scan-status">
                    <div class="scan-status-left">
                        <h2>🔍 Stock Scanner</h2>
                        <div class="scan-settings">
                            <span class="scan-option">Pattern: {pattern}</span>
                            <span class="scan-option">Interval: {interval}</span>
                            <span class="scan-option">Exchange: {exchange}</span>
                        </div>
                    </div>
                    <div class="scan-status-right">
                        <button class="new-search-button" onclick="window.location.href=window.location.pathname">
                            <span class="button-icon">🔄</span>
                            <span class="button-text">New Search</span>
                        </button>
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            progress_container = st.empty()
            stats_container = st.empty()
            stop_button_container = st.empty()
            results_container = st.container()
            results_header = st.empty()
            fetched_header = st.empty()
            
            stop_button_container.button(
                "🛑 Stop Scan",
                key="stop_scan_button",
                on_click=stop_scan,
                type="primary"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        try:
            for i, ticker in enumerate(tickers):
                if st.session_state.stop_scan:
                    st.warning(f"Scan stopped by user after processing {i} stocks")
                    break
                
                progress = (i + 1) / total_stocks
                elapsed_time = (datetime.now() - start_time).seconds
                eta = int((elapsed_time / (i + 1)) * (total_stocks - i - 1)) if i > 0 else 0
                
                progress_container.markdown(f"""
                    <div class="scan-progress">
                        <div style="width: {progress*100}%"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                stats_container.markdown(f"""
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-label">Progress</div>
                            <div class="stat-value">{progress*100:.1f}%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Stocks Scanned</div>
                            <div class="stat-value">{i+1}/{total_stocks}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Time Elapsed</div>
                            <div class="stat-value">{elapsed_time}s</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">ETA</div>
                            <div class="stat-value">{eta}s</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                data, has_period_issues = fetch_stock_data(ticker, interval)
                if not data.empty:
                    company_name = get_company_name(ticker)
                    fetched_header.info(f"Processing {ticker}...")
                    
                    if has_period_issues:
                        st.session_state.stocks_with_issues.append((ticker, company_name, data))
                    
                    if detect_pattern(data, pattern, ticker):
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
                
        finally:
            progress_container.empty()
            stats_container.empty()
            stop_button_container.empty()
            fetched_header.empty()
            scan_container.empty()
            
            total_time = (datetime.now() - start_time).seconds
            if st.session_state.stop_scan:
                st.info(f"Scan stopped after {total_time} seconds. Showing all results...")
            else:
                st.success(f"Scan completed in {total_time} seconds!")

    if len(st.session_state.stocks_with_issues) > 0:
        st.header("All Rest Matched Stocks Old Chart Data Not Available")
        st.info(f"Found {len(st.session_state.stocks_with_issues)} stocks with data availability issues")
        
        for ticker, company_name, data in st.session_state.stocks_with_issues:
            with st.expander(f"{company_name} ({ticker}) - Limited Data", expanded=False):
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
        st.markdown("""
            <div class="new-search-container">
                <button class="new-search-button" onclick="window.location.href=window.location.pathname">🔄 New Search</button>
            </div>
        """, unsafe_allow_html=True)
    elif st.session_state.stop_scan:
        st.warning("No matching stocks found before scan was stopped")

if __name__ == "__main__":
    main()