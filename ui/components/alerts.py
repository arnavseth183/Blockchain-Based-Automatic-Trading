import streamlit as st


def show_success(message):
    st.success(message)


def show_error(message):
    st.error(message)


def show_warning(message):
    st.warning(message)


def show_info(message):
    st.info(message)


def risk_alert(risk_score):

    if risk_score > 0.8:
        st.error("Critical Risk Level")
    elif risk_score > 0.5:
        st.warning("Moderate Risk")
    else:
        st.success("Low Risk")


def governance_alert(proposal_status):

    if proposal_status == "pending":
        st.info("Proposal Pending Approval")
    elif proposal_status == "approved":
        st.success("Proposal Approved")
    elif proposal_status == "rejected":
        st.error("Proposal Rejected")