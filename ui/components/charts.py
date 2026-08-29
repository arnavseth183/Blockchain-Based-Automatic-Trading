import streamlit as st
import pandas as pd


def render_price_chart(price_series):

    st.subheader("Price Chart")
    st.line_chart(price_series)


def render_allocation_chart(allocation):

    st.subheader("Portfolio Allocation")
    st.bar_chart(allocation)


def render_volume_chart(volume_series):

    st.subheader("Volume Analysis")
    st.area_chart(volume_series)


def render_pnl_chart(pnl_series):

    st.subheader("PnL Over Time")
    st.line_chart(pnl_series)