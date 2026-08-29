import streamlit as st
import pandas as pd
from datetime import datetime
from ui.utils.formatters import format_currency


def render_portfolio(portfolio_state):

    st.title("💼 Blockchain Portfolio View")

    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------
    if not isinstance(portfolio_state, dict):
        st.error("Invalid portfolio state")
        return

    cash = float(portfolio_state.get("cash", 0))

    tx_history = portfolio_state.get("transactions", None)
    positions = portfolio_state.get("positions", {})

    # --------------------------------------------------
    # REBUILD HOLDINGS FROM BLOCKCHAIN TX (SOURCE OF TRUTH)
    # --------------------------------------------------
    holdings = {}

    if isinstance(tx_history, list) and len(tx_history) > 0:

        # ✅ SAME NORMALIZATION AS BLOCKCHAIN EXPLORER
        normalized_events = []

        for event in tx_history:
            normalized_events.append({
                "symbol": event.get("symbol", "N/A"),
                "action": event.get("action", event.get("signal", "N/A")),
                "quantity": float(event.get("quantity", 0) or 0),
                "price": float(event.get("price", 0) or 0),
                "timestamp": event.get("timestamp", datetime.now())
            })

        df_tx = pd.DataFrame(normalized_events)

        if not df_tx.empty:

            # SAME timestamp handling
            df_tx["timestamp"] = pd.to_datetime(df_tx["timestamp"], errors="coerce")

            # IMPORTANT → chronological processing
            df_tx = df_tx.sort_values(by="timestamp")

            for _, row in df_tx.iterrows():

                symbol = row["symbol"]
                action = str(row["action"]).upper()
                qty = float(row["quantity"])
                price = float(row["price"])

                if symbol == "N/A" or qty <= 0:
                    continue

                if symbol not in holdings:
                    holdings[symbol] = {
                        "quantity": 0.0,
                        "price": price   # ✅ use price instead of avg_price
                    }

                # ✅ ALWAYS update latest price (like explorer latest row)
                holdings[symbol]["price"] = price

                # BUY
                if action == "BUY":
                    holdings[symbol]["quantity"] += qty

                # SELL
                elif action == "SELL":
                    holdings[symbol]["quantity"] -= qty
                    if holdings[symbol]["quantity"] < 0:
                        holdings[symbol]["quantity"] = 0

    # --------------------------------------------------
    # FALLBACK (LEGACY SUPPORT)
    # --------------------------------------------------
    else:
        for symbol, data in positions.items():

            if isinstance(data, dict):
                qty = float(data.get("quantity", 0) or 0)
                price = float(data.get("price", 0) or 0)
            else:
                qty = float(data or 0)
                price = 0.0

            holdings[symbol] = {
                "quantity": qty,
                "price": price
            }

    # --------------------------------------------------
    # NORMALIZE FOR DISPLAY
    # --------------------------------------------------
    normalized_positions = []

    for symbol, data in holdings.items():

        qty = float(data.get("quantity", 0))
        price = float(data.get("price", 0))

        if qty > 0:
            value = qty * price

            normalized_positions.append({
                "symbol": symbol,
                "quantity": qty,
                "price": price,   # ✅ replaced avg_price
                "value": value
            })

    df = pd.DataFrame(normalized_positions)

    # --------------------------------------------------
    # EMPTY STATE
    # --------------------------------------------------
    if df.empty:
        st.info("No open positions found.")
        st.metric("Cash Balance", format_currency(cash))
        st.metric("Total Portfolio Value", format_currency(cash))
        return

    # --------------------------------------------------
    # FINAL CALCULATIONS
    # --------------------------------------------------
    holdings_value = float(df["value"].sum())
    total_value = holdings_value + cash

    # --------------------------------------------------
    # TABLE VIEW
    # --------------------------------------------------
    st.subheader("Open Positions")

    st.dataframe(
        df.sort_values("value", ascending=False),
        use_container_width=True
    )

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Cash Balance", format_currency(cash))

    with col2:
        st.metric("Holdings Value", format_currency(holdings_value))

    with col3:
        st.metric("Total Portfolio", format_currency(total_value))

    # --------------------------------------------------
    # VISUAL BREAKDOWN
    # --------------------------------------------------
    st.subheader("Allocation Breakdown")

    if not df.empty:
        st.bar_chart(df.set_index("symbol")["value"])

    # --------------------------------------------------
    # DETAILED VIEW
    # --------------------------------------------------
    st.subheader("Detailed Position View")

    for _, row in df.iterrows():
        with st.expander(f"📊 {row['symbol']}"):

            st.write("Quantity:", row["quantity"])
            st.write("Price:", row["price"])   # ✅ updated label
            st.write("Value:", row["value"])

    st.caption("Portfolio reconstructed using latest blockchain transaction prices")