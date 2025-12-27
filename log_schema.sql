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

CREATE INDEX IF NOT EXISTS idx_logs_created_at ON interaction_logs(created_at);
