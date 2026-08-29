import streamlit as st
from blockchain_protocol.execution_engine.protocol_controller import ProtocolController

def render_governance():

    st.title("🏛 Governance Panel")

    controller = ProtocolController()

    st.subheader("Protocol Parameters")

    params = controller.get_protocol_parameters()

    for key, value in params.items():
        st.write(f"{key}: {value}")

    st.subheader("Propose Parameter Update")

    param = st.selectbox("Select Parameter", list(params.keys()))
    new_value = st.number_input("New Value", value=float(params[param]))

    if st.button("Submit Proposal"):
        tx_hash = controller.propose_change(param, new_value)
        st.success("Proposal Submitted")
        st.write("Transaction:", tx_hash)

    st.caption("Governance actions executed via smart contracts.")

if __name__ == "__main__":
    render_governance()