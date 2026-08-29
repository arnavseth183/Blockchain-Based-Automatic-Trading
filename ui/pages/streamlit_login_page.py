"""
Streamlit Login Interface
"""

import streamlit as st
from security.wallet_auth import WalletAuth

auth = WalletAuth()

st.title("AI Blockchain Trading Platform")

menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------------------------------------
# SESSION INIT (IMPORTANT FIX)
# ---------------------------------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------------------------------
# REGISTER
# ---------------------------------------
if choice == "Register":

    st.subheader("Create Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):

        wallet = auth.register_user(username, password)

        st.success("Account Created")

        st.write("Wallet Address:", wallet["address"])
        st.write("Private Key:", wallet["private_key"])
        st.warning("Save private key safely!")

        # optional session setup after register
        st.session_state.user = {
            "username": username,
            "wallet": wallet["address"],
            "balance": wallet.get("balance", 10000)
        }

        st.info("User session created. You can now trade.")

# ---------------------------------------
# LOGIN
# ---------------------------------------
if choice == "Login":

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        user = auth.login(username, password)

        if user:

            st.success("Login Successful")

            # ✅ IMPORTANT FIX: session state integration
            st.session_state.user = {
                "username": username,
                "wallet": user["address"],
                "balance": user.get("balance", 10000)
            }

            st.write("Wallet Address:", user["address"])
            st.write("Balance: ₹", user["balance"])

            st.info("Session initialized for trading system")

        else:
            st.error("Invalid Credentials")

# ---------------------------------------
# OPTIONAL DEBUG VIEW
# ---------------------------------------
if st.session_state.user:
    st.markdown("---")
    st.subheader("Active Session")
    st.json(st.session_state.user)