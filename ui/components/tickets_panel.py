import streamlit as st
from db_read import load_latest_tickets

def render_tickets_panel(db_path: str):
    st.subheader("Tickets Table (latest 20)")
    try:
        tickets = load_latest_tickets(db_path=db_path, limit=20)
        st.dataframe(tickets, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load tickets. Error: {e}")
