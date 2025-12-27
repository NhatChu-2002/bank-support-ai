import os
import sqlite3

DB_PATH = os.getenv("DB_PATH", "support.db")

SUPPORT_TICKETS_SQL = """
CREATE TABLE IF NOT EXISTS support_tickets (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticket_number TEXT UNIQUE NOT NULL,
  customer_name TEXT,
  message TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'unresolved',
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  updated_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_support_tickets_ticket_number
ON support_tickets(ticket_number);
"""

INTERACTION_LOGS_SQL = """
CREATE TABLE IF NOT EXISTS interaction_logs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  customer_name TEXT,
  user_message TEXT NOT NULL,
  category TEXT NOT NULL,
  sentiment TEXT,
  extracted_ticket_number TEXT,
  response_text TEXT NOT NULL,
  db_action TEXT,
  db_ticket_number TEXT
);

CREATE INDEX IF NOT EXISTS idx_logs_created_at
ON interaction_logs(created_at);
"""

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    conn = get_conn()
    conn.executescript(SUPPORT_TICKETS_SQL)
    conn.executescript(INTERACTION_LOGS_SQL)
    conn.commit()
    conn.close()
