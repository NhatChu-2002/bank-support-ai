import streamlit as st
from config import API_URL, DB_PATH, PAGE_TITLE, LAYOUT
from state import init_state
from components.chat_panel import render_chat_panel
from components.logs_panel import render_logs_panel
from components.tickets_panel import render_tickets_panel


st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)
st.title(PAGE_TITLE)

init_state()

col1, col2 = st.columns([2, 1])

with col1:
    render_chat_panel(API_URL)

with col2:
    render_logs_panel(DB_PATH)

st.divider()
render_tickets_panel(DB_PATH)
