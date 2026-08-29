import streamlit as st
import logging
import os
import time
import base64
from streamlit_autorefresh import st_autorefresh

from config import AppConfig
from ai_oracle.prediction.predictor import Predictor
from blockchain_protocol.execution_engine.protocol_controller import ProtocolController
from blockchain_protocol.web3_layer.web3_provider import get_web3_connection

from ui.pages.dashboard import render_dashboard
from ui.pages.trade_panel import render_trade_panel
from ui.pages.portfolio import render_portfolio
from ui.pages.blockchain_explorer import render_blockchain_explorer
from ui.components.sidebar import render_sidebar

from blockchain_protocol.storage.user_wallet_registry import UserWalletRegistry

# --------------------------------------------------
# BACKGROUND IMAGES (FIXED VERSION)
# --------------------------------------------------

def get_base64(img_path):
    with open(img_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = get_base64("C:/Users/arnav/decentralized_ai_blockchain_trading/image1.jpg")
img2 = get_base64("C:/Users/arnav/decentralized_ai_blockchain_trading/image2.jpg")
img3 = get_base64("C:/Users/arnav/decentralized_ai_blockchain_trading/image3.jpg")
img4 = get_base64("C:/Users/arnav/decentralized_ai_blockchain_trading/image4.jpg")

st.markdown(
    f"""
    <style>
    .stApp {{
        background-size: cover;
        animation: slide 20s infinite;
    }}

    @keyframes slide {{
        0% {{
            background-image: url("data:image/jpg;base64,{img1}");
        }}
        25% {{
            background-image: url("data:image/jpg;base64,{img2}");
        }}
        50% {{
            background-image: url("data:image/jpg;base64,{img3}");
        }}
        75% {{
            background-image: url("data:image/jpg;base64,{img4}");
        }}
        100% {{
            background-image: url("data:image/jpg;base64,{img1}");
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# SETUP
# --------------------------------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

st.set_page_config(
    page_title="Decentralized AI Blockchain Trading",
    layout="wide"
)

config = AppConfig()

st_autorefresh(interval=10000, key="live_refresh")

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_wallet" not in st.session_state:
    st.session_state.user_wallet = None

# FIX: AUTO TRADE COOLDOWN STATE
if "last_auto_trade" not in st.session_state:
    st.session_state.last_auto_trade = 0

AUTO_COOLDOWN = 20  # seconds

# --------------------------------------------------
# LOGIN SYSTEM
# --------------------------------------------------

registry = UserWalletRegistry()

if not st.session_state.logged_in:

    st.title("🔐 Blockchain Trading Login")

    tab1, tab2, tab3 = st.tabs(["Login", "Create Account", "Forgot Password"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            user = registry.authenticate_user(username, password)

            if user:
                st.session_state.logged_in = True
                st.session_state.user_wallet = user["wallet_address"]
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        username_new = st.text_input("New Username")
        password_new = st.text_input("New Password", type="password")

        if st.button("Create Account"):
            account = registry.create_user(username_new, password_new)
            st.success("Account created")
            st.code(account["wallet_address"])

    with tab3:
        st.info("Use private key reset (if implemented)")

    st.stop()

# --------------------------------------------------
# LOAD CORE ENGINE
# --------------------------------------------------

@st.cache_resource
def load_predictor():
    return Predictor(config)

@st.cache_resource
def load_protocol():
    web3 = get_web3_connection()
    return ProtocolController(config, web3)

predictor = load_predictor()
protocol = load_protocol()

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

page, data_mode, execution_mode = render_sidebar()

st.sidebar.write("Logged in:")
st.sidebar.code(st.session_state.user_wallet)

if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_wallet = None
    st.rerun()

# --------------------------------------------------
# STOCK SELECTION
# --------------------------------------------------

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    config.SUPPORTED_STOCKS
)

# --------------------------------------------------
# MARKET + PREDICTION
# --------------------------------------------------

market_data = None
prediction = {"signal": "HOLD", "confidence": 0.0, "price": 0.0}

try:
    market_data = predictor.fetch_latest_data(selected_stock)

    if market_data is not None and len(market_data) > 0:
        prediction = predictor.generate_signal(market_data)
        prediction["price"] = float(market_data["Close"].iloc[-1])

except Exception as e:
    st.error(f"Prediction error: {e}")
    logging.error(e)

# --------------------------------------------------
# AUTO EXECUTION
# --------------------------------------------------

if (
    execution_mode == "AUTO"
    and market_data is not None
    and prediction.get("confidence", 0) >= config.CONFIDENCE_THRESHOLD
):

    current_time = time.time()

    if current_time - st.session_state.last_auto_trade > AUTO_COOLDOWN:

        try:
            signal_payload = {
                "stock": selected_stock,
                "signal": prediction["signal"],
                "confidence": prediction["confidence"],
                "price": prediction["price"],
                "quantity": 10,
                "user": st.session_state.user_wallet
            }

            tx = protocol.execute_trade(signal_payload)

            st.session_state.last_auto_trade = current_time

            logging.info(f"Auto trade executed: {tx}")

        except Exception as e:
            logging.error(f"Auto execution failed: {e}")

# --------------------------------------------------
# PAGE ROUTING
# --------------------------------------------------

active_page = page

if active_page == "Dashboard":
    render_dashboard(predictor, protocol, prediction, selected_stock, data_mode)

elif active_page == "Trade Panel":
    render_trade_panel(prediction, selected_stock, protocol, execution_mode)

elif active_page == "Portfolio":
    render_portfolio(protocol.get_portfolio_state())

elif active_page == "Blockchain Explorer":
    render_blockchain_explorer(protocol.get_transaction_history())

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")
st.caption("Blockchain Automatic Trading System | Capstone Project")