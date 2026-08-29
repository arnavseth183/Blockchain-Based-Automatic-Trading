import streamlit as st
import time


def render_trade_panel(prediction, selected_stock, protocol, execution_mode):

    st.title("⚡ AI Assisted Trade Panel")
    st.markdown("Manual + Auto execution over AI signals")

    # --------------------------------------
    # SESSION STATE
    # --------------------------------------
    if "last_trade_time" not in st.session_state:
        st.session_state.last_trade_time = 0

    if "last_signal" not in st.session_state:
        st.session_state.last_signal = None

    COOLDOWN_SECONDS = 10

    # --------------------------------------
    # SAFE SIGNAL
    # --------------------------------------
    action = str(prediction.get("signal", "HOLD"))
    confidence = float(prediction.get("confidence", 0))
    price = float(prediction.get("price", 0))

    st.info(f"🔒 AI Signal: {action}")

    # --------------------------------------
    # PORTFOLIO SAFE READ
    # --------------------------------------
    portfolio = protocol.get_portfolio_state()
    cash = float(portfolio.get("cash", 0))
    positions = portfolio.get("positions", {})

    def get_qty(symbol):
        """SAFE extractor for both int and dict formats"""
        val = positions.get(symbol, 0)

        if isinstance(val, dict):
            return int(val.get("quantity", 0))
        try:
            return int(val)
        except:
            return 0

    # --------------------------------------
    # CURRENT PRICE + AVG PRICE (FIXED)
    # --------------------------------------
    existing = positions.get(selected_stock, {})
    if isinstance(existing, dict):
        avg_price = float(existing.get("price", 0))
    else:
        avg_price = 0.0

    colp1, colp2 = st.columns(2)

    with colp1:
        st.metric("Current Market Price", f"₹ {price:.2f}")

    with colp2:
        # ✅ FIX: hide when 0
        if avg_price and avg_price > 0:
            st.metric("Avg Buy Price", f"₹ {avg_price:.2f}")
        else:
            st.empty()

    # --------------------------------------
    # SIDEBAR
    # --------------------------------------
    st.sidebar.markdown("### 💰 Portfolio")
    st.sidebar.write("Cash:", cash)
    st.sidebar.write("Positions:", positions)

    # --------------------------------------
    # UI
    # --------------------------------------
    st.subheader("AI Recommendation")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Signal", action)

    with col2:
        st.metric("Confidence", f"{confidence * 100:.2f}%")

    if action == "BUY":
        st.success("Recommended: BUY")
    elif action == "SELL":
        st.error("Recommended: SELL")
    else:
        st.warning("Recommended: HOLD")

    st.markdown("---")

    # --------------------------------------
    # INPUT
    # --------------------------------------
    quantity = int(st.number_input("Quantity", min_value=1, value=10))

    # --------------------------------------
    # PAYLOAD
    # --------------------------------------
    signal_payload = {
        "stock": selected_stock,
        "signal": action,
        "confidence": confidence,
        "price": price,
        "quantity": quantity,
        "user": st.session_state.get("user_wallet")
    }

    # --------------------------------------
    # VALIDATION
    # --------------------------------------
    def can_trade():

        if action == "HOLD":
            return False, "Hold signal"

        if confidence < 0.4:
            return False, "Low confidence"

        if price <= 0:
            return False, "Invalid price"

        if action == "BUY":
            if cash < price * quantity:
                return False, "Insufficient balance"

        if action == "SELL":
            qty = get_qty(selected_stock)
            if qty < quantity:
                return False, "Not enough holdings"

        return True, "OK"

    allowed, reason = can_trade()

    # --------------------------------------
    # EXECUTION
    # --------------------------------------
    def execute_trade():
        try:
            tx = protocol.execute_trade(signal_payload)

            st.success("✅ Trade Executed")
            st.json(tx)

            st.session_state.last_trade_time = time.time()
            st.session_state.last_signal = action

        except Exception as e:
            st.error(f"Trade failed: {e}")

    # --------------------------------------
    # AUTO MODE
    # --------------------------------------
    if execution_mode == "AUTO":

        now = time.time()

        if (
            allowed
            and action in ["BUY", "SELL"]
            and now - st.session_state.last_trade_time > COOLDOWN_SECONDS
        ):
            execute_trade()
        else:
            st.info(f"Auto waiting: {reason}")

    # --------------------------------------
    # MANUAL MODE
    # --------------------------------------
    if st.button("Execute Trade"):

        if allowed:
            execute_trade()
        else:
            st.warning(f"Blocked: {reason}")

        with st.expander("Debug Payload"):
            st.json(signal_payload)

    st.markdown("---")
    st.caption("Trades processed via protocol layer (simulation mode)")