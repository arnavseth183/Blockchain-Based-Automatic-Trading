import streamlit as st
from ai_oracle.evaluation.risk_score import RiskScore
from ai_oracle.evaluation.sharpe_ratio import SharpeRatio

def render_risk_dashboard():

    st.title("📉 Risk & Performance Dashboard")

    risk_engine = RiskScore()
    sharpe_engine = SharpeRatio()

    risk_score = risk_engine.calculate()
    sharpe = sharpe_engine.compute()

    st.metric("Risk Score", round(risk_score, 2))
    st.metric("Sharpe Ratio", round(sharpe, 2))

    if risk_score > 0.7:
        st.error("High Risk Strategy")
    elif risk_score > 0.4:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk Strategy")

    st.caption("Risk enforced both off-chain and on-chain.")

if __name__ == "__main__":
    render_risk_dashboard()