import streamlit as st
from db_read import load_latest_logs

def render_logs_panel(db_path: str):
    st.subheader("Latest Logs (from SQLite)")
    try:
        df = load_latest_logs(db_path=db_path, limit=20)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Could not load logs. Did you create interaction_logs table? Error: {e}")
