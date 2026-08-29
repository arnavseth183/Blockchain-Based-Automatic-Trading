import streamlit as st
import pandas as pd
from datetime import datetime


def render_blockchain_explorer(tx_history):

    st.title("⛓ Blockchain Explorer")

    # --------------------------------------------------
    # SAFETY CHECKS
    # --------------------------------------------------

    if tx_history is None:
        st.info("Blockchain layer not initialized.")
        return

    if not isinstance(tx_history, list) or len(tx_history) == 0:
        st.info("No blockchain transactions yet.")
        return

    # --------------------------------------------------
    # NORMALIZE DATA
    # --------------------------------------------------

    normalized_events = []

    for event in tx_history:

        normalized_events.append({
            "tx_hash": event.get("tx_hash", "N/A"),
            "symbol": event.get("symbol", "N/A"),
            "action": event.get("action", event.get("signal", "N/A")),
            "quantity": event.get("quantity", 0),
            "price": event.get("price", 0),
            "status": event.get("status", "UNKNOWN"),
            "timestamp": event.get("timestamp", datetime.now())
        })

    df = pd.DataFrame(normalized_events)

    # --------------------------------------------------
    # EMPTY CHECK AFTER NORMALIZATION
    # --------------------------------------------------

    if df.empty:
        st.info("No valid transaction data to display.")
        return

    # --------------------------------------------------
    # FIX: SAFE TIMESTAMP CONVERSION
    # --------------------------------------------------

    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # --------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Transactions", len(df))

    with col2:
        successful = len(df[df["status"].isin(["SUCCESS", "SIMULATED"])])
        st.metric("Successful/Simulated", successful)

    with col3:
        failed = len(df[df["status"] == "FAILED"])
        st.metric("Failed", failed)

    st.markdown("---")

    # --------------------------------------------------
    # TRANSACTION TABLE
    # --------------------------------------------------

    st.subheader("Transaction History")

    st.dataframe(
        df.sort_values(by="timestamp", ascending=False),
        use_container_width=True
    )

    # --------------------------------------------------
    # STATUS DISTRIBUTION
    # --------------------------------------------------

    st.subheader("Execution Status Distribution")

    status_counts = df["status"].value_counts()
    st.bar_chart(status_counts)

    # --------------------------------------------------
    # EXPANDABLE DETAILED VIEW
    # --------------------------------------------------

    st.subheader("Detailed Transaction View")

    for _, row in df.iterrows():

        with st.expander(f"🔎 Tx Hash: {row['tx_hash']}"):

            st.write("Symbol:", row["symbol"])
            st.write("Action:", row["action"])
            st.write("Quantity:", row["quantity"])
            st.write("Price:", row["price"])
            st.write("Status:", row["status"])
            st.write("Timestamp:", row["timestamp"])

    st.caption(
        "All trades are enforced by smart contracts (or simulation layer) and are immutable once recorded."
    )


# --------------------------------------------------
# TEST RUN
# --------------------------------------------------
if __name__ == "__main__":
    render_blockchain_explorer([])