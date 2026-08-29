import streamlit as st


def render_sidebar():

    st.sidebar.title("DABTP Control Panel")

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Trade Panel",
            "Portfolio",
            "Blockchain Explorer",
            
        ]
    )

    st.sidebar.markdown("---")

    # ✅ ADDED: Data Source Toggle
    data_mode = st.sidebar.radio(
        "Data Source",
        ["LIVE", "SIMULATED"]
    )

    # ✅ ADDED: Execution Mode Toggle
    execution_mode = st.sidebar.radio(
        "Execution Mode",
        ["MANUAL", "AUTO"]
    )

    st.sidebar.markdown("---")

    st.sidebar.subheader("Protocol Status")

    st.sidebar.success("Blockchain Connected")
    st.sidebar.success("AI Oracle Active")

    

    st.sidebar.caption("Decentralized AI-Blockchain Trading")

    # ✅ UPDATED RETURN
    return page, data_mode, execution_mode