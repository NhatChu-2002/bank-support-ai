import streamlit as st
from state import set_msg
from api_client import send_message

def render_chat_panel(api_url: str):
    st.subheader("Send a message")

    st.text_input("Customer name", key="customer_name")
    st.text_area("Message", height=120, key="msg")

    presets = st.columns(3)
    presets[0].button(
        "Preset: Positive",
        use_container_width=True,
        on_click=set_msg,
        args=("Thanks for sorting out my net banking login issue!",),
    )
    presets[1].button(
        "Preset: Negative",
        use_container_width=True,
        on_click=set_msg,
        args=("My debit card replacement still hasn’t arrived.",),
    )
    presets[2].button(
        "Preset: Query",
        use_container_width=True,
        on_click=set_msg,
        args=("Could you check the status of ticket 123456?",),
    )

    if st.button("Send to API"):
        try:
            st.session_state["last_response"] = send_message(
                api_url=api_url,
                customer_name=st.session_state.customer_name,
                message=st.session_state.msg,
            )
        except Exception as e:
            st.error(f"API call failed: {e}")

    if "last_response" in st.session_state:
        st.markdown("### Result")
        st.json(st.session_state["last_response"])
