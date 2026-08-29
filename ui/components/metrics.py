import streamlit as st


def display_metric(title, value, delta=None):

    st.metric(
        label=title,
        value=value,
        delta=delta
    )


def display_protocol_metrics(protocol_state):

    st.subheader("Protocol Metrics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Trades", protocol_state["trades"])

    with col2:
        st.metric("Active Positions", protocol_state["positions"])

    with col3:
        st.metric("Treasury Balance", protocol_state["treasury"])

    st.markdown("---")