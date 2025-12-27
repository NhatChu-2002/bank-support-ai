import sqlite3
import pandas as pd

def load_latest_logs(db_path: str, limit: int = 20) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query(
            f"""
            SELECT id, created_at, customer_name, category, sentiment,
                   extracted_ticket_number, db_action, db_ticket_number
            FROM interaction_logs
            ORDER BY id DESC
            LIMIT {int(limit)}
            """,
            conn
        )
    finally:
        conn.close()

def load_latest_tickets(db_path: str, limit: int = 20) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    try:
        return pd.read_sql_query(
            f"""
            SELECT ticket_number, customer_name, status, created_at, updated_at
            FROM support_tickets
            ORDER BY id DESC
            LIMIT {int(limit)}
            """,
            conn
        )
    finally:
        conn.close()
