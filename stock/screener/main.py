import streamlit as st
from fetch_data import fetch_stock_data, get_company_name, fetch_all_tickers
from plot_chart import plot_candlestick
from pattern_detection import detect_pattern, generate_summary_report
from datetime import datetime
from cache_manager import CacheManager

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
    cache_manager = CacheManager()

    def display_results():
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
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.button("🔄 New Search", key="new_search_button", 
                         help="Start a new stock scan", on_click=trigger_reset)
        elif st.session_state.stop_scan:
            st.warning("No matching stocks found before scan was stopped")

    # Initialize session state
    if 'should_reset' not in st.session_state:
        st.session_state.should_reset = False
        st.session_state.total_stocks = 0
        
    # Reset all states if should_reset is True
    if st.session_state.should_reset:
        st.session_state.matching_stocks = []
        st.session_state.stocks_with_issues = []
        st.session_state.stop_scan = False
        st.session_state.scanning = False
        st.session_state.total_stocks = 0
        st.session_state.should_reset = False
        st.session_state.form_data = {
            'pattern': 'Volatility Contraction',
            'interval': '1h',
            'exchange': 'NSE'
        }
    
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

    def trigger_reset():
        st.session_state.should_reset = True

    if not st.session_state.scanning:
        with st.form(key='scan_form'):
            st.title("Indian Stock Market Screener")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                pattern = st.selectbox(
                    "Select the chart Pattern",
                    ["Volatility Contraction", "Low Volume Stock Selection", "15% Reversal"]
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

        tickers = fetch_all_tickers(exchange)
        if not tickers:
            st.error("Unable to fetch stock list. Please try again later.")
            return

        progress_data = cache_manager.get_progress_from_cache(pattern, interval, exchange)
        
        if progress_data and not st.session_state.should_reset:
            processed_stocks = progress_data['processed_stocks']
            st.session_state.matching_stocks = progress_data['matching_stocks']
            st.session_state.stocks_with_issues = progress_data['stocks_with_issues']
            total_stocks = progress_data['total_stocks']
            stocks_processed = len(processed_stocks)
            initial_progress = stocks_processed / total_stocks
            
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
                    </div>
                </div>
            ''', unsafe_allow_html=True)
            
            with st.container():
                st.button("🔄 New Search", key="new_search_status", 
                         help="Start a new stock scan", on_click=trigger_reset)
            
            progress_container = st.empty()
            stats_container = st.empty()
            stop_button_container = st.empty()
            resume_info = st.empty()
            results_container = st.container()
            results_header = st.empty()
            fetched_header = st.empty()
            
            stop_button_container.button(
                "🛑 Stop Scan",
                key="stop_scan_button",
                on_click=stop_scan,
                type="primary"
            )

            if progress_data and not st.session_state.should_reset:
                resume_info.info(f"Resuming scan from {stocks_processed} previously processed stocks ({initial_progress:.1%})")
                if st.session_state.matching_stocks:
                    with results_container:
                        st.success(f"Found {len(st.session_state.matching_stocks)} stocks matching the {pattern} pattern")
                        for ticker, company_name, data in st.session_state.matching_stocks:
                            with st.expander(f"{company_name} ({ticker}) - Pattern Match", expanded=False):
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
            
            st.markdown('</div>', unsafe_allow_html=True)

        # Add total_processed counter to session state
        if 'total_processed' not in st.session_state:
            st.session_state.total_processed = 0

        # Add resume_start_time to track elapsed time for resumed scans
        if 'resume_start_time' not in st.session_state:
            st.session_state.resume_start_time = datetime.now()
            st.session_state.initial_processed = 0

        # Reset counter when starting fresh
        if not progress_data or st.session_state.should_reset:
            st.session_state.total_processed = 0
            processed_stocks = set()
            total_stocks = len(tickers)
            st.session_state.total_stocks = total_stocks
            stocks_processed = 0
            initial_progress = 0
            st.session_state.resume_start_time = datetime.now()
            st.session_state.initial_processed = 0
        else:
            # Use cached progress data
            processed_stocks = progress_data['processed_stocks']
            st.session_state.total_processed = len(processed_stocks)
            st.session_state.total_stocks = progress_data['total_stocks']
            stocks_processed = st.session_state.total_processed
            initial_progress = stocks_processed / st.session_state.total_stocks
            if 'initial_processed' not in st.session_state:
                st.session_state.initial_processed = stocks_processed

        # Filter out already processed stocks
        if progress_data and not st.session_state.should_reset:
            tickers = [t for t in tickers if t not in processed_stocks]

        start_time = datetime.now()
        
        # Check for final results first
        final_results = None if st.session_state.should_reset else cache_manager.get_final_results(pattern, interval, exchange)
        if final_results:
            st.session_state.matching_stocks = final_results['matching_stocks']
            st.session_state.stocks_with_issues = final_results['stocks_with_issues']
            st.session_state.total_stocks = final_results['total_stocks']
            st.session_state.scanning = False
            display_results()
            return

        try:
            for i, ticker in enumerate(tickers):
                if st.session_state.stop_scan:
                    st.warning(f"Scan stopped by user after processing {st.session_state.total_processed} stocks")
                    break

                processed_stocks.add(ticker)
                st.session_state.total_processed = len(processed_stocks)
                progress = min(st.session_state.total_processed / st.session_state.total_stocks, 1.0)
                
                if i % 10 == 0 or st.session_state.stop_scan:
                    cache_manager.save_progress_to_cache(
                        pattern,
                        interval,
                        exchange,
                        processed_stocks,
                        st.session_state.matching_stocks,
                        st.session_state.stocks_with_issues,
                        st.session_state.total_stocks
                    )

                elapsed_time = max(1, (datetime.now() - st.session_state.resume_start_time).seconds)
                processed_since_resume = st.session_state.total_processed - st.session_state.initial_processed
                
                if processed_since_resume > 0 and elapsed_time > 0:
                    stocks_per_second = processed_since_resume / elapsed_time
                    remaining_stocks = st.session_state.total_stocks - st.session_state.total_processed
                    eta = int(remaining_stocks / stocks_per_second) if stocks_per_second > 0 else 0
                else:
                    eta = 0
                
                progress_container.markdown(f"""
                    <div class="scan-progress">
                        <div style="width: {progress*100}%"></div>
                    </div>
                """, unsafe_allow_html=True)
                
                stats_container.markdown(f"""
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-label">Progress</div>
                            <div class="stat-value">{min(progress*100, 100):.1f}%</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Stocks Scanned</div>
                            <div class="stat-value">{st.session_state.total_processed}/{st.session_state.total_stocks}</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">Time Elapsed</div>
                            <div class="stat-value">{elapsed_time}s</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-label">ETA</div>
                            <div class="stat-value">{max(0, eta)}s</div>
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
            
            if not st.session_state.stop_scan and st.session_state.total_processed >= st.session_state.total_stocks:
                # Save final results when scan completes
                cache_manager.save_final_results(
                    pattern,
                    interval,
                    exchange,
                    st.session_state.matching_stocks,
                    st.session_state.stocks_with_issues,
                    st.session_state.total_stocks
                )
                cache_manager.clear_progress_cache(pattern, interval, exchange)
                st.session_state.scanning = False
                
        finally:
            if st.session_state.stop_scan:
                cache_manager.save_progress_to_cache(
                    pattern,
                    interval,
                    exchange,
                    processed_stocks,
                    st.session_state.matching_stocks,
                    st.session_state.stocks_with_issues,
                    st.session_state.total_stocks
                )

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

if __name__ == "__main__":
    main()