import streamlit as st
from datetime import datetime

from ui.utils.helpers import fetch_market_data
from ui.utils.formatters import format_currency

# Data Source Manager
from ui.utils.data_source_manager import DataSourceManager


def render_dashboard(predictor, protocol, prediction, selected_stock, data_mode):

    st.title("📊 AI Blockchain Trading Dashboard")
    st.markdown("Real-time delayed market feed with AI signal overlay")

    col1, col2, col3 = st.columns(3)

    # ----------------------------
    # MARKET DATA (SAFE)
    # ----------------------------
    try:
        data_manager = DataSourceManager(mode=data_mode)
        market_data = data_manager.get_data(selected_stock) or {}

    except Exception as e:
        st.error(f"Market data error: {e}")
        return

    price = market_data.get("price", 0)
    price_series = market_data.get("historical", None)

    # ----------------------------
    # SIGNAL SAFE HANDLING
    # ----------------------------
    signal = prediction if prediction else {"signal": "HOLD", "confidence": 0}

    # ----------------------------
    # PORTFOLIO (FIXED)
    # ----------------------------
    try:
        portfolio = protocol.get_portfolio_state()

        # FIX: portfolio already returns cash directly
        portfolio_value = float(portfolio.get("cash", 0))

    except Exception as e:
        st.error(f"Portfolio error: {e}")
        portfolio_value = 0

    # ----------------------------
    # METRICS
    # ----------------------------
    with col1:
        st.metric("Current Price", format_currency(price))

    with col2:
        st.metric("AI Signal", signal.get("signal", "HOLD"))

    with col3:
        st.metric("Cash Balance", format_currency(portfolio_value))

    # ----------------------------
    # PRICE CHART
    # ----------------------------
    st.subheader("Market Price Chart")

    if price_series is not None:
        st.line_chart(price_series)
    else:
        st.warning("No historical data available")

    # ----------------------------
    # CONFIDENCE BAR
    # ----------------------------
    st.subheader("AI Confidence")

    confidence_value = int(signal.get("confidence", 0) * 100)
    confidence_value = max(0, min(confidence_value, 100))  # safety clamp

    st.progress(confidence_value)

    # ----------------------------
    # TIMESTAMP
    # ----------------------------
    st.write("Last Updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    st.markdown("---")
    st.caption("Data refreshes automatically every 10 seconds.")

    # ----------------------------
    # RETURN (FOR TRADE PANEL)
    # ----------------------------
    return {
        "signal": signal.get("signal", "HOLD"),
        "confidence": signal.get("confidence", 0),
        "price": price
    }