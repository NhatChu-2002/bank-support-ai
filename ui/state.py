import streamlit as st

DEFAULT_MESSAGE = "My debit card replacement still hasn’t arrived."
DEFAULT_CUSTOMER = "Vy"

def init_state():
    if "msg" not in st.session_state:
        st.session_state.msg = DEFAULT_MESSAGE
    if "customer_name" not in st.session_state:
        st.session_state.customer_name = DEFAULT_CUSTOMER

def set_msg(text: str):
    st.session_state.msg = text
